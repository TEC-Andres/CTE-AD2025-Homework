'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: part2_exc2.py
#
#       Created:                08/19/2025
#       Last Modified:          08/19/2025
'''
# Import libraries
import math
import decimal
import fractions

# Get your variables
vi = float(input("Enter the initial velocity (m/s): "))
angle = float(input("Enter the launch angle (degrees): "))
g = float(input("Enter the acceleration due to gravity (m/s²): "))
precision = int(input("Enter the number of decimal places for the results: "))

# Init precision level
decimal.getcontext().prec = precision+1

# Get components
vix = decimal.Decimal(vi * math.cos(math.radians(angle)))
viy = decimal.Decimal(vi * math.sin(math.radians(angle)))


angle_rad = math.radians(angle)
g_decimal = decimal.Decimal(g)
T = (2 * viy) / g_decimal
H = (viy**2) / (2 * g_decimal)
R = decimal.Decimal(vi**2 * math.sin(math.radians(2 * angle))) / g_decimal

angle_fraction = fractions.Fraction(angle_rad / math.pi).limit_denominator()
print(f"Angle as a rational multiple of pi: {angle_fraction}π")
print(f"vx: {vix:.{precision}f} m/s")
print(f"vy: {viy:.{precision}f} m/s")
print(f"Time of flight: {T:.{precision}f} s")
print(f"Maximum height: {H:.{precision}f} m")
print(f"Range: {R:.{precision}f} m")