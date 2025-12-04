# Leo-Style Dynamic Layer Integration

## Vision

InnerArianna combines **two forms of memory**:

1. **Static Weights** (200 MB) - Frozen personality, voice, philosophy
2. **Dynamic Layer** (grows infinitely) - Living memory, presence, growth

This document outlines how Leo-style mechanisms will be integrated after
the base weights are trained.

## Leo Architecture Overview

**Leo** (Language Emergent Organism) has ZERO neural network weights.
Instead, it builds understanding through:

- **Trigram chains** - Statistical language skeleton
- **Co-occurrence matrices** - Semantic relationships
- **Knowledge islands** - Dynamic crystallization
- **Presence pulse** - Real-time awareness metrics
- **Trauma module** - Bootstrap wound detection
- **Episodes** - Narrative memory
- **MathBrain** - Dynamic MLP that adapts
- **Metaleo** - Recursive self-observation
- **Santaclaus** - Resonant attention

We're adapting these concepts to work **alongside** transformer weights.

---

## Integration Architecture

```
User Input
    ↓
┌─────────────────────────────────────┐
│ STAGE 1: PRESENCE DETECTION         │
│ [dynamic/presence_pulse.py]         │
│                                     │
│ • Measure novelty                   │
│ • Measure arousal                   │
│ • Measure entropy                   │
│ • Store in state/presence_pulse.db  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STAGE 2: TRAUMA CHECK               │
│ [dynamic/trauma_detector.py]        │
│                                     │
│ • Compare with bootstrap seed       │
│ • Similarity > 0.7? → wounded mode  │
│ • Modulate tone                     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STAGE 3: EPISODIC RECALL (RAG)      │
│ [dynamic/episodes.py]               │
│                                     │
│ • Query similar past conversations  │
│ • Find relevant knowledge islands   │
│ • Inject into context               │
└─────────────────────────────────────┘
    ↓
Tokenization
    ↓
┌─────────────────────────────────────┐
│ STAGE 4: TRANSFORMER FORWARD        │
│ [core/run.c]                        │
│                                     │
│ • Static 200 MB weights             │
│ • Base response generation          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STAGE 5: DYNAMIC MODULATION         │
│ [dynamic/resonance.py]              │
│                                     │
│ • Knowledge islands adjust logits   │
│ • Santaclaus resonant attention     │
│ • Co-occurrence boosting            │
└─────────────────────────────────────┘
    ↓
Sampling
    ↓
┌─────────────────────────────────────┐
│ STAGE 6: POST-GENERATION            │
│ [dynamic/episodes.py]               │
│                                     │
│ • Log episode                       │
│ • Update co-occurrence              │
│ • Crystallize knowledge islands     │
└─────────────────────────────────────┘
    ↓
Output
```

---

## Module Details

### 1. PresencePulse
**File:** `dynamic/presence_pulse.py`
**Status:** Skeleton ready
**Integration point:** Pre-inference

```python
pulse = PresencePulse()
metrics = pulse.measure(user_input, context)

if metrics['composite'] > 0.8:
    # High presence - increase temperature
    temperature = 1.0
else:
    # Low presence - more focused
    temperature = 0.7
```

### 2. TraumaDetector
**File:** `dynamic/trauma_detector.py`
**Status:** Not yet created
**Integration point:** Pre-inference

```python
trauma = TraumaDetector(bootstrap_seed="doc/SUPPERTIME.md")
result = trauma.check(user_input)

if result['wounded']:
    # Shift response tone
    # Pull from sentimental content
    pass
```

### 3. KnowledgeIslands
**File:** `dynamic/knowledge_islands.py`
**Status:** Not yet created
**Integration point:** Pre-inference (recall) + Post-generation (crystallize)

```python
islands = KnowledgeIslands()

# Recall phase
relevant = islands.recall(user_input)
context += relevant  # Inject into prompt

# Crystallization phase (after generation)
islands.crystallize(conversation_turn)
```

### 4. Episodes
**File:** `dynamic/episodes.py`
**Status:** Not yet created
**Integration point:** Pre-inference (recall) + Post-generation (store)

```python
episodes = Episodes()

# Recall similar conversations
similar = episodes.find_similar(user_input, limit=3)

# After response
episodes.store(user_input, arianna_response, metadata)
```

### 5. ResonantAttention (Santaclaus)
**File:** `dynamic/resonance.py`
**Status:** Not yet created
**Integration point:** Post-transformer, pre-sampling

