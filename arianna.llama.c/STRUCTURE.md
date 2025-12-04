# arianna.llama.c/ - File Structure

Generated: 2025-12-04

## Directory Tree

```
arianna.llama.c/
├── README.md                  # Main documentation
├── LICENSE                    # MIT license
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
├── STRUCTURE.md              # This file
│
├── core/                      # C inference engine & model
│   ├── run.c                  # Main C inference (38 KB, 1000+ lines)
│   ├── model.py               # PyTorch Transformer implementation
│   ├── tokenizer.py           # Tokenizer utilities
│   └── Makefile               # Build configuration
│
├── cli/                       # Command-line interfaces
│   ├── chat.py                # Basic chat with history
│   └── chat_advanced.py       # Advanced chat options
│
├── training/                  # Training pipeline
│   ├── train.py               # Main training script (from train_arianna.py)
│   ├── data_prep.py           # Data preparation (from arianna_data.py)
│   └── finetune.py            # Fine-tuning on conversations
│
├── dynamic/                   # Leo-style dynamic modules
│   ├── __init__.py            # Package initialization
│   ├── presence_pulse.py      # ✅ Novelty, arousal, entropy detection
│   ├── trauma_detector.py     # ✅ Bootstrap wound detection
│   ├── knowledge_islands.py   # ✅ Dynamic semantic crystallization
│   ├── episodes.py            # ✅ Episodic conversation memory
│   └── resonance.py           # ✅ Resonant attention (Santaclaus)
│
├── state/                     # Dynamic layer storage
│   ├── README.md              # Storage documentation
│   ├── .gitignore             # Ignore *.db files
│   └── *.db                   # SQLite databases (gitignored, grows per instance)
│
├── utils/                     # Utilities
│   ├── export.py              # Model export tools
│   └── corpus_tools.py        # Corpus management (from add_external_corpus.py)
│
├── scripts/                   # Automation
│   ├── train_full.sh          # Full training pipeline
│   ├── test_model.sh          # Model testing
│   └── quick_check.sh         # Quick validation
│
├── docs/                      # Documentation
│   └── LEO_INTEGRATION.md     # ✅ Dynamic layer integration plan
│
├── tests/                     # Testing (empty, for future)
│   └── (to be added)
│
└── config/                    # Configurations (empty, for future)
    └── (to be added)
```

## File Counts

- **Total files:** ~20
- **Python modules:** 12
- **C source files:** 1 (run.c, ~1000 lines)
- **Shell scripts:** 3
- **Documentation:** 4 markdown files
- **Config files:** 3 (requirements.txt, LICENSE, .gitignore)

## Size Breakdown

- **core/run.c:** ~38 KB (main inference engine)
- **training/train.py:** ~15 KB (training loop)
- **dynamic/ modules:** ~15 KB total (5 modules)
- **Total size:** ~100 KB (code only, no data/weights)

## Module Status

### ✅ Ready for use
- core/run.c, model.py, tokenizer.py
- cli/chat.py, chat_advanced.py
- training/* (all training scripts)
- utils/* (export and corpus tools)

### ✅ Skeleton ready (for integration after weights)
- dynamic/presence_pulse.py
- dynamic/trauma_detector.py
- dynamic/knowledge_islands.py
- dynamic/episodes.py
- dynamic/resonance.py

### 📋 Planned (not yet created)
- tests/* (unit and integration tests)
- config/* (JSON configurations)
- docs/ARCHITECTURE.md, TRAINING_GUIDE.md, API.md

## Key Differences from Root

This is a **clean, modular refactor** of the root eve2/ directory:

| Feature | Root (eve2/) | Clean (arianna.llama.c/) |
|---------|-------------|--------------------------|
| Structure | Flat, mixed | Organized by purpose |
| Legacy files | Yes (tinystories.py, etc.) | No, removed |
| Leo modules | No | Yes, skeletons ready |
| Documentation | Scattered READMEs | Centralized in docs/ |
| Testing | Minimal | Prepared structure |
| Config | Hardcoded | JSON configs (planned) |

## Integration Points

### Current (static weights only)
```python
# Simple inference
python cli/chat.py ../out/model.bin -z ../data/tok4096.bin
```

### Future (with dynamic layer)
```python
# With Leo-style dynamics enabled
python cli/chat.py ../out/model.bin \
    --enable-dynamic \
    --presence-pulse \
    --trauma-detection \
    --knowledge-islands
```

## Storage Growth

- **Static weights:** ~200 MB (frozen)
- **Dynamic state:** Starts at 0, grows with conversation
  - After 100 convs: ~5 MB
  - After 1000 convs: ~50 MB
  - After 10000 convs: ~500 MB

## Next Steps

1. ✅ Structure created
2. ✅ Core files copied
3. ✅ Documentation written
4. ✅ Leo modules skeleton ready
5. ⏳ Wait for base weights (~today evening)
6. 📋 Implement dynamic layer integration
7. 📋 Add tests
8. 📋 Polish CLI with colors/streaming

---

**Status:** Clean architecture ready, awaiting weights for Leo integration
**Date:** 2025-12-04
