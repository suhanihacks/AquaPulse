from __future__ import annotations
import math
import pandas as pd


def build_baselines(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []
    grouped = df.groupby(["segment_id", "segment_name", "parameter", "unit", "direction"], dropna=False)
    output = []
    for keys, g in grouped:
        values = pd.to_numeric(g["value"], errors="coerce").dropna().tolist()
        n = len(values)
        mean = sum(values) / n if n else None
        ordered = sorted(values)
        median = ordered[n // 2] if n % 2 else ((ordered[n//2-1] + ordered[n//2]) / 2 if n else None)
        variance = sum((x - mean) ** 2 for x in values) / n if n else 0
        stdev = math.sqrt(variance)
        output.append({
            "segment_id": keys[0], "segment_name": keys[1], "parameter": keys[2], "unit": keys[3],
            "direction": keys[4], "n": n, "mean": round(mean, 4) if mean is not None else None,
            "median": round(median, 4) if median is not None else None,
            "stdev": round(stdev, 4),
            "min": min(values) if values else None, "max": max(values) if values else None,
            "baseline_status": "contextual_only" if n >= 3 else "sparse_context_only",
            "note": "CPCB observations are periodic contextual samples; sparse groups must not be treated as live sensor baselines."
        })
    return output


def anomaly(value: float, baseline: dict) -> dict:
    n = baseline.get("n", 0)
    mean = baseline.get("mean")
    stdev = baseline.get("stdev") or 0.0
    direction = baseline.get("direction", "both")
    if n < 3 or mean is None or stdev < 1e-9:
        return {"anomaly_strength": 0.0, "z_score": None, "status": "insufficient_baseline"}
    z = (value - mean) / stdev
    signal = max(0.0, z) if direction == "high" else max(0.0, -z) if direction == "low" else abs(z)
    return {"anomaly_strength": round(min(signal / 4.0, 1.0), 4), "z_score": round(z, 4), "status": "computed"}
