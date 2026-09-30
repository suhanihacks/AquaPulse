from dataclasses import dataclass

WEIGHTS = {
    "rainfall_signal": 0.20,
    "water_quality_signal": 0.25,
    "citizen_signal": 0.15,
    "historical_similarity": 0.20,
    "spatial_coherence": 0.10,
    "temporal_coherence": 0.10,
}

@dataclass
class FusionResult:
    confidence: float
    potential_impact: str
    evidence_quality: str


def fuse(evidence: dict[str, float]) -> FusionResult:
    confidence = sum(WEIGHTS[k] * float(evidence.get(k, 0.0)) for k in WEIGHTS)
    confidence = max(0.0, min(1.0, confidence))
    strong = sum(1 for k in WEIGHTS if evidence.get(k, 0.0) >= 0.65)
    corroborating = sum(1 for k in ("water_quality_signal", "citizen_signal", "historical_similarity", "spatial_coherence") if evidence.get(k, 0.0) >= 0.45)
    if confidence >= 0.80 and strong >= 3 and corroborating >= 2:
        impact = "HIGH"
    elif confidence >= 0.55 and corroborating >= 1:
        impact = "MEDIUM"
    else:
        impact = "LOW"
    nonzero = sum(1 for k in WEIGHTS if evidence.get(k, 0.0) > 0.05)
    quality = "HIGH" if nonzero >= 5 else "MEDIUM" if nonzero >= 2 else "LOW"
    return FusionResult(round(confidence, 3), impact, quality)
