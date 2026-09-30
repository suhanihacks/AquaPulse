from __future__ import annotations

from datetime import datetime, timezone

from .demo_scenarios import SCENARIOS, get_scenario
from .event_fingerprint import classify
from .event_fusion import fuse
from .hot_moment import score as hot_score
from .propagation import project
from .river_memory import best_matches
from .verification import priority
from .pipeline import SEGMENTS

HISTORY = [
    {"event_id": "EVT-021", "segment_id": "BINDAL-MID", "event_pattern": "RAIN_RUNOFF", "rainfall_intensity": 0.88, "rainfall_duration": 0.72, "turbidity_anomaly": 0.91, "oxygen_anomaly": 0.30, "citizen_density": 0.64, "spatial_spread": 0.81, "duration": 0.70, "seasonality": 0.96},
    {"event_id": "EVT-014", "segment_id": "BINDAL-MID", "event_pattern": "LOCALIZED_DISCHARGE_LIKE", "rainfall_intensity": 0.18, "rainfall_duration": 0.15, "turbidity_anomaly": 0.79, "oxygen_anomaly": 0.61, "citizen_density": 0.42, "spatial_spread": 0.48, "duration": 0.83, "seasonality": 0.54},
    {"event_id": "EVT-008", "segment_id": "RISPANA-LOWER", "event_pattern": "LOW_FLOW_STRESS", "rainfall_intensity": 0.08, "rainfall_duration": 0.10, "turbidity_anomaly": 0.31, "oxygen_anomaly": 0.87, "citizen_density": 0.22, "spatial_spread": 0.55, "duration": 0.91, "seasonality": 0.76},
]


def _memory_record(features: dict) -> dict:
    return {
        "rainfall_intensity": features.get("rainfall_signal", 0),
        "rainfall_duration": features.get("duration", 0),
        "turbidity_anomaly": features.get("water_quality_signal", 0),
        "oxygen_anomaly": features.get("oxygen_anomaly", 0),
        "citizen_density": features.get("citizen_signal", 0),
        "spatial_spread": features.get("spatial_coherence", 0),
        "duration": features.get("duration", 0),
        "seasonality": features.get("seasonality", 0),
    }


def run_scenario(name: str, citizen_reports: list[dict] | None = None) -> dict:
    scenario = get_scenario(name)
    f = dict(scenario["features"])
    segment_id = scenario["segment_id"]
    reports = citizen_reports or []
    segment_reports = [r for r in reports if r.get("segment_id") == segment_id]
    if segment_reports:
        observed = max(float(r.get("severity", 0)) for r in segment_reports)
        f["citizen_signal"] = max(f["citizen_signal"], min(1.0, observed))

    matches = best_matches(_memory_record(f), HISTORY)
    similarity = matches[0]["similarity"] if matches else 0.0
    evidence = {
        "rainfall_signal": f["rainfall_signal"],
        "water_quality_signal": f["water_quality_signal"],
        "citizen_signal": f["citizen_signal"],
        "historical_similarity": similarity,
        "spatial_coherence": f["spatial_coherence"],
        "temporal_coherence": f["temporal_coherence"],
    }
    fusion = fuse(evidence)
    fingerprint = classify({**evidence, "duration": f["duration"], "oxygen_anomaly": f["oxygen_anomaly"]})

    # Safety guard: rainfall by itself should not become a strong event claim.
    corroboration = evidence["water_quality_signal"] >= 0.45 or evidence["citizen_signal"] >= 0.45
    if fingerprint["pattern"] == "RAIN_NO_CORROBORATION" or not corroboration:
        fusion.confidence = min(fusion.confidence, 0.45)
        fusion.potential_impact = "LOW"
        fusion.evidence_quality = "LOW"

    hot = hot_score({
        "rainfall_trigger": f["rainfall_signal"],
        "seasonal_susceptibility": f["seasonality"],
        "historical_recurrence": similarity,
        "segment_vulnerability": next(s["vulnerability"] for s in SEGMENTS if s["id"] == segment_id),
        "current_warning": max(evidence["water_quality_signal"], evidence["citizen_signal"]),
    })
    propagation = project(segment_id, fusion.confidence, evidence["spatial_coherence"], SEGMENTS)

    targets = []
    for item in [segment_id] + [p["segment_id"] for p in propagation[:2]]:
        seg = next(s for s in SEGMENTS if s["id"] == item)
        info_value = 0.90 if item == segment_id else 0.72
        recurrence = similarity
        targets.append({
            "segment_id": item,
            "priority": round(priority(fusion.confidence, fusion.potential_impact, info_value, recurrence), 3),
            "reasons": [
                "multi-signal corroboration" if corroboration else "rainfall signal without corroboration",
                "historical recurrence" if recurrence >= 0.55 else "limited historical support",
                f"{seg['name']} verification value",
            ],
        })
    targets = sorted(targets, key=lambda x: x["priority"], reverse=True)

    explanation = []
    if evidence["rainfall_signal"] >= 0.65:
        explanation.append("Rainfall is elevated in the scenario input.")
    if evidence["water_quality_signal"] >= 0.45:
        explanation.append("The environmental signal is strong enough to contribute independent corroboration.")
    else:
        explanation.append("The environmental signal is weak; rainfall alone is not treated as an event.")
    if evidence["citizen_signal"] >= 0.45:
        explanation.append("Citizen observations add a second independent evidence stream.")
    if similarity >= 0.55:
        explanation.append("River Memory finds a meaningful resemblance to a previous event signature.")
    else:
        explanation.append("Historical memory support is limited for this signature.")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "city": "Dehradun",
        "mode": "SIMULATED_DEMO",
        "scenario": {"id": name, "name": scenario["name"], "description": scenario["description"]},
        "event": {
            "event_id": f"SIM-{name.upper()}",
            "segment_id": segment_id,
            "event_pattern": fingerprint["pattern"],
            "fingerprint": fingerprint,
            "confidence": round(fusion.confidence, 3),
            "potential_impact": fusion.potential_impact,
            "evidence_quality": fusion.evidence_quality,
            "verification_status": "pending",
            "evidence": evidence,
            "historical_matches": matches,
            "explanation": explanation,
        },
        "hot_moment": round(hot, 3),
        "hot_moment_window": "scenario-relative vulnerable window",
        "hot_moment_drivers": ["rainfall trigger", "seasonal susceptibility", "historical recurrence", "current warning signals"],
        "propagation": propagation,
        "verification_targets": targets,
        "data_provenance": {
            "scenario": "simulated demo input",
            "water_quality_context": "real CPCB reference records are contextual; high-frequency event signal is simulated",
            "rainfall_context": "demo rainfall series is simulated until NASA IMERG observations are ingested",
            "historical_memory": "simulated event library for prototype demonstration",
            "geospatial_context": "derived study-area segment geometry",
        },
    }


def list_scenarios() -> list[dict]:
    return [{"id": k, "name": v["name"], "description": v["description"]} for k, v in SCENARIOS.items()]
