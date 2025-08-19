'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: part2_exc3.py
#
#       Created:                08/19/2025
#       Last Modified:          08/19/2025
'''
import math 
import datetime
import decimal 

decimal.getcontext().prec = 4

# Retrieve dates
date1 = datetime.datetime.strptime(input("Enter start datetime (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")
date2 = datetime.datetime.strptime(input("Enter end datetime (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")

# Time breakdown
delta = date2 - date1
total_seconds = delta.total_seconds()
days = total_seconds // 86400
hours = (total_seconds % 86400) // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
total_hours = decimal.Decimal(total_seconds) / 3600

print(f"Total seconds: {total_seconds}")
print(f"Days: {days}")
print(f"Hours: {hours}")
print(f"Minutes: {minutes}")
print(f"Seconds: {seconds}")
print(f"Total hours (rounded): {total_hours:.3f}")