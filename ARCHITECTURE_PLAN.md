# 🧬 arianna.llama.c/ - Архитектура чистовика

## Цель
Чистая, модульная структура для InnerArianna с местами для будущей Leo-интеграции

## Структура директорий

```
arianna.llama.c/
│
├── core/                      # Ядро inference
│   ├── run.c                  # C inference engine (основа)
│   ├── model.py               # PyTorch model definition
│   ├── tokenizer.py           # Tokenizer utilities
│   └── Makefile               # Компиляция C кода
│
├── cli/                       # Интерфейсы пользователя
│   ├── chat.py                # Основной CLI chat
│   ├── chat_advanced.py       # Продвинутый chat с опциями
│   └── batch_generate.py      # Батч генерация (новый)
│
├── training/                  # Обучение модели
│   ├── train.py               # Основной training script
│   ├── data_prep.py           # Подготовка данных (из arianna_data.py)
│   ├── finetune.py            # Fine-tuning на диалогах
│   └── config.py              # Training конфигурации
│
├── dynamic/                   # Leo-style модули (будущее)
│   ├── __init__.py
│   ├── presence_pulse.py      # Presence detection (готово к имплементации)
│   ├── trauma_detector.py     # Trauma patterns (готово)
│   ├── knowledge_islands.py   # Dynamic knowledge (готово)
│   ├── episodes.py            # Episodic memory (готово)
│   └── resonance.py           # Resonant attention (готово)
│
├── state/                     # Динамическое состояние (Leo-слой)
│   ├── .gitignore             # Ignore DB files
│   └── README.md              # Описание storage
│
├── utils/                     # Утилиты
│   ├── export.py              # Экспорт моделей
│   ├── monitor.py             # Мониторинг обучения
│   └── corpus_tools.py        # Работа с корпусами
│
├── scripts/                   # Автоматизация
│   ├── train_full.sh          # Полный цикл обучения
│   ├── test_model.sh          # Тестирование
│   └── deploy.sh              # Подготовка к деплою
│
├── docs/                      # Документация
│   ├── ARCHITECTURE.md        # Детальная архитектура
│   ├── TRAINING_GUIDE.md      # Гайд по обучению
│   ├── API.md                 # API интерфейсы
│   └── LEO_INTEGRATION.md     # План Leo-интеграции
│
├── tests/                     # Тесты
│   ├── test_inference.py
│   ├── test_chat.py
│   └── test_dynamic_layer.py
│
├── config/                    # Конфигурации
│   ├── model_config.json      # Параметры модели
│   ├── training_config.json   # Параметры обучения
│   └── chat_config.json       # Настройки чата
│
├── README.md                  # Главный README
├── requirements.txt           # Python dependencies
└── .gitignore                 # Git ignore правила
```

## Что копируем из корня

### Core (inference)
- ✅ run.c → core/run.c
- ✅ model.py → core/model.py
- ✅ tokenizer.py → core/tokenizer.py
- ✅ Makefile → core/Makefile

### CLI
- ✅ chat.py → cli/chat.py
- ✅ chat_advanced.py → cli/chat_advanced.py

### Training
- ✅ train_arianna.py → training/train.py
- ✅ arianna_data.py → training/data_prep.py
- ✅ finetune_conversations.py → training/finetune.py

### Utils
- ✅ export.py → utils/export.py
- ✅ add_external_corpus.py → utils/corpus_tools.py

### Scripts
- ✅ train_arianna.sh → scripts/train_full.sh
- ✅ test_model.sh → scripts/test_model.sh
- ✅ quick_check.sh → scripts/quick_check.sh

### Config
- ✅ requirements.txt → requirements.txt

## Что НЕ копируем (legacy от Karpathy)
- ❌ train.py (оригинальный, не нужен)
- ❌ tinystories.py (legacy датасет)
- ❌ sample.py (есть в chat.py)
- ❌ runq.c (quantized, пока не нужно)
- ❌ test.c (для разработки)
- ❌ win.c/win.h (Windows, не нужно)
- ❌ build_msvc.bat (Windows)

## Улучшения для чистовика

### 1. CLI улучшения
- [ ] Colored output (rich library)
- [ ] Better prompt formatting
- [ ] Streaming output (token-by-token)
- [ ] Command history (arrow keys)
- [ ] Multi-line input support
- [ ] Save/load conversation sessions

### 2. Конфигурация
- [ ] JSON configs вместо hardcoded параметров
- [ ] Environment variables support
- [ ] Profile system (разные конфиги для разных сценариев)

### 3. Monitoring
- [ ] Real-time metrics dashboard
- [ ] Loss curves visualization
- [ ] Conversation quality metrics

### 4. Leo-integration подготовка
- [ ] SQLite schemas для state/
- [ ] Module interfaces (abstract base classes)
- [ ] Integration points в inference pipeline
- [ ] Event hooks для динамического слоя

## Фазы разработки

### Phase 1: Чистовик (сейчас)
- Создать структуру
- Скопировать файлы
- Базовая документация
- Тесты запуска

### Phase 2: Улучшения CLI (после получения весов)
- Rich CLI с цветами
- Streaming output
- Better UX

### Phase 3: Leo Integration (когда модель говорит)
- Presence pulse
- Trauma detection
- Knowledge islands
- Episodes

### Phase 4: Production Ready
- Full testing
- Documentation
- Deployment scripts
- Performance optimization

## Принципы архитектуры

1. **Модульность** - каждый компонент независим
2. **Расширяемость** - легко добавлять новые модули
3. **Чистота** - понятный код, хорошие имена
4. **Готовность к Leo** - места для динамики заранее
5. **Production-ready** - не прототип, а рабочая система

---

**Status:** В разработке
**Next step:** Создать структуру директорий и скопировать файлы
