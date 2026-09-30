from datetime import datetime, timezone
from .models import CitizenReport, VerificationAction

citizen_reports: list[dict] = []
verification_log: list[dict] = []

def add_report(report: CitizenReport) -> dict:
    item = report.model_dump()
    item.update({"report_id": f"CR-{len(citizen_reports)+1:03d}", "timestamp": datetime.now(timezone.utc).isoformat(), "source_type":"simulated"})
    citizen_reports.append(item)
    return item

def add_verification(action: VerificationAction) -> dict:
    item = action.model_dump()
    item.update({"timestamp": datetime.now(timezone.utc).isoformat(), "source_type":"simulated"})
    verification_log.append(item)
    return item
