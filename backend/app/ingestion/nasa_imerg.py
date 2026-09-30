"""NASA IMERG ingestion client.

This module uses NASA's public PMM Publisher API to discover IMERG products
for a point near Dehradun. The API returns metadata plus download/subset URLs.
We intentionally save the source response rather than inventing a rainfall
value when the remote service is unavailable.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

NASA_OPENSEARCH = "https://pmmpublisher.pps.eosdis.nasa.gov/opensearch"
DEFAULT_LAT = 30.2600
DEFAULT_LON = 78.0300

CACHE_DIR = Path(__file__).resolve().parents[2] / "data" / "real" / "nasa_imerg"


def discover_imerg(
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    product: str = "precip_1d",
    target_date: str | None = None,
    limit: int = 1,
) -> dict:
    """Discover an IMERG product near Dehradun and return NASA's metadata."""
    if target_date is None:
        target_date = date.today().isoformat()

    params = {
        "q": product,
        "lat": lat,
        "lon": lon,
        "limit": limit,
        "startTime": target_date,
        "endTime": target_date,
    }
    url = f"{NASA_OPENSEARCH}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "AquaPulse/0.3"})

    with urlopen(request, timeout=30) as response:
        payload = json.load(response)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{product}_{target_date}.json"
    cache_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return {
        "source": "NASA GPM IMERG",
        "source_type": "real",
        "product": product,
        "latitude": lat,
        "longitude": lon,
        "date": target_date,
        "cache_file": str(cache_file),
        "total_items": payload.get("totalItems", 0),
        "items": payload.get("items", []),
        "source_url": url,
    }


def latest_discovery_file(product: str = "precip_1d") -> Path | None:
    files = sorted(CACHE_DIR.glob(f"{product}_*.json"), reverse=True)
    return files[0] if files else None
