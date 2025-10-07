import tkinter as tk

class Tensor:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def create_tensor(rank, size, count=1):
        if rank == 1:
            return [count + i for i in range(size)]
        else:
            return [Tensor.create_tensor(rank-1, size, count + size * i) for i in range(size)]

def print_tensor(tensor, indent=0):
    if isinstance(tensor[0], list):
        for sub_tensor in tensor:
            print_tensor(sub_tensor, indent + 2)
            print()
    else:
        print(' ' * indent + str(tensor))

if __name__ == "__main__":
    tensor = Tensor.create_tensor(4, 4)
    print_tensor(tensor)