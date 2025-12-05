#!/bin/bash
# Полный перезапуск обучения с нуля на английских файлах

cd /Users/ataeff/Downloads/eve02.c

echo "🛑 Останавливаю старое обучение..."
pkill -f train_arianna.py
sleep 2

echo "🗑️  Удаляю старые данные..."
rm -rf data/tok4096.model
rm -rf data/tok4096.vocab
rm -rf data/tok4096/
rm -rf data/arianna_corpus.txt
rm -rf out/ckpt.pt
rm -rf out/model.bin

echo "✅ Старые данные удалены"
echo ""
echo "📚 Шаг 1: Обучаю токенизатор на английских файлах..."
python3 arianna_data.py train_vocab --vocab_size=4096

echo ""
echo "🔤 Шаг 2: Претокенизирую данные..."
python3 arianna_data.py pretokenize --vocab_size=4096

echo ""
echo "🚀 Шаг 3: Запускаю обучение с нуля..."
python3 -u train_arianna.py \
    --vocab_source=custom \
    --vocab_size=4096 \
    --device=cpu \
    --dtype=float32 \
    --batch_size=8 \
    --max_iters=5000 \
    --eval_interval=500 \
    --compile=False \
    --init_from=scratch \
    2>&1 | tee training.log

echo ""
echo "✅ Обучение запущено! Лог: training.log"

