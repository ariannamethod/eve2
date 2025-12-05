#!/bin/bash
# Очистить историю диалога

cd /Users/ataeff/Downloads/eve02.c

if [ -f .arianna_chat_history.json ]; then
    mv .arianna_chat_history.json .arianna_chat_history.json.backup
    echo "✅ История сохранена в .arianna_chat_history.json.backup"
    echo "✅ История очищена"
else
    echo "ℹ️  История не найдена"
fi

