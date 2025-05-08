'''def periodo(s):
    n = len(s)
    for p in range(1, n):
        periodo = True
        for i in range(n):
            if (s[i] != s[i % p]):
                periodo = False
        if periodo == True:
            return p
    return n

s = input()

a = periodo(s)
print(a)'''