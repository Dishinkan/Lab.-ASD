import time
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# -------------------------------
# IMPLEMENTAZIONE DEGLI ALGORITMI
# -------------------------------

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

# -------------------------------
# FUNZIONI DI SUPPORTO
# -------------------------------

def generate_array(n, m):
    """Genera un array di n interi casuali compresi in [1, m]."""
    return [random.randint(1, m) for _ in range(n)]

def generate_worst_case_array(n, m): # caso di array ordinato
    """
    Genera un array 'worst-case': ad esempio, un array ordinato in modo crescente.
    Per alcuni algoritmi l'input ordinato può rappresentare il caso pessimo
    """
    arr = generate_array(n, m)
    arr.sort()
    return arr

def clock_resolution():
    """Stima la risoluzione del clock usando time.perf_counter()."""
    start = time.perf_counter()
    while time.perf_counter() == start:
        pass
    stop = time.perf_counter()
    return stop - start

def measure_init_time(n, m, T_min, num_trials=10):
    """Misura il tempo medio di inizializzazione (generazione dell'array)."""
    trial_init_times = []
    for _ in range(num_trials):
        count = 0
        total_init_time = 0.0
        trial_start = time.perf_counter()
        t0 = time.perf_counter()
        while True:
            generate_array(n, m)
            t1 = time.perf_counter()
            total_init_time += (t1 - t0)
            count += 1
            if (time.perf_counter() - trial_start) >= T_min:
                break
        trial_init_times.append(total_init_time / count)
    return np.mean(trial_init_times)

def measure_sorting_time(sort_func, n, m, T_min, num_trials=10, subtract_init=False, init_time=0.0):
    """
    Misura il tempo medio di esecuzione del sort_func su array di dimensione n e range m.
    Esegue l'algoritmo ripetutamente fino a superare T_min e calcola il tempo medio per iterazione.
    Se subtract_init=True, viene sottratto il tempo medio di inizializzazione.
    """
    trial_times = []
    for _ in range(num_trials):
        count = 0
        total_sort_time = 0.0
        trial_start = time.perf_counter()
        t0 = time.perf_counter()
        while True:
            arr = generate_array(n, m)
            sort_func(arr[:])
            t1 = time.perf_counter()
            total_sort_time += (t1 - t0)
            count += 1
            if (time.perf_counter() - trial_start) >= T_min:
                break
        avg_time = total_sort_time / count
        if subtract_init:
            avg_time -= init_time
        trial_times.append(avg_time)
    mean_time = np.mean(trial_times)
    std_time = np.std(trial_times)
    return mean_time, std_time

def measure_sorting_time_worst(sort_func, n, m, T_min, num_trials=10, subtract_init=False, init_time=0.0,
                               worst_case_generator=generate_worst_case_array):
    """
    Misura il tempo medio di esecuzione del sort_func su array worst-case.
    Funziona come measure_sorting_time(), ma utilizza un input deterministico.
    """
    trial_times = []
    for _ in range(num_trials):
        count = 0
        total_sort_time = 0.0
        trial_start = time.perf_counter()
        t0 = time.perf_counter()
        while True:
            arr = worst_case_generator(n, m)
            sort_func(arr[:])
            t1 = time.perf_counter()
            total_sort_time += (t1 - t0)
            count += 1
            if (time.perf_counter() - trial_start) >= T_min:
                break
        avg_time = total_sort_time / count
        if subtract_init:
            avg_time -= init_time
        trial_times.append(avg_time)
    mean_time = np.mean(trial_times)
    std_time = np.std(trial_times)
    return mean_time, std_time

# -------------------------------
# FUNZIONE GENERALE PER LA CREAZIONE DEI GRAFICI
# -------------------------------

def plot_experiment(df, param_col, param_label, title, file_name=None):
    """
    Plotta i risultati di un esperimento.
    df: DataFrame con colonne [param_col, 'algorithm', 'mean_time'].
    param_col: nome della colonna del parametro (ad es. 'n' o 'm').
    param_label: etichetta per l'asse x.
    title: titolo del grafico.
    file_name: se specificato, salva il grafico in un file.
    log_scale: se True, usa scala logaritmica per entrambi gli assi.
    """
    plt.figure(figsize=(10, 6))
    for algo in df['algorithm'].unique():
        subdf = df[df['algorithm'] == algo].sort_values(by=param_col)
        plt.plot(subdf[param_col], subdf['mean_time'], marker='o', alpha=0.6, label=algo)
    plt.xlabel(param_label)
    plt.ylabel("Tempo medio di esecuzione (s)")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    if file_name is not None:
        plt.savefig(file_name, bbox_inches='tight')
    plt.show()

