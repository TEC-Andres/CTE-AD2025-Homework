'''
#       Sesion 3: Functions with Decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: exercise1_2.py
#       Title: Progressive Utility Bill (tiers, surcharge, caps)
#
#       Created:                08/31/2025
#       Last Modified:          09/02/2025
'''
def show_time_slot(day_code, hour_24):
    # Day list
    l_daycode = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    # Basic check to see if day_code is valid
    if day_code not in l_daycode:
        print("Invalid day code.")
    # Time slot classifications
    if (9 <= hour_24 <= 17) and (day_code in l_daycode[0:5]):
        print("Peak")
    elif (7 <= hour_24 < 9 or 17 < hour_24 <= 19) and (day_code in l_daycode[0:5]):
        print("Shoulder")
    else:
        print("Off-peak")

# Function execution
if __name__ == "__main__":
    a = input("Enter day code (e.g., MON): ")
    b = int(input("Enter hour (24-hour format): "))
    show_time_slot(a, b)