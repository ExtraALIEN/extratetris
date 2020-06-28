def calculate_rating_change(points, pos, start_ratings):
    rating_before = start_ratings[pos]
    k = 40
    other_ratings = [start_ratings[x] for x in start_ratings if x != pos]
    delta = 0
    total_expected = 0
    for x in other_ratings:
        total_expected += expected_points(rating_before, x)
    delta = k * ((points/100) - total_expected/len(other_ratings))
    return delta

def expected_points(a, b):
    return 1 / (1 + 10 ** ((b-a)/400))
