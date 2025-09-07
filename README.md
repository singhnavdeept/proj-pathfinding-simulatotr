

# Pathfinding Algorithm Visualizer 🗺️

An interactive desktop application built with Python and Tkinter to visualize the inner workings of classic pathfinding algorithms in real-time.

This tool serves as an educational sandbox to help understand how algorithms like A\*, Dijkstra's, BFS, and DFS explore a grid, handle obstacles, and find a path from a start to an end point. By watching the process unfold step-by-step, abstract concepts become tangible and intuitive.



---

## ✨ Features

*   **Interactive Grid:** Click and drag to place the start (🟢), end (🔴), and wall (⬛) nodes. Right-click to erase.
*   **Algorithm Selection:** Choose from four fundamental pathfinding algorithms from a dropdown menu.
*   **Real-time Visualization:** Watch the selected algorithm explore the grid step-by-step.
    *   **Visiting Nodes (Frontier):** Light Blue 🔵
    *   **Visited Nodes (Explored):** Dark Blue 🟦
    *   **Final Path:** Yellow 🟡
*   **Adjustable Speed:** A speed slider allows you to slow down the animation to carefully analyze the algorithm's decisions or speed it up for a quick overview.
*   **Maze Generation:** Instantly generate a random maze to create complex test scenarios.
*   **Dynamic Controls:** Clear only the path to test another algorithm on the same maze, or perform a full reset to start fresh.

---

## 🧠 Algorithms Visualized

This project provides a visual demonstration of the following algorithms:

*   **A\* Search:** The "Intelligent Hunter." An efficient, heuristic-based algorithm that intelligently guides its search towards the goal. It's one of the most popular pathfinding algorithms.
*   **Dijkstra's Algorithm:** The "Methodical Explorer." A foundational algorithm that guarantees the shortest path by systematically exploring outwards from the start.
*   **Breadth-First Search (BFS):** The "Ripple Effect." Explores the grid layer by layer. It's simple and guarantees the shortest path (in steps) on an unweighted grid.
*   **Depth-First Search (DFS):** The "Deep Explorer." Dives as deep as possible down one path before backtracking. It finds a path, but not necessarily the shortest one.

---

## 🛠️ Technologies Used

*   **Language:** Python 3
*   **GUI Framework:** Tkinter (standard with Python)
*   **Core Data Structures:** Queues, Stacks, and Priority Queues (`heapq`)

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.x installed on your system.

