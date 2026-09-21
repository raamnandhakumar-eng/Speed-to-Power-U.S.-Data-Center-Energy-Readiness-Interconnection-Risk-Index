"""Transparent scoring utilities for Speed-to-Power."""

from __future__ import annotations
from typing import Dict, Optional


def minmax_score(value: float, minimum: float, maximum: float, higher_is_better: bool = True) -> float:
    """Normalize a value to 0-100 within a defined comparison range."""
    if maximum <= minimum:
        raise ValueError("maximum must be greater than minimum")
    raw = (value - minimum) / (maximum - minimum)
    raw = max(0.0, min(1.0, raw))
    if not higher_is_better:
        raw = 1.0 - raw
    return round(raw * 100.0, 2)


def weighted_score(scores: Dict[str, Optional[float]], weights: Dict[str, float]) -> Optional[float]:
    """
    Calculate a weighted score without silently imputing missing data.

    Returns None if any weighted dimension is missing.
    """
    missing = [k for k, w in weights.items() if w > 0 and scores.get(k) is None]
    if missing:
        return None

    total_weight = sum(weights.values())
    if abs(total_weight - 1.0) > 1e-9:
        raise ValueError(f"Weights must sum to 1.0, got {total_weight}")

    return round(sum(scores[k] * weights[k] for k in weights), 2)


def validate_scores(scores: Dict[str, Optional[float]]) -> None:
    for key, value in scores.items():
        if value is not None and not (0 <= value <= 100):
            raise ValueError(f"{key} must be between 0 and 100")
