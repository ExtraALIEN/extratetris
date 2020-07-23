def buildEmptyFieldList(width, height):
    return [[0 for j in range(width)] for i in range(height)]


def rotate(arr, clockwise):
    result = []
    for i in range(len(arr[0])):
        s = [arr[j][i] for j in range(len(arr))]
        if clockwise:
            s.reverse()
            result.append(s)
        else:
            result.insert(0, s)
    return result


def diff_obj(prev, cur):
    result = {}
    for y in prev:
        if isinstance(y, int):
            if y not in cur:
                result[y] = {}
                for x in prev[y]:
                    if prev[y][x] > 0:
                        result[y][x] = 0
            else:
                for x in prev[y]:
                    if x not in cur[y]:
                        if prev[y][x] > 0:
                            if y not in result:
                                result[y] = {}
                            result[y][x] = 0
    for y in cur:
        if isinstance(y, int):
            if y not in prev:
                result[y] = {}
                for x in cur[y]:
                    if cur[y][x] > 0:
                        result[y][x] = cur[y][x]
            else:
                for x in cur[y]:
                    if x not in prev[y]:
                        if y not in result:
                            result[y] = {}
                        result[y][x] = cur[y][x]
                    elif cur[y][x] != prev[y][x]:
                        if y not in result:
                            result[y] = {}
                        result[y][x] = cur[y][x]
    return result


def sum(shape):
    s = 0
    for y in shape:
        for x in y:
            if x > 0:
                s += 1
    return s


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
