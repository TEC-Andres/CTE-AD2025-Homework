import tkinter as tk
import tkinter.ttk as ttk
from assets import * 
from UI.app import *

class Initializer:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()         
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        self.logo_img = tk.PhotoImage(file=png.banner)
        splash_width = self.logo_img.width()
        splash_height = self.logo_img.height()
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (splash_width // 2)
        y = (screen_height // 2) - (splash_height // 2)
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        label = tk.Label(self.splash, image=self.logo_img)
        label.image = self.logo_img 
        label.pack()

        self.splash.after(2000, self.close_splash)

    def close_splash(self):
        """Destroys the splash screen and launches the main app with menu."""
        self.splash.destroy()
        # Ensure the main window is visible before initializing the app
        self.root.deiconify()
        Menu(self.root)

class Menu(App):
    def __init__(self, root):
        super().__init__(root)