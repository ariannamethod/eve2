"""
Подготовка данных из markdown файлов для обучения InnerArianna модели.
Аналог tinystories.py, но для Arianna Method материалов.
"""

import argparse
import glob
import json
import os
import random
from typing import List

import numpy as np
import sentencepiece as spm
import torch
import torch.distributed as dist
from tqdm import tqdm

from tokenizer import Tokenizer

DATA_CACHE_DIR = "data"
DOC_DIR = "english_train"  # Только английские файлы!

def collect_markdown_files():
    """Собирает все markdown файлы из english_train/ директории (только английские!)."""
    md_files = glob.glob(os.path.join(DOC_DIR, "*.md"))
    md_files += glob.glob(os.path.join(DOC_DIR, "*.txt"))  # Включаем .txt файлы тоже
    # Исключаем README.md и другие служебные файлы если нужно
    md_files = [f for f in md_files if not os.path.basename(f).startswith("README")]
    
    # В english_train уже только английские файлы, но на всякий случай проверяем
    return sorted(md_files)

def prepare_text_data():
    """Собирает весь текст из markdown файлов в один файл для обучения токенизатора."""
    os.makedirs(DATA_CACHE_DIR, exist_ok=True)
    
    md_files = collect_markdown_files()
    if not md_files:
        print(f"❌ Не найдено markdown файлов в {DOC_DIR}/")
        return None
    
    output_file = os.path.join(DATA_CACHE_DIR, "arianna_corpus.txt")
    
    print(f"📚 Собираю текст из {len(md_files)} markdown файлов...")
    total_size = 0
    
    with open(output_file, "w", encoding="utf-8") as f:
        for md_file in tqdm(md_files):
            try:
                with open(md_file, "r", encoding="utf-8") as inf:
                    content = inf.read().strip()
                    if content:
                        f.write(content + "\n\n")
                        total_size += len(content)
            except Exception as e:
                print(f"⚠️  Ошибка при чтении {md_file}: {e}")
    
    file_size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"✅ Создан файл: {output_file}")
    print(f"📊 Размер: {file_size_mb:.2f} MB, символов: {total_size:,}")
    
    return output_file

def train_vocab(vocab_size=4096):
    """
    Обучает кастомный sentencepiece токенизатор на корпусе Arianna Method.
    """
    assert vocab_size > 0, "Vocab size must be positive"
    
    # Подготовить текст
    corpus_file = prepare_text_data()
    if not corpus_file:
        return
    
    # Путь для сохранения токенизатора
    prefix = os.path.join(DATA_CACHE_DIR, f"tok{vocab_size}")
    
    print(f"🧬 Обучаю токенизатор с vocab_size={vocab_size}...")
    
    spm.SentencePieceTrainer.train(
        input=corpus_file,
        model_prefix=prefix,
        model_type="bpe",
        vocab_size=vocab_size,
        self_test_sample_size=0,
        input_format="text",
        character_coverage=1.0,
        num_threads=os.cpu_count(),
        split_digits=True,
        allow_whitespace_only_pieces=True,
        byte_fallback=True,
        unk_surface=r" \342\201\207 ",
        normalization_rule_name="identity"
    )
    
    print(f"✅ Токенизатор сохранен: {prefix}.model")
    print("Done.")

def process_markdown_shard(args, vocab_size):
    """Обрабатывает один markdown файл и токенизирует его."""
    shard_id, md_file = args
    tokenizer_model = get_tokenizer_model_path(vocab_size)
    enc = Tokenizer(tokenizer_model)
    
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        if not content:
            return
        
        # Токенизируем весь текст
        tokens = enc.encode(content, bos=True, eos=False)
        
        # Сохраняем в .bin файл
        all_tokens = np.array(tokens, dtype=np.uint16)
        
        # Создаем имя выходного файла
        if vocab_size == 0:
            # Используем Llama 2 токенизатор
            bin_dir = os.path.join(DATA_CACHE_DIR, "arianna_data")
            os.makedirs(bin_dir, exist_ok=True)
            basename = os.path.basename(md_file).replace(".md", ".bin")
            tokenized_filename = os.path.join(bin_dir, basename)
        else:
            # Кастомный токенизатор
            bin_dir = os.path.join(DATA_CACHE_DIR, f"tok{vocab_size}")
            os.makedirs(bin_dir, exist_ok=True)
            basename = os.path.basename(md_file).replace(".md", ".bin")
            tokenized_filename = os.path.join(bin_dir, basename)
        
        # Записываем байты
        with open(tokenized_filename, "wb") as f:
            f.write(all_tokens.tobytes())
        
        avg_seq_len = all_tokens.size / ((all_tokens == 1).sum()) if (all_tokens == 1).sum() > 0 else all_tokens.size
        print(f"✅ {os.path.basename(tokenized_filename)}, tokens: {len(tokens)}, avg_seq_len: {avg_seq_len:.2f}")
        
    except Exception as e:
        print(f"❌ Ошибка при обработке {md_file}: {e}")

