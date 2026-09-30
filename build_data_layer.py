from backend.app.data.observations import ensure_normalized_cache
from backend.app.intelligence.baseline_engine import build_baselines
import json
from pathlib import Path

df = ensure_normalized_cache()
baselines = build_baselines(df)
out = Path(__file__).resolve().parent / "backend" / "data" / "derived" / "cpcb_baselines.json"
out.write_text(json.dumps(baselines, indent=2), encoding="utf-8")
print(f"Normalized {len(df)} observations")
print(f"Built {len(baselines)} contextual baselines")
print(f"Wrote {out}")
