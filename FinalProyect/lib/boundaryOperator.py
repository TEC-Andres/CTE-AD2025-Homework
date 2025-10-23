from collections import deque
from itertools import product
from typing import Iterable, List, Sequence, Set, Tuple


Coord3D = Tuple[int, int, int]


class BoundaryOperator:
	"""
	Compute the "zero region" in an n-D tensor (Minesweeper-style), with a
	compatibility helper for 3D slices.

	Given a solved tensor where bombs are non-zero (e.g., 100) and empty cells are 0,
	this operator performs a flood-fill starting at a coordinate (x, y, z) on the
	selected primary index (a) and returns two sets of coordinates:

	- zeros: all contiguous zero-valued cells reachable from the start (using 3^N-1 neighbor adjacency)
	- boundary: all non-zero neighbors that are adjacent to any cell in zeros

	Typical usage is to reveal all coordinates in `zeros ∪ boundary` when the user
	clicks a zero cell, which mirrors classic Minesweeper behavior.
	"""

	# ----------------------------- Public API ----------------------------- #
	def compute_zero_region(
		self,
		solved_tensor: Sequence,  # Can be the full N-D tensor
		primary_index: int,
		start: Coord3D,
	) -> Tuple[Set[Coord3D], Set[Coord3D]]:
		"""
		Backward-compatible helper: perform a flood-fill from `start` within the
		3D slice `solved_tensor[primary_index]`.

		Returns:
			(zeros, boundary) as 3D coordinates relative to that slice.
		"""
		# Extract 3D slice T[a]
		try:
			slice3d = solved_tensor[primary_index]
		except Exception:
			return set(), set()

		shape = self._shape3d(slice3d)
		if shape is None:
			return set(), set()
		sx, sy, sz = shape

		x0, y0, z0 = start
		if not (0 <= x0 < sx and 0 <= y0 < sy and 0 <= z0 < sz):
			return set(), set()

		if self._get3(slice3d, x0, y0, z0) != 0:
			return set(), set()

		zeros: Set[Coord3D] = set()
		boundary: Set[Coord3D] = set()

		q: deque[Coord3D] = deque()
		q.append((x0, y0, z0))
		zeros.add((x0, y0, z0))

		neighbors3 = self._neighbor_offsets_nd(3)  # 26 neighbors

		while q:
			x, y, z = q.popleft()
			for dx, dy, dz in neighbors3:
				nx, ny, nz = x + dx, y + dy, z + dz
				if not (0 <= nx < sx and 0 <= ny < sy and 0 <= nz < sz):
					continue
				val = self._get3(slice3d, nx, ny, nz)
				if val == 0:
					if (nx, ny, nz) not in zeros:
						zeros.add((nx, ny, nz))
						q.append((nx, ny, nz))
				else:
					boundary.add((nx, ny, nz))

		return zeros, boundary

	def compute_zero_region_all(
		self,
		tensor: Sequence,
		start: Tuple[int, ...],
	) -> Tuple[Set[Tuple[int, ...]], Set[Tuple[int, ...]]]:
		"""
		Perform a flood-fill across the entire N-D tensor starting at `start`.
		Uses 3^N - 1 neighbor connectivity.

		Returns:
			(zeros, boundary) as N-D coordinate tuples.
		"""
		shape = self._shape_nd(tensor)
		if shape is None:
			return set(), set()
		ndim = len(shape)
		if len(start) != ndim:
			return set(), set()

		if not self._in_bounds_nd(start, shape):
			return set(), set()
		if self._get_nd(tensor, start) != 0:
			return set(), set()

		zeros: Set[Tuple[int, ...]] = set()
		boundary: Set[Tuple[int, ...]] = set()
		q: deque[Tuple[int, ...]] = deque()
		q.append(start)
		zeros.add(start)

		neighbors = self._neighbor_offsets_nd(ndim)

		while q:
			idx = q.popleft()
			for off in neighbors:
				nbr = tuple(i + d for i, d in zip(idx, off))
				if not self._in_bounds_nd(nbr, shape):
					continue
				val = self._get_nd(tensor, nbr)
				if val == 0:
					if nbr not in zeros:
						zeros.add(nbr)
						q.append(nbr)
				else:
					boundary.add(nbr)

		return zeros, boundary

	# --------------------------- Helper methods -------------------------- #
	def _shape3d(self, arr) -> Tuple[int, int, int] | None:
		try:
			sx = len(arr)
			sy = len(arr[0])
			sz = len(arr[0][0])
			return sx, sy, sz
		except Exception:
			return None

	def _get3(self, arr, x: int, y: int, z: int) -> int:
		return int(arr[x][y][z])

	def _shape_nd(self, tensor) -> Tuple[int, ...] | None:
		# Determine shape of nested lists, assuming rectangular structure
		shape: List[int] = []
		cur = tensor
		try:
			while isinstance(cur, list):
				shape.append(len(cur))
				if len(cur) == 0:
					break
				cur = cur[0]
			return tuple(shape)
		except Exception:
			return None

	def _in_bounds_nd(self, idx: Tuple[int, ...], shape: Sequence[int]) -> bool:
		return all(0 <= i < s for i, s in zip(idx, shape))

	def _get_nd(self, tensor, idx: Tuple[int, ...]) -> int:
		ref = tensor
		for i in idx:
			ref = ref[i]
		return int(ref)

	def _neighbor_offsets_nd(self, ndim: int) -> List[Tuple[int, ...]]:
		# All combinations in {-1,0,1}^ndim except the all-zero vector
		offs = [t for t in product((-1, 0, 1), repeat=ndim) if any(x != 0 for x in t)]
		return offs

