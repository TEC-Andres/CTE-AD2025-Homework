'''
#       Sesion 3: Functions with Decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: exercise2_1.py
#       Title: Progressive Utility Bill (tiers, surcharge, caps)
#
#       Created:                08/31/2025
#       Last Modified:          09/02/2025
'''
def tax_rate(subtotal, state):
    if state == "TX":
        subtotal *= 0.0825
    elif state == "CA":
        subtotal *= 0.075
    else:
        subtotal *= 0.06
    return float(subtotal)

def main() -> None:
    a = float(input("Enter subtotal: "))
    b = input("Enter state (TX, CA, or other): ")
    print(f"Tax: {tax_rate(a, b):.2f}")

if __name__ == "__main__":
    main()