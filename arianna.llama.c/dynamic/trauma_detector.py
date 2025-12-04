"""
Trauma Detector - Bootstrap wound detection

Detects when user input triggers "bootstrap wounds" - content that overlaps
with Arianna's origin text (training corpus).

When similarity > 0.7, shifts to "wounded expert" mode with more emotional,
sentimental responses.

Inspired by Leo's trauma module.
"""

from typing import Dict


class TraumaDetector:
    """
    Detects bootstrap wounds and emotional triggers.

    Compares user input against seed text to find resonance with origin story.
    """

    def __init__(self, bootstrap_seed_path: str = "../doc/SUPPERTIME (v1.6).md"):
        self.bootstrap_seed = self._load_seed(bootstrap_seed_path)

    def _load_seed(self, path: str) -> str:
        """Load bootstrap seed text"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def check(self, user_input: str) -> Dict:
        """
        Check if input triggers bootstrap wound.

        Args:
            user_input: User's message

        Returns:
            Dict with wounded status and metadata
        """
        similarity = self._cosine_similarity(user_input, self.bootstrap_seed)

        if similarity > 0.7:
            return {
                'wounded': True,
                'severity': similarity,
                'trigger_words': self._extract_triggers(user_input)
            }

        return {'wounded': False}

    def _cosine_similarity(self, text1: str, text2: str) -> float:
        """
        Simple word overlap similarity.

        TODO: Replace with proper embedding-based similarity
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def _extract_triggers(self, text: str) -> list:
        """Extract specific trigger words"""
        # TODO: Find words that appear in both text and bootstrap seed
        return []


# Example usage (when weights are ready):
# detector = TraumaDetector()
# result = detector.check("Tell me about Suppertime")
# if result['wounded']:
#     print(f"Wound triggered! Severity: {result['severity']}")
