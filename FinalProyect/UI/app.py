import tkinter as tk
import tkinter.ttk as ttk
from assets import * 
from lib import *
from UI.gameUI import gameWindowHandler
from UI.sidebar import SidebarControls
from assets._globalVariables import GlobalVars
import random

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("4D Minesweeper")
        self.root.overrideredirect(False)
        self.root.state('zoomed')
        self.set_window_icon()
        self.build_layout()
        self.menu()

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
        self.sidebar = ttk.Frame(self.root)
        self.sidebar.grid(row=0, column=1, sticky="nsew")
        self.game_view = gameWindowHandler(self.game_area)

        # Sidebar controls hooked to the game view
        SidebarControls(self.sidebar, self.game_view)

    def menu(self):
        # Create a background overlay to simulate modal behavior
        bg_image = tk.PhotoImage(file=png.blurGame)
        overlay = tk.Label(self.game_area, image=bg_image)
        overlay.image = bg_image  # Keep a reference to avoid garbage collection
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create the pseudo-window (menu)
        menu_frame = ttk.Frame(
            overlay,
            padding=30,
            relief="raised",
            borderwidth=3
        )
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ttk.Label(menu_frame, text="Choose Board Size:", font=("Arial", 16))
        label.pack(pady=(0, 15))

        # Seed entry
        seed_label = ttk.Label(menu_frame, text="Seed (optional):", font=("Arial", 12))
        seed_label.pack(pady=(0, 5))
        seed_var = tk.StringVar()
        seed_entry = ttk.Entry(menu_frame, textvariable=seed_var)
        seed_entry.pack(pady=(0, 15))

        def start_game(size):
            # Destroy the pseudowindow
            overlay.destroy()
            # Set bomb count, size, and seed in VAR (the singleton used by the game)
            from assets import VAR
            VAR.SIZE = size
            VAR.BOMBS = {3: 5, 4: 10, 5: 15}.get(size, 0)
            user_seed = seed_var.get()
            if user_seed.strip() == "":
                VAR.SEED = random.randint(0, 2**32 - 1)
            else:
                try:
                    VAR.SEED = int(user_seed)
                except ValueError:
                    VAR.SEED = hash(user_seed)
            # Restart the game with new parameters
            self.game_view.new_game(size, VAR.BOMBS)

        # Buttons
        for size in [3, 4, 5]:
            btn = ttk.Button(menu_frame, text=f"{size} × {size}", command=lambda s=size: start_game(s))
            btn.pack(fill="x", padx=40, pady=5)
