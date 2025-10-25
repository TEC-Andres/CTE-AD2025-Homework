lista = ['canvas', 'acquisitions', 'targets', 'urge', 'refer', 'occasion',
         'montana', 'hebrew', 'lightweight', 'were', 'respondent', 'hoped',
         'micro', 'forge', 'investigator', 'additional', 'symbol', 'prove',
         'holiday', 'competent', 'george', 'ability', 'upskirt', 'precision',
         'cow', 'photograph', 'chairman', 'electronic', 'float', 'spend',
         'starring', 'establishing', 'fold', 'logical', 'lower', 'ic',
         'boundaries', 'petersburg', 'grand', 'journalism', 'heard', 'chips',
         'global', 'pays', 'september', 'semiconductor', 'furnished',
         'wonderful', 'aged', 'generic', "as"]

prim = lista[0]
long_max = len(prim)
long_min = len(prim)
mas_largas = [prim]
mas_cortas = [prim]

for palabra in lista:
    L = len(palabra)

    if L > long_max:
        long_max = L
        mas_largas = [palabra]
    elif L == long_max:
        mas_largas.append(palabra)

    # Para mínimas
    if L < long_min:
        long_min = L
        mas_cortas = [palabra]
    elif L == long_min:
        mas_cortas.append(palabra)

print("Palabras más largas (longitud={}):".format(long_max), mas_largas)
print("Palabras más cortas (longitud={}):".format(long_min), mas_cortas)