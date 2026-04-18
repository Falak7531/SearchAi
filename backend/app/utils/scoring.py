"""
utils/scoring.py - Score normalization and combination utilities.
Helpers to normalize scores to [0, 1] and apply fusion strategies.
"""

from typing import Dict, List, Tuple


def min_max_normalize(scores: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize a dict of {id: score} to the [0, 1] range.
    Returns same dict if all scores are equal.
    """
    if not scores:
        return {}
    min_s = min(scores.values())
    max_s = max(scores.values())
    rng = max_s - min_s
    if rng == 0:
        return {k: 1.0 for k in scores}
    return {k: (v - min_s) / rng for k, v in scores.items()}


def reciprocal_rank_fusion(
    rankings: List[List[str]],
    k: int = 60,
) -> Dict[str, float]:
    """
    Reciprocal Rank Fusion (RRF) - a robust rank aggregation strategy.

    Args:
        rankings: Multiple ranked lists of product IDs.
        k: RRF constant (default 60 is widely used).

    Returns:
        Dict mapping product_id → RRF score.
    """
    rrf_scores: Dict[str, float] = {}
    for ranked_list in rankings:
        for rank, pid in enumerate(ranked_list, start=1):
            rrf_scores[pid] = rrf_scores.get(pid, 0.0) + 1.0 / (k + rank)
    return rrf_scores


def weighted_combine(
    score_maps: List[Tuple[Dict[str, float], float]]
) -> Dict[str, float]:
    """
    Combine multiple normalized score maps with weights.

    Args:
        score_maps: List of (score_dict, weight) tuples. Weights should sum to 1.

    Returns:
        Combined score dict.
    """
    combined: Dict[str, float] = {}
    for scores, weight in score_maps:
        for pid, score in scores.items():
            combined[pid] = combined.get(pid, 0.0) + weight * score
    return combined
