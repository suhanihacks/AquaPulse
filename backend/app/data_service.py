from pathlib import Path
import pandas as pd
from .ingestion.registry import DATA_REGISTRY
from .ingestion.cpcb import summarize_cpcb
from .data.observations import load_normalized
from .intelligence.baseline_engine import build_baselines
from .intelligence.rainfall_features import compute_features
from .intelligence.evidence_service import get_evidence_overview


def get_data_registry() -> dict:
    return {"sources": DATA_REGISTRY, "source_types": ["real", "derived", "simulated"]}


def get_cpcb_summary() -> dict:
    return summarize_cpcb()


def get_cpcb_observations() -> dict:
    df = load_normalized()
    return {"source": "CPCB", "source_type": "real", "records": df.fillna("").to_dict(orient="records"), "count": len(df)}


def get_baselines() -> dict:
    df = load_normalized()
    baselines = build_baselines(df)
    return {"source": "CPCB", "source_type": "derived", "baseline_type": "contextual", "baselines": baselines}


def get_demo_rainfall_features() -> dict:
    path = Path(__file__).resolve().parents[1] / "data" / "simulated" / "demo_rainfall_timeseries.csv"
    df = pd.read_csv(path)
    features = compute_features(df)
    return {"source": "DEMO rainfall scenario", "source_type": "simulated", "records": features.to_dict(orient="records")}


def get_evidence() -> dict:
    return get_evidence_overview()
