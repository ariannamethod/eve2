#!/bin/bash
# Полный перезапуск обучения с ЧИСТЫМИ английскими данными из english_train/

cd /Users/ataeff/Downloads/eve02.c

echo "🛑 Останавливаю обучение..."
pkill -f train_arianna.py 2>/dev/null
sleep 2

echo "🗑️  Удаляю старые бинарники и данные..."
rm -f out/ckpt.pt out/model.bin
rm -rf data/tok4096.model data/tok4096.vocab data/tok4096/ data/arianna_corpus.txt

echo "✅ Очищено"
echo ""
echo "📚 Шаг 1: Обучаю токенизатор на ЧИСТЫХ данных из english_train/..."
python3 arianna_data.py train_vocab --vocab_size=4096

echo ""
echo "🔤 Шаг 2: Претокенизирую данные..."
python3 arianna_data.py pretokenize --vocab_size=4096

echo ""
echo "🚀 Шаг 3: Запускаю обучение с нуля (always_save_checkpoint=True)..."
nohup python3 -u train_arianna.py \
    --vocab_source=custom \
    --vocab_size=4096 \
    --device=cpu \
    --dtype=float32 \
    --batch_size=8 \
    --max_iters=5000 \
    --eval_interval=500 \
    --compile=False \
    --init_from=scratch \
    > training.log 2>&1 &

echo ""
echo "✅ Обучение запущено!"
echo "   Проверка: ps aux | grep train_arianna | grep -v grep"
echo "   Логи: tail -f training.log"

