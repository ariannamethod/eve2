#!/usr/bin/env python3
"""
Добавление внешних корпусов к данным InnerArianna для расширения знаний.
"""

import os
import glob
from pathlib import Path

DATA_CACHE_DIR = "data"
DOC_DIR = "doc"
EXTERNAL_DIR = "external_corpus"  # Директория для внешних корпусов

def add_external_corpus(corpus_file, corpus_name=None):
    """
    Добавляет внешний корпус к данным для обучения.
    
    Args:
        corpus_file: Путь к файлу с корпусом (txt, md, или другой текст)
        corpus_name: Имя для корпуса (опционально)
    """
    if not os.path.exists(corpus_file):
        print(f"❌ Файл не найден: {corpus_file}")
        return False
    
    os.makedirs(EXTERNAL_DIR, exist_ok=True)
    
    # Определяем имя файла
    if corpus_name is None:
        corpus_name = os.path.basename(corpus_file)
    
    # Копируем файл в external_corpus
    import shutil
    dest_path = os.path.join(EXTERNAL_DIR, corpus_name)
    shutil.copy2(corpus_file, dest_path)
    
    print(f"✅ Добавлен корпус: {corpus_name}")
    print(f"   Путь: {dest_path}")
    print(f"   Размер: {os.path.getsize(dest_path) / 1024 / 1024:.2f} MB")
    
    return True

def list_external_corpora():
    """Показывает список добавленных внешних корпусов."""
    if not os.path.exists(EXTERNAL_DIR):
        print("📂 Директория external_corpus не существует")
        return []
    
    files = list(Path(EXTERNAL_DIR).glob("*"))
    files = [f for f in files if f.is_file()]
    
    if not files:
        print("📂 Внешние корпуса не добавлены")
        return []
    
    print(f"📚 Добавленные внешние корпуса ({len(files)}):")
    total_size = 0
    for f in sorted(files):
        size = f.stat().st_size / 1024 / 1024
        total_size += size
        print(f"   - {f.name} ({size:.2f} MB)")
    
    print(f"\n   Всего: {total_size:.2f} MB")
    return files

def prepare_combined_corpus():
    """
    Подготавливает объединенный корпус из doc/ и external_corpus/.
    """
    os.makedirs(DATA_CACHE_DIR, exist_ok=True)
    
    output_file = os.path.join(DATA_CACHE_DIR, "combined_corpus.txt")
    
    print("📚 Создание объединенного корпуса...")
    print("=" * 60)
    
    total_size = 0
    
    with open(output_file, "w", encoding="utf-8") as f:
        # 1. Добавляем Arianna Method материалы
        print("1️⃣  Добавление Arianna Method материалов...")
        md_files = list(Path(DOC_DIR).glob("*.md"))
        md_files = [f for f in md_files if not f.name.startswith("README")]
        
        for md_file in md_files:
            try:
                with open(md_file, "r", encoding="utf-8") as inf:
                    content = inf.read().strip()
                    if content:
                        f.write(f"=== {md_file.name} ===\n")
                        f.write(content + "\n\n")
                        total_size += len(content)
            except Exception as e:
                print(f"   ⚠️  Ошибка при чтении {md_file.name}: {e}")
        
        print(f"   ✅ Добавлено {len(md_files)} файлов из doc/")
        
        # 2. Добавляем внешние корпуса
        if os.path.exists(EXTERNAL_DIR):
            print("\n2️⃣  Добавление внешних корпусов...")
            external_files = list(Path(EXTERNAL_DIR).glob("*"))
            external_files = [f for f in external_files if f.is_file()]
            
            for ext_file in external_files:
                try:
                    with open(ext_file, "r", encoding="utf-8") as inf:
                        content = inf.read().strip()
                        if content:
                            f.write(f"=== EXTERNAL: {ext_file.name} ===\n")
                            f.write(content + "\n\n")
                            total_size += len(content)
                except Exception as e:
                    print(f"   ⚠️  Ошибка при чтении {ext_file.name}: {e}")
            
            print(f"   ✅ Добавлено {len(external_files)} внешних файлов")
        else:
            print("\n2️⃣  Внешние корпуса не найдены (пропуск)")
    
    file_size_mb = os.path.getsize(output_file) / 1024 / 1024
    print()
    print("=" * 60)
    print(f"✅ Объединенный корпус создан: {output_file}")
    print(f"📊 Размер: {file_size_mb:.2f} MB, символов: {total_size:,}")
    print()
    print("💡 Следующие шаги:")
    print("   1. python3 arianna_data.py train_vocab --vocab_size=4096  # Переобучить токенизатор")
    print("   2. python3 arianna_data.py pretokenize --vocab_size=4096  # Претокенизировать")
    print("   3. python3 train_arianna.py --init_from=resume  # Продолжить обучение")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
Использование:
  python3 add_external_corpus.py add <file> [name]  - Добавить корпус
  python3 add_external_corpus.py list                - Показать список
  python3 add_external_corpus.py prepare             - Подготовить объединенный корпус
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("❌ Укажите файл: python3 add_external_corpus.py add <file> [name]")
            sys.exit(1)
        corpus_file = sys.argv[2]
        corpus_name = sys.argv[3] if len(sys.argv) > 3 else None
        add_external_corpus(corpus_file, corpus_name)
    
    elif command == "list":
        list_external_corpora()
    
    elif command == "prepare":
        prepare_combined_corpus()
    
    else:
        print(f"❌ Неизвестная команда: {command}")
        sys.exit(1)

