from .constants import NodeState

class Node:
    """
    Represents a single cell in the grid. It knows its own state, position,
    and holds data crucial for pathfinding algorithms (like its parent for
    path reconstruction).
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = NodeState.EMPTY
        self.parent = None

    def is_walkable(self):
        """A node is walkable if it's not a wall."""
        return self.state != NodeState.WALL

    def reset(self, keep_essentials=True):
        """
        Resets the node's state. If keep_essentials is True, it preserves
        start, end, and wall nodes, which is used for 'Clear Path'.
        Otherwise, it's a full reset for 'Clear All'.
        """
        if keep_essentials and self.state in (NodeState.START, NodeState.END, NodeState.WALL):
            self.parent = None
            return
        
        # If this node was the start or end, it should be fully reset
        if self.state in (NodeState.START, NodeState.END):
            if not keep_essentials:
                self.state = NodeState.EMPTY

        # Reset visualization states
        elif self.state not in (NodeState.WALL, NodeState.EMPTY):
             self.state = NodeState.EMPTY

        self.parent = None

    def __lt__(self, other):
        """
        Comparison method for the priority queue. If priorities are equal,
        Python may try to compare the Node objects themselves. This method
        provides a fallback to prevent errors.
        """
        return False