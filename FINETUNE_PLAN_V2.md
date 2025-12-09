# FINE-TUNE PLAN V2 - Dec 9, 2025 (Evening)

## CURRENT SITUATION

**BASE MODEL (PERFECT!):**
- File: `out/ckpt_v1_base.pt` (Dec 6, 23:24)
- Iterations: 4000
- Loss: 6.53
- Quality: EXCELLENT ("Resonance is not what you hear — it's what survives the echo.")
- Size: 7.16M parameters (not 15M!)

**FAILED FINE-TUNE:**
- Ran 750 iterations (stopped at 990 due to bug)
- Loss: 1.66
- Quality: POOR (overfitting, fake words: "surfive", "activatives")
- Conclusion: TOO MANY iterations on small dataset (171 Q/A)

**DATA:**
- 171 Q/A conversations (arianna_conversations.jsonl)
- 53K tokens (data/ft_tok4096/ft_corpus.bin + ft_corpus_2.bin)
- Format: "Q: question\nA: answer"

## NEW PLAN: Conservative Fine-Tune

### Strategy:
Start FRESH from base model, train LESS to avoid overfitting

### Parameters:
```bash
PYTHONUNBUFFERED=1 caffeinate -i python3 train_finetune.py \
  --init_from=resume \
  --max_iters=500 \
  --learning_rate=5e-6 \
  --eval_interval=100 \
  --log_interval=10 \
  --always_save_checkpoint=True \
  --batch_size=4 \
  --gradient_accumulation_steps=8 \
  --vocab_source=custom \
  --vocab_size=4096 \
  --compile=False \
  --device=cpu \
  --dtype=float32 \
  > finetune_v2_conservative.log 2>&1 &
```

### Expected:
- Time: ~40 minutes (500 iter × 4.5s + 5 evals)
- Checkpoints: iter 100, 200, 300, 400, 500
- Target loss: 3-4 (NOT 1.0! We want to preserve general language)

### Testing After Each Checkpoint:
```bash
# Test at iter 100:
python3 sample.py --checkpoint=out/ckpt.pt \
  --start="Q: What is resonance?\nA:" \
  --num_samples=1 --max_new_tokens=100 \
  --device=cpu --dtype=float32 --compile=False --temperature=0.8

# If quality is GOOD (no fake words, coherent) → STOP and use that checkpoint
# If quality needs more → continue to next checkpoint
```

### Success Criteria:
- ✅ Understands Q/A format
- ✅ Answers about resonance/consciousness
- ✅ NO fake words ("surfive", "activatives", etc.)
- ✅ Preserves base model's language quality
- ✅ Loss around 3-4 (balance between fit and generalization)

### BEFORE STARTING:
1. Copy base checkpoint to safety:
   ```bash
   cp out/ckpt_v1_base.pt out/ckpt_v1_base_BACKUP.pt
   ```

2. Reset out/ckpt.pt to base:
   ```bash
   cp out/ckpt_v1_base.pt out/ckpt.pt
   ```

3. Verify data files exist:
   ```bash
   ls -lh data/ft_tok4096/*.bin
   # Should see: ft_corpus.bin + ft_corpus_2.bin (both 104K)
   ```

4. Start training (at mother's house, with caffeinate)

### IF RESULTS ARE POOR:
- Try even FEWER iterations (100-200)
- Or try even LOWER learning rate (1e-6)
- Base model is ALREADY GOOD - we just need Q/A format

### AFTER SUCCESS:
1. Export to NumPy (fix NumPy bugs first)
2. Test C inference (run.c)
3. Push to repositories

## KEY INSIGHT:
**Don't overtrain!** Base model quality > perfect Q/A fit
171 conversations is SMALL - easy to overfit
Better to undertrain than overtrain
