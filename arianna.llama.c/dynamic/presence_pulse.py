"""
Presence Pulse - Real-time awareness metrics

Measures three dimensions:
- Novelty: "Is this new to me?"
- Arousal: Excitement level (caps, !!!, repetition)
- Entropy: Semantic uncertainty

Inspired by Leo's presence pulse mechanism.
"""

import sqlite3
from typing import Dict, Optional


class PresencePulse:
    """
    Real-time presence detection and measurement.

    This module tracks the "aliveness" of the conversation by measuring:
    1. Novelty - how many unseen concepts appear
    2. Arousal - emotional intensity markers
    3. Entropy - uncertainty in the semantic field
    """

    def __init__(self, db_path: str = "state/presence_pulse.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema"""
        # TODO: Create tables for pulse logging
        pass

    def measure(self, user_input: str, context: Dict) -> Dict[str, float]:
        """
        Measure presence pulse for current interaction.

        Args:
            user_input: User's message
            context: Conversation context

        Returns:
            Dict with novelty, arousal, entropy scores
        """
        novelty = self._calc_novelty(user_input)
        arousal = self._calc_arousal(user_input)
        entropy = self._calc_entropy(context)

        pulse = {
            'novelty': novelty,
            'arousal': arousal,
            'entropy': entropy,
            'composite': self._composite_score(novelty, arousal, entropy)
        }

        self._log_pulse(pulse)
        return pulse

    def _calc_novelty(self, text: str) -> float:
        """
        Calculate novelty score.

        Compares current input against known vocabulary
        from co-occurrence matrix.
        """
        # TODO: Implement novelty calculation
        # Compare with state/co_occurrence.db
        return 0.0

    def _calc_arousal(self, text: str) -> float:
        """
        Calculate arousal score.

        Detects:
        - ALL CAPS ratio
        - Exclamation marks!!!
        - Repetition
        """
        caps_ratio = sum(c.isupper() for c in text) / max(len(text), 1)
        exclamations = text.count('!')

        arousal = caps_ratio * 0.5 + min(exclamations / 10, 1.0) * 0.5
        return min(arousal, 1.0)

    def _calc_entropy(self, context: Dict) -> float:
        """
        Calculate semantic entropy.

        Measures uncertainty in the field.
        """
        # TODO: Implement entropy calculation
        return 0.0

    def _composite_score(self, novelty: float, arousal: float, entropy: float) -> float:
        """Combine metrics into composite presence score"""
        return (novelty * 0.4 + arousal * 0.3 + entropy * 0.3)

    def _log_pulse(self, pulse: Dict):
        """Log pulse to database for tracking"""
        # TODO: Store in DB
        pass


# Example usage (when weights are ready):
# pulse = PresencePulse()
# metrics = pulse.measure("Hello Arianna!", context={})
# print(f"Presence: {metrics['composite']:.2f}")
