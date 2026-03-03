*This project has been created as part of the 42 curriculum by selhor, masselgu.*

# 🧩 A-Maze-ing — This is the way

## 📖 Description

A-Maze-ing is a Python-based maze generator capable of creating random mazes with optional perfect structure (single unique path between entry and exit).

The project reads a configuration file, generates a maze accordingly, visually renders it in the terminal, and exports it to a file using a hexadecimal wall representation.

The maze generation logic is reusable as a standalone Python package (`mazegen-*`), making it suitable for integration into future projects.

This project explores:
- Graph theory
- Spanning trees
- Breadth-First Search (BFS)
- Randomized maze generation algorithms
- Clean code architecture and reusability

---

## 🚀 Features

- Random maze generation
- Seed-based reproducibility
- Perfect / non-perfect maze option
- BFS shortest path solver
- ASCII terminal visualization
- Interactive menu:
  - Regenerate maze
  - Show/Hide shortest path
  - Play mode (WASD movement)
  - Change wall theme
  - Display maze information
- Hexadecimal export format
- Flake8 compliant
- Fully typed (mypy checked)

---

## 🛠 Instructions

### 1️⃣ Install dependencies

```bash
make install
```

or manually:
``` bash
pip3 install -r requirements.txt
```
▶️ Run the program
``` bash
make run
```

or manually:
``` bash
python3 a_maze_ing.py config.txt
```
🐞 Debug Mode
``` bash
make debug
```
Runs the program using Python's debugger (pdb).

🧹 Clean Cache
``` bash
make clean
```
Removes:

- __pycache__

- .mypy_cache

🧪 Lint & Type Checking
``` bash
make lint
```
Runs:
``` bash
flake8
```
mypy with strict typing options

⚙ Configuration File Format

- The configuration file contains one KEY=VALUE per line.

- Lines starting with # are ignored.

Mandatory keys:
- Key	Description	Example
- WIDTH	Maze width	WIDTH=20
- HEIGHT	Maze height	HEIGHT=15
- ENTRY	Entry coordinates (x,y)	ENTRY=0,0
- EXIT	Exit coordinates (x,y)	EXIT=19,14
- OUTPUT_FILE	Output filename	OUTPUT_FILE=maze.txt
- PERFECT	Perfect maze flag	PERFECT=True
Optional keys:
- Key	Description
- SEED	Random seed for reproducibility
- 🧱 Maze Generation Algorithm

### The maze is generated using a randomized depth-first search algorithm.

Why this algorithm?

- Simple to implement

- Efficient

- Naturally produces perfect mazes

- Easy to control with seed for reproducibility

- Produces visually pleasing corridors

If PERFECT=True, the maze ensures:

- Exactly one unique path between entry and exit


## 🔢 Output File Format

### Each cell is represented by a single hexadecimal digit.

Each bit represents a closed wall:

Bit	Direction
- 0	North
- 1	East
- 2	South
- 3	West

Example:

- 3 (0011) → North & East walls closed

- A (1010) → East & West walls closed

File structure:
``` bash
<maze rows>

<entry coordinates>
<exit coordinates>
<shortest path using N,E,S,W>
```
🖥 Visual Representation

- The maze is displayed in the terminal using ASCII rendering.

The interface allows:

- [R] Regenerate maze

- [S] Show/Hide shortest path

- [P] Play mode (WASD movement)

- [C] Change theme

- [I] Info display

- [Q] Quit

The maze includes a visible "42" pattern made of fully closed cells.

## ♻ Code Reusability

The maze generation logic is implemented as a reusable module:

MazeGenerator class (inside mazegen package)

It allows:
``` bash
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15, entry=(0,0), exit=(19,14))
generator.generate(perfect=True)
grid = generator.get_cells()
```
You can:

- Set custom size

- Use a seed

- Access generated structure

- Use built-in solver

The reusable package can be built as:

- mazegen-1.0.0-py3-none-any.whl
## 🧠 Shortest Path Algorithm

Shortest path is computed using Breadth-First Search (BFS).

Why BFS?

- Guarantees shortest path in unweighted grid

- Simple

- Efficient for maze structure

## 👥 Team & Project Management
Roles

- Maze generation logic

- Rendering system

- Configuration parser

- Solver implementation

- Makefile & packaging

- Testing & debugging

### Planning

Initial plan:

- Implement generator

- Add config parser

- Add rendering

- Add solver

- Add packaging

Adjustments:

- Improved validation

- Refactored for reusability

- Added play mode

- Improved error handling

### Tools Used

- Python 3.10+

- flake8

- mypy

- pdb

- Makefile

- Virtual environment

- Git

## 🤖 AI Usage

AI was used for:

- Clarifying algorithm logic

- Debugging assistance

- Improving type hints

- Understanding BFS deeply

- Improving documentation structure

- All generated content was reviewed, tested, and fully understood before integration.

## 📚 Resources

- Graph Theory (Spanning Trees)

- Breadth-First Search documentation

- Python official documentation

- PEP 8 / flake8 documentation

- mypy documentation

## 🏁 Conclusion

This project demonstrates:

- Algorithmic thinking

- Clean architecture

- Reusable module design

- File format design

- Interactive terminal rendering

- Strong type-safe Python code

### A-Maze-ing is not just a maze generator — it is a structured, reusable, and extensible system built with production-level discipline.