def max_sub_string(s):
    n = len(s)
    r = [0] * n
    for i in range(1, n):
        k = r[i-1]
        while k > 0 and s[k] != s[i]:
            k = r[k - 1]
        if (s[k] == s[i]):
            k += 1
        r[i] = k
    p = n - k
    return p

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

s = input()

b = max_sub_string(s)
print(b)