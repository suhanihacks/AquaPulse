WEIGHTS = {
    "rainfall_trigger": 0.30,
    "seasonal_susceptibility": 0.20,
    "historical_recurrence": 0.20,
    "segment_vulnerability": 0.15,
    "current_warning": 0.15,
}

def score(features: dict[str, float]) -> float:
    value = sum(WEIGHTS[k] * float(features.get(k, 0.0)) for k in WEIGHTS)
    return max(0.0, min(1.0, value))
