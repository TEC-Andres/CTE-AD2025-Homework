import tkinter as tk
import tkinter.ttk as ttk
import os
from lib.UI.UI import GameUI

assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
icon_path = os.path.join(assets_dir, 'logo.ico')
splash_image_path = os.path.join(assets_dir, 'banner.png')

class Initializer:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()         
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        self.logo_img = tk.PhotoImage(file=splash_image_path)
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
        """Destroys the splash screen and launches the main app."""
        self.splash.destroy()
        App(self.root)
        self.root.deiconify()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("4D Minesweeper")
        self.root.overrideredirect(False)
        self.root.state('zoomed')
        self.set_window_icon()
        self.game_ui = GameUI(self.root)

    def set_window_icon(self):
        try:
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print(f"Icon not found at: {icon_path}")


if __name__ == "__main__":
    root = tk.Tk()
    initializer = Initializer(root) 
    root.mainloop()