import random

def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value

def weighted_choice(items, key="prob"):
    r = random.random()
    cur = 0.0
    for item in items:
        cur += item[key]
        if r <= cur:
            return item
    return items[-1]
