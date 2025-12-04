#!/bin/bash
# Быстрая проверка статуса обучения и тест модели

echo "📊 InnerArianna Status Check"
echo "============================"
echo ""

# Проверяем процесс
if ps aux | grep -v grep | grep "train_arianna.py" > /dev/null; then
    PID=$(ps aux | grep -v grep | grep "train_arianna.py" | awk '{print $2}' | head -1)
    CPU=$(ps aux | grep -v grep | grep "train_arianna.py" | awk '{print $3}' | head -1)
    echo "✅ Обучение запущено (PID: $PID, CPU: ${CPU}%)"
else
    echo "❌ Обучение не запущено"
fi

echo ""

# Проверяем checkpoint
if [ -f "out/ckpt.pt" ]; then
    python3 << EOF
import torch
try:
    ckpt = torch.load('out/ckpt.pt', map_location='cpu')
    iter_num = ckpt['iter_num']
    loss = ckpt['best_val_loss']
    max_iters = 5000
    progress = (iter_num / max_iters) * 100
    remaining = max_iters - iter_num
    hours_left = (remaining / (iter_num / 339)) / 60  # Примерно
    
    print(f"📈 Прогресс обучения:")
    print(f"   Итерация: {iter_num} / {max_iters} ({progress:.1f}%)")
    print(f"   Loss: {loss:.4f}")
    print(f"   Осталось: ~{hours_left:.1f} часов")
    print(f"   Модель обновлена: {iter_num // 500 * 500} итераций")
except Exception as e:
    print(f"❌ Ошибка чтения checkpoint: {e}")
EOF
else
    echo "❌ Checkpoint не найден"
fi

echo ""
echo "💾 Размер модели:"
ls -lh out/model.bin 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'

echo ""
echo "🧪 Быстрый тест модели:"
echo "   ./test_model.sh"
echo ""
echo "💬 Интерактивный чат:"
echo "   python3 chat_advanced.py out/model.bin -z data/tok4096.bin"

