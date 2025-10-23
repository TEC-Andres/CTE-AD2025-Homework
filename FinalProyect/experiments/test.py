import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.bombOperator import BombOperator
from lib.tensor import Tensor, TensorPrinter

if __name__ == "__main__":
    tensor = Tensor(rank=4, size=3)
    op = BombOperator()
    printer = TensorPrinter(tensor.data)
    printer.print_grid(per_line=3)
    op.apply(tensor.data)
    print("\nAfter applying BombOperator:\n")
    printer = TensorPrinter(op.apply(tensor.data))
    printer.print_grid(per_line=3)
