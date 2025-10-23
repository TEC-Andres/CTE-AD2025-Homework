import math
import tkinter as tk
from lib.tensor import Tensor
from lib.bombOperator import BombOperator

class ConnectTensor:
    """
    A placeholder class to represent connections to the Tensor functionality.
    This class can be expanded to manage interactions between the 4D tensor
    representation and the 3D visualization.
    """
    def __init__(self, tensor):
        self.tensor = Tensor(rank=4, size=4)

    def get_value_at(self, indices):
        """Retrieve the value from the tensor at the given 4D indices."""
        return self.tensor.get_value(indices)

    def set_value_at(self, indices, value):
        """Set the value in the tensor at the given 4D indices."""
        self.tensor.set_value(indices, value)

class Minesweeper3DGrid:
    """
    Represents a 3D grid of cubes for the 4D Minesweeper game.
    Each cube corresponds to a cell in the 4D grid projected into 3D space.
    """
    def __init__(self, i, j, k, spacing=10):
        self.i = i
        self.j = j
        self.k = k
        self.spacing = spacing

        # Generate grid of cube centers
        offset_x = (i - 1) * spacing / 2
        offset_y = (j - 1) * spacing / 2
        offset_z = (k - 1) * spacing / 2

        self.cube_centers = []
        for x in range(i):
            for y in range(j):
                for z in range(k):
                    cx = x * spacing - offset_x
                    cy = y * spacing - offset_y
                    cz = z * spacing - offset_z
                    self.cube_centers.append((cx, cy, cz))

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

        # Store canvas item ids for picking
        self._cube_items = []

    def draw_on_canvas(self, canvas3d):
        """Draw all cubes in the grid as solid (filled) cubes."""
        self._cube_items.clear()
        for idx, center in enumerate(self.cube_centers):
            self._draw_single_cube(canvas3d, idx, center)

    def _draw_single_cube(self, canvas3d, idx, center):
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

        # Draw all faces, but only bind to the front face for picking
        for order, (z, fidx) in enumerate(face_depths):
            face = self.cube_faces[fidx]
            poly = [pts[v] for v in face]
            item = canvas3d.canvas.create_polygon(
                poly,
                fill="#6cf",
                outline="#39a",
                width=1,
                stipple="gray50"
            )
            self._bind_cube_click(canvas3d, item, idx)
            self._cube_items.append(item)

    def _bind_cube_click(self, canvas3d, item, cube_idx):
        def callback(event):
            print(f"Cube {cube_idx} clicked!")
        canvas3d.canvas.tag_bind(item, "<Button-1>", callback)

class Interactive3DCanvas:
    """
    Lightweight 3D wireframe renderer on a Tkinter Canvas.

    - Renders a rotating cube you can interact with.
    - Drag with left mouse button to rotate (yaw/pitch).
    - Mouse wheel to zoom.
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
        self.zoom = 450.0  # focal length scaling (increased for more zoom)
        self.dist = 1.5    # camera distance from origin
        self.yaw = 0.7
        self.pitch = 0.5
        self._dragging = False
        self._last = (0, 0)

        # Create 3D grid
        self.grid = Minesweeper3DGrid(4, 4, 4, spacing=0.3)
        self.vertices = []
        self.edges = []

        # Bindings
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
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

    def _on_drag(self, event: tk.Event):
        if not self._dragging:
            return
        dx = event.x - self._last[0]
        dy = event.y - self._last[1]
        self._last = (event.x, event.y)
        self.yaw += dx * 0.01
        self.pitch += dy * 0.01
        self.pitch = max(min(self.pitch, math.pi / 2), -math.pi / 2)
        self.draw()

    def _on_release(self, event: tk.Event):
        self._dragging = False

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
        self.canvas.delete("all")
        self.grid.draw_on_canvas(self)

    def _schedule_animation(self):
        if not self._animate:
            return
        self.yaw += 0.003
        self.draw()
        self.canvas.after(33, self._schedule_animation)  # ~30 FPS


def gameWindowHandler(parent: tk.Widget, width: int | None = None, height: int | None = None) -> Interactive3DCanvas:
    """Create and attach the interactive 3D canvas to the given parent."""
    return Interactive3DCanvas(parent, width=width, height=height)
