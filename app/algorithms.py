# app/algorithms.py

import collections
import heapq
from .constants import NodeState

# --- Helper function for all algorithms ---
def _reconstruct_path(draw_callback, end_node):
    """Backtracks from the end node to the start, drawing the path."""
    current = end_node.parent
    while current and current.parent:
        current.state = NodeState.PATH
        draw_callback()
        current = current.parent

# --- Pathfinding Algorithm Implementations ---

def a_star_search(grid, draw_callback):
    """
    A* Search Algorithm. Uses a heuristic (Manhattan distance) to find the
    most promising path. It's both complete and optimal.
    Yields control to allow for animation.
    """
    def h(p1, p2):
        return abs(p1.row - p2.row) + abs(p1.col - p2.col)

    count = 0
    open_set = [(0, count, grid.start_node)]
    g_score = {node: float("inf") for row in grid.nodes for node in row}
    g_score[grid.start_node] = 0
    f_score = {node: float("inf") for row in grid.nodes for node in row}
    f_score[grid.start_node] = h(grid.start_node, grid.end_node)

    open_set_hash = {grid.start_node}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == grid.end_node:
            _reconstruct_path(draw_callback, grid.end_node)
            return True

        for neighbor in grid.get_neighbors(current):
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                neighbor.parent = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor, grid.end_node)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor.state != NodeState.END:
                        neighbor.state = NodeState.VISITING
        yield
        if current != grid.start_node:
            current.state = NodeState.VISITED
    return False

def dijkstra(grid, draw_callback):
    """
    Dijkstra's Algorithm. Finds the shortest path in a weighted graph.
    For our unweighted grid, it behaves identically to BFS but is implemented
    with a priority queue for correctness and extensibility.
    Yields control to allow for animation.
    """
    count = 0
    pq = [(0, count, grid.start_node)] # (distance, count, node)
    distances = {node: float('inf') for row in grid.nodes for node in row}
    distances[grid.start_node] = 0
    
    visited_hash = {grid.start_node}

    while pq:
        dist, _, current = heapq.heappop(pq)

        if current == grid.end_node:
            _reconstruct_path(draw_callback, grid.end_node)
            return True
            
        if current.state != NodeState.START:
            current.state = NodeState.VISITED

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited_hash:
                neighbor.parent = current
                distances[neighbor] = dist + 1
                count += 1
                heapq.heappush(pq, (distances[neighbor], count, neighbor))
                visited_hash.add(neighbor)
                if neighbor.state != NodeState.END:
                    neighbor.state = NodeState.VISITING
        yield
    return False

def breadth_first_search(grid, draw_callback):
    """
    Breadth-First Search (BFS). Explores layer by layer. Guarantees the
    shortest path on an unweighted grid.
    Yields control to allow for animation.
    """
    queue = collections.deque([grid.start_node])
    visited = {grid.start_node}

    while queue:
        current = queue.popleft()

        if current == grid.end_node:
            _reconstruct_path(draw_callback, grid.end_node)
            return True

        if current != grid.start_node:
            current.state = NodeState.VISITED

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                queue.append(neighbor)
                if neighbor.state != NodeState.END:
                    neighbor.state = NodeState.VISITING
        yield
    return False

def depth_first_search(grid, draw_callback):
    """
    Depth-First Search (DFS). Explores as deeply as possible before
    backtracking. Does not guarantee the shortest path.
    Yields control to allow for animation.
    """
    stack = [grid.start_node]
    visited = {grid.start_node}

    while stack:
        current = stack.pop()

        if current == grid.end_node:
            _reconstruct_path(draw_callback, grid.end_node)
            return True

        if current != grid.start_node:
            current.state = NodeState.VISITED

        for neighbor in reversed(grid.get_neighbors(current)): # Reverse for more intuitive visualization
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                stack.append(neighbor)
                if neighbor.state != NodeState.END:
                    neighbor.state = NodeState.VISITING
        yield
    return False

# Map algorithm names to functions
ALGORITHM_MAP = {
    "A* Search": a_star_search,
    "Dijkstra": dijkstra,
    "Breadth-First Search (BFS)": breadth_first_search,
    "Depth-First Search (DFS)": depth_first_search,
}