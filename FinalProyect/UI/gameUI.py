import math
from math import hypot
import tkinter as tk
from lib import BombOperator, Tensor, BoundaryOperator
from assets import VAR

class TensorHandling:
    """
    A placeholder class to represent connections to the Tensor functionality.
    """
    def __init__(self):
        self.op = BombOperator()
        self.tensor = Tensor(rank=VAR.RANK, size=VAR.SIZE, bombs=VAR.BOMBS)
        self.solve = self.op.apply(self.tensor.data)

        print(f"Initialized Tensor of rank {VAR.RANK}, size {VAR.SIZE}, with {VAR.BOMBS} bombs.")

class Minesweeper3DGrid:
    """
    Represents a 3D grid of cubes for the 4D Minesweeper game.
    Each cube corresponds to a cell in the 4D grid projected into 3D space.
    """
    def __init__(self, i, j, k, spacing=10, solved_tensor=None):
        self.i = i
        self.j = j
        self.k = k
        self.spacing = spacing
        # We'll fix a=0 for the 3D view and map (x,y,z) -> (b,c,d)
        self.solved_tensor = solved_tensor
        self.primary_index = 0  # corresponds to first dimension: T[a][x][y][z]
        # Track revealed cubes per tensor slice a: {a: set(idx)}
        self._revealed_by_slice = {}
        # Track flagged cubes per tensor slice a: {a: set(idx)}
        self._flagged_by_slice = {}
        # Boundary operator for zero-region reveals
        self._boundary_op = BoundaryOperator()

        # Generate grid of cube centers
        offset_x = (i - 1) * spacing / 2
        offset_y = (j - 1) * spacing / 2
        offset_z = (k - 1) * spacing / 2

        self.cube_centers = []
        self.cube_indices = []
        for x in range(i):
            for y in range(j):
                for z in range(k):
                    cx = x * spacing - offset_x
                    cy = y * spacing - offset_y
                    cz = z * spacing - offset_z
                    self.cube_centers.append((cx, cy, cz))
                    self.cube_indices.append((x, y, z))

        # Fast coord->idx mapping for region reveals
        self._coord_to_idx = {coord: idx for idx, coord in enumerate(self.cube_indices)}

        # Each small cube's vertices (relative to center)
        s = spacing / 2 * 0.8
        self.cube_vertices = [
            (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s),
            (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s),
        ]
        # Faces as lists of vertex indices (for filled polygons)
        self.cube_faces = [
            [0, 1, 2, 3],  # back
            [4, 5, 6, 7],  # front
            [0, 1, 5, 4],  # bottom
            [2, 3, 7, 6],  # top
            [1, 2, 6, 5],  # right
            [0, 3, 7, 4],  # left
        ]

    # -------------------- Utility geometry --------------------
    @staticmethod
    def _convex_hull(points):
        """Monotone chain convex hull. points is list of (x,y). Returns hull in CCW order."""
        pts = sorted(set(points))
        if len(pts) <= 1:
            return pts
        def cross(o, a, b):
            return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
        lower = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        hull = lower[:-1] + upper[:-1]
        return hull

    @staticmethod
    def _point_in_poly(x, y, poly):
        """Ray-casting algorithm for point-in-polygon. poly is list of (x,y)."""
        inside = False
        n = len(poly)
        if n == 0:
            return False
        px, py = x, y
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            # check if edge straddles horizontal ray
            if ((y1 > py) != (y2 > py)):
                # compute x coordinate of intersection
                xinters = (x2 - x1) * (py - y1) / (y2 - y1 + 1e-12) + x1
                if px < xinters:
                    inside = not inside
        return inside

    # -------------------- Drawing & picking --------------------
    def draw_on_canvas(self, canvas3d):
        """Draw all cubes in the grid as solid (filled) cubes. Revealed cubes are not drawn."""
        # The Interactive3DCanvas maintains canvas3d._pick_regions.
        revealed_set = self._revealed_by_slice.get(self.primary_index, set())
        flagged_set = self._flagged_by_slice.get(self.primary_index, set())
        for idx, center in enumerate(self.cube_centers):
            is_revealed = idx in revealed_set
            is_flagged = idx in flagged_set
            self._draw_single_cube(canvas3d, idx, center, is_revealed, is_flagged)

    def _draw_single_cube(self, canvas3d, idx, center, is_revealed, is_flagged):
        # If revealed, draw only value text and skip faces
        if is_revealed:
            tv_center = canvas3d._rotate(center)
            px, py = canvas3d._project(tv_center)
            value = self._get_value_for_cube(idx)
            text = canvas3d.canvas.create_text(
                px, py,
                text=str(value),
                fill="#ffffff",
                font=("Segoe UI", 10, "bold")
            )
            # Lower so it doesn't block clicks to cubes behind
            canvas3d.canvas.tag_lower(text)
            return

        # Transform vertices to world position
        verts = [(vx + center[0], vy + center[1], vz + center[2]) for (vx, vy, vz) in self.cube_vertices]
        # Rotate and project
        tv = [canvas3d._rotate(v) for v in verts]
        pts = [canvas3d._project(v) for v in tv]

        # Draw faces (filled polygons)
        # Simple painter's algorithm: sort faces by average z (furthest first)
        face_depths = []
        for fidx, face in enumerate(self.cube_faces):
            avg_z = sum(tv[v][2] for v in face) / 4
            face_depths.append((avg_z, fidx))
        face_depths.sort()  # draw furthest first

        # Choose color for visible (not revealed) cube
        if is_flagged:
            # Yellow flagged cube
            fill_color = "#ffeb3b"
            outline_color = "#b58900"
            stipple = "gray25"
        else:
            fill_color = "#6cf"
            outline_color = "#39a"
            stipple = "gray12" 

        for order, (z, fidx) in enumerate(face_depths):
            face = self.cube_faces[fidx]
            poly = [pts[v] for v in face]
            kwargs = {
                'fill': fill_color,
                'outline': outline_color,
                'width': 1
            }
            if stipple:
                kwargs['stipple'] = stipple
            canvas3d.canvas.create_polygon(poly, **kwargs)

        # Build a convex pick polygon covering the projected cube (from all 8 vertices)
        hull = self._convex_hull(pts)  # pts are 2-tuples (x,y)
        # Compute average depth metric (use average camera z to estimate closeness)
        avg_tv_z = sum(vz for (_, _, vz) in tv) / len(tv)
        # Also compute average projection scale (approx closeness): average of f = zoom / (z_cam)
        z_cam_vals = [vz + canvas3d.dist for (_, _, vz) in tv]
        avg_f = sum((canvas3d.zoom / (zc if zc != 0 else 1e-6)) for zc in z_cam_vals) / len(z_cam_vals)

        # Append pick region: polygon, index, and depth metrics
        canvas3d._pick_regions.append({
            'idx': idx,
            'poly': hull,
            'avg_tv_z': avg_tv_z,
            'avg_f': avg_f,
        })

    def _get_value_for_cube(self, idx: int) -> int:
        """Get solved tensor value for cube at idx using mapping tensor[a][x][y][z]."""
        if self.solved_tensor is None:
            return 0
        x, y, z = self.cube_indices[idx]
        try:
            a = self.primary_index
            return int(self.solved_tensor[a][x][y][z])
        except Exception:
            return 0

    def _get_value_at(self, a: int, coord3: tuple[int, int, int]) -> int:
        if self.solved_tensor is None:
            return 0
        x, y, z = coord3
        try:
            return int(self.solved_tensor[a][x][y][z])
        except Exception:
            return 0

    def _is_bomb(self, val: int) -> bool:
        # In this project bombs are marked as value 100 in the tensor
        return val >= 100

    def set_primary_index(self, a: int):
        if self.solved_tensor is None:
            self.primary_index = 0
            return
        size_a = len(self.solved_tensor)
        if size_a <= 0:
            self.primary_index = 0
            return
        self.primary_index = max(0, min(a, size_a - 1))

    def reveal_cube(self, idx, canvas3d):
        """Reveal the cube with index idx and redraw the canvas."""
        revealed = self._revealed_by_slice.setdefault(self.primary_index, set())
        flagged = self._flagged_by_slice.setdefault(self.primary_index, set())
        # Do not reveal flagged cubes
        if idx in flagged:
            return False
        if idx in revealed:
            return False
        revealed.add(idx)
        # Debug/info: report tensor position and value
        try:
            x, y, z = self.cube_indices[idx]
            val = self._get_value_for_cube(idx)
            print(f"Reveal -> Tensor[{self.primary_index}][{x}][{y}][{z}] = {val}")
        except Exception:
            pass
        canvas3d.draw()
        print(f"Revealed cube at index: {idx}")
        return True

    def reveal_zero_region_from(self, idx: int, canvas3d) -> int:
        """Reveal the contiguous zero region (and its numeric boundary) starting from idx."""
        a = self.primary_index
        start_coord = self.cube_indices[idx]
        zeros, boundary = self._boundary_op.compute_zero_region(self.solved_tensor, a, start_coord)
        # Filter: never reveal bombs in boundary
        filtered_boundary = {c for c in boundary if not self._is_bomb(self._get_value_at(a, c))}
        to_reveal_coords = zeros | filtered_boundary

        revealed = self._revealed_by_slice.setdefault(a, set())
        flagged = self._flagged_by_slice.setdefault(a, set())

        revealed_count = 0
        for coord in to_reveal_coords:
            ridx = self._coord_to_idx.get(coord)
            if ridx is None:
                continue
            if ridx in flagged or ridx in revealed:
                continue
            revealed.add(ridx)
            revealed_count += 1

        if revealed_count > 0:
            canvas3d.draw()
        print(f"Region reveal starting at {start_coord}: zeros={len(zeros)} boundary={len(boundary)} total={revealed_count}")
        return revealed_count

    def reveal_zero_region_all_from(self, idx: int, canvas3d) -> int:
        """Reveal the contiguous zero region across the entire tensor (all 'a' slices)."""
        a0 = self.primary_index
        start3 = self.cube_indices[idx]
        start_nd = (a0, *start3)
        zerosN, boundaryN = self._boundary_op.compute_zero_region_all(self.solved_tensor, start_nd)

        # Partition by 'a' and filter bombs from boundary
        revealed_total = 0
        for coord in zerosN | boundaryN:
            if len(coord) != 4:
                continue
            a, x, y, z = coord
            val = self._get_value_at(a, (x, y, z))
            # Reveal zeros and numeric boundary only (exclude bombs)
            if val != 0 and self._is_bomb(val):
                continue
            ridx = self._coord_to_idx.get((x, y, z))
            if ridx is None:
                continue
            revealed = self._revealed_by_slice.setdefault(a, set())
            flagged = self._flagged_by_slice.setdefault(a, set())
            if ridx in flagged or ridx in revealed:
                continue
            revealed.add(ridx)
            revealed_total += 1

        if revealed_total > 0:
            canvas3d.draw()
        print(f"ND region reveal from {start_nd}: zeros={len(zerosN)} boundary={len(boundaryN)} total={revealed_total}")
        return revealed_total

    def toggle_flag(self, idx, canvas3d):
        """Toggle flagged state for the given cube in the current tensor slice."""
        # Can't flag revealed cubes
        revealed = self._revealed_by_slice.setdefault(self.primary_index, set())
        if idx in revealed:
            return False
        flagged = self._flagged_by_slice.setdefault(self.primary_index, set())
        if idx in flagged:
            flagged.remove(idx)
            print(f"Unflagged cube at index: {idx} (slice {self.primary_index})")
        else:
            flagged.add(idx)
            print(f"Flagged cube at index: {idx} (slice {self.primary_index})")
        canvas3d.draw()
        return True

