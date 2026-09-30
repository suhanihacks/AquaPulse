from __future__ import annotations
from math import hypot

SEGMENTS = [
    {"id":"BINDAL-UPPER","name":"Bindal Upper","river":"Bindal","lat":30.2850,"lon":78.0250,"vulnerability":0.55,"upstream":[],"downstream":["BINDAL-MID"]},
    {"id":"BINDAL-MID","name":"Bindal Middle","river":"Bindal","lat":30.2705,"lon":78.0270,"vulnerability":0.78,"upstream":["BINDAL-UPPER"],"downstream":["BINDAL-CONFLUENCE"]},
    {"id":"BINDAL-CONFLUENCE","name":"Bindal Confluence","river":"Bindal/Song system","lat":30.2599,"lon":78.0270,"vulnerability":0.83,"upstream":["BINDAL-MID"],"downstream":["BINDAL-LOWER"]},
    {"id":"BINDAL-LOWER","name":"Bindal Lower","river":"Bindal/Suswa-Song system","lat":30.2450,"lon":78.0450,"vulnerability":0.74,"upstream":["BINDAL-CONFLUENCE"],"downstream":[]},
    {"id":"RISPANA-MID","name":"Rispana Middle","river":"Rispana","lat":30.2700,"lon":78.0500,"vulnerability":0.76,"upstream":[],"downstream":["RISPANA-LOWER"]},
    {"id":"RISPANA-LOWER","name":"Rispana Lower","river":"Rispana/Song system","lat":30.2550,"lon":78.0300,"vulnerability":0.84,"upstream":["RISPANA-MID"],"downstream":[]},
]


def nearest_segment(lat: float, lon: float) -> dict:
    # Simple MVP nearest-centroid assignment. Replace with PostGIS geometry matching later.
    return min(SEGMENTS, key=lambda s: hypot((lat - s["lat"]) * 111.0, (lon - s["lon"]) * 96.0))
