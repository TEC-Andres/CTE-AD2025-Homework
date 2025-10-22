from bombOperator import BombOperator
from tensor import Tensor, TensorPrinter

if __name__ == "__main__":
    tensor = Tensor(rank=4, size=4)
    op = BombOperator()
    printer = TensorPrinter(tensor.data)
    printer.print_grid(per_line=4)
    op.apply(tensor.data)
    print("\nAfter applying BombOperator:\n")
    printer = TensorPrinter(op.apply(tensor.data))
    printer.print_grid(per_line=4)
