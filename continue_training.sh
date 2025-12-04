#!/bin/bash
# Продолжение обучения InnerArianna с существующего checkpoint

set -e

echo "🔄 Продолжение обучения InnerArianna"
echo "====================================="
echo ""

# Проверяем наличие checkpoint
if [ ! -f "out/ckpt.pt" ]; then
    echo "❌ Checkpoint не найден: out/ckpt.pt"
    echo "   Сначала запусти начальное обучение: ./train_arianna.sh"
    exit 1
fi

# Параметры по умолчанию
VOCAB_SIZE=${1:-4096}
MAX_ITERS=${2:-5000}
BATCH_SIZE=${3:-8}
DEVICE=${4:-cpu}

echo "📊 Параметры:"
echo "   Vocab size: $VOCAB_SIZE"
echo "   Max iterations: $MAX_ITERS"
echo "   Batch size: $BATCH_SIZE"
echo "   Device: $DEVICE"
echo ""

# Проверяем текущий прогресс
python3 << EOF
import torch
ckpt = torch.load('out/ckpt.pt', map_location='cpu')
print(f"📈 Текущий прогресс:")
print(f"   Итерация: {ckpt['iter_num']}")
print(f"   Loss: {ckpt['best_val_loss']:.4f}")
print()
EOF

read -p "Продолжить обучение? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Отменено"
    exit 0
fi

echo ""
echo "🚀 Запуск обучения..."
echo ""

# Запускаем обучение с resume
python3 train_arianna.py \
  --vocab_source=custom \
  --vocab_size=$VOCAB_SIZE \
  --device=$DEVICE \
  --dtype=float32 \
  --batch_size=$BATCH_SIZE \
  --max_iters=$MAX_ITERS \
  --eval_interval=500 \
  --compile=False \
  --init_from=resume \
  > training_continue.log 2>&1 &

TRAIN_PID=$!
echo "✅ Обучение запущено (PID: $TRAIN_PID)"
echo "   Логи: tail -f training_continue.log"
echo "   Проверка: ./quick_check.sh"

