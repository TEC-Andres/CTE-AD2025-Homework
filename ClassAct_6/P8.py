num_elements = int(input("How many elements will the list contain? "))
user_list = []
for i in range(num_elements):
    element = input(f"Enter element {i+1}: ")
    user_list.append(element)

print(user_list)

unique_list = []
for item in user_list:
    if item not in unique_list:
        unique_list.append(item)

print(unique_list)