import math
import tkinter as tk


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
		self.zoom = 300.0  # focal length scaling
		self.dist = 3.5    # camera distance from origin
		self.yaw = 0.7
		self.pitch = -0.5
		self._dragging = False
		self._last = (0, 0)

		# Cube geometry
		s = 1.0
		self.vertices = [
			(-s, -s, -s), ( s, -s, -s), ( s,  s, -s), (-s,  s, -s),
			(-s, -s,  s), ( s, -s,  s), ( s,  s,  s), (-s,  s,  s),
		]
		self.edges = [
			(0, 1), (1, 2), (2, 3), (3, 0),  # back face
			(4, 5), (5, 6), (6, 7), (7, 4),  # front face
			(0, 4), (1, 5), (2, 6), (3, 7),  # connectors
		]

		# Bindings
		self.canvas.bind("<Configure>", self._on_resize)
		self.canvas.bind("<ButtonPress-1>", self._on_press)
		self.canvas.bind("<B1-Motion>", self._on_drag)
		self.canvas.bind("<ButtonRelease-1>", self._on_release)
		self.canvas.bind("<MouseWheel>", self._on_wheel)  # Windows/macOS
		# Optional: Linux wheel events (not required on Windows)
		self.canvas.bind("<Button-4>", lambda e: self._zoom(+120))
		self.canvas.bind("<Button-5>", lambda e: self._zoom(-120))

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
		# keep zoom sensible relative to size
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
		# Sensitivity factors
		self.yaw += dx * 0.01
		self.pitch += dy * 0.01
		# Clamp pitch to avoid flipping singularities
		self.pitch = max(min(self.pitch, math.pi / 2), -math.pi / 2)
		self.draw()

	def _on_release(self, event: tk.Event):
		self._dragging = False

	def _on_wheel(self, event: tk.Event):
		self._zoom(event.delta)

	def _zoom(self, delta: int):
		# Windows delta multiples of 120
		factor = 1.0 + (delta / 1200.0)
		# Limit zoom range
		new_zoom = self.zoom * factor
		self.zoom = max(80.0, min(1200.0, new_zoom))
		self.draw()

	# ----------------------------- Rendering -----------------------------
	def _rotate(self, v):
		x, y, z = v
		# Yaw (around Y)
		cy = math.cos(self.yaw)
		sy = math.sin(self.yaw)
		xz = (cy * x + sy * z, y, -sy * x + cy * z)
		# Pitch (around X)
		x2, y2, z2 = xz
		cp = math.cos(self.pitch)
		sp = math.sin(self.pitch)
		return (x2, cp * y2 - sp * z2, sp * y2 + cp * z2)

	def _project(self, v):
		x, y, z = v
		# Simple perspective projection with camera at (0,0,-dist)
		z_cam = z + self.dist
		if z_cam == 0:
			z_cam = 1e-6
		f = self.zoom / z_cam
		return (self.cx + x * f, self.cy + y * f)

	def draw(self):
		self.canvas.delete("all")
		# Transform all vertices
		tv = [self._rotate(v) for v in self.vertices]
		pts = [self._project(v) for v in tv]

		# Depth sort edges for a pleasant look (optional)
		def edge_depth(e):
			a, b = e
			return (tv[a][2] + tv[b][2]) / 2.0

		for a, b in sorted(self.edges, key=edge_depth):
			x1, y1 = pts[a]
			x2, y2 = pts[b]
			self.canvas.create_line(x1, y1, x2, y2, fill="#e6edf3", width=2)

	def _schedule_animation(self):
		if not self._animate:
			return
		# Subtle idle spin
		self.yaw += 0.01
		self.draw()
		self.canvas.after(33, self._schedule_animation)  # ~30 FPS


def gameWindowHandler(parent: tk.Widget, width: int | None = None, height: int | None = None) -> Interactive3DCanvas:
	"""Create and attach the interactive 3D canvas to the given parent.

	Args:
		parent: Tkinter container (Frame) where the canvas should live.
		width: Optional initial width.
		height: Optional initial height.

	Returns:
		The Interactive3DCanvas instance (access .canvas if you need the widget).
	"""
	return Interactive3DCanvas(parent, width=width, height=height)

