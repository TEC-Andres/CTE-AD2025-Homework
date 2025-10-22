import tkinter as tk
import tkinter.ttk as ttk
from assets import * 
from lib import *
from UI.gameUI import gameWindowHandler

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("4D Minesweeper")
        self.root.overrideredirect(False)
        self.root.state('zoomed')
        self.set_window_icon()
        self.build_layout()

    def set_window_icon(self):
        try:
            self.root.iconbitmap(icon.path)
        except tk.TclError:
            print(f"Icon not found at: {icon.path}")

    def build_layout(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=6)
        self.root.columnconfigure(1, weight=1)

        # Pseudowindow (game area)
        self.game_area = ttk.Frame(self.root)
        self.game_area.grid(row=0, column=0, sticky="nsew")

        # Sidebar (controls / future UI)
        self.sidebar = ttk.Frame(self.root)
        self.sidebar.grid(row=0, column=1, sticky="nsew")

        # Optional placeholder content on sidebar
        lbl = ttk.Label(self.sidebar, text="Controls / Info", anchor="center")
        lbl.pack(padx=12, pady=12)

        self.game_view = gameWindowHandler(self.game_area)
