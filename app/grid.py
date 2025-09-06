import random
from .node import Node
from .constants import GRID_ROWS, GRID_COLS, NodeState

class Grid:
    """Manages the 2D array of nodes, their states, and grid-wide operations."""
    def __init__(self):
        self.nodes = [[Node(row, col) for col in range(GRID_COLS)] for row in range(GRID_ROWS)]
        self.start_node = None
        self.end_node = None

    def get_node(self, row, col):
        """Safely retrieves a node from the grid."""
        if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
            return self.nodes[row][col]
        return None

    def _set_node_as(self, node, new_state_attr, old_node_attr):
        """Helper to set start/end nodes and reset the old ones."""
        old_node = getattr(self, old_node_attr)
        if old_node:
            old_node.state = NodeState.EMPTY
        
        setattr(self, old_node_attr, node)
        if node:
            node.state = getattr(NodeState, new_state_attr.upper())

    def set_start(self, node):
        self._set_node_as(node, "start", "start_node")

    def set_end(self, node):
        self._set_node_as(node, "end", "end_node")

    def clear_path(self):
        """Resets the grid but keeps walls, start, and end points."""
        for row in self.nodes:
            for node in row:
                node.reset(keep_essentials=True)

    def clear_all(self):
        """Resets the entire grid to its initial state."""
        self.start_node = None
        self.end_node = None
        for row in self.nodes:
            for node in row:
                node.reset(keep_essentials=False)

    def get_neighbors(self, node):
        """Returns valid neighbors (up, down, left, right)."""
        neighbors = []
        row, col = node.row, node.col
        # No diagonal movement as per MVP
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_row, neighbor_col = row + dr, col + dc
            neighbor = self.get_node(neighbor_row, neighbor_col)
            if neighbor and neighbor.is_walkable():
                neighbors.append(neighbor)
        return neighbors
        
    def generate_random_walls(self, density=0.25):
        """Generates random walls across the grid."""
        self.clear_all() # Start with a clean slate
        for row in self.nodes:
            for node in row:
                if random.random() < density:
                    node.state = NodeState.WALL