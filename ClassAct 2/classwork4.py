'''
#       Sesion 2: Programs that make decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork4.py
#
#       Created:                08/22/2025
#       Last Modified:          08/23/2025
'''
purchase = 1200
if purchase < 100:
    print("Pay with cash")
elif purchase < 300:
    print("Pay with debit card.")
else:
    print("Pay with credit card.")