class Interactive3DCanvas:
    """
    Lightweight 3D wireframe renderer on a Tkinter Canvas with robust picking.
    """

    def __init__(self, parent: tk.Widget, width: int | None = None, height: int | None = None, bg: str = "#101214"):
        self.parent = parent
        self.canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        if width and height:
            self.canvas.config(width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Scene state
        self.cx = 0
        self.cy = 0
        self.zoom = 450.0  # focal length scaling
        self.dist = 1.5    # camera distance from origin
        self.yaw = 0.7
        self.pitch = 0.5
        self._dragging = False
        self._last = (0, 0)
        self._press_pos = (0, 0)

        # Prepare solved tensor and create 3D grid
        th = TensorHandling()
        solved = th.solve
        self.grid = Minesweeper3DGrid(VAR.SIZE, VAR.SIZE, VAR.SIZE, spacing=0.3, solved_tensor=solved)

        # Pick regions populated each frame: list of dicts {idx, poly, avg_f, ...}
        self._pick_regions = []

        # Bindings
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<ButtonPress-3>", self._on_right_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<MouseWheel>", self._on_wheel)  # Windows/macOS
        self.canvas.bind("<Button-4>", lambda e: self._zoom(+120))  # Linux up
        self.canvas.bind("<Button-5>", lambda e: self._zoom(-120))  # Linux down

        # Initial layout and draw
        self._on_resize()
        self.draw()

        # Gentle idle animation
        self._animate = True
        self._schedule_animation()

    # --------------------------- Public API ---------------------------
    def rotate_tensor_index(self):
        """Advance the primary tensor index a -> (a+1) mod N and redraw."""
        if self.grid.solved_tensor is None:
            return 0
        n = len(self.grid.solved_tensor)
        self.grid.set_primary_index((self.grid.primary_index + 1) % n)
        self.draw()
        return self.grid.primary_index

    def get_tensor_index(self) -> int:
        return getattr(self.grid, 'primary_index', 0)

    # ---------------------------- Interaction ----------------------------
    def _on_resize(self, event: tk.Event | None = None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.cx = w // 2
        self.cy = h // 2
        self.draw()

    def _on_press(self, event: tk.Event):
        self._dragging = True
        self._last = (event.x, event.y)
        self._press_pos = (event.x, event.y)

    def _on_drag(self, event: tk.Event):
        if not self._dragging:
            return
        dx = event.x - self._last[0]
        dy = event.y - self._last[1]
        self._last = (event.x, event.y)
        # If the mouse moved more than a pixel, it's a drag that should rotate
        if abs(dx) > 0 or abs(dy) > 0:
            self.yaw += dx * 0.01
            self.pitch += dy * 0.01
            self.pitch = max(min(self.pitch, math.pi / 2), -math.pi / 2)
            self.draw()

    def _on_release(self, event: tk.Event):
        # Determine whether this was a click (press+release w/o significant movement)
        press_x, press_y = self._press_pos
        dist = hypot(event.x - press_x, event.y - press_y)
        CLICK_THRESHOLD = 6  # pixels
        self._dragging = False
        if dist <= CLICK_THRESHOLD:
            # Treat as click: pick cube (if any)
            self._handle_click(event.x, event.y)

    def _on_wheel(self, event: tk.Event):
        self._zoom(event.delta)

    def _zoom(self, delta: int):
        factor = 1.0 + (delta / 1200.0)
        new_zoom = self.zoom * factor
        self.zoom = max(80.0, min(1200.0, new_zoom))
        self.draw()

    # ----------------------------- Rendering -----------------------------
    def _rotate(self, v):
        x, y, z = v
        cy = math.cos(self.yaw)
        sy = math.sin(self.yaw)
        xz = (cy * x + sy * z, y, -sy * x + cy * z)
        x2, y2, z2 = xz
        cp = math.cos(self.pitch)
        sp = math.sin(self.pitch)
        return (x2, cp * y2 - sp * z2, sp * y2 + cp * z2)

    def _project(self, v):
        x, y, z = v
        z_cam = z + self.dist
        if z_cam == 0:
            z_cam = 1e-6
        f = self.zoom / z_cam
        return (self.cx + x * f, self.cy + y * f)

    def draw(self):
        # Clear canvas and recompute pick regions
        self.canvas.delete("all")
        self._pick_regions = []
        self.grid.draw_on_canvas(self)

    def _schedule_animation(self):
        if not self._animate:
            return
        self.yaw += 0.003
        self.draw()
        self.canvas.after(33, self._schedule_animation)  # ~30 FPS

    # ----------------------------- Picking -----------------------------
    def _handle_click(self, x, y):
        # Gather candidates whose polygon contains (x,y)
        candidates = []
        for pr in self._pick_regions:
            if Minesweeper3DGrid._point_in_poly(x, y, pr['poly']):
                candidates.append(pr)
        if not candidates:
            return  # clicked empty space

        # Choose the candidate with maximum avg_f (closest to camera roughly)
        best = max(candidates, key=lambda p: p.get('avg_f', 0))
        chosen_idx = best['idx']
        # If it's a zero, reveal the whole zero-region across all slices; else reveal single
        val = self.grid._get_value_for_cube(chosen_idx)
        if val == 0:
            # Reveal region across all dimensions
            revealed = self.grid.reveal_zero_region_all_from(chosen_idx, self)
            if revealed == 0:
                self.grid.reveal_cube(chosen_idx, self)
        else:
            self.grid.reveal_cube(chosen_idx, self)

    def _on_right_click(self, event: tk.Event):
        # Immediate flag toggle on right click
        x, y = event.x, event.y
        candidates = []
        for pr in self._pick_regions:
            if Minesweeper3DGrid._point_in_poly(x, y, pr['poly']):
                candidates.append(pr)
        if not candidates:
            return
        best = max(candidates, key=lambda p: p.get('avg_f', 0))
        chosen_idx = best['idx']
        self.grid.toggle_flag(chosen_idx, self)

def gameWindowHandler(parent: tk.Widget, width: int | None = None, height: int | None = None) -> Interactive3DCanvas:
    """Create and attach the interactive 3D canvas to the given parent."""
    return Interactive3DCanvas(parent, width=width, height=height)
