
def leggi_input(s):
    tokens = s.split()
    return ["NULL" if x == "NULL" else int(x) for x in tokens]

def verifica_bst(array):
    i = [0]

    def parsing(min_val, max_val):
        # Punto 1: leggo il nodo corrente
        if i[0] >= len(array):
            return True

        val = array[i[0]]
        i[0] += 1

        # Punto 6: controllo se è NULL
        if val == "NULL":
            return True

        # Punto 2-4: confronto con min e max (padri in memoria)
        if not (min_val < val < max_val):
            return False

        # Punto 5: se supera il confronto, "scendo" e tengo in memoria il nodo attuale come nuovo max o min
        # Punto 6: vado a sinistra (sx dev'essere < val)
        left_valid = parsing(min_val, val)

        # Punto 7: completato il ramo sx, controllo il ramo dx
        # Punto 9: vado a destra (dx dev'essere > val)
        right_valid = parsing(val, max_val)

        # Punto 8, 15, 20, 21, 22: ritorno verso l'alto, controllo che entrambi i rami siano validi
        return left_valid and right_valid

    return int(parsing(float('-inf'), float('inf')))

s = input()

array = leggi_input(s)

print(verifica_bst(array))

'''
NON BST
5 3 2 NULL NULL 6 NULL NULL 8 7 NULL NULL 4 NULL NULL

BST
0 -3 -10 NULL NULL -2 NULL NULL 9 5 NULL NULL 12 NULL NULL
'''