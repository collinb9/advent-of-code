"""Helper functions"""
import re


def ints(s: str):
    return list(map(int, re.findall(r"-?\d+", s)))


def intervals_intersect(test, intervals):
    """
    test is an interval
    intervals is a list of intervals
    """
    test_start, test_end = test
    for start, end in intervals:
        if (
            (start <= test_start <= end)
            or (start <= test_end <= end)
            or (test_start <= start <= test_end)
            or (test_start <= end <= test_end)
        ):
            return True
    return False


def merge_intervals(*intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    end = None
    result = []
    merged_interval = None
    _type = type(intervals[0])
    for start, end in intervals:
        if merged_interval is None:
            merged_interval = _type([start, end])
        else:
            if merged_interval[1] is None or merged_interval[1] >= start - 1:
                if merged_interval[1] >= end:
                    continue
                else:
                    merged_interval = _type([merged_interval[0], end])
            else:
                result.append(merged_interval)
                merged_interval = _type([start, end])
    result.append(merged_interval)
    return result
