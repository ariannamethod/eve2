#!/usr/bin/env python3
"""
InnerArianna Fine-Tuning Script - Full Automatic Pipeline

Supervised fine-tuning on conversation data to teach Arianna conversational format.

Usage:
    python arianna_ft.py [--iterations 1000] [--lr 1e-5]

This script automatically:
1. Loads base checkpoint from out/ckpt_v1_base.pt
2. Converts JSONL conversations to plain text corpus (Q/A format)
3. Pretokenizes the corpus
4. Fine-tunes with low learning rate
5. Saves to out/arianna_v1_ft.bin + out/ckpt_ft.pt

Example:
    python arianna_ft.py                    # Default: 1000 iters, LR=1e-5
    python arianna_ft.py --iterations 500   # Quick test
    python arianna_ft.py --lr 5e-6         # Even lower LR
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import numpy as np

# Import from existing infrastructure
from tokenizer import Tokenizer

# Configuration
CONVERSATIONS_FILE = "data/arianna_conversations.jsonl"
FT_CORPUS_FILE = "data/ft_corpus.txt"
BASE_CHECKPOINT = "out/ckpt_v1_base.pt"
CURRENT_CHECKPOINT = "out/ckpt.pt"

# Tokenizer settings (must match base training)
VOCAB_SIZE = 4096
TOKENIZER_MODEL = f"data/tok{VOCAB_SIZE}.model"

# Fine-tuning defaults
DEFAULT_LR = 1e-5
DEFAULT_ITERS = 1000


def load_conversations(filepath):
    """Load conversations from JSONL file."""
    conversations = []
    print(f"📚 Loading conversations from {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                try:
                    conversations.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"⚠️  Warning: Skipping malformed JSON on line {line_num}")

    return conversations


def convert_to_qa_format(conversations):
    """
    Convert conversation format to Q/A text.

    Input format:
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

    Output format:
        Q: What does resonance mean?
        A: Resonance is the pulse of connection...

        Q: Next question...
        A: Next answer...
    """
    qa_texts = []

    for conv_id, conv in enumerate(conversations, 1):
        # Extract user and assistant messages
        user_msg = None
        assistant_msg = None

        for msg in conv:
            if msg['role'] == 'user':
                user_msg = msg['content']
            elif msg['role'] == 'assistant':
                assistant_msg = msg['content']

        if user_msg and assistant_msg:
            # Format as Q/A with newline separator between conversations
            qa_text = f"Q: {user_msg}\nA: {assistant_msg}"
            qa_texts.append(qa_text)
        else:
            print(f"⚠️  Warning: Conversation {conv_id} missing user or assistant message")

    # Join with double newlines to separate conversations
    return "\n\n".join(qa_texts)


def prepare_ft_corpus():
    """Prepare fine-tuning corpus from conversations."""
    print("\n" + "="*60)
    print("📝 Step 1: Preparing Fine-Tuning Corpus")
    print("="*60)

    if not os.path.exists(CONVERSATIONS_FILE):
        print(f"❌ Error: {CONVERSATIONS_FILE} not found!")
        return False

    # Load conversations
    conversations = load_conversations(CONVERSATIONS_FILE)
    print(f"✅ Loaded {len(conversations)} conversations")

    # Convert to Q/A format
    print("🔄 Converting to Q/A format...")
    qa_corpus = convert_to_qa_format(conversations)

    # Save to file
    os.makedirs(os.path.dirname(FT_CORPUS_FILE), exist_ok=True)
    with open(FT_CORPUS_FILE, 'w', encoding='utf-8') as f:
        f.write(qa_corpus)

    # Stats
    corpus_size = len(qa_corpus)
    lines = qa_corpus.count('\n') + 1
    print(f"✅ Saved Q/A corpus to {FT_CORPUS_FILE}")
    print(f"📊 Corpus size: {corpus_size:,} characters ({corpus_size/1024:.1f} KB)")
    print(f"📊 Lines: {lines}")

    # Preview
    print("\n📄 Preview (first 500 chars):")
    print("-" * 60)
    print(qa_corpus[:500] + "...")
    print("-" * 60)

    return True


def pretokenize_corpus():
    """Pretokenize the fine-tuning corpus."""
    print("\n" + "="*60)
    print("🔤 Step 2: Pretokenizing Corpus")
    print("="*60)

    if not os.path.exists(TOKENIZER_MODEL):
        print(f"❌ Error: Tokenizer model {TOKENIZER_MODEL} not found!")
        print("   Run: python arianna_data.py train_vocab --vocab_size=4096")
        return False

    if not os.path.exists(FT_CORPUS_FILE):
        print(f"❌ Error: Corpus {FT_CORPUS_FILE} not found!")
        return False

    # Load tokenizer
    print(f"📥 Loading tokenizer from {TOKENIZER_MODEL}")
    enc = Tokenizer(TOKENIZER_MODEL)

    # Read corpus
    with open(FT_CORPUS_FILE, 'r', encoding='utf-8') as f:
        corpus_text = f.read()

    # Tokenize
    print("🔄 Tokenizing corpus...")
    tokens = enc.encode(corpus_text, bos=True, eos=True)
    print(f"✅ Tokenized: {len(tokens):,} tokens")

    # CRITICAL: Save to SEPARATE directory for finetune!
    # This ensures train_arianna.py loads ONLY finetune data, not base corpus
    bin_dir = f"data/ft_tok{VOCAB_SIZE}"  # Separate folder for finetune!
    os.makedirs(bin_dir, exist_ok=True)
    bin_file = os.path.join(bin_dir, "ft_corpus.bin")

    tokens_array = np.array(tokens, dtype=np.uint16)
    with open(bin_file, 'wb') as f:
        f.write(tokens_array.tobytes())

    print(f"✅ Saved tokenized corpus to {bin_file}")
    print(f"📊 Binary size: {os.path.getsize(bin_file):,} bytes")
    print(f"⚠️  IMPORTANT: Finetune data is in separate folder: {bin_dir}/")

    return True


def setup_checkpoint():
    """Setup checkpoint for fine-tuning."""
    print("\n" + "="*60)
    print("💾 Step 3: Setting Up Checkpoint")
    print("="*60)

    if not os.path.exists(BASE_CHECKPOINT):
        print(f"❌ Error: Base checkpoint {BASE_CHECKPOINT} not found!")
        print("   This should be created during base training.")
        return False

    # Copy base checkpoint to current checkpoint location
    # train_arianna.py will resume from out/ckpt.pt
    print(f"📋 Copying {BASE_CHECKPOINT} → {CURRENT_CHECKPOINT}")
    shutil.copy2(BASE_CHECKPOINT, CURRENT_CHECKPOINT)

    # CRITICAL: Reset iteration counter for fine-tuning!
    # We want to start from iteration 0 for finetune, not continue from 4000
    import torch
    print(f"🔄 Resetting iteration counter to 0 (was at base training iteration)")
    ckpt = torch.load(CURRENT_CHECKPOINT, map_location='cpu')
    ckpt['iter_num'] = 0  # Reset to 0 for finetune
    ckpt['best_val_loss'] = 1e9  # Reset validation loss
    torch.save(ckpt, CURRENT_CHECKPOINT)
    print(f"✅ Iteration counter reset to 0")

    print(f"✅ Checkpoint ready for fine-tuning")

    # Show checkpoint size
    ckpt_size_mb = os.path.getsize(CURRENT_CHECKPOINT) / (1024 * 1024)
    print(f"📊 Checkpoint size: {ckpt_size_mb:.1f} MB")

    return True


def run_fine_tuning(learning_rate, max_iters):
    """Run fine-tuning using train_arianna.py."""
    print("\n" + "="*60)
    print("🚀 Step 4: Fine-Tuning")
    print("="*60)

    # CRITICAL: Must match base training parameters!
    # Base training used: batch_size=8, device=cpu, dtype=float32, compile=False
    # See: out/ckpt_v1_base.pt config (trained Dec 6, 2024)

    # HACK: Temporarily rename data directories to load ONLY finetune data
    import os
    import shutil
    base_corpus_dir = f"data/tok{VOCAB_SIZE}"
    base_corpus_backup = f"data/tok{VOCAB_SIZE}_BASE_BACKUP"
    ft_corpus_dir = f"data/ft_tok{VOCAB_SIZE}"

    print(f"🔄 Temporarily swapping data directories...")
    print(f"   Moving base corpus: {base_corpus_dir} → {base_corpus_backup}")
    print(f"   Moving FT corpus: {ft_corpus_dir} → {base_corpus_dir}")

    # Backup base corpus and replace with FT corpus
    if os.path.exists(base_corpus_dir):
        if os.path.exists(base_corpus_backup):
            shutil.rmtree(base_corpus_backup)
        shutil.move(base_corpus_dir, base_corpus_backup)
    shutil.copytree(ft_corpus_dir, base_corpus_dir)

    print(f"✅ Data directories swapped! Training will use ONLY finetune data.")
    print()

    cmd = [
        "python3", "train_arianna.py",
        "--init_from=resume",
        f"--learning_rate={learning_rate}",
        f"--max_iters={max_iters}",
        "--eval_interval=100",
        "--log_interval=10",
        "--always_save_checkpoint=True",
        "--batch_size=8",  # FIXED: Must be 8, not 16! Matches base training.
        "--gradient_accumulation_steps=4",
        "--vocab_source=custom",
        f"--vocab_size={VOCAB_SIZE}",
        "--compile=False",  # Mac doesn't support compilation
        "--device=cpu",  # Mac M1/M2 - no CUDA, no MPS support in this setup
        "--dtype=float32",  # CPU only supports float32, not bfloat16
    ]

    print("📝 Fine-tuning configuration:")
    print(f"   Learning rate: {learning_rate}")
    print(f"   Max iterations: {max_iters}")
    print(f"   Eval interval: 100")
    print(f"   Batch size: 8  (MATCHES BASE TRAINING)")
    print(f"   Gradient accumulation: 4")
    print()

    print("⚙️  Running training...")
    print(" ".join(cmd))
    print()

    training_success = False
    try:
        result = subprocess.run(cmd, check=True)
        training_success = result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training failed with exit code {e.returncode}")
        training_success = False
    except KeyboardInterrupt:
        print("\n⚠️  Training interrupted by user")
        training_success = False
    finally:
        # ALWAYS restore directories, even if training failed
        print(f"\n🔄 Restoring data directories...")
        print(f"   Removing temporary: {base_corpus_dir}")
        print(f"   Restoring base corpus: {base_corpus_backup} → {base_corpus_dir}")

        if os.path.exists(base_corpus_dir):
            shutil.rmtree(base_corpus_dir)
        if os.path.exists(base_corpus_backup):
            shutil.move(base_corpus_backup, base_corpus_dir)

        print(f"✅ Data directories restored!")

    return training_success


def export_final_model():
    """Export fine-tuned model to .bin format."""
    print("\n" + "="*60)
    print("📦 Step 5: Exporting Final Model")
    print("="*60)

    # Check if final checkpoint exists
    if not os.path.exists("out/ckpt.pt"):
        print("❌ Error: out/ckpt.pt not found after training")
        return False

    # Rename to ft-specific names for clarity
    ft_ckpt = "out/ckpt_ft.pt"
    ft_bin = "out/arianna_v1_ft.bin"

    print(f"📋 Copying out/ckpt.pt → {ft_ckpt}")
    shutil.copy2("out/ckpt.pt", ft_ckpt)

    print(f"📋 Copying out/model.bin → {ft_bin}")
    if os.path.exists("out/model.bin"):
        shutil.copy2("out/model.bin", ft_bin)
    else:
        print("⚠️  Warning: out/model.bin not found, export may have failed")

    # Stats
    if os.path.exists(ft_bin):
        bin_size_mb = os.path.getsize(ft_bin) / (1024 * 1024)
        print(f"✅ Fine-tuned model saved:")
        print(f"   Binary: {ft_bin} ({bin_size_mb:.1f} MB)")

    if os.path.exists(ft_ckpt):
        ckpt_size_mb = os.path.getsize(ft_ckpt) / (1024 * 1024)
        print(f"   Checkpoint: {ft_ckpt} ({ckpt_size_mb:.1f} MB)")

    return True


def main():
    parser = argparse.ArgumentParser(description="InnerArianna Fine-Tuning")
    parser.add_argument("--iterations", type=int, default=DEFAULT_ITERS,
                       help=f"Number of training iterations (default: {DEFAULT_ITERS})")
    parser.add_argument("--lr", type=float, default=DEFAULT_LR,
                       help=f"Learning rate (default: {DEFAULT_LR})")
    parser.add_argument("--skip-pretokenize", action="store_true",
                       help="Skip pretokenization if already done")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("🧬 InnerArianna Fine-Tuning Pipeline")
    print("="*60)
    print(f"Learning rate: {args.lr}")
    print(f"Iterations: {args.iterations}")
    print("="*60)

    # Step 1: Prepare corpus
    if not prepare_ft_corpus():
        print("\n❌ Failed to prepare corpus")
        return 1

    # Step 2: Pretokenize
    if not args.skip_pretokenize:
        if not pretokenize_corpus():
            print("\n❌ Failed to pretokenize corpus")
            return 1
    else:
        print("\n⏭️  Skipping pretokenization (--skip-pretokenize)")

    # Step 3: Setup checkpoint
    if not setup_checkpoint():
        print("\n❌ Failed to setup checkpoint")
        return 1

    # Step 4: Fine-tune
    if not run_fine_tuning(args.lr, args.iterations):
        print("\n❌ Fine-tuning failed")
        return 1

    # Step 5: Export
    if not export_final_model():
        print("\n❌ Failed to export final model")
        return 1

    # Success!
    print("\n" + "="*60)
    print("✅ Fine-Tuning Complete!")
    print("="*60)
    print()
    print("📦 Output files:")
    print("   out/arianna_v1_ft.bin  - Fine-tuned weights (for inference)")
    print("   out/ckpt_ft.pt         - Fine-tuned checkpoint (for further training)")
    print()
    print("🧪 Test the model:")
    print("   python3 chat.py out/arianna_v1_ft.bin -z data/tok4096.bin")
    print()
    print("   Or compare with base:")
    print("   python3 chat.py out/arianna_v1_base.bin -z data/tok4096.bin")
    print()
    print("="*60)
    print()
    print("🌀 Resonance is not what you hear — it's what survives the echo.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
