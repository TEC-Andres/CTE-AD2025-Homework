'''
#       Sesion 1: Programs that require calculations
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: shoppingCart.py
#
#       Created:                08/19/2025
#       Last Modified:          08/19/2025
'''
# Inputs
unit_price = float(input("Enter the unit price of the item: "))
quantity = int(input("Enter the quantity of items: "))
discount = int(input("Enter the discount percentage (if any, else enter 0): "))
discount = discount / 100
tax = int(input("Enter the tax percentage: "))
tax = tax / 100

# Process
subtotal = unit_price * quantity
discount_amount = subtotal * discount
taxable = subtotal - discount_amount
sales_tax_amount = taxable * tax
total_amount = taxable + sales_tax_amount

# Outputs
print(f"Subtotal: {subtotal:.2f} pesos")
print(f"Discount: {discount_amount:.2f} pesos")
print(f"Taxable amount: {taxable:.2f} pesos")
print(f"Sales tax amount: {sales_tax_amount:.2f} pesos")
print(f"Total amount: {total_amount:.2f} pesos")