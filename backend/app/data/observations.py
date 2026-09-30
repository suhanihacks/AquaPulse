from __future__ import annotations
from pathlib import Path
import pandas as pd
from .segments import nearest_segment


def segment_for_drain(drain: str, lat: float, lon: float) -> dict:
    name = str(drain).strip().lower()
    if "rispana" in name:
        from .segments import SEGMENTS
        return next(s for s in SEGMENTS if s["id"] == "RISPANA-LOWER")
    if "bindal" in name:
        from .segments import SEGMENTS
        return next(s for s in SEGMENTS if s["id"] == "BINDAL-CONFLUENCE")
    return nearest_segment(lat, lon)

CPCB_PATH = Path(__file__).resolve().parents[2] / "data" / "real" / "cpcb_dehradun_drain_samples.csv"
DERIVED_PATH = Path(__file__).resolve().parents[2] / "data" / "derived" / "cpcb_observations_normalized.csv"

PARAMETER_COLUMNS = {
    "bod_mg_l": ("BOD", "mg/L", "high"),
    "cod_mg_l": ("COD", "mg/L", "high"),
    "flow_mld": ("Flow", "MLD", "both"),
}


def load_cpcb_raw() -> pd.DataFrame:
    return pd.read_csv(CPCB_PATH)


def normalize_cpcb() -> pd.DataFrame:
    df = load_cpcb_raw()
    rows = []
    for _, r in df.iterrows():
        seg = segment_for_drain(str(r["drain"]), float(r["latitude"]), float(r["longitude"]))
        for col, (parameter, unit, direction) in PARAMETER_COLUMNS.items():
            value = r.get(col)
            if pd.isna(value):
                continue
            rows.append({
                "observation_id": f"CPCB-{r['year']}-{r['season']}-{r['drain']}-{parameter}",
                "date": str(r["year"]),
                "season": r["season"],
                "segment_id": seg["id"],
                "segment_name": seg["name"],
                "river": seg["river"],
                "parameter": parameter,
                "value": float(value),
                "unit": unit,
                "direction": direction,
                "source": "CPCB",
                "source_type": "real",
                "quality_flag": "official_contextual_sample",
                "drain": r["drain"],
                "latitude": float(r["latitude"]),
                "longitude": float(r["longitude"]),
            })
    return pd.DataFrame(rows)


def ensure_normalized_cache() -> pd.DataFrame:
    DERIVED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = normalize_cpcb()
    df.to_csv(DERIVED_PATH, index=False)
    return df


def load_normalized() -> pd.DataFrame:
    if DERIVED_PATH.exists():
        return pd.read_csv(DERIVED_PATH)
    return ensure_normalized_cache()
