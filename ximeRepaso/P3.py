def contar_primos(n):
    cantidad = 0
    for i in range(2, n+1):
        es_primo = True
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                es_primo = False
                break
        if es_primo:
            cantidad += 1
    return cantidad