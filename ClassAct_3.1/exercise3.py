native_city = "MTY"

n_clients = int(input("Enter the number of clients: "))
client_data = {
    'age': [],
    'city': []
}

for i in range(n_clients):
    age = int(input(f"Enter age for client {i + 1}: "))
    city = input(f"Enter city for client {i + 1}: ")
    client_data['age'].append(age)
    client_data['city'].append(city.upper())

print(f"Total adult clients: {sum(1 for age in client_data['age'] if age >= 18)}")
print(f"Total visitor clients: {sum(1 for city in client_data['city'] if city == native_city)}")
print(f"Total local clients: {sum(1 for city in client_data['city'] if city != native_city)}")
