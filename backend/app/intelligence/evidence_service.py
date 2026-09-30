from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from .baseline_engine import build_baselines
from ..data.observations import load_normalized
from ..ingestion.nasa_imerg import latest_discovery_file

BASE = Path(__file__).resolve().parents[2]

EVIDENCE_SOURCES = [
    {
        "id": "cpcb",
        "name": "CPCB Dehradun drain observations",
        "type": "real",
        "role": "historical/contextual water-quality evidence",
        "status": "available",
        "limitation": "Periodic drain samples; not continuous telemetry.",
        "reference": "CPCB 2022–2023 drain monitoring records bundled with AquaPulse.",
    },
    {
        "id": "nasa-imerg",
        "name": "NASA GPM IMERG V07B",
        "type": "real",
        "role": "rainfall forcing and event-trigger evidence",
        "status": "discovery_ready",
        "limitation": "Runtime must successfully reach NASA's publisher service to obtain product metadata; no rainfall value is fabricated when unavailable.",
        "reference": "NASA GPM IMERG official data service.",
    },
    {
        "id": "sentinel-2",
        "name": "Copernicus Sentinel-2",
        "type": "real",
        "role": "satellite contextual/spatial water evidence",
        "status": "contextual_ready",
        "limitation": "Satellite observations are contextual and episodic; this prototype does not claim live high-frequency water-quality retrieval.",
        "reference": "ESA Copernicus Sentinel-2 water-body monitoring documentation.",
    },
    {
        "id": "research",
        "name": "Dehradun Rispana/Bindal research evidence",
        "type": "real",
        "role": "scientific recurrence and event-context evidence",
        "status": "documented",
        "limitation": "Research findings are evidence/context, not live measurements for the current event.",
        "reference": "Peer-reviewed Dehradun river studies recorded in data/real/sources.md.",
    },
    {
        "id": "citizen",
        "name": "Citizen observations",
        "type": "simulated",
        "role": "human field signal",
        "status": "prototype_input",
        "limitation": "Current browser reports are prototype records and require field verification.",
        "reference": "AquaPulse prototype citizen-report workflow.",
    },
]


def _cpcb_highlights() -> list[dict]:
    df = load_normalized()
    # Keep the UI grounded in the exact contextual observations bundled with the build.
    rows = df[df["parameter"].isin(["BOD", "COD"])].copy()
    rows["value"] = rows["value"].astype(float)
    rows = rows.sort_values(["date", "season", "segment_id", "parameter"], ascending=[False, False, True, True])
    return rows[["observation_id", "date", "season", "segment_id", "segment_name", "parameter", "value", "unit", "drain", "source_type", "quality_flag"]].head(12).to_dict(orient="records")


def get_evidence_overview() -> dict:
    cpcb = load_normalized()
    baselines = build_baselines(cpcb)
    cached = latest_discovery_file()
    sources = []
    for item in EVIDENCE_SOURCES:
        x = dict(item)
        if item["id"] == "nasa-imerg":
            x["cached_discovery"] = str(cached) if cached else None
            x["cache_status"] = "cached_metadata_available" if cached else "no_runtime_cache"
        sources.append(x)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "city": "Dehradun",
        "sources": sources,
        "cpcb": {
            "record_count": int(len(cpcb)),
            "contextual_baselines": int(len(baselines)),
            "highlights": _cpcb_highlights(),
        },
        "interpretation_rules": [
            "Real source records are evidence, not proof of a current event.",
            "CPCB samples are contextual and are never presented as live telemetry.",
            "Satellite evidence is spatial/contextual rather than a substitute for field or laboratory verification.",
            "Rainfall alone cannot create a high-confidence environmental event.",
            "High-consequence claims remain subject to human verification.",
        ],
    }
