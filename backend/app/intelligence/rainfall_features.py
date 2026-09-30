from __future__ import annotations
import pandas as pd

REQUIRED = {"timestamp", "rain_mm"}


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute rainfall accumulations from a time-indexed observation table.

    Input: timestamp, rain_mm (increment for the observation interval).
    Output adds 1h/3h/24h/72h rolling accumulations. The function does not
    fabricate missing intervals; callers should resample explicitly if needed.
    """
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing rainfall columns: {sorted(missing)}")
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)
    out = out.sort_values("timestamp").set_index("timestamp")
    series = pd.to_numeric(out["rain_mm"], errors="coerce").fillna(0.0)
    out["rain_1h"] = series.rolling("1h", min_periods=1).sum()
    out["rain_3h"] = series.rolling("3h", min_periods=1).sum()
    out["rain_24h"] = series.rolling("24h", min_periods=1).sum()
    out["rain_72h"] = series.rolling("72h", min_periods=1).sum()
    out["rain_intensity_mm_hr"] = series * 2.0  # intended for 30-min IMERG increments
    return out.reset_index()
