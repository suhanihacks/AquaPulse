from __future__ import annotations
import numpy as np

FEATURES = [
    "rainfall_intensity", "rainfall_duration", "turbidity_anomaly",
    "oxygen_anomaly", "citizen_density", "spatial_spread",
    "duration", "seasonality",
]

def vector(record: dict) -> np.ndarray:
    return np.array([float(record.get(k, 0.0)) for k in FEATURES], dtype=float)

def cosine_similarity(a: dict, b: dict) -> float:
    va, vb = vector(a), vector(b)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)

def best_matches(current: dict, history: list[dict], limit: int = 3) -> list[dict]:
    scored = [{**item, "similarity": round(cosine_similarity(current, item), 3)} for item in history]
    return sorted(scored, key=lambda x: x["similarity"], reverse=True)[:limit]
