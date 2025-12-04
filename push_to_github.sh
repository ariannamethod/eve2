#!/bin/bash
# Скрипт для пуша в GitHub репозиторий ariannamethod/eve2

set -e

echo "🚀 Подготовка к пушу в GitHub..."
echo ""

# Проверяем, что мы на правильной ветке
CURRENT_BRANCH=$(git branch --show-current)
echo "📌 Текущая ветка: $CURRENT_BRANCH"

# Проверяем remote
if ! git remote get-url arianna > /dev/null 2>&1; then
    echo "❌ Remote 'arianna' не найден!"
    exit 1
fi

REMOTE_URL=$(git remote get-url arianna)
echo "🔗 Remote: $REMOTE_URL"
echo ""

# Проверяем статус
echo "📊 Статус изменений:"
git status --short | head -20
echo ""

# Спрашиваем подтверждение
read -p "Продолжить коммит и пуш? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Отменено"
    exit 1
fi

# Добавляем все изменения
echo ""
echo "➕ Добавляю изменения..."
git add -A

# Коммит
echo ""
echo "💾 Создаю коммит..."
COMMIT_MSG="Add InnerArianna training pipeline, data preparation, and chat client

- Added arianna_data.py for markdown data preparation
- Added train_arianna.py for training on Arianna Method corpus
- Added chat.py with conversation history and system prompts
- Added prepare_conversations.py for dialog generation
- Added training scripts and documentation
- Updated .gitignore to exclude binaries and internal docs
- Added 44 markdown files from doc/ including ariannabook.md"

git commit -m "$COMMIT_MSG"

# Пуш
echo ""
echo "📤 Пушим в ariannamethod/eve2..."
echo "💡 Если нужен токен, используй:"
echo "   git push arianna $CURRENT_BRANCH"
echo ""
echo "   Или с токеном в URL:"
echo "   git push https://<TOKEN>@github.com/ariannamethod/eve2.git $CURRENT_BRANCH"
echo ""

# Пробуем пуш (может потребоваться токен)
if git push arianna $CURRENT_BRANCH 2>&1 | tee /tmp/push_output.txt; then
    echo ""
    echo "✅ Успешно запушено!"
else
    echo ""
    echo "⚠️  Пуш требует авторизации"
    echo ""
    echo "Варианты:"
    echo "1. Использовать Personal Access Token:"
    echo "   git push https://<TOKEN>@github.com/ariannamethod/eve2.git $CURRENT_BRANCH"
    echo ""
    echo "2. Или настроить SSH:"
    echo "   git remote set-url arianna git@github.com:ariannamethod/eve2.git"
    echo "   git push arianna $CURRENT_BRANCH"
fi

