from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "real" / "cpcb_dehradun_drain_samples.csv"


def load_cpcb_samples() -> pd.DataFrame:
    """Load the official Dehradun drain observations bundled with the prototype."""
    return pd.read_csv(DATA_PATH)


def summarize_cpcb() -> dict:
    df = load_cpcb_samples()
    parameters = []
    for col, label in [("bod_mg_l", "BOD"), ("cod_mg_l", "COD"), ("flow_mld", "Flow")]:
        if col in df.columns and df[col].notna().any():
            parameters.append(label)
    return {
        "source": "CPCB",
        "source_type": "real",
        "records": int(len(df)),
        "locations": sorted(df["drain"].dropna().unique().tolist()),
        "parameters": parameters,
        "date_range": {"start": str(df["year"].min()), "end": str(df["year"].max())},
        "note": "Official CPCB drain observations used as contextual/historical evidence; they are not treated as live telemetry.",
    }
