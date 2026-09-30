from __future__ import annotations

PATTERNS = {
    "RAIN_AMPLIFIED_URBAN_RUNOFF": {
        "label": "Rain-amplified urban runoff",
        "description": "Rainfall, environmental change and downstream coherence occur together.",
    },
    "LOCALIZED_DISCHARGE_LIKE": {
        "label": "Localized discharge-like anomaly",
        "description": "A strong local environmental signal appears without a matching rainfall trigger.",
    },
    "LOW_FLOW_STRESS": {
        "label": "Low-flow / heat stress",
        "description": "Low-flow conditions and oxygen-related stress dominate the event signature.",
    },
    "RAIN_NO_CORROBORATION": {
        "label": "Rainfall without corroboration",
        "description": "Rainfall is elevated, but other signals do not currently support an event hypothesis.",
    },
}


def _clamp(v: float) -> float:
    return max(0.0, min(1.0, float(v)))


def classify(features: dict[str, float]) -> dict:
    rain = _clamp(features.get("rainfall_signal", 0))
    water = _clamp(features.get("water_quality_signal", 0))
    citizen = _clamp(features.get("citizen_signal", 0))
    spatial = _clamp(features.get("spatial_coherence", 0))
    temporal = _clamp(features.get("temporal_coherence", 0))
    historical = _clamp(features.get("historical_similarity", 0))
    oxygen = _clamp(features.get("oxygen_anomaly", 0))
    duration = _clamp(features.get("duration", 0))

    scores = {
        "RAIN_AMPLIFIED_URBAN_RUNOFF": 0.30 * rain + 0.22 * water + 0.12 * citizen + 0.14 * spatial + 0.12 * temporal + 0.10 * historical,
        "LOCALIZED_DISCHARGE_LIKE": 0.34 * water + 0.18 * citizen + 0.16 * spatial + 0.12 * temporal + 0.12 * historical + 0.08 * (1 - rain),
        "LOW_FLOW_STRESS": 0.38 * oxygen + 0.22 * duration + 0.15 * (1 - rain) + 0.10 * water + 0.15 * historical,
        "RAIN_NO_CORROBORATION": 0.48 * rain + 0.20 * (1 - water) + 0.12 * (1 - citizen) + 0.10 * (1 - spatial) + 0.10 * (1 - temporal),
    }
    # Explicit branch for the signature the product is designed to recognize:
    # strong local environmental evidence with little rainfall support.
    if rain < 0.25 and water >= 0.70:
        scores["LOCALIZED_DISCHARGE_LIKE"] = max(scores["LOCALIZED_DISCHARGE_LIKE"], 0.82)
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_id, top_score = ranked[0]
    return {
        "pattern": top_id,
        "label": PATTERNS[top_id]["label"],
        "description": PATTERNS[top_id]["description"],
        "score": round(_clamp(top_score), 3),
        "alternatives": [{"pattern": k, "score": round(_clamp(v), 3)} for k, v in ranked[1:3]],
        "method": "rule-based prototype fingerprint; not a diagnostic classifier",
    }
