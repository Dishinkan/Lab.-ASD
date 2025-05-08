import time
import random
import numpy as np

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def quick_sort_3way(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[random.randint(0, len(arr) - 1)]
    lt, eq, gt = [], [], []
    for x in arr:
        if x < pivot:
            lt.append(x)
        elif x == pivot:
            eq.append(x)
        else:
            gt.append(x)
    return quick_sort_3way(lt) + eq + quick_sort_3way(gt)

def counting_sort(arr, max_val):
    if not arr:
        return []
    
    min_val = min(arr)
    offset = -min_val
    range_size = max_val - min_val + 1
    count = [0] * range_size
    for num in arr:
        count[num + offset] += 1

    sorted_arr = []
    for num, freq in enumerate(count):
        sorted_arr.extend([num - offset] * freq)

    return sorted_arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    sorted_arr = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    return sorted_arr

def clock_resolution():
    """Stima la risoluzione del clock usando time.perf_counter()."""
    start = time.perf_counter()
    while time.perf_counter() == start:
        pass
    stop = time.perf_counter()
    return stop - start

R = clock_resolution()
T_min = R * 10
subtract_init = True

m_fixed = 100000
n_values = np.logspace(np.log10(100), np.log10(100000), num=100, dtype=int)

algoritmi = {
        "Quick Sort": lambda arr: quick_sort(arr),
        "Quick Sort 3-Way": lambda arr: quick_sort_3way(arr),
        "Counting Sort": lambda arr: counting_sort(arr, m_fixed),
        "Merge Sort": lambda arr: merge_sort(arr),
        "Sorting python": lambda arr: arr.sort()
        }

def generate_array(n, m):
    """Genera un array di n interi casuali compresi in [1, m]."""
    return [random.randint(1, m) for _ in range(n)]