import numpy as np

def bomb_preserve_values(A, kernel=None):
    """
    Bomb operator that:
      - treats any nonzero entry of A as a binary source (1)
      - convolves the binary source map with `kernel` to get local counts
      - preserves original nonzero entries in the output (they are NOT overwritten by counts)
    Parameters
    ----------
    A : array-like, shape (m,n) or any r-D
        Input tensor (numbers). Nonzero entries are treated as sources.
    kernel : ndarray or None
        r-D kernel of small integer weights. If None (default) uses the 3x3
        8-neighbour kernel with centre=0 (i.e. count of neighbour sources).
    Returns
    -------
    out : ndarray same shape as A
        Output with original nonzero values preserved and counts elsewhere.
    """
    A = np.asarray(A)
    if kernel is None:
        # default: 2D 3x3 kernel (all neighbours count; center = 0)
        kernel = np.array([[1,1,1],
                           [1,0,1],
                           [1,1,1]], dtype=int)

    kernel = np.asarray(kernel, dtype=int)
    # Only support same-rank kernel for now (common case: 2D image-like)
    if A.ndim != kernel.ndim:
        # allow passing a 2D kernel for 2D input only
        raise ValueError("Kernel dimensionality must match input dimensionality")

    # Build binary source map (1 where A != 0)
    sources = (A != 0).astype(int)

    # Compute 'same' convolution of sources with kernel using padding and sliding window
    pads = tuple((k//2, k//2) for k in kernel.shape)  # center anchor
    padded = np.pad(sources, pads, mode='constant', constant_values=0)
    out_counts = np.zeros_like(A, dtype=int)

    # iterate over all output positions and compute dot product with kernel
    # This is pure NumPy and works for any small kernel and tensor rank
    it = np.ndindex(*A.shape)
    for idx in it:
        # build slices to extract the neighborhood from padded
        slices = []
        for axis, i in enumerate(idx):
            start = i
            end = start + kernel.shape[axis]
            slices.append(slice(start, end))
        neighborhood = padded[tuple(slices)]
        out_counts[idx] = int(np.sum(neighborhood * kernel))

    # Compose final output: where A is nonzero keep A; otherwise put counts
    out = np.where(A != 0, A, out_counts).astype(int)
    return out

A = np.array([
    [0, 0, 100, 0,100],
    [0, 0, 0, 100, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

B = bomb_preserve_values(A)
print(B)

