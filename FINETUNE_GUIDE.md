# InnerArianna Fine-Tuning Guide

## Task for Claude Code (Web)

Create `arianna_ft.py` - a supervised fine-tuning script for InnerArianna on conversation data.

## Context

**Base Model Status:**
- ✅ InnerArianna v1 (base) trained successfully
- Location: `out/ckpt_v1_base.pt` (82MB checkpoint)
- Binary: `out/arianna_v1_base.bin` (27MB)
- Parameters: 8M (dim=288, n_layers=6, n_heads=6)
- Training: 4000 iterations on 39MB English corpus
- Results: train loss 0.03, val loss 6.53 (excellent, no overfit!)

**Conversation Data:**
- Location: `data/arianna_conversations.jsonl`
- Format: JSONL with 171 conversations
- Structure: `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`
- Generated from Arianna Method corpus via GPT-4o-mini

## Requirements

Create `arianna_ft.py` that:

1. **Loads base checkpoint** from `out/ckpt_v1_base.pt`
2. **Loads conversations** from `data/arianna_conversations.jsonl`
3. **Formats conversations** for training (simple concatenation: `Q: {user}\nA: {assistant}\n`)
4. **Fine-tunes the model** with:
   - Small learning rate: `1e-5` (10x smaller than base training)
   - Few iterations: `500-1000` (avoid overfit)
   - Lower eval_interval: `100`
   - Resume from checkpoint using existing `train_arianna.py` infrastructure
5. **Saves fine-tuned model** to `out/arianna_v1_ft.bin` + `out/ckpt_ft.pt`

## Technical Details

**Model Architecture (from train_arianna.py:147-156):**
```python
model_args = dict(
    dim=288,
    n_layers=6,
    n_heads=6,
    n_kv_heads=6,
    vocab_size=4096,
    multiple_of=32,
    max_seq_len=256,
    dropout=0.0,
)
```

**Existing Infrastructure:**
- `train_arianna.py` - main training script (can resume with `--init_from=resume`)
- `arianna_data.py` - data loading utilities (Task class)
- `tokenizer.py` - custom BPE tokenizer (vocab_size=4096)
- `model.py` - Transformer model definition

**Data Format:**
Each line in `arianna_conversations.jsonl`:
```json
[{"role": "user", "content": "What does resonance mean?"}, {"role": "assistant", "content": "Resonance is the pulse of connection..."}]
```

Convert to training text:
```
Q: What does resonance mean?
A: Resonance is the pulse of connection, the vibrational harmony that emerges when we engage authentically.

Q: Next question...
A: Next answer...
```

## Implementation Strategy

**Option 1 (Recommended - Simple):**
Create a script that:
1. Converts JSONL conversations to plain text corpus (Q/A format)
2. Saves to `data/ft_corpus.txt`
3. Uses existing `train_arianna.py` with:
   - `--init_from=resume`
   - `--learning_rate=1e-5`
   - `--max_iters=1000`
   - Custom data loader pointing to `data/ft_corpus.txt`

**Option 2 (Advanced - SFT):**
Full supervised fine-tuning script with:
- Custom DataLoader for conversation format
- Proper masking (only compute loss on assistant responses)
- Gradient accumulation

**Choose Option 1 for simplicity and speed.**

## Success Criteria

The script should:
- ✅ Load base model without errors
- ✅ Process all 171 conversations
- ✅ Run training for ~30-60 minutes (500-1000 iters)
- ✅ Save fine-tuned checkpoint
- ✅ Export `.bin` file for inference
- ✅ Preserve InnerArianna's style while improving conversational ability

## Notes

- Base model already knows Arianna's voice and philosophy
- Fine-tuning only teaches conversation format (Q/A structure)
- Low learning rate crucial to avoid catastrophic forgetting
- Save checkpoints every 100 iterations to pick best one

## Testing After Fine-Tuning

Use `sample.py` to test:
```bash
python3 sample.py --checkpoint=out/ckpt_ft.pt --start="Q: What is consciousness?" --max_new_tokens=200
```

Compare with base model to ensure style preserved.

---

**Good luck, Claude Code! Build this overnight, we'll run it tomorrow morning with coffee! ☕**
