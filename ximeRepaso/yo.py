lista = ['canvas', 'acquisitions', 'targets', 'urge', 'refer', 'occasion',
         'montana', 'hebrew', 'lightweight', 'were', 'respondent', 'hoped',
         'micro', 'forge', 'investigator', 'additional', 'symbol', 'prove',
         'holiday', 'competent', 'george', 'ability', 'upskirt', 'precision',
         'cow', 'photograph', 'chairman', 'electronic', 'float', 'spend',
         'starring', 'establishing', 'fold', 'logical', 'lower', 'ic',
         'boundaries', 'petersburg', 'grand', 'journalism', 'heard', 'chips',
         'global', 'pays', 'september', 'semiconductor', 'furnished',
         'wonderful', 'aged', 'generic', "as"]



a = [lista[0]]
alen = len(a[0])

b = [lista[0]]
blen = len(b[0])

for palabra in lista:
    lenPalabra = len(palabra)
    if lenPalabra == alen:
        a.append(palabra)
    elif lenPalabra > alen:
        a = [palabra]
        alen = lenPalabra

    if lenPalabra == blen:
        b.append(palabra)
    elif lenPalabra < blen:
        b = [palabra]
        blen = lenPalabra

print(a, b)