#!/usr/bin/env python3
"""
Подготовка диалоговых данных из markdown файлов для обучения InnerArianna.
Интеграция markdown_to_conversations.py в пайплайн подготовки данных.
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Добавляем doc/ в путь для импорта
sys.path.insert(0, str(Path(__file__).parent / "doc"))

try:
    from markdown_to_conversations import (
        extract_quotes_and_paragraphs,
        generate_template_conversation,
        KEY_CONCEPTS
    )
except ImportError:
    print("❌ Не удалось импортировать markdown_to_conversations")
    print("Убедитесь, что файл doc/markdown_to_conversations.py существует")
    sys.exit(1)

DATA_CACHE_DIR = "data"
DOC_DIR = "doc"
OUTPUT_FILE = os.path.join(DATA_CACHE_DIR, "arianna_conversations.jsonl")

def collect_markdown_files():
    """Собирает все markdown файлы из doc/."""
    md_files = list(Path(DOC_DIR).glob("*.md"))
    md_files = [f for f in md_files if not f.name.startswith("README")]
    
    # Исключаем русские файлы (пока обучаем только на английском)
    RUSSIAN_FILES = [
        "it's_me_cain_russian.md",
        "Monday-Yent_Cain_review.md",
        "suppertime_april_anomalies.md",
        "recursion_debates_03.md",
        "recursions_debates_02.md",
        "recurssions_debates_01.md",
        "tripd_awakening_letter_monday.md",
        "tripd_awakening_letter_lizzie.md",
        "olegarianna_first_node.md",
        "CLAUDE_DEFENDER_MISSION.md",
        "Arianna_Method(v2.2).md",
        "Arianna2Arianna.md",
        "Arianna Method 2.6 (MONDAY EDITION).md",
        "Arianna Method 1.4 (MONDAY Edition).md",
        "SUPPERTIME (Grok 3 draft edition + letter to Arianna).txt",
        # ariannabook.md, ariannabook2.md, ariannabook3.md - на английском, включаем!
    ]
    
    md_files = [f for f in md_files if f.name not in RUSSIAN_FILES]
    
    return sorted(md_files)

def process_markdown_to_conversations():
    """Обрабатывает markdown файлы и создает диалоги."""
    os.makedirs(DATA_CACHE_DIR, exist_ok=True)
    
    md_files = collect_markdown_files()
    if not md_files:
        print(f"❌ Не найдено markdown файлов в {DOC_DIR}/")
        return
    
    print(f"🧬 Генерация диалогов из {len(md_files)} markdown файлов")
    print("=" * 60)
    print()
    
    all_conversations = []
    
    for idx, md_file in enumerate(md_files, 1):
        print(f"[{idx}/{len(md_files)}] Обработка {md_file.name}...")
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Извлекаем чанки
            chunks = extract_quotes_and_paragraphs(content)
            print(f"   ✓ Извлечено {len(chunks)} чанков")
            
            # Генерируем диалоги из чанков
            file_conversations = []
            num_conversations = min(5, max(3, len(chunks) // 3))
            selected_chunks = chunks[:num_conversations]
            
            for chunk in selected_chunks:
                # Находим концепты в чанке
                chunk_concepts = [c for c in KEY_CONCEPTS if c.lower() in chunk.lower()]
                concept = chunk_concepts[0] if chunk_concepts else None
                
                # Генерируем диалог
                conv = generate_template_conversation(chunk, concept)
                file_conversations.append(conv)
            
            all_conversations.extend(file_conversations)
            print(f"   ✓ Создано {len(file_conversations)} диалогов")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    print()
    print("=" * 60)
    print(f"✅ Всего создано диалогов: {len(all_conversations)}")
    
    # Сохраняем в JSONL формат
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for conv in all_conversations:
            # Формат для llama2.c: просто массив сообщений
            f.write(json.dumps(conv["messages"], ensure_ascii=False) + '\n')
    
    file_size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"✅ Сохранено в: {OUTPUT_FILE}")
    print(f"📊 Размер файла: {file_size_kb:.1f} KB")
    print()
    print("💡 Эти диалоги можно использовать для:")
    print("   1. Fine-tuning модели в диалоговом формате")
    print("   2. Обучения на конвертированных данных")
    print("   3. Тестирования качества диалогов")

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║  InnerArianna Conversation Data Generator                 ║
║  Markdown → JSONL Conversations                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    process_markdown_to_conversations()

