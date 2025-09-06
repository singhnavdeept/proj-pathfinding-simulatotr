# app/constants.py

import tkinter as tk  # <--- THIS LINE IS THE CRITICAL FIX

# --- Grid & Window Dimensions ---
GRID_ROWS = 25
GRID_COLS = 40
CELL_SIZE = 24  # Pixels
CONTROL_PANEL_WIDTH = 280
GRID_WIDTH = GRID_COLS * CELL_SIZE
GRID_HEIGHT = GRID_ROWS * CELL_SIZE
WINDOW_WIDTH = GRID_WIDTH + CONTROL_PANEL_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT

# --- Colors (Modern, Flat UI Palette) ---
COLOR_BG = "#FFFFFF"            # White
COLOR_GRID_LINE = "#E0E0E0"     # Light Grey
COLOR_START = "#2ECC71"         # Emerald Green
COLOR_END = "#E74C3C"           # Alizarin Red
COLOR_WALL = "#34495E"          # Wet Asphalt (Dark Blue/Grey)
COLOR_VISITED = "#3498DB"       # Peter River Blue
COLOR_VISITING = "#85C1E9"      # Lighter Blue for open set
COLOR_PATH = "#F1C40F"          # Sunflower Yellow

# --- Node States (Enum-style class for clarity and type safety) ---
class NodeState:
    EMPTY = 0
    START = 1
    END = 2
    WALL = 3
    VISITED = 4
    VISITING = 5
    PATH = 6

# --- Map states to colors for easy lookup ---
STATE_COLORS = {
    NodeState.EMPTY: COLOR_BG,
    NodeState.START: COLOR_START,
    NodeState.END: COLOR_END,
    NodeState.WALL: COLOR_WALL,
    NodeState.VISITED: COLOR_VISITED,
    NodeState.VISITING: COLOR_VISITING,
    NodeState.PATH: COLOR_PATH,
}

# --- UI & Algorithm Settings ---
ALGORITHMS = ["A* Search", "Dijkstra", "Breadth-First Search (BFS)", "Depth-First Search (DFS)"]
DEFAULT_ALGORITHM = ALGORITHMS[0]
DEFAULT_SPEED = 5 # ms delay between animation steps (higher is slower)

# --- Class for shared Tkinter variables ---
# This class needs `tk` to be defined, which is why the import was crucial.
class TkinterState:
    def __init__(self):
        self.tool_var = tk.StringVar(value="start")
        self.speed_var = tk.DoubleVar(value=DEFAULT_SPEED)
        self.algorithm_var = tk.StringVar(value=DEFAULT_ALGORITHM)