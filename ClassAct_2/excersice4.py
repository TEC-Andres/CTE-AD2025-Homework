'''
#       Sesion 2: Programs that make decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: exercise4.py
#       Title: E-Commerce Checkout (coupons, shipping, state tax rules)
#
#       Created:                08/22/2025
#       Last Modified:          08/23/2025
'''
# Init Variables
saved = 0
noShipFee = 0
shipping_fee = 0

# Tax Districts
tx = 8.25
ca = 7.25
other = 6.00

# Misc constants
weightStdFee = 8
weightOverFee = 12
save10AfterAmount = 50
freeShipAmount = 75

# Inputs
subtotal = float(input("Enter goods subtotal ($): "))
weight_kg = float(input("Enter the total weight (kg): "))
state = input("Enter the state (TX, CA, other): ")
coupon_code = input("Enter coupon code (if any): ")

if coupon_code == "SAVE10" and subtotal >= save10AfterAmount:
    saved = subtotal * 0.1
    subtotal = subtotal - saved
elif coupon_code == "FREESHIP" and subtotal >= freeShipAmount:
    noShipFee = 1

if noShipFee == 1:
    subtotal = subtotal
elif weight_kg > 10:
    shipping_fee = weightOverFee
    subtotal += shipping_fee
else:
    shipping_fee = weightStdFee
    subtotal += shipping_fee

if state == "TX":
    taxPercentage = (1 + tx / 100)
    subtotal *= taxPercentage
elif state == "CA":
    taxPercentage = (1 + ca / 100)
    subtotal *= taxPercentage
else:
    taxPercentage = (1 + other / 100)
    subtotal *= taxPercentage


print(f"Discount: -${saved:.2f}")
print(f"Shipping: ${shipping_fee:.2f}")
print(f"Tax on goods: ${subtotal - (subtotal / taxPercentage):.2f}")
print(f"ORDER TOTAL: ${subtotal:.2f}")