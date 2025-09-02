import os
import pandas as pd

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mobile_game_inapp_purchases.xlsx")
df = pd.read_excel(data_path)

average_age = df.iloc[:, 1].mean()          # Column 'B2:B'
payment_method = df.iloc[:, 11].mode()[0]   # Column 'L2:L'
print(f"Average age of all users: {average_age}")
print(f"Most popular payment method: {payment_method}")