from __future__ import annotations


def downstream_segments(start_id: str, segments: list[dict], limit: int = 3) -> list[dict]:
    by_id = {s["id"]: s for s in segments}
    out = []
    frontier = [(start_id, 0)]
    seen = {start_id}
    while frontier and len(out) < limit:
        current, depth = frontier.pop(0)
        segment = by_id.get(current)
        if not segment:
            continue
        for child in segment.get("downstream", []):
            if child in seen:
                continue
            seen.add(child)
            out.append({"segment_id": child, "step": depth + 1})
            frontier.append((child, depth + 1))
    return out


def project(start_id: str, event_confidence: float, spatial_coherence: float, segments: list[dict], limit: int = 3) -> list[dict]:
    by_id = {s["id"]: s for s in segments}
    results = []
    for item in downstream_segments(start_id, segments, limit=limit):
        seg = by_id[item["segment_id"]]
        decay = 0.82 ** item["step"]
        score = event_confidence * spatial_coherence * decay * float(seg.get("vulnerability", 0.5))
        results.append({
            "segment_id": item["segment_id"],
            "segment_name": seg["name"],
            "step": item["step"],
            "relative_risk": round(max(0.0, min(1.0, score)), 3),
            "interpretation": "downstream verification candidate",
        })
    return results