# -------------------------------
# ESPERIMENTI
# -------------------------------

'''

n = numero di elementi nell'array
m = range min-max tra gli elementi nell'array

'''

def main():
    # Mostra la directory corrente per verificare dove salvare i file
    print("Current working directory:", os.getcwd())
    
    # Calcola la risoluzione del clock e Tmin
    R = clock_resolution()
    T_min = R * 10
    subtract_init = True
    
    # Container per i risultati
    exp1_results = []  # Esperimento 1: variare n (con m fisso)
    exp2_results = []  # Esperimento 2: variare m (con n fisso)
    exp3_results = []  # Esperimento 3: worst-case (variare n, con m fisso)
    
    # Esperimento 1: Variare n (con m fisso = 100000)
    m_fixed = 100000
    n_values = np.logspace(np.log10(100), np.log10(100000), num=100, dtype=int)
    algorithms = {
        "Quick Sort": lambda arr: quick_sort(arr),
        "Quick Sort 3-Way": lambda arr: quick_sort_3way(arr),
        "Counting Sort": lambda arr: counting_sort(arr, m_fixed),
        "Merge Sort": lambda arr: merge_sort(arr),
        "Sort": lambda arr: arr.sort()
    }
    for n in n_values:
        init_avg = measure_init_time(n, m_fixed, T_min) if subtract_init else 0.0
        for name, func in algorithms.items():
            mean_time, std_time = measure_sorting_time(func, n, m_fixed, T_min, subtract_init=subtract_init, init_time=init_avg)
            rel_error = std_time / mean_time if mean_time > 0 else 0.0
            exp1_results.append({
                "experiment": "Exp1",
                "n": n,
                "algorithm": name,
                "mean_time": mean_time,
                "std_time": std_time,
                "relative_error": rel_error
            })
            
    df_exp1 = pd.DataFrame(exp1_results)
    df_exp1.to_csv("experiment1.csv", index=False)
    plot_experiment(df_exp1, "n", "Dimensione n dell'array", 
                    "Esperimento 1: Tempo in funzione di n (m fisso)",
                    file_name="exp1_graph.png")
    
    # Esperimento 2: Variare m (con n fisso = 10000)
    n_fixed = 10000
    m_values = np.logspace(np.log10(10), np.log10(1000000), num=100, dtype=int)
    for m_val in m_values:
        init_avg = measure_init_time(n_fixed, m_val, T_min) if subtract_init else 0.0
        for name in algorithms.keys():
            func = (lambda arr, m_val=m_val: counting_sort(arr, m_val)) if name == "Counting Sort" else algorithms[name]
            mean_time, std_time = measure_sorting_time(func, n_fixed, m_val, T_min, subtract_init=subtract_init, init_time=init_avg)
            rel_error = std_time / mean_time if mean_time > 0 else 0.0
            exp2_results.append({
                "experiment": "Exp2",
                "m": m_val,
                "algorithm": name,
                "mean_time": mean_time,
                "std_time": std_time,
                "relative_error": rel_error
            })
    df_exp2 = pd.DataFrame(exp2_results)
    df_exp2.to_csv("experiment2.csv", index=False)
    plot_experiment(df_exp2, "m", "Intervallo m dei valori", 
                    "Esperimento 2: Tempo in funzione di m (n fisso)",
                    file_name="exp2_graph.png")
    
    # Esperimento 3: Worst-case: variare n (con m fisso = 100000)
    m_fixed_wc = 100000
    n_values_wc = np.logspace(np.log10(100), np.log10(100000), num=100, dtype=int)
    for n in n_values_wc:
        init_avg = measure_init_time(n, m_fixed_wc, T_min) if subtract_init else 0.0
        for name, func in algorithms.items():
            mean_time, std_time = measure_sorting_time_worst(func, n, m_fixed_wc, T_min,
                                                              subtract_init=subtract_init, init_time=init_avg)
            rel_error = std_time / mean_time if mean_time > 0 else 0.0
            exp3_results.append({
                "experiment": "Exp3",
                "n": n,
                "algorithm": name,
                "mean_time": mean_time,
                "std_time": std_time,
                "relative_error": rel_error
            })
    df_exp3 = pd.DataFrame(exp3_results)
    df_exp3.to_csv("experiment3.csv", index=False)
    plot_experiment(df_exp3, "n", "Dimensione n dell'array (worst-case)", 
                    "Esperimento 3: Casi Pessimi con m fisso",
                    file_name="exp3_graph.png")
    
    return df_exp1, df_exp2, df_exp3

if __name__ == "__main__":
    df1, df2, df3 = main()