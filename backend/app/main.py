from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .intelligence.pipeline import run_demo_pipeline, SEGMENTS
from .models import CitizenReport, VerificationAction
from .state import add_report, add_verification, citizen_reports, verification_log
from .data_service import get_data_registry, get_cpcb_summary, get_cpcb_observations, get_baselines, get_evidence
from .intelligence.intelligence_service import run_scenario, list_scenarios
from .ingestion.nasa_imerg import discover_imerg

app = FastAPI(title="AquaPulse API", version="1.0.0", description="Freshwater Event Intelligence — Dehradun prototype — final hackathon build")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status":"ok","service":"aquapulse-api","version":"1.0.0"}

@app.get("/api/v1/dashboard")
def dashboard():
    return run_demo_pipeline()

@app.get("/api/v1/intelligence/scenarios")
def intelligence_scenarios():
    return {"scenarios": list_scenarios(), "source_type": "simulated"}

@app.get("/api/v1/intelligence/run")
def intelligence_run(scenario: str = "rain_runoff"):
    try:
        return run_scenario(scenario, citizen_reports)
    except KeyError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail={"message": "Unknown demo scenario", "available": [s["id"] for s in list_scenarios()]})

@app.get("/api/v1/propagation")
def propagation():
    return run_scenario("rain_runoff", citizen_reports)["propagation"]

@app.get("/api/v1/intelligence/fingerprint")
def intelligence_fingerprint(scenario: str = "rain_runoff"):
    return run_scenario(scenario, citizen_reports)["event"]["fingerprint"]

@app.get("/api/v1/segments")
def segments():
    return {"city":"Dehradun","segments":SEGMENTS,"source_type":"derived"}

@app.get("/api/v1/event")
def event():
    return run_demo_pipeline()["event"]

@app.get("/api/v1/river-memory")
def river_memory():
    result=run_demo_pipeline(); return {"matches":result["event"]["historical_matches"],"source_type":"simulated"}

@app.get("/api/v1/hot-moments")
def hot_moments():
    result=run_demo_pipeline(); return {"city":result["city"],"score":result["hot_moment"],"window":result["hot_moment_window"],"drivers":result["hot_moment_drivers"],"source_type":"derived"}

@app.get("/api/v1/verification")
def verification():
    return {"targets":run_demo_pipeline()["verification_targets"],"source_type":"derived"}


@app.get("/api/v1/citizen-reports")
def citizen_reports_endpoint():
    return {"reports": citizen_reports, "source_type":"simulated"}

@app.post("/api/v1/citizen-reports")
def create_citizen_report(report: CitizenReport):
    return add_report(report)

@app.post("/api/v1/verification")
def create_verification(action: VerificationAction):
    return add_verification(action)


@app.get("/api/v1/verification/log")
def verification_log_endpoint():
    return {"log": verification_log, "source_type":"simulated"}


@app.get("/api/v1/data/sources")
def data_sources():
    return get_data_registry()

@app.get("/api/v1/data/cpcb/summary")
def cpcb_summary():
    return get_cpcb_summary()

@app.get("/api/v1/data/rainfall/discover")
def rainfall_discover(lat: float = 30.2600, lon: float = 78.0300, product: str = "precip_1d", target_date: str | None = None):
    """Discover an official NASA IMERG product for the requested point/date.

    This endpoint returns NASA metadata and caches the response locally. It does
    not fabricate a rainfall value if NASA is unavailable.
    """
    try:
        return discover_imerg(lat=lat, lon=lon, product=product, target_date=target_date)
    except Exception as exc:
        return {
            "source": "NASA GPM IMERG",
            "source_type": "real",
            "status": "unavailable",
            "error": str(exc),
            "message": "NASA could not be reached from this runtime. No rainfall value was fabricated.",
        }

@app.get("/api/v1/data/cpcb/observations")
def cpcb_observations():
    return get_cpcb_observations()

@app.get("/api/v1/data/cpcb/baselines")
def cpcb_baselines():
    return get_baselines()

@app.get("/api/v1/evidence/overview")
def evidence_overview():
    return get_evidence()

@app.get("/api/v1/data/overview")
def data_overview():
    return {"city":"Dehradun", "sources":get_data_registry(), "cpcb_summary":get_cpcb_summary(), "cpcb_baselines":get_baselines()}

@app.get("/api/v1/data/rainfall/demo-features")
def rainfall_demo_features():
    from .data_service import get_demo_rainfall_features
    return get_demo_rainfall_features()

@app.get("/api/v1/evidence/cpcb")
def cpcb_evidence():
    import csv
    from pathlib import Path
    path = Path(__file__).resolve().parents[1] / "data" / "real" / "cpcb_dehradun_drain_samples.csv"
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {"source":"CPCB","rows":rows,"source_type":"real","note":"Normalized Dehradun Rispana/Bindal drain records used as official contextual evidence; not live telemetry."}
