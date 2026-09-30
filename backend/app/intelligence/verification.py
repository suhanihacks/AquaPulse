WEIGHTS = {"confidence": 0.40, "impact": 0.20, "information_value": 0.20, "historical_recurrence": 0.20}
IMPACT = {"LOW": 0.25, "MEDIUM": 0.60, "HIGH": 1.0}

def priority(confidence: float, impact: str, information_value: float, historical_recurrence: float) -> float:
    score = (WEIGHTS["confidence"] * confidence + WEIGHTS["impact"] * IMPACT.get(impact, 0.25) + WEIGHTS["information_value"] * information_value + WEIGHTS["historical_recurrence"] * historical_recurrence)
    return max(0.0, min(1.0, score))
