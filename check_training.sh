#!/bin/bash
# Скрипт для проверки прогресса обучения

echo "📊 Статус обучения InnerArianna"
echo "================================"
echo ""

# Проверяем процесс
if ps aux | grep -v grep | grep "train_arianna.py" > /dev/null; then
    echo "✅ Обучение запущено"
    ps aux | grep -v grep | grep "train_arianna.py" | awk '{print "   PID:", $2, "CPU:", $3"%", "Memory:", $11"MB"}'
else
    echo "❌ Обучение не запущено"
fi

echo ""
echo "📈 Последние логи:"
echo "-----------------"
tail -20 training.log 2>/dev/null | grep -E "(step |loss |iter_num)" | tail -5 || echo "Логи еще не созданы"

echo ""
echo "💾 Сохраненные модели:"
ls -lh out/*.bin 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'

echo ""
echo "Для просмотра полных логов: tail -f training.log"

