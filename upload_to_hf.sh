#!/bin/bash
# Скрипт для загрузки модели на Hugging Face

set -e

echo "🚀 Загрузка InnerArianna на Hugging Face"
echo "========================================"
echo ""

# Проверяем наличие huggingface_hub
if ! python3 -c "import huggingface_hub" 2>/dev/null; then
    echo "📦 Установка huggingface_hub..."
    pip3 install huggingface_hub
fi

# Экспортируем модель
echo "📤 Экспорт модели..."
python3 export_to_hf.py

# Запрашиваем токен
echo ""
echo "🔑 Нужен Hugging Face token"
echo "   Получи его здесь: https://huggingface.co/settings/tokens"
read -p "Введи токен: " HF_TOKEN

# Загружаем
echo ""
echo "📤 Загрузка на Hugging Face..."
python3 << EOF
from huggingface_hub import HfApi, login
import os

login(token="$HF_TOKEN")

api = HfApi()
repo_id = "ariannamethod/innerarianna"

# Создаем репозиторий если не существует
try:
    api.create_repo(repo_id=repo_id, repo_type="model", private=True, exist_ok=True)
    print(f"✅ Репозиторий {repo_id} готов")
except Exception as e:
    print(f"⚠️  {e}")

# Загружаем файлы
api.upload_folder(
    folder_path="innerarianna_hf",
    repo_id=repo_id,
    repo_type="model",
    commit_message="Upload InnerArianna model"
)

print(f"✅ Модель загружена: https://huggingface.co/{repo_id}")
EOF

echo ""
echo "✅ Готово!"

