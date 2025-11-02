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

def rects_intersect(a, b):
    (ax1, ay1, ax2, ay2) = a
    (bx1, by1, bx2, by2) = b

    # если один прямоугольник полностью левее другого
    if ax2 < bx1:
        return False
    if bx2 < ax1:
        return False

    # если один полностью выше другого
    if ay2 < by1:
        return False
    if by2 < ay1:
        return False

    return True
