#!/bin/bash
# Быстрый тест модели InnerArianna

MODEL="${1:-out/model.bin}"
TOKENIZER="${2:-data/tok4096.bin}"
PROMPT="${3:-Что такое резонанс в Arianna Method?}"

echo "🧪 Тест InnerArianna"
echo "===================="
echo ""
echo "Модель: $MODEL"
echo "Токенизатор: $TOKENIZER"
echo "Промпт: $PROMPT"
echo ""
echo "---"
echo ""

./run "$MODEL" -z "$TOKENIZER" -n 150 -i "$PROMPT" -t 0.8 -p 0.9

echo ""
echo "---"
echo ""
echo "💡 Для интерактивного чата:"
echo "   python3 chat_advanced.py $MODEL -z $TOKENIZER"