def pretokenize(vocab_size=0):
    """Претокенизирует все markdown файлы."""
    md_files = collect_markdown_files()
    
    if not md_files:
        print(f"❌ Не найдено markdown файлов в {DOC_DIR}/")
        return
    
    print(f"🔤 Претокенизирую {len(md_files)} файлов...")
    
    # Создаем директорию для .bin файлов
    if vocab_size == 0:
        bin_dir = os.path.join(DATA_CACHE_DIR, "arianna_data")
    else:
        bin_dir = os.path.join(DATA_CACHE_DIR, f"tok{vocab_size}")
    os.makedirs(bin_dir, exist_ok=True)
    
    # Обрабатываем файлы ПОСЛЕДОВАТЕЛЬНО (без multiprocessing из-за проблем с tempdir)
    for idx, md_file in enumerate(md_files):
        process_markdown_shard((idx, md_file), vocab_size)
    
    print("✅ Done.")

class PretokDataset(torch.utils.data.IterableDataset):
    """Загружает претокенизированные примеры из .bin файлов."""
    
    def __init__(self, split, max_seq_len, vocab_size, vocab_source):
        super().__init__()
        self.split = split
        self.max_seq_len = max_seq_len
        self.vocab_size = vocab_size
        self.vocab_source = vocab_source
    
    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        worker_id = worker_info.id if worker_info else 0
        rank = dist.get_rank() if dist.is_initialized() else 0
        seed = 42 + worker_id + 1337 * rank
        rng = random.Random(seed)
        
        if self.vocab_source == "llama2":
            bin_dir = os.path.join(DATA_CACHE_DIR, "arianna_data")
        elif self.vocab_source == "custom":
            bin_dir = os.path.join(DATA_CACHE_DIR, f"tok{self.vocab_size}")
        else:
            raise ValueError(f"Unknown vocab_source: {self.vocab_source}")
        
        shard_filenames = sorted(glob.glob(os.path.join(bin_dir, "*.bin")))
        
        if not shard_filenames:
            raise ValueError(f"No .bin files found in {bin_dir}")
        
        # Разделение на train/val: 90% train, 10% val
        split_idx = int(len(shard_filenames) * 0.9)
        if self.split == "train":
            shard_filenames = shard_filenames[:split_idx]
        else:
            shard_filenames = shard_filenames[split_idx:]
        
        while True:
            rng.shuffle(shard_filenames)
            for shard in shard_filenames:
                try:
                    m = np.memmap(shard, dtype=np.uint16, mode="r")
                    num_batches = len(m) // self.max_seq_len
                    num_batches -= 1
                    if num_batches <= 0:
                        continue
                    ixs = list(range(num_batches))
                    rng.shuffle(ixs)
                    for ix in ixs:
                        start = ix * self.max_seq_len
                        end = start + self.max_seq_len + 1
                        chunk = torch.from_numpy((m[start:end]).astype(np.int64))
                        x = chunk[:-1]
                        y = chunk[1:]
                        yield x, y
                except Exception as e:
                    print(f"⚠️  Ошибка при чтении {shard}: {e}")
                    continue

def get_tokenizer_model_path(vocab_size):
    """Возвращает путь к токенизатору."""
    if vocab_size == 0:
        return None
    else:
        return os.path.join(DATA_CACHE_DIR, f"tok{vocab_size}.model")

class Task:
    """Task класс для использования в train.py."""
    
    @staticmethod
    def iter_batches(batch_size, device, num_workers=0, **dataset_kwargs):
        ds = PretokDataset(**dataset_kwargs)
        dl = torch.utils.data.DataLoader(
            ds, batch_size=batch_size, pin_memory=True, num_workers=num_workers
        )
        for x, y in dl:
            x = x.to(device, non_blocking=True)
            y = y.to(device, non_blocking=True)
            yield x, y

if __name__ == "__main__":
    """
    Использование:
    
    # С кастомным токенизатором (рекомендуется для маленького корпуса):
    python arianna_data.py train_vocab --vocab_size=4096
    python arianna_data.py pretokenize --vocab_size=4096
    
    # С Llama 2 токенизатором:
    python arianna_data.py pretokenize
    """
    parser = argparse.ArgumentParser(description="Подготовка данных Arianna Method для обучения")
    parser.add_argument("stage", type=str, choices=["prepare", "train_vocab", "pretokenize"],
                       help="Этап подготовки данных")
    parser.add_argument("--vocab_size", type=int, default=0,
                       help="Размер словаря. 0 = использовать Llama 2 токенизатор")
    args = parser.parse_args()
    
    if args.stage == "prepare":
        prepare_text_data()
    elif args.stage == "train_vocab":
        train_vocab(vocab_size=args.vocab_size)
    elif args.stage == "pretokenize":
        pretokenize(vocab_size=args.vocab_size)
    else:
        raise ValueError(f"Unknown stage: {args.stage}")

