#!/bin/bash
# Скрипт для обучения InnerArianna модели на данных из doc/

set -e

echo "🧬 InnerArianna Training Pipeline"
echo "=================================="
echo ""

# Шаг 1: Подготовка данных
echo "📚 Шаг 1: Подготовка данных из markdown файлов..."
python arianna_data.py prepare

# Шаг 2: Обучение токенизатора (опционально, можно использовать Llama 2)
VOCAB_SIZE=${1:-0}  # По умолчанию 0 = Llama 2 токенизатор

if [ "$VOCAB_SIZE" != "0" ]; then
    echo ""
    echo "🔤 Шаг 2: Обучение кастомного токенизатора (vocab_size=$VOCAB_SIZE)..."
    python arianna_data.py train_vocab --vocab_size=$VOCAB_SIZE
    
    echo ""
    echo "📝 Шаг 3: Экспорт токенизатора в .bin формат..."
    python tokenizer.py --tokenizer-model=data/tok${VOCAB_SIZE}.model
fi

# Шаг 3: Претокенизация
echo ""
echo "🔤 Шаг 3: Претокенизация данных..."
python arianna_data.py pretokenize --vocab_size=$VOCAB_SIZE

# Шаг 4: Обучение модели
echo ""
echo "🚀 Шаг 4: Обучение модели..."
echo ""

if [ "$VOCAB_SIZE" != "0" ]; then
    python train_arianna.py --vocab_source=custom --vocab_size=$VOCAB_SIZE
else
    python train_arianna.py --vocab_source=llama2 --vocab_size=32000
fi

echo ""
echo "✅ Обучение завершено! Модель сохранена в out/model.bin"
echo ""
echo "Для запуска чата:"
if [ "$VOCAB_SIZE" != "0" ]; then
    echo "  python chat.py out/model.bin -z data/tok${VOCAB_SIZE}.bin"
else
    echo "  python chat.py out/model.bin"
fi

