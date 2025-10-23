from typing import Any, List, Sequence, Tuple

class BombOperator:
    """Apply the bomb operator to n-D nested list tensors without NumPy.

    Usage:
        op = BombOperator()
        result = op.apply(A)                 # default 3^n kernel
        result = op.apply(A, custom_kernel)  # with custom kernel
    """

    # ----------------------------- Public API ----------------------------- #
    def apply(self, A: Any, kernel: Any | None = None) -> Any:
        """Apply the bomb operator.

        Args:
            A: n-D rectangular nested list (tensor) of numbers.
            kernel: Optional n-D nested list of integer weights. Must have the
                    same number of dimensions as A. If None, a default kernel
                    of shape (3,)*ndim with a zero center is used.

        Returns:
            A new nested list of ints with the same shape as A.
        """
        shape = self._get_shape(A)
        ndim = len(shape)
        if ndim == 0:
            # Scalar edge case: just return the scalar untouched.
            return A

        if kernel is None:
            kernel_shape = (3,) * ndim
            kernel = self._make_default_kernel(kernel_shape)
        else:
            kernel_shape = self._get_shape(kernel)
            if len(kernel_shape) != ndim:
                raise ValueError(
                    "Kernel dimensionality must match input dimensionality"
                )

        # Convert A into a binary sources tensor (1 where non-zero, else 0)
        sources = self._map_like(A, lambda v: 0 if v == 0 else 1)

        # Preprocess kernel into list of (offset, weight) excluding zero weights.
        offsets = self._kernel_offsets(kernel)

        # Compute neighbor counts using the sources tensor.
        counts = self._zeros(shape)
        for idx in self._iterate_indices(shape):
            total = 0
            for rel_off, weight in offsets:
                # Compute neighbor index
                nbr = tuple(i + d for i, d in zip(idx, rel_off))
                if self._in_bounds(nbr, shape):
                    val = self._get_item(sources, nbr)
                    if val:  # micro optimization: skip multiply if zero
                        total += weight * val
            self._set_item(counts, idx, int(total))

        # Merge: preserve original non-zero values.
        result = self._map_two(A, counts, lambda orig, cnt: int(orig) if orig != 0 else cnt)
        return result

    # -------------------------- Kernel Construction ----------------------- #
    def _make_default_kernel(self, shape: Sequence[int]):
        kernel = self._zeros(shape)
        # Fill with ones and set center to zero.
        for idx in self._iterate_indices(shape):
            self._set_item(kernel, idx, 1)
        center = tuple(s // 2 for s in shape)
        self._set_item(kernel, center, 0)
        return kernel

    def _kernel_offsets(self, kernel: Any) -> List[Tuple[Tuple[int, ...], int]]:
        shape = self._get_shape(kernel)
        center = tuple(s // 2 for s in shape)
        offsets: List[Tuple[Tuple[int, ...], int]] = []
        for idx in self._iterate_indices(shape):
            weight = self._get_item(kernel, idx)
            if weight == 0:
                continue
            rel = tuple(i - c for i, c in zip(idx, center))
            offsets.append((rel, int(weight)))
        return offsets

    # ----------------------------- Tensor Utils --------------------------- #
    def _get_shape(self, tensor: Any) -> Tuple[int, ...]:
        shape: List[int] = []
        self._accumulate_shape(tensor, shape, level=0)
        return tuple(shape)

    def _accumulate_shape(self, tensor: Any, shape: List[int], level: int):
        if isinstance(tensor, list):
            length = len(tensor)
            if level >= len(shape):
                shape.append(length)
            else:
                if shape[level] != length:
                    raise ValueError("Tensor is not rectangular (ragged list) at level {}".format(level))
            for item in tensor:
                self._accumulate_shape(item, shape, level + 1)
        else:
            # Reached scalar; ensure deeper levels don't claim further dims.
            return

    def _zeros(self, shape: Sequence[int]) -> Any:
        if not shape:
            return 0
        first, *rest = shape
        return [self._zeros(rest) for _ in range(first)]

    def _iterate_indices(self, shape: Sequence[int]):
        if not shape:
            yield ()
            return
        # Iterative Cartesian product to avoid recursion overhead.
        ranges = [range(s) for s in shape]
        def rec(pos: int, prefix: List[int]):
            if pos == len(ranges):
                yield tuple(prefix)
                return
            for v in ranges[pos]:
                prefix.append(v)
                yield from rec(pos + 1, prefix)
                prefix.pop()
        yield from rec(0, [])

    def _get_item(self, tensor: Any, idx: Tuple[int, ...]):
        ref = tensor
        for i in idx:
            ref = ref[i]
        return ref

    def _set_item(self, tensor: Any, idx: Tuple[int, ...], value: Any):
        ref = tensor
        for i in idx[:-1]:
            ref = ref[i]
        ref[idx[-1]] = value

    def _in_bounds(self, idx: Tuple[int, ...], shape: Sequence[int]) -> bool:
        return all(0 <= i < s for i, s in zip(idx, shape))

    def _map_like(self, tensor: Any, fn):
        if isinstance(tensor, list):
            return [self._map_like(x, fn) for x in tensor]
        return fn(tensor)

    def _map_two(self, A: Any, B: Any, fn):
        if isinstance(A, list):
            return [self._map_two(a, b, fn) for a, b in zip(A, B)]
        return fn(A, B)    