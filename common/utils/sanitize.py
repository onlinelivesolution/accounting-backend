import math

def sanitize_nan_for_db(obj):
    """Recursively replace NaN/Infinity values with None."""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: sanitize_nan_for_db(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_nan_for_db(v) for v in obj]
    return obj