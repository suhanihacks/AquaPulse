from __future__ import annotations

SCENARIOS = {
    "rain_runoff": {
        "name": "Rain-amplified runoff",
        "description": "Heavy rainfall coincides with environmental and citizen signals, resembling a remembered event.",
        "segment_id": "BINDAL-MID",
        "features": {
            "rainfall_signal": 0.90, "water_quality_signal": 0.84, "citizen_signal": 0.68,
            "spatial_coherence": 0.79, "temporal_coherence": 0.88, "duration": 0.69,
            "oxygen_anomaly": 0.22, "seasonality": 0.95,
        },
    },
    "localized_discharge": {
        "name": "Localized discharge-like anomaly",
        "description": "A strong local environmental signal appears with little rainfall support.",
        "segment_id": "BINDAL-MID",
        "features": {
            "rainfall_signal": 0.08, "water_quality_signal": 0.88, "citizen_signal": 0.55,
            "spatial_coherence": 0.43, "temporal_coherence": 0.76, "duration": 0.81,
            "oxygen_anomaly": 0.61, "seasonality": 0.54,
        },
    },
    "rain_no_event": {
        "name": "Rainfall without corroboration",
        "description": "A storm occurs, but independent signals do not currently support an environmental event hypothesis.",
        "segment_id": "BINDAL-MID",
        "features": {
            "rainfall_signal": 0.94, "water_quality_signal": 0.16, "citizen_signal": 0.08,
            "spatial_coherence": 0.12, "temporal_coherence": 0.19, "duration": 0.52,
            "oxygen_anomaly": 0.05, "seasonality": 0.80,
        },
    },
}


def get_scenario(name: str) -> dict:
    if name not in SCENARIOS:
        raise KeyError(name)
    item = SCENARIOS[name]
    return {"id": name, **item}
