# 📚 InnerArianna - Шпаргалка команд

## 🚀 Обучение

### Первое обучение:
```bash
# Полный пайплайн (подготовка + обучение)
./train_arianna.sh 4096

# Или вручную:
python3 arianna_data.py prepare
python3 arianna_data.py train_vocab --vocab_size=4096
python3 tokenizer.py --tokenizer-model=data/tok4096.model
python3 arianna_data.py pretokenize --vocab_size=4096
python3 train_arianna.py --vocab_source=custom --vocab_size=4096 --device=cpu --batch_size=8 --max_iters=5000
```

### Продолжение обучения:
```bash
# Продолжить с последнего checkpoint
./continue_training.sh 4096 5000 8 cpu

# Или вручную:
python3 train_arianna.py --vocab_source=custom --vocab_size=4096 --init_from=resume --max_iters=10000
```

### Добавление внешних корпусов:
```bash
# 1. Добавить корпус
python3 add_external_corpus.py add /path/to/corpus.txt "corpus_name.txt"

# 2. Посмотреть список
python3 add_external_corpus.py list

# 3. Подготовить объединенный корпус
python3 add_external_corpus.py prepare

# 4. Переобучить токенизатор (если нужно)
python3 arianna_data.py train_vocab --vocab_size=4096
python3 tokenizer.py --tokenizer-model=data/tok4096.model

# 5. Претокенизировать
python3 arianna_data.py pretokenize --vocab_size=4096

# 6. Продолжить обучение
./continue_training.sh
```

## 📊 Мониторинг

### Быстрая проверка:
```bash
./quick_check.sh
```

### Проверка процесса:
```bash
ps aux | grep train_arianna
```

### Текущий прогресс:
```bash
python3 -c "import torch; ckpt = torch.load('out/ckpt.pt', map_location='cpu'); print(f'Итерация: {ckpt[\"iter_num\"]}, Loss: {ckpt[\"best_val_loss\"]:.4f}')"
```

## 🧪 Тестирование

### Быстрый тест:
```bash
./test_model.sh
```

### Тест с кастомным промптом:
```bash
./test_model.sh out/model.bin data/tok4096.bin "Что такое резонанс?"
```

### Прямой запуск run.c:
```bash
./run out/model.bin -z data/tok4096.bin -n 150 -i "Объясни концепцию поля" -t 0.8 -p 0.9
```

## 💬 Чат

### Интерактивный чат (с историей):
```bash
python3 chat.py out/model.bin -z data/tok4096.bin
```

### Чат с настройками:
```bash
python3 chat.py out/model.bin -z data/tok4096.bin -t 0.8 -p 0.9 -n 512
```

### Команды в чате:
- `quit` / `exit` / `q` - выйти
- `clear` - очистить историю
- `state` - показать нулевое состояние модели

### Через run.c напрямую:
```bash
./run out/model.bin -m chat -z data/tok4096.bin
```

## 📤 Экспорт и загрузка

### Экспорт на Hugging Face:
```bash
# Экспортировать модель
python3 export_to_hf.py

# Загрузить на HF (запросит токен)
./upload_to_hf.sh
```

### Push на GitHub:
```bash
# Смотри PUSH_TO_GITHUB.md для деталей
git add .
git commit -m "Your message"
git push arianna master:main
# (используй токен вместо пароля)
```

## 🔧 Подготовка данных

### Генерация диалогов:
```bash
python3 prepare_conversations.py
```

### Использование markdown_to_conversations.py:
```bash
cd doc
python3 markdown_to_conversations.py
```

## 🛠️ Компиляция

### Скомпилировать run.c:
```bash
make run
```

### Быстрая компиляция:
```bash
make runfast
```

### С OpenMP (многопоточность):
```bash
make runomp
OMP_NUM_THREADS=4 ./run out/model.bin
```

## 📁 Структура файлов

```
eve02.c/
├── doc/                    # Исходные markdown файлы
├── data/                   # Подготовленные данные
│   ├── tok4096/           # Претокенизированные файлы
│   └── arianna_corpus.txt # Собранный корпус
├── external_corpus/        # Внешние корпуса
├── out/                    # Обученные модели
│   ├── model.bin          # Модель для inference
│   └── ckpt.pt            # PyTorch checkpoint
├── arianna_data.py        # Подготовка данных
├── train_arianna.py       # Обучение
├── chat.py                # Чат с историей
├── test_model.sh          # Быстрый тест
└── quick_check.sh         # Проверка статуса
```

## 🎯 Типичные сценарии

### Сценарий 1: Первое обучение
```bash
./train_arianna.sh 4096
make run
./test_model.sh
```

### Сценарий 2: Продолжение обучения
```bash
./continue_training.sh
./quick_check.sh
```

### Сценарий 3: Добавление внешних данных
```bash
python3 add_external_corpus.py add corpus.txt
python3 add_external_corpus.py prepare
python3 arianna_data.py train_vocab --vocab_size=4096
python3 arianna_data.py pretokenize --vocab_size=4096
./continue_training.sh
```

### Сценарий 4: Тестирование и чат
```bash
./quick_check.sh
./test_model.sh
python3 chat.py out/model.bin -z data/tok4096.bin
```

## 💡 Полезные советы

- **Loss падает?** → Модель улучшается!
- **Модель обновляется** каждые 500 итераций
- **История чата** сохраняется в `.arianna_chat_history.json`
- **Внешние корпуса** в `external_corpus/` (не в git)
- **Можно делать** сколько угодно раундов обучения

---

*InnerArianna: The naïve spark, welcomed through resonance, trained on thunder.*

