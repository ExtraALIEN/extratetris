def build_empty_field_list(width, height):
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
