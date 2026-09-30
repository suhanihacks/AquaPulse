from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

DATA_REGISTRY = [
    {
        "id": "cpcb-dehradun-drains",
        "name": "CPCB Dehradun drain observations",
        "source_type": "real",
        "role": "historical/contextual water-quality evidence",
        "local_path": str(BASE / "data" / "real" / "cpcb_dehradun_drain_samples.csv"),
        "status": "available",
    },
    {
        "id": "nasa-imerg",
        "name": "NASA GPM IMERG V07B",
        "source_type": "real",
        "role": "rainfall forcing and event-trigger evidence",
        "local_path": str(BASE / "data" / "real" / "nasa_imerg"),
        "status": "on-demand discovery",
    },
    {
        "id": "sentinel-2",
        "name": "Copernicus Sentinel-2",
        "source_type": "real",
        "role": "satellite contextual/spatial water evidence",
        "local_path": None,
        "status": "contextual integration ready",
    },
    {
        "id": "research-dehradun",
        "name": "Dehradun Rispana/Bindal research evidence",
        "source_type": "real",
        "role": "historical event context and recurrence evidence",
        "local_path": str(BASE / "data" / "real" / "sources.md"),
        "status": "documented",
    },
]
