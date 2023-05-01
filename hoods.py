import utils

def v1(array):
    hood = []
    for i in range(1, len(array)):
        solution = utils.reversion(array, 0, i)
        hood.append(solution)
    return hood

def v2(array):
    hood = []
    for i in range(len(array)):
        for k in range(i + 1, len(array)):
            solution = utils.reversion(array, i, k)
            hood.append(solution)
    return hood
