'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: exercise1.py
#       Title: Progressive Electricity Billing (tiers, surcharges, caps)
#
#       Created:                08/22/2025
#       Last Modified:          08/22/2025
'''
khw = int(input("Enter the number of kWh consumed: "))
senior_test = input("Are you a senior? (yes/no): ").strip().lower()
fixed_charge = float(input("Enter the fixed charge: "))
minimum_bill_after_everything = 50

# Calculate energy charge
if khw <= 100:
    energy_charge = khw * 0.12
elif khw <= 300:
    energy_charge = (100 * 0.12) + ((khw - 100) * 0.15)
else:
    energy_charge = (100 * 0.12) + (200 * 0.15) + ((khw - 300) * 0.2)

# Environmental fee applies if khw > 250
if khw > 250:
    environmental_fee = energy_charge * 0.05
else:
    environmental_fee = 0

# Senior discount applies if senior
if senior_test == "yes":
    senior_discount = (energy_charge + environmental_fee) * 0.1
else:
    senior_discount = 0

# Total calculation
total = energy_charge + environmental_fee + fixed_charge - senior_discount
if total < minimum_bill_after_everything:
    total = minimum_bill_after_everything

print(f"Energy charge: ${energy_charge:.2f}")
print(f"Environmental fee: ${environmental_fee:.2f}")
print(f"Senior discount: -${senior_discount:.2f}")
print(f"Fixed fee: +${fixed_charge:.2f}")
print(f"TOTAL DUE: ${total:.2f}")
