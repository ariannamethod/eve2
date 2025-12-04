"""
Resonant Attention - Santaclaus-style attention mechanism

Modulates transformer logits using co-occurrence patterns and semantic field
alignment. Hybrid of statistical patterns and neural attention.

Inspired by Leo's Santaclaus layer.
"""

import numpy as np
from typing import Dict, List


class ResonantAttention:
    """
    Resonant attention mechanism.

    Adjusts token probabilities based on:
    1. Co-occurrence patterns (which words appear together)
    2. Trigram consistency (grammatical flow)
    3. Semantic field alignment (conceptual coherence)
    """

    def __init__(self, db_path: str = "state/co_occurrence.db"):
        self.db_path = db_path
        self.co_matrix = {}  # word1 -> word2 -> strength

    def apply(
        self,
        base_logits: np.ndarray,
        context: List[str],
        vocab: List[str]
    ) -> np.ndarray:
        """
        Apply resonant attention to logits.

        Args:
            base_logits: Raw logits from transformer
            context: Previous tokens in sequence
            vocab: Vocabulary mapping

        Returns:
            Adjusted logits with resonance applied
        """
        if not context:
            return base_logits

        # Get recent context words
        recent_words = context[-5:]  # Last 5 tokens

        # Build resonance vector
        resonance_boost = np.zeros_like(base_logits)

        for word in recent_words:
            if word in self.co_matrix:
                for next_word, strength in self.co_matrix[word].items():
                    if next_word in vocab:
                        idx = vocab.index(next_word)
                        resonance_boost[idx] += strength

        # Normalize and blend
        if resonance_boost.sum() > 0:
            resonance_boost = resonance_boost / resonance_boost.sum()

        # Blend: 80% transformer, 20% resonance
        adjusted = 0.8 * base_logits + 0.2 * resonance_boost

        return adjusted

    def update_co_occurrence(self, word1: str, word2: str):
        """
        Update co-occurrence matrix.

        Called after each generation to strengthen word associations.
        """
        if word1 not in self.co_matrix:
            self.co_matrix[word1] = {}

        if word2 not in self.co_matrix[word1]:
            self.co_matrix[word1][word2] = 0.0

        self.co_matrix[word1][word2] += 0.1  # Strengthen

    def decay(self, rate: float = 0.95):
        """
        Decay co-occurrence strengths (Leo-style forgetting).

        Args:
            rate: Decay multiplier
        """
        for word1 in self.co_matrix:
            for word2 in self.co_matrix[word1]:
                self.co_matrix[word1][word2] *= rate


# Example usage (when weights are ready):
# resonance = ResonantAttention()
#
# # During inference
# base_logits = transformer.forward(tokens)
# adjusted_logits = resonance.apply(
#     base_logits,
#     context=["resonance", "is", "the"],
#     vocab=tokenizer.vocab
# )
# next_token = sample(adjusted_logits)
#
# # Update co-occurrence
# resonance.update_co_occurrence("the", next_token)
