"""Maze generation algorithms."""

import random
from .cell import Cell
from .validator import MazeValidator
from .exporter import MazeExporter
from utils.errors import InvalidDistinationFor42Path, InvalidEntryExitPoint


class MazeGenerator:
    """Generates mazes using recursive backtracker."""
    
    def __init__(self, cols, rows, Entry, EXIT, out_file, perfect=True):
        self.x = cols
        self.y = rows
        self.maze = [[Cell() for _ in range(self.x)] for _ in range(self.y)]
        self.entry = Entry
        self.exit = EXIT
        self.out_file = out_file
        self.validator = MazeValidator()
        self.exporter = MazeExporter()
        self.perfect = perfect
    
    # ========== PUBLIC API ==========
    def generate(self):
        """Generate maze with recursive backtracker."""
        if self.x < 9 or self.y < 9:
            raise InvalidDistinationFor42Path("Maze too small for 42 pattern")
        
        self._create_42_pattern()
        
        if self.maze[self.entry[1]][self.entry[0]]._42_path or \
           self.maze[self.exit[1]][self.exit[0]]._42_path:
            raise InvalidEntryExitPoint("Entry/exit cannot be inside 42 pattern")
        
        self._backtracker(0, 0)
        if not self.perfect:
            self._add_loops()
        
        if not self.validator.is_fully_connected(self.maze, self.entry, self.x, self.y):
            raise RuntimeError("Generated maze is not fully connected")
    
    def save(self, path):
        """Save maze to output file."""
        self.exporter.save_to_file(
            self.out_file, self.maze, self.x, self.y, 
            self.entry, self.exit, path
        )
    
    def reset(self):
        """Reset visited flags for regeneration."""
        for y in range(self.y):
            for x in range(self.x):
                self.maze[y][x].visited = False
    
    # ========== ALGORITHM ==========
    def _backtracker(self, i, j):
        """Recursive backtracker algorithm."""
        self.maze[j][i].visited = True
        neighbors = self._get_unvisited_neighbors(i, j)
        
        while neighbors:
            nx, ny, direction = random.choice(neighbors)
            self.maze[ny][nx].visited = True
            self._remove_wall(i, j, nx, ny, direction)
            self._backtracker(nx, ny)
            neighbors = self._get_unvisited_neighbors(i, j)
    
    def _get_unvisited_neighbors(self, x, y):
        """Find all unvisited neighbors."""
        neighbors = []
        
        if x > 0 and not self.maze[y][x-1].visited and not self.maze[y][x-1]._42_path:
            neighbors.append((x-1, y, "left"))
        if x < self.x-1 and not self.maze[y][x+1].visited and not self.maze[y][x+1]._42_path:
            neighbors.append((x+1, y, "right"))
        if y > 0 and not self.maze[y-1][x].visited and not self.maze[y-1][x]._42_path:
            neighbors.append((x, y-1, "top"))
        if y < self.y-1 and not self.maze[y+1][x].visited and not self.maze[y+1][x]._42_path:
            neighbors.append((x, y+1, "bottom"))
        
        return neighbors
    
    def _remove_wall(self, x1, y1, x2, y2, direction):
        """Remove wall between two cells."""
        if direction == "left":
            self.maze[y1][x1].west = False
            self.maze[y2][x2].east = False
        elif direction == "right":
            self.maze[y1][x1].east = False
            self.maze[y2][x2].west = False
        elif direction == "top":
            self.maze[y1][x1].north = False
            self.maze[y2][x2].south = False
        elif direction == "bottom":
            self.maze[y1][x1].south = False
            self.maze[y2][x2].north = False
    
    # ========== 42 PATTERN ==========
    def _create_42_pattern(self):
        """Create '42' pattern in the center of the maze."""
        cx = self.x // 2 - 3
        cy = self.y // 2 - 3

        # --- mark all 42 cells as visited so backtracker won't overwrite ---
        for y in range(self.y):
            for x in range(self.x):
                if self.maze[y][x]._42_path:
                    self.maze[y][x].visited = True

        # --- connect top-left of 42 to outside so validator passes ---
        if cy - 1 >= 0:
            self.maze[cy][cx].north = False
            self.maze[cy - 1][cx].south = False
        
    def _add_loops(self):
        """Randomly remove walls to create loops (imperfect maze)."""
        import random
        num_loops = max(1, (self.x * self.y) // 20)  # adjust density

        for _ in range(num_loops):
            x = random.randint(0, self.x - 2)
            y = random.randint(0, self.y - 2)
            # randomly pick horizontal or vertical neighbor
            if random.choice([True, False]) and x < self.x - 1:
                # remove east wall
                self.maze[y][x].east = False
                self.maze[y][x+1].west = False
            elif y < self.y - 1:
                # remove south wall
                self.maze[y][x].south = False
                self.maze[y+1][x].north = False
