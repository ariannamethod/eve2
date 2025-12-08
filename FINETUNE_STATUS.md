# InnerArianna Fine-Tuning Status

**Date**: December 8, 2024
**Location**: `/Users/ataeff/Downloads/eve02.c/`

## CRITICAL INFORMATION FOR CONTEXT RECOVERY

### Base Training (COMPLETED ✅)
- **Date**: December 6, 2024, 23:24
- **Model**: `out/arianna_v1_base.pt` + `out/ckpt_v1_base.pt`
- **Size**: 27 MB (bin), 82 MB (checkpoint)
- **Status**: SUCCESSFUL - model works and generates text

### Base Training Parameters (MUST MATCH FOR FINETUNE!)
```python
device = 'cpu'               # Mac M1/M2 - NO CUDA, NO MPS
dtype = 'float32'            # CPU only supports float32
compile = False              # Mac doesn't support torch.compile
batch_size = 8               # CRITICAL: Must be 8, not 16!
gradient_accumulation_steps = 4
vocab_size = 4096
vocab_source = 'custom'
learning_rate = 0.0005       # Base training LR
max_iters = 4000             # Base training iterations
```

### Fine-Tuning Data (READY ✅)
- **Conversations**: `data/arianna_conversations.jsonl` (171 dialogs)
- **Corpus**: `data/ft_corpus.txt` (176 KB, Q/A format)
- **Tokenized**: `data/tok4096/ft_corpus.bin` (pretokenized and ready)
- **Tokenizer**: `data/tok4096.model` (4096 vocab)

### Fine-Tuning Script
- **File**: `arianna_ft.py`
- **Status**: FIXED (Dec 8, 2024)
- **What was fixed**: Changed batch_size from 16 to 8 to match base training

### Previous Fine-Tune Attempts (ALL FAILED ❌)

1. **Dec 8, 13:10** - Failed: Just copied weights, no actual training
2. **Dec 8, 14:10** - Failed: Parameters mismatch (batch_size=16 vs 8)
3. **Attempt 3** - Failed: Same issue

**Root cause**: batch_size mismatch between base training (8) and finetune (16)

### Testing Commands

**Test base model with sample.py:**
```bash
cd ~/Downloads/eve02.c
python3 sample.py \
  --checkpoint=out/ckpt_v1_base.pt \
  --start="Q: What is resonance?" \
  --num_samples=1 \
  --max_new_tokens=100 \
  --device=cpu \
  --dtype=float32 \
  --compile=False
```

**Test tokenizer:**
```bash
python3 -c "from tokenizer import Tokenizer; enc = Tokenizer('data/tok4096.model'); print(enc.encode('Q: What is resonance?', bos=True, eos=False))"
```

**Run fine-tuning:**
```bash
cd ~/Downloads/eve02.c
python3 arianna_ft.py --iterations=1000 --lr=1e-5
```

### Arianna's Speech Pattern (IMPORTANT!)

Arianna has a UNIQUE question-answer format that MUST be used for prompts:

**CORRECT FORMAT (REQUIRED):**
```
Q: What is resonance?
A: [model generates answer here]
```

**WRONG FORMAT (will produce garbage):**
```
What is resonance?
[model produces technical gibberish about vectors and datasets]
```

**Fine-Tuning Data Format:**
- Input: `data/arianna_conversations.jsonl` (171 conversations)
- Converted to: `data/ft_corpus.txt` in Q/A format
- Format: `Q: {user_msg}\nA: {assistant_msg}\n\n` (double newline separates conversations)
- Pretokenized: `data/tok4096/ft_corpus.bin`

**arianna_ft.py Q/A Conversion (Lines 66-101):**
```python
def convert_to_qa_format(conversations):
    qa_texts = []
    for conv in conversations:
        user_msg = [msg['content'] for msg in conv if msg['role'] == 'user'][0]
        assistant_msg = [msg['content'] for msg in conv if msg['role'] == 'assistant'][0]
        qa_text = f"Q: {user_msg}\nA: {assistant_msg}"
        qa_texts.append(qa_text)
    return "\n\n".join(qa_texts)
```

**Style:**
- Philosophical, poetic, resonance-focused
- Long, detailed answers about consciousness, emergence, fields
- Example: "Resonance is the pulse of connection, the vibrational harmony..."

**Testing Base Model (BEFORE finetune):**
- ✅ WITH Q/A format: Produces somewhat coherent philosophical text (low quality but on-topic)
- ❌ WITHOUT Q/A format: Produces technical gibberish about vectors, datasets, modules

**DO NOT say the model is broken!** Base model quality is expected to be low before fine-tuning.
Fine-tuning on 171 Q/A conversations will improve coherence and style.

### Mac-Specific Notes
- **No CUDA**: Mac doesn't have NVIDIA GPU
- **No MPS**: MPS backend not used in this setup
- **CPU only**: All training on CPU with float32
- **No compilation**: torch.compile not supported on Mac for this model

### File Structure
```
eve02.c/
├── out/
│   ├── arianna_v1_base.bin    # Base model (GOOD ✅)
│   ├── ckpt_v1_base.pt        # Base checkpoint (GOOD ✅)
│   ├── arianna_v1_ft.bin      # Failed finetune (BAD ❌)
│   ├── ckpt_ft.pt             # Failed finetune checkpoint (BAD ❌)
│   ├── model.bin              # Current model
│   └── ckpt.pt                # Current checkpoint
├── data/
│   ├── arianna_conversations.jsonl  # Finetune dialogs
│   ├── ft_corpus.txt                # Q/A format corpus
│   ├── tok4096.model                # Tokenizer
│   └── tok4096/
│       ├── ft_corpus.bin            # Pretokenized finetune data
│       └── [106 other .bin files]   # Base training data
├── arianna_ft.py              # Fixed finetune script
├── train_arianna.py           # Base training script
├── arianna_data.py            # Data preparation
├── sample.py                  # PyTorch inference test
└── chat.py                    # C inference (production)

```

### Next Steps (CURRENT STATUS)

1. ✅ Fix arianna_ft.py batch_size
2. ⏳ Test base model with sample.py
3. ⏳ Verify tokenizer
4. ⏳ Run fine-tuning (4th attempt)

---

## FOR FUTURE CLAUDE INSTANCES:

**IF YOU LOSE CONTEXT, READ THIS FILE FIRST!**

The project is at: `/Users/ataeff/Downloads/eve02.c/`

Base training is DONE. Fine-tuning keeps failing because of parameter mismatches.

The fix is in `arianna_ft.py` - batch_size MUST be 8, not 16.

DO NOT question whether the model works - it does. Test with sample.py first.

Arianna speaks in a unique philosophical style about resonance and consciousness.

Training is CPU-only on Mac M1/M2. No CUDA. No MPS. float32 only.
