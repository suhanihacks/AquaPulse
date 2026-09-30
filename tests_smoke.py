"""AquaPulse final backend smoke test.

Run from the project root with the project CPython 3.12 environment.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
checks = []


def check(name, fn):
    response = fn()
    assert response.status_code < 400, f"{name}: HTTP {response.status_code} -> {response.text[:500]}"
    checks.append((name, response.status_code))
    return response


health = check("health", lambda: client.get("/health"))
assert health.json()["version"] == "1.0.0"

for scenario in ("rain_runoff", "localized_discharge", "rain_no_event"):
    result = check(
        f"scenario:{scenario}",
        lambda s=scenario: client.get(f"/api/v1/intelligence/run?scenario={s}"),
    ).json()
    assert 0 <= result["event"]["confidence"] <= 1
    assert result["event"]["segment_id"]
    assert result["mode"] == "SIMULATED_DEMO"

unknown = client.get("/api/v1/intelligence/run?scenario=does_not_exist")
assert unknown.status_code == 404, f"unknown scenario should be 404, got {unknown.status_code}"
checks.append(("unknown-scenario", unknown.status_code))

check("segments", lambda: client.get("/api/v1/segments"))
check("river-memory", lambda: client.get("/api/v1/river-memory"))
check("hot-moments", lambda: client.get("/api/v1/hot-moments"))
check("verification", lambda: client.get("/api/v1/verification"))
check("evidence", lambda: client.get("/api/v1/evidence/overview"))
check("cpcb", lambda: client.get("/api/v1/evidence/cpcb"))
check("data-overview", lambda: client.get("/api/v1/data/overview"))
check("rainfall-demo-features", lambda: client.get("/api/v1/data/rainfall/demo-features"))

rain_no_event = client.get("/api/v1/intelligence/run?scenario=rain_no_event").json()["event"]
assert rain_no_event["confidence"] <= 0.45
assert rain_no_event["potential_impact"] == "LOW"

report = check(
    "citizen-report",
    lambda: client.post(
        "/api/v1/citizen-reports",
        json={"segment_id": "BINDAL-MID", "category": "Foam", "severity": 0.72, "description": "Smoke-test observation"},
    ),
)
assert report.json()["source_type"] == "simulated"

verification = check(
    "verification-action",
    lambda: client.post(
        "/api/v1/verification",
        json={"status": "confirmed", "note": "Smoke-test review", "segment_id": "BINDAL-MID", "event_id": "SIM-RAIN_RUNOFF"},
    ),
)
assert verification.json()["status"] == "confirmed"


print("AquaPulse backend smoke test: PASS")
for name, status in checks:
    print(f"  {status}  {name}")
