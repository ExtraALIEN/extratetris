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
    print(prev)
    print(cur)
    for y in prev:
        for x in prev[y]:
            if prev[y][x] != 0:
                if y not in cur or x not in cur[y]:
                    if y not in result:
                        result[y] = {}
                    result[y][x] = 0
                elif cur[y][x] != prev[y][x]:
                    if y not in result:
                        result[y] = {}
                    result[y][x] = cur[y][x]
    for y in cur:
        for x in cur[y]:
            if cur[y][x] != 0:
                if y not in prev or x not in prev[y]:
                    if y not in result:
                        result[y] = {}
                    result[y][x] = cur[y][x]
                elif cur[y][x] != prev[y][x]:
                    if y not in result:
                        result[y] = {}
                    result[y][x] = cur[y][x]

    print(result)
    return result





    # result = {}
    # for y in cur:
    #     if y not in prev:
    #         result[y] = cur[y]
    #     else:
    #         for x in cur[y]:
    #             if x not in prev[y] or cur[y][x] != prev[y][x]:
    #                 if y not in result:
    #                     result[y] = {}
    #                 result[y][x] = cur[y][x]
    # for y in prev:
    #     if y not in cur:
    #         result[y] = {}
    #         for x in prev[y]:
    #             result[y][x] = 0
    #     else:
    #         for x in prev[y]:
    #             if x not in cur[y]:
    #                 result[y][x] = 0
    #
    # return result