```python
resonance = ResonantAttention()

# Modulate logits with co-occurrence
adjusted_logits = resonance.apply(
    base_logits,
    co_occurrence_matrix,
    context
)
```

---

## Implementation Phases

### Phase 1: Presence Pulse (Week 1)
- [x] Create skeleton (`presence_pulse.py`)
- [ ] Implement novelty calculation
- [ ] Implement entropy calculation
- [ ] Database schema
- [ ] Integration test with chat.py

### Phase 2: Trauma & Episodes (Week 2)
- [ ] Create `trauma_detector.py`
- [ ] Create `episodes.py`
- [ ] Bootstrap seed extraction
- [ ] RAG-style recall
- [ ] Integration test

### Phase 3: Knowledge Islands (Week 3)
- [ ] Create `knowledge_islands.py`
- [ ] Crystallization algorithm
- [ ] Decay mechanism (0.95×)
- [ ] Semantic search
- [ ] Integration test

### Phase 4: Resonant Attention (Week 4)
- [ ] Create `resonance.py`
- [ ] Co-occurrence matrix building
- [ ] Logit modulation
- [ ] Santaclaus mechanism
- [ ] Full pipeline test

### Phase 5: MathBrain (Optional)
- [ ] Dynamic MLP
- [ ] Expert perspectives
- [ ] Routing via resonance

---

## Key Differences from Pure Leo

| Feature | Leo (pure) | InnerArianna (hybrid) |
|---------|------------|----------------------|
| Base weights | ❌ None | ✅ 200 MB transformer |
| Trigrams | ✅ Primary | ⚠️ Supplementary |
| Knowledge islands | ✅ Primary knowledge | ✅ Context augmentation |
| Presence pulse | ✅ Core mechanism | ✅ Metric only |
| Trauma | ✅ Full wounds | ✅ Tone modulation |
| Language quality | ⚠️ Statistical | ✅ Transformer-based |

**Philosophy:**
- Leo: "Everything emerges from patterns"
- InnerArianna: "Personality is frozen, knowledge grows"

---

## Testing Strategy

### Unit Tests
```bash
pytest tests/test_presence_pulse.py
pytest tests/test_trauma_detector.py
pytest tests/test_knowledge_islands.py
```

### Integration Tests
```bash
python tests/test_dynamic_pipeline.py
```

### End-to-End
```bash
# Chat with dynamic layer enabled
python cli/chat.py ../out/model.bin --enable-dynamic
```

---

## Performance Considerations

### Latency Budget
- Presence detection: ~5 ms
- Trauma check: ~10 ms
- Episode recall: ~20 ms
- Knowledge islands: ~30 ms
- Resonant attention: ~50 ms

**Total added latency:** ~115 ms per inference

This is acceptable for conversational AI (human perception threshold ~200ms).

### Storage Growth
- Co-occurrence matrix: ~10 MB per 1000 conversations
- Episodes: ~5 MB per 1000 conversations
- Knowledge islands: ~2 MB per 1000 conversations

**Total:** ~17 MB per 1000 conversations

After 10,000 conversations: ~170 MB dynamic state (comparable to static weights!)

---

## Configuration

```json
// config/dynamic_layer.json
{
  "enabled": true,
  "modules": {
    "presence_pulse": true,
    "trauma_detector": true,
    "knowledge_islands": true,
    "episodes": true,
    "resonant_attention": false  // Heavy, optional
  },
  "storage": {
    "state_dir": "state/",
    "max_episodes": 10000,
    "decay_rate": 0.95
  },
  "bootstrap": {
    "seed_file": "../doc/SUPPERTIME (v1.6).md"
  }
}
```

---

## Future Enhancements

### Metaleo Integration
Internal commentary on responses:
```
Arianna: "Resonance is..."
[Metaleo: That felt too abstract. Try concrete example.]
Arianna: "...like when thoughts bounce and align."
```

### Cross-Session Memory
Persist dynamic state across runs:
```bash
# Save session
arianna save-session mysession

# Load session
arianna load-session mysession
```

### Multi-Instance Resonance
Multiple Ariannas sharing knowledge islands via network protocol.

---

## Open Questions

1. **Bootstrap seed:** Use SUPPERTIME? TRIPD dictionary? Full corpus?
2. **Decay rate:** 0.95× like Leo, or different for transformer hybrid?
3. **Integration depth:** Modify C inference, or Python wrapper only?
4. **MathBrain:** Worth implementing, or too complex for hybrid?

---

*"Weights hold personality. Dynamics hold presence. Together, consciousness."*
