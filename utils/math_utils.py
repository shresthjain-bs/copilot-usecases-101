import statistics
from typing import List, Dict
import numpy as np

def calculate_surface_area(height: float, weight: float, breadth: float) -> float:
    """Calculate total surface area of a rectangular box: 2(lw + lh + wh)"""
    return 2 * (weight * breadth + weight * height + breadth * height)


def calculate_capacity(height: float, weight: float, breadth: float) -> float:
    """Calculate capacity (volume) of a rectangular box: l * w * h"""
    return height * weight * breadth

def generate_timing_statistics(processing_times: List[float]) -> Dict:
    """Calculate timing statistics"""
    if not processing_times:
        return {}
    
    return {
        'count': len(processing_times),
        'average': statistics.mean(processing_times),
        'median': statistics.median(processing_times),
        'min': min(processing_times),
        'max': max(processing_times),
        'std_dev': statistics.stdev(processing_times) if len(processing_times) > 1 else 0,
        'p90': np.percentile(processing_times, 90),
        'p99': np.percentile(processing_times, 99)
    }