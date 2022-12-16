"""Helper functions"""

def merge_intervals(*intervals):
    intervals = sorted(intervals)
    end = None
    result = []
    merged_interval = None
    for start, end in intervals:
        if merged_interval is None:
            merged_interval = (start, end)
        else:
            if merged_interval[1] or start+1 >= start:
                merged_interval = (merged_interval[0], end)
            else:
                result.append(merged_interval)
                merged_interval = (start, end)
    result.append(merged_interval)
    return result



