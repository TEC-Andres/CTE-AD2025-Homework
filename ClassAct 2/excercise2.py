'''
#       Sesion 2: Programs that make decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: exercise2.py
#       Title: Income Tax Calculator (status rules, thresholds, credits)
#
#       Created:                08/22/2025
#       Last Modified:          08/23/2025
'''
# Constants 
ten_percent = 0.1
twelve_percent = 0.12
twenty_two_percent = 0.22
deduction_single = 13000
deduction_married = 26000
dependent_credit = 1500

# Inputs
incomeAnual = float(input("Please enter your annual income: "))
filingStatus = input("Please enter your filing status (single/married): ")
dependentsNum = int(input("Please enter the number of dependents: "))
tax = 0

# Check whether the filing status is single or married
if filingStatus == "single":
    incomeAnual -= deduction_single
elif filingStatus == "married":
    incomeAnual -= deduction_married

# Check the income range and calculate tax
if incomeAnual <= 40000:
    tax = incomeAnual * ten_percent
elif incomeAnual <= 85000:
    tax = 4000 + (incomeAnual - 40000) * twelve_percent
else:
    tax = 10600 + (incomeAnual - 85000) * twenty_two_percent

# Check for dependents and apply credit
if dependentsNum > 0:
    tax -= dependent_credit

# Check whether the tax is below the minimum threshold
if tax < 200:
    tax = 0

print(f"Tax due: {tax:.2f}")