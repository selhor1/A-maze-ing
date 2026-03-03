from typing import List, Tuple, Set, Dict, Optional

PALETTES: List[Dict[str, str]] = [
    {"name": "Classic/Bold", "walls": "38;5;160", "inner": "38;5;231",
     "pattern": "38;5;21"},
    {"name": "Vibrant/Natural", "walls": "38;5;30", "inner": "38;5;201",
     "pattern": "38;5;220"},
    {"name": "Earth/Moody", "walls": "38;5;172", "inner": "38;5;235",
     "pattern": "38;5;244"},
    {"name": "Calm/Modern", "walls": "38;5;182", "inner": "38;5;181",
     "pattern": "38;5;103"},
    {"name": "Dynamic", "walls": "38;5;34", "inner": "38;5;208",
     "pattern": "38;5;129"},
    {"name": "Crisp/Natural", "walls": "38;5;24", "inner": "38;5;15",
     "pattern": "38;5;196"}
]

ORANGE = "38;5;208"
PATH_SYMBOL = "\u272F"
N, E, S, W = 1, 2, 4, 8


def get_42_pattern_coords(width: int, height: int) -> Set[Tuple[int, int]]:
    """Exact same 7x5 coordinates logic as generator.py."""
    start_x, start_y = (width - 7) // 2, (height - 5) // 2
    pattern = ["1000111", "1000001", "1110111", "0010100", "0010111"]
    blocked = set()
    for dy, row in enumerate(pattern):
        for dx, char in enumerate(row):
            if char == "1":
                blocked.add((start_x + dx, start_y + dy))
    return blocked


def render_ascii(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    origin_theme: Dict[str, str],
    show_42: bool = False,
    path_cells: Optional[Set[Tuple[int, int]]] = None,
    current_cell: Optional[Tuple[int, int]] = None
) -> None:
    """
    Render the maze in ASCII art with optional path highlighting.

    Parameters:
    - grid: 2D list of ints representing the maze cells and walls.
    - entry: (x, y) coordinates of the maze entry.
    - exit_: (x, y) coordinates of the maze exit.
    - origin_theme: dict with color codes for walls, inner cells, pattern.
    - show_42: whether to render the 42 pattern inside the maze.
    - visited: optional set of visited cells (not used here, just placeholder).
    - path_cells: optional set of cells forming a path to highlight.
    - current_cell: optional current cell for animation purposes.

    Returns:
    - None
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    p42 = get_42_pattern_coords(width, height) if show_42 else set()

    V_WALL = (f"\033[{origin_theme['walls']}m\u2503\033[0m")
    H_WALL = (f"\033[{origin_theme['walls']}m\u2501\u2501\u2501\033[0m")
    TL, TR = (f"\033[{origin_theme['walls']}m\u250F\033[0m",
              f"\033[{origin_theme['walls']}m\u2513\033[0m")
    BL, BR = (f"\033[{origin_theme['walls']}m\u2517\033[0m",
              f"\033[{origin_theme['walls']}m\u251B\033[0m")
    JT, JB = (f"\033[{origin_theme['walls']}m\u2501\033[0m",
              f"\033[{origin_theme['walls']}m\u2501\033[0m")
    JL, JR = (f"\033[{origin_theme['walls']}m\u2503\033[0m",
              f"\033[{origin_theme['walls']}m\u2503\033[0m")
    JI = f"\033[{origin_theme['inner']}m✦\033[0m"

    for y in range(height):
        top_line = ""
        for x in range(width):
            char = (TL if x == 0 else JT) if y == 0 else (JL if x == 0 else JI)
            top_line += char + (H_WALL if (grid[y][x] & N) else "   ")
        top_line += (TR if y == 0 else JR)
        print(top_line)

        mid_line = ""
        for x in range(width):
            mid_line += (V_WALL if (grid[y][x] & W) else " ")
            pos = (x, y)

            if pos == entry:
                mid_line += f"\033[{origin_theme['inner']}m🐁 \033[0m"

            elif pos == exit_:
                mid_line += f"\033[{origin_theme['inner']}m🧀 \033[0m"

            elif current_cell and pos == current_cell:
                mid_line += "\033[33m◆  \033[0m"

            elif path_cells and pos in path_cells:
                mid_line += f"\033[{ORANGE}m{PATH_SYMBOL}  \033[0m"

            elif pos in p42:
                mid_line += f"\033[{origin_theme['pattern']}m███\033[0m"

            else:
                mid_line += "   "
        mid_line += V_WALL
        print(mid_line)

    bottom_line = BL + "".join(H_WALL + (JB if x < width - 1 else BR)
                               for x in range(width))
    print(bottom_line)
