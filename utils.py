def swapping(array, i, j):
    arr = array.copy()
    aux = arr[i]
    arr[i] = arr[j]
    arr[j] = aux
    return arr

def reversion(array, i, j):
    arr = array.copy()
    arr[i:(j+1)] = arr[i:(j+1)][::-1]
    return arr

def insertion(array, i, j):
    arr = array.copy()
    arr.insert(i, arr.pop(j))
    return arr

def objective_func(array):
    return array[0] + array[5] + array[9]

def factible_func(array):
    return True