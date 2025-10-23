
import random
from typing import Any, List, Sequence, Tuple
from assets import VAR

class Tensor:
    """Creates rank-N tensors as nested Python lists upon instantiation."""
    def __init__(self, rank, size, bombs=1):
        # Seed RNG from current global VAR to allow reproducible or random boards
        try:
            random.seed(getattr(VAR, 'SEED', 98734987344567))
        except Exception:
            random.seed(98734987344567)
        self.rank = rank
        self.size = size
        self.bomb = bombs  # Adjust bomb count to match expected behavior
        self.data = self._create(rank, size)

    def _create(self, rank, size, counter=None):
        """Recursively creates a rank-N tensor with n-th number of bombs at random positions. It will replace the bombs with '100' """
        if counter is None:
            counter = [0]  

        if rank == 1:
            tensor = []
            for _ in range(size):
                if counter[0] < self.bomb and random.random() < self.bomb / (self.size ** self.rank):
                    tensor.append(100)  
                    counter[0] += 1
                else:
                    tensor.append(0)  
            return tensor
        else:
            return [self._create(rank - 1, size, counter) for _ in range(size)]

class TensorPrinter:
    """Handles labeled and formatted printing of tensors."""
    def __init__(self, tensor):
        self.tensor = tensor

    def _collect_matrices(self, subtensor, idx, matrices, indices):
        """Recursively collect all rank-2 matrices and their indices."""
        if isinstance(subtensor[0][0], list):
            for i, t in enumerate(subtensor):
                self._collect_matrices(t, idx + [i], matrices, indices)
        else:
            matrices.append(subtensor)
            indices.append(idx)

    def print_grid(self, per_line=4):
        """Displays matrices side-by-side in groups of `per_line`."""
        matrices, indices = [], []
        self._collect_matrices(self.tensor, [], matrices, indices)

        # Calculate max number width for clean alignment
        max_val = max(max(max(row) for row in mat) for mat in matrices)
        width = len(str(max_val)) + 1

        for block_start in range(0, len(matrices), per_line):
            block = matrices[block_start:block_start + per_line]
            block_indices = indices[block_start:block_start + per_line]

            # Header line
            header = " | ".join(f"T{''.join(f'[{i}]' for i in idx)}" for idx in block_indices)
            print(header)

            # Matrix rows
            for row_idx in range(len(block[0])):
                line = " | ".join(
                    " ".join(f"{val:{width}d}" for val in block[m][row_idx])
                    for m in range(len(block))
                )
                print(line)
            print("-" * (len(header) + width * len(block) * len(block[0])))