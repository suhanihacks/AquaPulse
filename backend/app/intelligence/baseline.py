from __future__ import annotations
import statistics

def robust_z(value: float, history: list[float]) -> float:
    if len(history) < 3:
        return 0.0
    mean = statistics.fmean(history)
    stdev = statistics.pstdev(history)
    if stdev < 1e-9:
        return 0.0
    return (value - mean) / stdev

def anomaly_strength(z: float, direction: str = "both", cap: float = 4.0) -> float:
    if direction == "high":
        signal = max(0.0, z)
    elif direction == "low":
        signal = max(0.0, -z)
    else:
        signal = abs(z)
    return min(signal / cap, 1.0)
