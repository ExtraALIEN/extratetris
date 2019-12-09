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


def vertical_blocks(arr, x):
    s = 0
    for el in arr:
        if el[arr] > 0:
            s += 1
    return s


def horizontal_blocks(arr, x):
    s = 0
    for el in arr[x]:
        if el > 0:
            s += 1
    return s
