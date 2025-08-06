from utils import compute_sleep_score

def overall_average_duration(records):
    if not isinstance(records, list):
        raise TypeError("records must be a list of DailySleepRecord instances.")

    durations = []
    for record in records:
        for segment in record.segments:
            duration,quality = segment
            durations.append(duration)
    return round(sum(durations)/len(durations),2) if durations else 0.00

def best_sleep_day(records):
    if not records:
        return None
    
    best_sleep_record = records[0]
    best_score = best_sleep_record.average_sleep_score()
    
    for record in records[1:]:
        actual_score = record.average_sleep_score()
        if actual_score>best_score:
            best_score = actual_score
            best_sleep_record=record

    return best_sleep_record.date

def detect_under_sleep_days(records, threshold=0):
    if not isinstance(records, list):
        raise TypeError("records must be a list of DailySleepRecord instances.")
    under_sleep_days = []
    for record in records:
        for segment in record.segments:
            duration,quality = segment
            if duration<threshold:
                under_sleep_days.append(record.date)
                break
    return under_sleep_days

def detect_spike(durations, *, threshold=2):
    if not isinstance(durations, list):
        raise TypeError("durations must be a list of float values.")
    if len(durations) < 2:
        raise ValueError("At least two durations are needed to detect spikes.")
    #if(len(durations)<2):
    #    return False
    
    for i in range(1,len(durations)):
        current = durations [i]
        previous = durations [i -1]
        difference = abs(current - previous)
        if difference >= threshold:
            return True
    return False

def duration_trend(durations):
    if not isinstance(durations, list):
        raise TypeError("durations must be a list of float values.")
    if len(durations) < 2:
        raise ValueError("At least two duration values are required to compute a trend.")
    
    trend = []
    for i in range(1, len(durations)):
        if durations[i] > durations[i - 1]:
            trend.append('up')
        elif durations[i] < durations[i - 1]:
            trend.append('down')
        else:
            trend.append('same')
    return trend

def average_sleep_score_across_days(records):
    if not isinstance(records, list):
        raise TypeError("records must be a list of DailySleepRecord instances.")
    scores_across_days = []
    for record in records:
        for segment in record.segments:
            duration,quality = segment
            score = compute_sleep_score(duration,quality)
            scores_across_days.append(score)
    return round(sum(scores_across_days)/len(scores_across_days),2) if scores_across_days else 0.00
