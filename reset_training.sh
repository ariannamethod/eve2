#!/bin/bash
# Полный сброс обучения - удаляем все данные и начинаем с нуля

cd /Users/ataeff/Downloads/eve02.c

echo "🛑 Останавливаю обучение..."
pkill -f train_arianna.py
sleep 2

echo "🗑️  Удаляю старые данные..."
rm -rf data/tok4096.model
rm -rf data/tok4096.vocab
rm -rf data/tok4096/
rm -rf data/arianna_corpus.txt
rm -rf out/ckpt.pt
rm -rf out/model.bin

echo "✅ Все старые данные удалены"
echo ""
echo "📚 Теперь нужно:"
echo "1. python3 arianna_data.py train_vocab --vocab_size=4096"
echo "2. python3 arianna_data.py pretokenize --vocab_size=4096"
echo "3. python3 train_arianna.py --init_from=scratch ..."

