import random
from typing import List, Tuple, Set, Optional

# Direction bitmasks
N, E, S, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {N: S, S: N, E: W, W: E}


class MazeGenerator:
    """Generate a perfect maze using DFS with animated generation."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int] = (0, 0),
        exit: Tuple[int, int] = (0, 0),
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.rng = random.Random(seed)

        # Grid: each cell holds wall bitmask
        self.grid: List[List[int]] = [
            [N | E | S | W for _ in range(width)] for _ in range(height)
        ]
        self.visited: List[List[bool]] = [
            [False for _ in range(width)] for _ in range(height)
        ]

        # Blocked cells for the "42" pattern
        self.blocked = self._create_42_pattern()

    # -----------------------------

    def _create_42_pattern(self) -> Set[Tuple[int, int]]:
        """Return coordinates for 42 pattern."""
        if self.width < 7 or self.height < 5:
            return set()

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        pattern = [
            "1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111",
        ]

        blocked: Set[Tuple[int, int]] = set()
        for dy, row in enumerate(pattern):
            for dx, char in enumerate(row):
                if char == "1":
                    blocked.add((start_x + dx, start_y + dy))
        return blocked

    # -----------------------------

    def get_unvisited_neighbors(self, x: int, y: int, visited: set) -> list:
        """Return unvisited neighbors for DFS."""
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in visited:
                    neighbors.append((nx, ny))
        return neighbors

    # -----------------------------

    def remove_wall(self, a: Tuple[int, int], b: Tuple[int, int]) -> None:
        """Remove wall between two adjacent cells."""
        x1, y1 = a
        x2, y2 = b
        if x2 == x1 + 1:
            self.grid[y1][x1] &= ~E
            self.grid[y2][x2] &= ~W
        elif x2 == x1 - 1:
            self.grid[y1][x1] &= ~W
            self.grid[y2][x2] &= ~E
        elif y2 == y1 + 1:
            self.grid[y1][x1] &= ~S
            self.grid[y2][x2] &= ~N
        elif y2 == y1 - 1:
            self.grid[y1][x1] &= ~N
            self.grid[y2][x2] &= ~S

    # -----------------------------

    def generate_animated(self, perfect: bool = True):
        """Iterative DFS with animation."""
        visited = set()
        entry = self.entry
        exit_ = self.exit

        # Temporary blocked set that never blocks entry/exit
        blocked = self.blocked.copy()
        blocked.discard(entry)
        blocked.discard(exit_)

        stack = [entry]
        visited.add(entry)

        while stack:
            cx, cy = stack[-1]

            # Exclude blocked "42" cells except entry/exit
            neighbors = [
                (nx, ny)
                for nx, ny in self.get_unvisited_neighbors(cx, cy, visited)
                if (nx, ny) not in blocked
            ]

            if neighbors:
                nx, ny = self.rng.choice(neighbors)
                self.remove_wall((cx, cy), (nx, ny))
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

            # Yield a copy of the grid and current cell for animation
            yield [row[:] for row in self.grid], (cx, cy)
        if not perfect:
            self._add_loops()
            # -----------------------------

    def generate(self, perfect: bool = True) -> None:
        """Non-animated DFS generation for final maze.
           If perfect=False, extra walls are removed to create loops."""

        # mark blocked 42 cells
        for x, y in self.blocked:
            self.visited[y][x] = True
            self.grid[y][x] = N | E | S | W  # block completely

        # Ensure entry and exit are not blocked
        for cell in [self.entry, self.exit]:
            if cell in self.blocked:
                self.blocked.remove(cell)

        # Generate perfect maze
        sx, sy = self.entry
        self._dfs_iterative(sx, sy)

        if not perfect:
            self._add_loops()

    def _dfs_iterative(self, start_x: int, start_y: int) -> None:
        """Iterative DFS to generate maze instead of recursive DFS."""
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True
    
        while stack:
            cx, cy = stack[-1]
    
            dirs = [N, E, S, W]
            self.rng.shuffle(dirs)
            moved = False
    
            for d in dirs:
                nx, ny = cx + DX[d], cy + DY[d]
    
                # Skip blocked cells
                if (nx, ny) in self.blocked:
                    continue
                
                # Check bounds and unvisited
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.visited[ny][nx]:
                        # Remove walls
                        self.grid[cy][cx] &= ~d
                        self.grid[ny][nx] &= ~OPPOSITE[d]
    
                        # Mark visited and push to stack
                        self.visited[ny][nx] = True
                        stack.append((nx, ny))
                        moved = True
                        break  # move to the next cell immediately
                    
            if not moved:
                # Dead end, backtrack
                stack.pop()

    # -----------------------------

    def get_cells(self) -> List[List[int]]:
        """Return a copy of the grid, keeping blocked cells fully walled."""
        grid_copy = [row[:] for row in self.grid]
        for x, y in self.blocked:
            grid_copy[y][x] = N | E | S | W
        return grid_copy
    
    def _add_loops(self):
        """Add more random loops to the maze for multiple paths."""
        num_loops = max(1, (self.width * self.height) // 5)  # more loops
        for _ in range(num_loops):
            x = self.rng.randint(0, self.width - 2)
            y = self.rng.randint(0, self.height - 2)
            directions = [N, E, S, W]
            self.rng.shuffle(directions)
            for d in directions:
                nx, ny = x + DX[d], y + DY[d]
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) in self.blocked:
                        continue
                    # Only remove if there is still a wall
                    if self.grid[y][x] & d:
                        self.grid[y][x] &= ~d
                        self.grid[ny][nx] &= ~OPPOSITE[d]
                        break
