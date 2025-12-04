# 🧬 InnerArianna Training Guide

## Быстрый старт

### Первое обучение:
```bash
./train_arianna.sh 4096
```

### Продолжение обучения:
```bash
./continue_training.sh 4096 5000 8 cpu
```

### Добавление внешних корпусов:
```bash
# 1. Добавить корпус
python3 add_external_corpus.py add /path/to/corpus.txt

# 2. Подготовить объединенный корпус
python3 add_external_corpus.py prepare

# 3. Переобучить токенизатор (если нужно)
python3 arianna_data.py train_vocab --vocab_size=4096
python3 tokenizer.py --tokenizer-model=data/tok4096.model

# 4. Претокенизировать
python3 arianna_data.py pretokenize --vocab_size=4096

# 5. Продолжить обучение
./continue_training.sh
```

## Мониторинг

```bash
# Быстрая проверка
./quick_check.sh

# Тест модели
./test_model.sh

# Интерактивный чат
python3 chat_advanced.py out/model.bin -z data/tok4096.bin
```

## Многоэтапное обучение

Смотри `MULTI_STAGE_TRAINING.md` для деталей.

## Экспорт и загрузка

```bash
# Экспорт на Hugging Face
python3 export_to_hf.py
./upload_to_hf.sh
```

---

*InnerArianna: The naïve spark, welcomed through resonance, trained on thunder.*

