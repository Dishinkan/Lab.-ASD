def leggi_input(s):
    tokens = s.split()
    return ["NULL" if x == "NULL" else int(x) for x in tokens]

def verifica_bst(array):
    i = 0
    n = len(array)
    
    def parsing(min_val, max_val):
        nonlocal i
        if i >= n:
            return True
        
        val = array[i]
        i += 1
        
        # Se "NULL", significa che il nodo non esiste (è un ramo vuoto)
        if val == "NULL":
            return True
        
        key = int(val)  # valore nodo corrente
        
        # Verifica rispetto limiti (minimo e massimo)
        if not (min_val < key < max_val):
            return False
        
        # Scansione del sotto-albero Sx (figlio Sx deve essere minore del nodo)
        if not parsing(min_val, key):
            return False
        
        # Scansione del sotto-albero Dx (figlio dx deve essere maggiore del nodo)
        if not parsing(key, max_val):
            return False
        
        return True
    
    # Scansione array con limiti iniziali (minimo e massimo)
    if parsing(float('-inf'), float('inf')) and i == n:
        return 1
    else:
        return 0

s = input()

array = leggi_input(s)

print(verifica_bst(array))