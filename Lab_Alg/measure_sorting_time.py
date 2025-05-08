from Algorithms import *

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

for n in n_values:
    init_avg = measure_init_time(n, m_fixed, T_min) if subtract_init else 0.0
    for name, func in algoritmi.items():
        mean_time, std_time = measure_sorting_time(func, n, m_fixed, T_min, subtract_init=subtract_init, init_time=init_avg)
        rel_error = std_time / mean_time if mean_time > 0 else 0.0