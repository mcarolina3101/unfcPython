from utils import compute_sleep_score, quality_label, normalize_quality

class DailySleepRecord:
    def __init__(self,date,segments=None,quality_max=100):
        if not date:
            raise ValueError("A date must be provided.")
        if not is_valid_date(date):
            raise ValueError("Date must be in format YYYY-MM-DD and be a valid calendar date.")
        if segments is None:
            raise ValueError("You must provide the 'segments' argument — a list of (duration, quality) tuples.")
        if not segments or not isinstance(segments, list):
            raise ValueError("At least one (duration, quality) segment must be provided in a list.")
        if not isinstance(quality_max, int):
                raise TypeError(f"quality_max must be of type int. Got: {type(quality_max).__name__}")
        if not (0 <= quality_max <= 100):
                raise ValueError(f"Normalized quality_max score must be between 0 and 100. Got: {quality_max}")
        self.date = date
        self.segments = []
        for segment in segments:
            if not isinstance(segment, tuple) or len(segment) != 2:
                raise ValueError	("Each segment must be a tuple of (duration, quality_score).")

            duration, quality = segment
            if not isinstance(duration, float):
                raise TypeError(f"Duration must be of type float. Got: {type(duration).__name__}")
            if not isinstance(duration, (float, int)) or duration < 0:
                raise ValueError(f"Duration must be a non-negative number. Got: {duration}")
            
            if not isinstance(quality, (float, int)):
                raise ValueError(f"Quality score must be a number. Got: {quality}")

            if quality_max != 100:
                normalized_quality = normalize_quality(quality, quality_max)
            else:
                normalized_quality = quality

            if not (0 <= normalized_quality <= 100):
                raise ValueError(f"Normalized quality score must be between 0 and 100. Got: {normalized_quality}")

            self.segments.append((float(duration), float(normalized_quality)))

    #returns the average of all quality scores, rounded to two decimal places
    def average_quality(self):
        scores = [quality for duration,quality in self.segments]
        return round(sum(scores) / len(scores), 2) if scores else 0.00
    
    #returns the sum of all sleep durations, rounded to two decimal places
    def total_duration(self):
        duration = [duration for duration,quality in self.segments]
        return round(sum(duration),2) if duration else 0.00
    
    # returns True if all segments of the day meet both duration and quality thresholds. 
    # Set default values of 7 and 75 for the thresholds respectively
    def is_restful(self, duration_threshold=7, quality_threshold=75):
        for segment in self.segments:
            duration, quality = segment
            if duration < duration_threshold or quality < quality_threshold:
                return False
        return True
   
    #returns the average computed sleep score (using compute_sleep_score() in utils), rounded to two decimal places
    def average_sleep_score(self):
        scores = [compute_sleep_score(duration,quality) for duration,quality in self.segments]
        return round(sum(scores)/len(scores),2) if scores else 0.00
    
    #returns a dictionary with keys 'date', 'avg_quality', 'total_duration', 'avg_sleep_score', and 'quality_label'
    def summary(self):
        avg_quality = self.average_quality()
        total_duration = self.total_duration()
        avg_sleep_score = self.average_sleep_score()
        label = quality_label(avg_sleep_score)
        return {
            'date': self.date,
            'avg_quality': avg_quality,
            'total_duration': total_duration,
            'avg_sleep_score': avg_sleep_score,
            'quality_label': label
        }
    

def is_valid_date(date_str):
    if not isinstance(date_str, str):
        return False

    parts = date_str.split("-")
    if len(parts) != 3:
        return False

    year, month, day = parts

    if not (year.isdigit() and len(year) == 4):
        return False
    if not (month.isdigit() and len(month) == 2):
        return False
    if not (day.isdigit() and len(day) == 2):
        return False

    year = int(year)
    month = int(month)
    day = int(day)

    if not (1 <= month <= 12):
        return False

    days_in_month = {
        1: 31, 2: 29, 3: 31, 4: 30,
        5: 31, 6: 30, 7: 31, 8: 31,
        9: 30, 10: 31, 11: 30, 12: 31
    }

    if day < 1 or day > days_in_month[month]:
        return False

    return True

    