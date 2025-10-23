import tkinter as tk
import tkinter.ttk as ttk

class SidebarControls(ttk.Frame):
    """
    Sidebar controls for rotating the primary tensor index (first dimension a in T[a][x][y][z]).
    """
    def __init__(self, parent: tk.Widget, game_view, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.game_view = game_view

        # Title/label
        self.title = ttk.Label(self, text="Tensor Slice", font=("Segoe UI", 11, "bold"))
        self.title.pack(padx=8, pady=(8,2))

        # Current index display
        self.index_var = tk.StringVar(value=self._format_label())
        self.index_label = ttk.Label(self, textvariable=self.index_var)
        self.index_label.pack(padx=8, pady=(0,8))

        # Rotate button
        self.rotate_btn = ttk.Button(self, text="Next T[n]", command=self._on_rotate)
        self.rotate_btn.pack(padx=8, pady=8, fill="x")

        # Attach to parent
        self.pack(fill="x", padx=8, pady=8)

    def _format_label(self):
        try:
            idx = self.game_view.get_tensor_index()
            return f"Current: T[{idx}]"
        except Exception:
            return "Current: T[0]"

    def _on_rotate(self):
        try:
            idx = self.game_view.rotate_tensor_index()
            self.index_var.set(f"Current: T[{idx}]")
        except Exception:
            # Fallback: update label anyway
            self.index_var.set(self._format_label())