### Installation & Usage

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/singhnavdeept/proj-pathfinding-simulatotr.git
    ```
2.  **Navigate to the project directory:**
    ```sh
    cd proj-pathfinding-simulatotr
    ```
3.  **Run the application:**
    ```sh
    python3 main.py
    ```The application window should now appear.

---

## 📖 How to Use the Application

1.  **Select a Tool:** Use the radio buttons in the control panel to choose whether you want to `Set Start`, `Set End`, `Add Wall`, or `Erase`.
2.  **Design Your Maze:**
    *   Click on the grid to place the Start and End nodes.
    *   Click and drag to draw continuous walls.
    *   Right-click (or use the Erase tool) to remove any node.
3.  **Choose an Algorithm:** Select your desired algorithm from the dropdown menu.
4.  **Adjust the Speed:** Use the slider to set the animation speed. A lower value means a faster animation.
5.  **Run and Observe:** Click the `Run Visualization` button and watch the algorithm work!
6.  **Analyze and Compare:**
    *   Click `Clear Path & Visited` to test a different algorithm on the same maze.
    *   Click `Generate Random Walls` for a new challenge.
    *   Click `Full Reset` to clear the entire grid.

---

## 🏛️ Project Architecture & Data Flow

The project is built on a **Model-View-Controller (MVC)** architectural pattern to ensure a clean separation of concerns, making the code modular, scalable, and easy to maintain.

### File Structure & Responsibilities

*   `main.py`: The **Entry Point**. Its sole job is to initialize and run the main application.
*   `app/constants.py`: The **Configuration Hub**. Centralizes all constants like colors, grid dimensions, and UI settings.
*   `app/node.py`: The **Data Atom (Model)**. Defines the `Node` class, which represents a single cell in the grid and holds its state (e.g., `WALL`, `VISITED`).
*   `app/grid.py`: The **Board Manager (Model)**. Manages the 2D array of all `Node` objects and provides methods to interact with the grid as a whole (e.g., `get_neighbors`, `clear_all`).
*   `app/algorithms.py`: The **Algorithm Logic**. Contains the pure implementation of each pathfinding algorithm as a generator function (`yield`), completely decoupled from the UI.
*   `app/visualizer.py`: The **Conductor (View/Controller)**. Manages the Tkinter window, draws the grid on the canvas (View), handles all user input like mouse clicks (Controller), and orchestrates the animation loop.

### How Data Flows: An Example

When you click on the grid to add a wall:

1.  **View (Input):** The Tkinter `Canvas` in `visualizer.py` detects a mouse click.
2.  **Controller (Interpretation):** The `handle_mouse_event` method in `visualizer.py` is triggered. It translates the pixel coordinates of the click into grid `(row, col)` coordinates.
3.  **Controller -> Model (Update):** The Controller accesses the `Grid` object and tells it to update the state of the specific `Node` at that `(row, col)` to `WALL`. The core data is now changed.
4.  **Model -> View (Redraw):** The Controller then calls its `_draw_node` method, which reads the new state from the updated `Node` object and redraws that single rectangle on the canvas with the `WALL` color.

This clean flow ensures that the application's logic and data are independent of how they are displayed.

---

## 💡 Algorithm Explanations

#### A\* Search
*   **Core Idea:** Finds the shortest path by minimizing a cost function `f(n) = g(n) + h(n)`, where `g(n)` is the known cost from the start and `h(n)` is an estimated cost to the end (the heuristic).
*   **Strategy:** Uses a **Priority Queue** to always explore the node that appears to be the most promising, based on the lowest `f(n)` score.
*   **Visual Behavior:** Creates a focused "comet trail" of explored nodes stretching towards the destination, exploring far fewer nodes than uninformed algorithms.
*   **Path Guarantee:** **Yes**, it guarantees the shortest path.

#### Dijkstra's Algorithm
*   **Core Idea:** Finds the shortest path by exploring the node that is closest to the start first.
*   **Strategy:** Uses a **Priority Queue** to always explore the node with the lowest known distance from the starting node.
*   **Visual Behavior:** Expands outwards from the start in a uniform, circular wave, exploring in all directions equally.
*   **Path Guarantee:** **Yes**, it guarantees the shortest path.

#### Breadth-First Search (BFS)
*   **Core Idea:** Explores the grid layer by layer, checking all neighbors at the current depth before moving on.
*   **Strategy:** Uses a **Queue (First-In, First-Out)**. This ensures that nodes are explored in the order they are discovered, creating the level-by-level search.
*   **Visual Behavior:** Identical to Dijkstra's on an unweighted grid—a uniform, circular wave.
*   **Path Guarantee:** **Yes**, it guarantees the shortest path in terms of the number of steps.

#### Depth-First Search (DFS)
*   **Core Idea:** Dives as deep as possible down a single path, only backtracking when it hits a dead end.
*   **Strategy:** Uses a **Stack (Last-In, First-Out)**. This causes it to always pursue the most recently discovered node first, leading to its deep exploration behavior.
*   **Visual Behavior:** Creates long, unpredictable "tendrils" that snake through the maze. The search pattern appears chaotic.
*   **Path Guarantee:** **No**, it does not guarantee the shortest path.

---

## 🔮 Future Enhancements

The project is designed with scalability in mind. Future improvements could include:
*   **Weighted Terrain:** Add nodes with different movement costs (e.g., sand, water) to highlight the true power of Dijkstra's and A\*.
*   **More Algorithms:** Implement advanced algorithms like Jump Point Search or Bidirectional Search.
*   **Performance Metrics:** Display statistics like path length, nodes visited, and execution time.
*   **Diagonal Movement:** Add a toggle to allow movement in eight directions.
*   **Save & Load Mazes:** Allow users to save their custom layouts to a file.