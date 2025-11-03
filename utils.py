import random

def clamp(value, lo, hi):
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value

def weighted_choice(items, key="prob"):
    r = random.random()
    cur = 0.0
    for item in items:
        cur += item[key]
        if r <= cur:
            return item
    return items[-1]

def rects_intersect(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b

    if ax2 < bx1 or bx2 < ax1:
        return False
    if ay2 < by1 or by2 < ay1:
        return False
    return True
