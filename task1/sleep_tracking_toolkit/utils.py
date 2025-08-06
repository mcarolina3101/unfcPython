def quality_label(score):
    if not isinstance(score, (int, float)):
        raise TypeError("Score must be numeric.")
    if score >= 85:
        return 'Excellent'
    elif score >= 70:
        return 'Good'
    elif score >= 50:
        return 'Fair'
    else:
        return 'Poor'

def normalize_quality(score, current_max=100):
    if not isinstance(score, (int, float)):
        raise TypeError("Score must be numeric.")
    if not isinstance(current_max, (int, float)):
        raise TypeError("current_max must be numeric.")
    if current_max <= 0:
        raise ValueError("current_max must be greater than 0 to avoid division by zero.")
    return round(score / current_max * 100, 2)

def compute_sleep_score(duration, quality_score): 
    if not isinstance(duration, (float, int)):
        raise TypeError("Duration must be a number.")
    if not isinstance(quality_score, (float, int)):
        raise TypeError("Quality score must be a number.")
    if duration < 0:
        raise ValueError("Duration cannot be negative.")
    score = min(duration / 8.0, 1.0) * 60 + quality_score * 0.4
    return round(min(score, 100), 2)

