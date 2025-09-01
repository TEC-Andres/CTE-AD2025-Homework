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
#       Last Modified:          08/31/2025
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
    print(f"Tax: {tax_rate(120, 'TX'):.2f}")

if __name__ == "__main__":
    main()