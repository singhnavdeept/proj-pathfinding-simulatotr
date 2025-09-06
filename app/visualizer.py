# app/visualizer.py

import tkinter as tk
from tkinter import ttk
import random
# Corrected line below: added TkinterState to the import
from .constants import (GRID_WIDTH, GRID_HEIGHT,GRID_ROWS,GRID_COLS, CONTROL_PANEL_WIDTH, COLOR_BG,
                        CELL_SIZE, NodeState, STATE_COLORS, COLOR_GRID_LINE,
                        ALGORITHMS, TkinterState)
from .grid import Grid
from .algorithms import ALGORITHM_MAP

class PathfindingVisualizer(tk.Tk):
    """
    The main application class. Manages the GUI, event handling,
    and orchestrates the visualization process by linking the Grid model,
    Algorithm logic, and Tkinter view.
    """
    def __init__(self):
        super().__init__()
        self.title("Pathfinding Visualizer")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()-100}") # Use screen dimensions for better fit
        # self.state('zoomed') # Alternative for Windows/some Linux DEs
        self.resizable(True, True) # Allow resizing
        
        self.grid = Grid()
        self.tk_state = TkinterState() # This will now work
        self.is_running = False
        self.animation_job = None
        self.control_widgets = []

        self._init_ui()
        self._bind_events()
        self.draw_grid(full_redraw=True)

    def _init_ui(self):
        """Initializes all UI components."""
        # --- Control Panel ---
        self.control_frame = ttk.Frame(self, width=CONTROL_PANEL_WIDTH, padding="10 20 10 20")
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.control_frame.pack_propagate(False) # Prevent resizing
        self._create_controls(self.control_frame)

        # --- Grid Canvas ---
        self.canvas = tk.Canvas(self, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _create_controls(self, parent):
        """Creates and places all the control widgets in the control panel."""
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TRadiobutton", padding= (10, 5))
        style.configure("TLabelFrame.Label", font=('Helvetica', 10, 'bold'))
        
        # --- Tool Selection ---
        tool_frame = ttk.LabelFrame(parent, text="Tools")
        tool_frame.pack(fill=tk.X, pady=(0, 15))
        tools = [("Set Start", "start"), ("Set End", "end"), ("Add Wall", "wall"), ("Erase", "empty")]
        for text, value in tools:
            rb = ttk.Radiobutton(tool_frame, text=text, variable=self.tk_state.tool_var, value=value)
            rb.pack(anchor=tk.W)
            self.control_widgets.append(rb)

        # --- Algorithm Selection ---
        algo_frame = ttk.LabelFrame(parent, text="Algorithm")
        algo_frame.pack(fill=tk.X, pady=(0, 15))
        algo_dropdown = ttk.Combobox(algo_frame, textvariable=self.tk_state.algorithm_var, values=ALGORITHMS, state="readonly")
        algo_dropdown.pack(pady=5, padx=10)
        self.control_widgets.append(algo_dropdown)
        
        # --- Speed Control ---
        speed_frame = ttk.LabelFrame(parent, text="Animation Speed (ms delay)")
        speed_frame.pack(fill=tk.X, pady=(0, 15))
        speed_slider = ttk.Scale(speed_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.tk_state.speed_var)
        speed_slider.pack(pady=5, padx=10, fill=tk.X)
        self.control_widgets.append(speed_slider)

        # --- Action Buttons ---
        run_button = ttk.Button(parent, text="Run Visualization", command=self.run_visualization, style="Accent.TButton")
        run_button.pack(fill=tk.X, pady=5)
        self.control_widgets.append(run_button)
        style.configure("Accent.TButton", foreground="white", background="#0078D4")

        clear_path_button = ttk.Button(parent, text="Clear Path & Visited", command=self.clear_path)
        clear_path_button.pack(fill=tk.X, pady=5)
        self.control_widgets.append(clear_path_button)
        
        generate_walls_button = ttk.Button(parent, text="Generate Random Walls", command=self.generate_random_walls)
        generate_walls_button.pack(fill=tk.X, pady=5)
        self.control_widgets.append(generate_walls_button)
        
        reset_button = ttk.Button(parent, text="Full Reset", command=self.reset_all)
        reset_button.pack(fill=tk.X, pady=(5,0))
        self.control_widgets.append(reset_button)

    def _bind_events(self):
        """Binds mouse events to the canvas."""
        self.canvas.bind("<Button-1>", self.handle_mouse_event)
        self.canvas.bind("<B1-Motion>", self.handle_mouse_event)
        self.canvas.bind("<Button-3>", self.handle_mouse_event)
        self.canvas.bind("<B3-Motion>", self.handle_mouse_event)

    def _toggle_controls(self, state):
        """Disables or enables all control widgets."""
        for widget in self.control_widgets:
            widget.config(state=state)

    def draw_grid(self, full_redraw=False):
        """Draws the nodes and grid lines onto the canvas."""
        self.canvas.delete("all")
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                self._draw_node(self.grid.get_node(r, c))
        self.update_idletasks() # Force UI update

    def _draw_node(self, node):
        """Draws a single node on the canvas."""
        x1, y1 = node.col * CELL_SIZE, node.row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        color = STATE_COLORS[node.state]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=COLOR_GRID_LINE)

    def handle_mouse_event(self, event):
        """Handles all mouse clicks and drags on the canvas."""
        if self.is_running: return
        
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        node = self.grid.get_node(row, col)
        if not node: return

        tool = self.tk_state.tool_var.get()
        if event.num == 3: # Right-click always erases
            tool = "empty"

        # Prevent changing start/end nodes while adding walls/erasing
        if tool in ["wall", "empty"] and (node == self.grid.start_node or node == self.grid.end_node):
            return

        if tool == "start":
            if node != self.grid.end_node:
                old_start = self.grid.start_node
                self.grid.set_start(node)
                if old_start: self._draw_node(old_start)
        elif tool == "end":
            if node != self.grid.start_node:
                old_end = self.grid.end_node
                self.grid.set_end(node)
                if old_end: self._draw_node(old_end)
        elif tool == "wall":
            node.state = NodeState.WALL
        elif tool == "empty":
            if node.state != NodeState.EMPTY:
                node.state = NodeState.EMPTY
            
        self._draw_node(node)
    
    def run_visualization(self):
        """Starts the selected pathfinding algorithm."""
        if self.is_running or not self.grid.start_node or not self.grid.end_node:
            print("LOG: Visualization blocked - already running or missing start/end node.")
            return
        
        print(f"LOG: Starting {self.tk_state.algorithm_var.get()}")
        self.is_running = True
        self._toggle_controls(tk.DISABLED)
        self.clear_path(draw=False)

        algorithm_func = ALGORITHM_MAP[self.tk_state.algorithm_var.get()]
        
        # We now need a callback that only draws the entire grid.
        # This is less performant but much simpler for the generator model.
        draw_callback = lambda: self.draw_grid(full_redraw=True)
        algo_generator = algorithm_func(self.grid, draw_callback)

        def _step_animation():
            try:
                next(algo_generator)
                self.animation_job = self.after(int(self.tk_state.speed_var.get()), _step_animation)
            except StopIteration as e:
                # The algorithm function will return True on success
                if not e.value:
                    print("LOG: No path found.")
                else:
                    print("LOG: Path found successfully.")
                self.is_running = False
                self._toggle_controls(tk.NORMAL)
        
        _step_animation()

    def stop_animation(self):
        """Stops any running animation."""
        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None
        self.is_running = False
        self._toggle_controls(tk.NORMAL)
    
    def clear_path(self, draw=True):
        if self.is_running: self.stop_animation()
        self.grid.clear_path()
        if draw:
            self.draw_grid(full_redraw=True)
        
    def generate_random_walls(self):
        if self.is_running: self.stop_animation()
        self.grid.generate_random_walls()
        self.draw_grid(full_redraw=True)

    def reset_all(self):
        if self.is_running: self.stop_animation()
        self.grid.clear_all()
        # Reset the tool selection back to default
        self.tk_state.tool_var.set("start")
        self.draw_grid(full_redraw=True)