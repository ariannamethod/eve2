# Инструкция для пуша на GitHub

## Когда получишь токен:

```bash
cd /Users/ataeff/Downloads/eve02.c

# 1. Проверь, что все файлы добавлены
git status

# 2. Если нужно, добавь новые файлы
git add chat_advanced.py prepare_conversations.py export_to_hf.py upload_to_hf.sh

# 3. Создай коммит (если еще не создан)
git commit -m "Add InnerArianna training pipeline with conversation support

- Add arianna_data.py for preparing training data from markdown files
- Add train_arianna.py for training on Arianna Method corpus
- Add chat.py and chat_advanced.py CLI clients with conversation history
- Add prepare_conversations.py for dialog format data
- Add export_to_hf.py for Hugging Face export
- Add training automation scripts
- Add documentation (QUICKSTART.md, README_ARIANNA.md)
- Add Arianna Method corpus (doc/*.md files)
- Update Makefile to support chat CLI compilation
- Add .gitignore for temporary files"

# 4. Запушь (GitHub попросит username и токен вместо password)
git push arianna master:main
```

## Если нужен Personal Access Token:

1. Иди на: https://github.com/settings/tokens
2. Generate new token (classic)
3. Выбери права: `repo` (полный доступ к репозиториям)
4. Скопируй токен
5. При `git push` используй:
   - Username: твой GitHub username
   - Password: вставь токен (не пароль!)

## Альтернатива через SSH:

```bash
# Измени remote на SSH
git remote set-url arianna git@github.com:ariannamethod/eve2.git

# Тогда push будет через SSH ключ
git push arianna master:main
```

