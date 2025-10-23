import numpy as np

def bomb_preserve_values(A, kernel=None):
    """
    Bomb operator generalized for any n-dimensional tensor.
    Nonzero entries are treated as sources; output preserves original nonzero values,
    and elsewhere shows the count of nonzero neighbors (as defined by the kernel).
    """
    A = np.asarray(A)
    ndim = A.ndim

    if kernel is None:
        # Create a default kernel: all ones, center zero
        kernel_shape = tuple([3] * ndim)
        kernel = np.ones(kernel_shape, dtype=int)
        center = tuple([1] * ndim)
        kernel[center] = 0

    kernel = np.asarray(kernel, dtype=int)
    if kernel.ndim != ndim:
        raise ValueError("Kernel dimensionality must match input dimensionality")

    sources = (A != 0).astype(int)
    pads = tuple((k//2, k//2) for k in kernel.shape)
    padded = np.pad(sources, pads, mode='constant', constant_values=0)
    out_counts = np.zeros_like(A, dtype=int)

    # Iterate over all output positions and compute dot product with kernel
    it = np.ndindex(*A.shape)
    for idx in it:
        slices = tuple(slice(i, i + k) for i, k in zip(idx, kernel.shape))
        neighborhood = padded[slices]
        out_counts[idx] = int(np.sum(neighborhood * kernel))

    out = np.where(A != 0, A, out_counts).astype(int)
    return out

# Example for 3D tensor
TENSOR = np.array([
    [
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ]
    ],
    [
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 0, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ]
    ],
    [
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 100, 100, 100, 0],
            [0, 0, 0, 0, 0]
        ]
    ]
])

print("Antes\n")

for i in range(TENSOR.shape[0]):
    # Print block headers
    headers = [f"Block ({i},{j})" for j in range(TENSOR.shape[1])]
    print("   ".join(h.ljust(25) for h in headers))
    # Print each row of all blocks in this slice
    for k in range(TENSOR.shape[2]):
        row_strs = []
        for j in range(TENSOR.shape[1]):
            row = TENSOR[i, j, k]
            row_strs.append("[" + " ".join("{:3d}".format(x) for x in row) + "]")
        print("   ".join(r.ljust(25) for r in row_strs))
    print()  # Separate blocks by a blank line


print("Despuñes\n")
B = bomb_preserve_values(TENSOR)
# Pretty print B in the requested format
for i in range(B.shape[0]):
    # Print block headers
    headers = [f"Block ({i},{j})" for j in range(B.shape[1])]
    print("   ".join(h.ljust(25) for h in headers))
    # Print each row of all blocks in this slice
    for k in range(B.shape[2]):
        row_strs = []
        for j in range(B.shape[1]):
            row = B[i, j, k]
            row_strs.append("[" + " ".join("{:3d}".format(x) for x in row) + "]")
        print("   ".join(r.ljust(25) for r in row_strs))
    print()  # Separate blocks by a blank line
