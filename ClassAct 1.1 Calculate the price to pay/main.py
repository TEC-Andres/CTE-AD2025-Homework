'''
#       Sesion 1: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: main.py
#
#       Created:                08/12/2025
#       Last Modified:          08/13/2025
'''
import random
import os

cost_per_kilo = 30

class Oranges(dict):
    def __init__(self):
        num_oranges = random.randint(20, 50)
        for i in range(num_oranges):
            self[f"orange_{i+1}"] = random.randint(100, 300)
        pass

class Choose():
    def __init__(self):
        self.chosen_oranges = []
        pass

    def choose_oranges(self, orange):
        while True:
            if len(orange)-len(self.chosen_oranges) == 0:
                print("No more oranges available to choose.")
                input("Continue")
                break
            os.system('cls')
            print(f"Press Enter to choose an orange. Theres currently {len(orange)-len(self.chosen_oranges)} oranges available")
            input(">>> ")
            chosen = random.choice(list(orange.items()))
            print(f"You have chosed an orange that weights {chosen[1]} grams!")
            self.chosen_oranges.append(chosen)

            if input("Do you want to choose another orange? (y/[Enter]=yes, n=no): ").lower() not in ["y", "yes", ""]:
                break
        
        # Subtotal Logic
        oranges_weight = int(sum(item[1] for item in self.chosen_oranges))
        subtotal = oranges_weight * cost_per_kilo / 1000

        print("Here are the oranges you have chosen:")
        for orange_item in self.chosen_oranges:
            print(f"- {orange_item[0]}: {orange_item[1]} grams")
        print(f"Total orange weight: {oranges_weight} grams")
        print(f"Subtotal: {subtotal} pesos")
        print(f"Total: {subtotal * 1.16} pesos")
        print(f"Thank you for choosing oranges!")

if __name__ == "__main__":
    oranges = Oranges()
    chooser = Choose()
    chooser.choose_oranges(oranges)

