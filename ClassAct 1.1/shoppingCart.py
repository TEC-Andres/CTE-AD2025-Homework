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
class Shop():
    def __init__(self):
        # I would do a JSON file here but I wanted to keep it simple
        self.items_dict = {
            "apple": {
                "name": "Apple",
                "price": 1.0,
                "quantity": 10,
                "discount_after_n_item": 3,
                "percentage_discount": 10
            },
            "banana": {
                "name": "Banana",
                "price": 0.5,
                "quantity": 20,
                "discount_after_n_item": 3,
                "percentage_discount": 15
            },
            "milk": {
                "name": "Milk",
                "price": 2.5,
                "quantity": 5,
                "discount_after_n_item": 3,
                "percentage_discount": 25
            }
        }

        self.items_in_cart = []
        self.tax = 1.16
    
    def exit_shop(self):
        print("This is your ticket:")
        print("-----------------------------")
        for item in self.items_in_cart:
            print(f"{item['name']} × {item['quantity']} = ${item['total_price']:.2f}")
        print(f"Total items bought: {self.total_items()}")
        print("-----------------------------")

    def buy_item(self):
        while True:
            item_name = input("Enter the item you want to buy (or 'exit' to finish): ").lower().strip()
            if item_name == 'exit':
                self.exit_shop()
                break

            if item_name not in self.items_dict:
                print("Item not found. Please try again.")
                continue
            
            item = self.items_dict[item_name]
            print(f"{item['name'].capitalize()} costs ${item['price']} each. {item['quantity']} in stock.")
            quantity = int(input(f"How many {item['name']}s would you like to buy? "))

            if quantity <= 0:
                print("Quantity must be positive.")
                continue
            if quantity > item['quantity']:
                print(f"Sorry, only {item['quantity']} {item['name']}s available.")
                continue
            total = item['price'] * quantity
            if quantity >= item['discount_after_n_item']:
                discount = total * (item['percentage_discount'] / 100)
                total -= discount
                print(f"Discount applied: -${discount:.2f}")
            item['quantity'] -= quantity
            self.items_in_cart.append({
                    "name": item['name'],
                    "quantity": quantity,
                    "total_price": total
                })
            print(f"Total price for {quantity} {item['name']}(s): ${total:.2f}")

    def total_items(self):
        return sum(item['quantity'] for item in self.items_in_cart)

if __name__ == "__main__":
    shop = Shop()
    print("Welcome to our shop! Where you can start getting discounts from buying 3 or more items!")
    print("Here are the items available:")
    for item in shop.items_dict.values():
        print(f"- {item['name'].capitalize()}: ${item['price']} each, {item['quantity']} in stock, {item['percentage_discount']}% off after {item['discount_after_n_item']} items")
    print("You can buy any item by typing its name. Type 'exit' to finish shopping.")
    shop.buy_item()
