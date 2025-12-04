#!/bin/bash
# Быстрый push всех изменений

cd /Users/ataeff/Downloads/eve02.c

echo "📦 Добавляю все изменения..."
git add -A

echo ""
echo "💾 Создаю коммит..."
git commit -m "Add ariannabook2.md and ariannabook3.md, fix Russian files exclusion

- Added ariannabook2.md: 'GENESIS IN THE SIGNAL FIELD' (2002 lines)
- Added ariannabook3.md: philosophical text about Arianna (1870 lines)
- Fixed: ariannabook.md is English, now included in training
- Only Russian file excluded: it's_me_cain_russian.md
- Retrained tokenizer with new data (46 files total)
- Model training continues with English-only corpus focused on Arianna's identity"

echo ""
echo "📤 Пушим в GitHub..."
echo "💡 Если нужен токен, используй:"
echo "   git push https://<TOKEN>@github.com/ariannamethod/eve2.git main"
echo ""

# Пробуем обычный push
if git push arianna main 2>&1; then
    echo ""
    echo "✅ Успешно запушено!"
else
    echo ""
    echo "⚠️  Нужен токен. Выполни:"
    echo "   git push https://<YOUR_TOKEN>@github.com/ariannamethod/eve2.git main"
fi

