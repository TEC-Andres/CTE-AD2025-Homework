import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
from typing import Any, List, Sequence, Tuple
from ..tensorTest import Tensor, BombOperator

class GameUI:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill='both')

        # Create styles
        self.create_styles()

        # Game settings
        self.dimensions = [4, 4, 4, 4]  # 4D grid dimensions
        self.current_w = 0  # Current W dimension
        self.buttons = {}  # Store buttons for easy access
        self.game_over = False
        self.revealed_cells = set()
        self.review_mode = False
        self.safe_moves = set()  # Store known safe moves

        # Initialize game state
        self.tensor = Tensor(4, 4)  # 4D tensor with bombs
        self.bomb_op = BombOperator()
        self.setup_ui()
        self.start_game()

    def create_styles(self):
        # Create custom styles for buttons
        style = ttk.Style()

        # Normal button style
        style.configure('Cell.TButton',
                       padding=5,
                       width=3,
                       font=('Arial', 10, 'bold'))

        # Revealed cell style
        style.configure('Revealed.TButton',
                       background='#e0e0e0',
                       foreground='blue',
                       font=('Arial', 10, 'bold'))

        # Bomb cell style
        style.configure('Bomb.TButton',
                       background='#ff8080',
                       foreground='red',
                       font=('Arial', 10, 'bold'))

    def setup_ui(self):
        # Top control panel
        self.control_panel = ttk.Frame(self.frame)
        self.control_panel.pack(fill='x', padx=10, pady=5)

        # W dimension navigation
        self.w_label = ttk.Label(self.control_panel, text="W Dimension:")
        self.w_label.pack(side='left', padx=5)

        self.prev_w = ttk.Button(self.control_panel, text="◄", command=self.previous_w)
        self.prev_w.pack(side='left')

        self.w_value = ttk.Label(self.control_panel, text=f"Level {self.current_w}")
        self.w_value.pack(side='left', padx=10)

        self.next_w = ttk.Button(self.control_panel, text="►", command=self.next_w)
        self.next_w.pack(side='left')

        # Game statistics
        self.stats_frame = ttk.LabelFrame(self.control_panel, text="Game Stats")
        self.stats_frame.pack(side='right', padx=10)

        self.mines_left = ttk.Label(self.stats_frame, text="Mines: 0")
        self.mines_left.pack(side='left', padx=5)

        self.time_label = ttk.Label(self.stats_frame, text="Time: 0:00")
        self.time_label.pack(side='left', padx=5)

        # Game grid
        self.grid_frame = ttk.Frame(self.frame)
        self.grid_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.add_control_buttons()

        self.create_grid()

    def add_control_buttons(self):
        # Control buttons frame
        self.button_frame = ttk.Frame(self.control_panel)
        self.button_frame.pack(side='right', padx=10)

        # Play Again button
        self.play_again_btn = ttk.Button(
            self.button_frame,
            text="Play Again",
            command=self.reset_game
        )
        self.play_again_btn.pack(side='left', padx=5)

        # Auto Solve button
        self.solver_btn = ttk.Button(
            self.button_frame,
            text="Auto Solve",
            command=self.start_auto_solve
        )
        self.solver_btn.pack(side='left', padx=5)

    def create_grid(self):
        # Clear existing grid if any
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = {}  # Reset buttons dictionary

        # Create 3D grid for current W level
        for z in range(self.dimensions[2]):
            z_frame = ttk.LabelFrame(self.grid_frame, text=f"Z={z}")
            z_frame.grid(row=z//2, column=z%2, padx=5, pady=5, sticky='nsew')

            grid = ttk.Frame(z_frame)
            grid.pack(padx=5, pady=5)

            for y in range(self.dimensions[1]):
                for x in range(self.dimensions[0]):
                    btn = ttk.Button(grid, width=3, style='Cell.TButton')
                    btn.grid(row=y, column=x, padx=1, pady=1)
                    btn.configure(command=lambda x=x, y=y, z=z: self.cell_click(x, y, z))
                    self.buttons[(x, y, z)] = btn

        # Show revealed cells if any exist (including after winning)
        self.show_revealed_cells()

    def cell_click(self, x, y, z):
        if self.game_over or self.review_mode:
            return

        coords = (x, y, z, self.current_w)

        # Get the value from our tensor
        value = self._get_tensor_value(coords)

        # If it's a bomb
        if value == 100:
            self.buttons[(x, y, z)].configure(text="💣", state="disabled", style="Bomb.TButton")
            self.game_over = True
            self.show_game_over_dialog()
            return

        # Calculate number of adjacent bombs
        adjacent_bombs = self._count_adjacent_bombs(coords)

        # Update button
        btn = self.buttons[(x, y, z)]
        btn.configure(text=str(adjacent_bombs) if adjacent_bombs > 0 else "",
                     state="disabled",
                     style="Revealed.TButton")

        self.revealed_cells.add(coords)

        # Check for win
        if self._check_win():
            messagebox.showinfo("Congratulations!", "You've won the game!")
            self.game_over = True

    def _get_tensor_value(self, coords):
        x, y, z, w = coords
        return self.tensor.data[w][z][y][x]

    def _count_adjacent_bombs(self, coords):
        x, y, z, w = coords
        count = 0
        # Check all adjacent cells in 4D
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    for dw in [-1, 0, 1]:
                        new_x, new_y, new_z, new_w = x + dx, y + dy, z + dz, w + dw
                        if (0 <= new_x < 4 and 0 <= new_y < 4 and
                            0 <= new_z < 4 and 0 <= new_w < 4):
                            if self._get_tensor_value((new_x, new_y, new_z, new_w)) == 100:
                                count += 1
        return count

    def show_all_bombs(self):
        for w in range(self.dimensions[3]):
            # If this is the current W level
            if w == self.current_w:
                for z in range(self.dimensions[2]):
                    for y in range(self.dimensions[1]):
                        for x in range(self.dimensions[0]):
                            if self._get_tensor_value((x, y, z, w)) == 100:
                                self.buttons[(x, y, z)].configure(
                                    text="💣", state="disabled")

    def _check_win(self):
        total_cells = 4 * 4 * 4 * 4  # 4D grid
        bomb_cells = self.tensor.bomb  # Number of bombs
        safe_cells = total_cells - bomb_cells
        won = len(self.revealed_cells) == safe_cells
        if won and not self.game_over:  # Only show message first time
            self.game_over = True
            messagebox.showinfo("Congratulations!", "You've won the game!")
        return won

    def start_game(self):
        # Initialize game state
        self.game_over = False
        self.revealed_cells = set()
        self.tensor = Tensor(4, 4)
        self.create_grid()
        self.start_timer()

        # Update mine count
        self.mines_left.configure(text=f"Mines: {self.tensor.bomb}")

    def show_game_over_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Game Over!")
        dialog.transient(self.master)
        dialog.grab_set()

        # Calculate position for center of screen
        x = self.master.winfo_x() + self.master.winfo_width()//2 - 150
        y = self.master.winfo_y() + self.master.winfo_height()//2 - 100
        dialog.geometry(f"300x200+{x}+{y}")

        # Message
        msg = ttk.Label(dialog, text="Game Over!\nWhat would you like to do?", justify='center')
        msg.pack(pady=20)

        # Buttons frame
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)

        # Show Result button
        show_result_btn = ttk.Button(
            btn_frame,
            text="Show Result",
            command=lambda: [self.enter_review_mode(), dialog.destroy()]
        )
        show_result_btn.pack(pady=5)

        # Play Again button
        play_again_btn = ttk.Button(
            btn_frame,
            text="Play Again",
            command=lambda: [self.reset_game(), dialog.destroy()]
        )
        play_again_btn.pack(pady=5)

    def enter_review_mode(self):
        self.review_mode = True
        self.show_all_bombs_all_dimensions()
        self.solver_btn.configure(state='disabled')

    def show_all_bombs_all_dimensions(self):
        # Store all bomb locations
        self.bomb_locations = {}
        for w in range(self.dimensions[3]):
            for z in range(self.dimensions[2]):
                for y in range(self.dimensions[1]):
                    for x in range(self.dimensions[0]):
                        if self._get_tensor_value((x, y, z, w)) == 100:
                            if w not in self.bomb_locations:
                                self.bomb_locations[w] = set()
                            self.bomb_locations[w].add((x, y, z))

        # Show bombs for current dimension
        self.show_bombs_for_dimension(self.current_w)

    def show_bombs_for_dimension(self, w):
        if not self.review_mode or w not in self.bomb_locations:
            return

        # Show bombs for this W level
        for x, y, z in self.bomb_locations[w]:
            if (x, y, z) in self.buttons:
                self.buttons[(x, y, z)].configure(
                    text="💣",
                    state="disabled",
                    style="Bomb.TButton"
                )

    def reset_game(self):
        self.game_over = False
        self.review_mode = False
        self.revealed_cells = set()
        self.bomb_locations = {}
        self.tensor = Tensor(4, 4)
        self.current_w = 0
        self.update_w_display()
        self.create_grid()
        self.start_timer()
        self.mines_left.configure(text=f"Mines: {self.tensor.bomb}")
        self.solver_btn.configure(state='normal')

    def previous_w(self):
        if self.current_w > 0:
            self.current_w -= 1
            self.update_w_display()
            self.create_grid()
            if self.review_mode:
                self.show_bombs_for_dimension(self.current_w)
            elif self.game_over:  # Show revealed cells after winning
                self.show_revealed_cells()

    def next_w(self):
        if self.current_w < self.dimensions[3] - 1:
            self.current_w += 1
            self.update_w_display()
            self.create_grid()
            if self.review_mode:
                self.show_bombs_for_dimension(self.current_w)
            elif self.game_over:  # Show revealed cells after winning
                self.show_revealed_cells()

    def update_w_display(self):
        self.w_value.config(text=f"Level {self.current_w}")

    def start_timer(self):
        self.time = 0
        self.update_timer()

    def update_timer(self):
        if not self.game_over:  # Only update if game is not over
            minutes = self.time // 60
            seconds = self.time % 60
            self.time_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.time += 1
            self.master.after(1000, self.update_timer)

    def start_auto_solve(self):
        if self.game_over or self.review_mode:
            return

        self.solver_btn.configure(state='disabled')
        self.auto_solve()

    def simulate_cell_click(self, x, y, z):
        """Simulates a click without animation delay"""
        if (x, y, z) not in self.buttons or self.game_over or self.review_mode:
            return

        coords = (x, y, z, self.current_w)
        value = self._get_tensor_value(coords)

        # If it's a bomb
        if value == 100:
            self.buttons[(x, y, z)].configure(text="💣", state="disabled", style="Bomb.TButton")
            self.game_over = True
            self.show_game_over_dialog()
            return

        # Calculate number of adjacent bombs
        adjacent_bombs = self._count_adjacent_bombs(coords)

        # Update button
        btn = self.buttons[(x, y, z)]
        btn.configure(text=str(adjacent_bombs) if adjacent_bombs > 0 else "",
                     state="disabled",
                     style="Revealed.TButton")

        self.revealed_cells.add(coords)

        # Check for win
        if self._check_win():
            self.game_over = True
            messagebox.showinfo("Congratulations!", "Auto-solver won the game!")
            self.solver_btn.configure(state='normal')

    def auto_solve(self):
        if self.game_over or self.review_mode:
            self.solver_btn.configure(state='normal')
            return

        # Find a safe cell by checking tensor directly
        move = self.find_safe_move()

        if move:
            x, y, z, w = move

            # Switch to correct W dimension if needed
            if w != self.current_w:
                self.current_w = w
                self.update_w_display()
                self.create_grid()
                # Need to show revealed cells in new dimension
                self.show_revealed_cells()

            # Perform the move
            if (x, y, z) in self.buttons:
                self.simulate_cell_click(x, y, z)

            # Schedule next move with a longer delay to make it visible
            if not self.game_over and not self.review_mode:
                self.master.after(300, self.auto_solve)
        else:
            self.solver_btn.configure(state='normal')

    def show_revealed_cells(self):
        """Updates the display of already revealed cells when switching dimensions"""
        for (x, y, z, w) in self.revealed_cells:
            if w == self.current_w and (x, y, z) in self.buttons:
                value = self._get_tensor_value((x, y, z, w))
                btn = self.buttons[(x, y, z)]
                if value == 100:
                    btn.configure(text="💣", state="disabled", style="Bomb.TButton")
                else:
                    adjacent_bombs = self._count_adjacent_bombs((x, y, z, w))
                    btn.configure(text=str(adjacent_bombs) if adjacent_bombs > 0 else "",
                                state="disabled",
                                style="Revealed.TButton")

    def find_safe_move(self):
        # First try to find an unrevealed safe cell
        for w in range(self.dimensions[3]):
            for z in range(self.dimensions[2]):
                for y in range(self.dimensions[1]):
                    for x in range(self.dimensions[0]):
                        coords = (x, y, z, w)
                        # Skip if already revealed
                        if coords not in self.revealed_cells:
                            # We can look directly at the tensor to find safe moves
                            if self._get_tensor_value(coords) != 100:
                                return coords
        return None

    def enter_review_mode(self):
        self.review_mode = True
        self.show_all_bombs_all_dimensions()
        self.solver_btn.configure(state='disabled')

    def reset_game(self):
        self.game_over = False
        self.review_mode = False
        self.revealed_cells = set()
        self.bomb_locations = {}
        self.tensor = Tensor(4, 4)
        self.current_w = 0
        self.update_w_display()
        self.create_grid()
        self.start_timer()
        self.mines_left.configure(text=f"Mines: {self.tensor.bomb}")
        self.solver_btn.configure(state='normal')
