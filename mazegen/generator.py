import random
from typing import List, Tuple, Set, Optional

# -----------------------------
# Direction bitmasks
N, E, S, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {N: S, S: N, E: W, W: E}
# -----------------------------


class MazeGenerator:
    """Generate perfect or imperfect maze using DFS with optional animation."""

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

        # Grid: each cell stores wall bitmask
        self.grid: List[List[int]] = [
            [N | E | S | W for _ in range(width)]
            for _ in range(height)
        ]
        self.visited: List[List[bool]] = [
            [False for _ in range(width)]
            for _ in range(height)
        ]

        # Blocked cells for "42" pattern
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
    def _dfs_iterative(self, start_x: int, start_y: int) -> None:
        """Iterative DFS to generate maze."""
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            cx, cy = stack[-1]
            dirs = [N, E, S, W]
            self.rng.shuffle(dirs)
            moved = False

            for d in dirs:
                nx, ny = cx + DX[d], cy + DY[d]
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.visited[ny][nx] and (nx, ny) not in self.blocked:
                        self.remove_wall((cx, cy), (nx, ny))
                        self.visited[ny][nx] = True
                        stack.append((nx, ny))
                        moved = True
                        break

            if not moved:
                stack.pop()

    # -----------------------------
    def _break_random_walls(self, extra_paths: int = None) -> None:
        """
        Imperfect maze logic: break walls to create extra paths.
        Guaranteed to create actual new connections.
        """
        if extra_paths is None:
            extra_paths = int((self.width * self.height) / 10)

        added = 0
        attempts = 0
        max_attempts = extra_paths * 10  # safety to prevent infinite loop

        while added < extra_paths and attempts < max_attempts:
            x = self.rng.randint(0, self.width - 1)
            y = self.rng.randint(0, self.height - 1)
            directions = [N, E, S, W]
            self.rng.shuffle(directions)

            for d in directions:
                nx, ny = x + DX[d], y + DY[d]
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Skip blocked or entry/exit
                    if (x, y) in self.blocked or (nx, ny) in self.blocked:
                        continue
                    if (x, y) in [self.entry, self.exit] or (nx, ny) in [self.entry, self.exit]:
                        continue
                    # Only break if wall exists
                    if self.grid[y][x] & d:
                        self.remove_wall((x, y), (nx, ny))
                        added += 1
                        break
            attempts += 1

    # -----------------------------
    def generate(self, perfect: bool = True) -> None:
        """Generate maze without animation."""

        # Ensure entry/exit not blocked
        for cell in [self.entry, self.exit]:
            self.blocked.discard(cell)

        # Block 42 cells
        for x, y in self.blocked:
            self.visited[y][x] = True
            self.grid[y][x] = N | E | S | W

        # Generate perfect maze
        sx, sy = self.entry
        self._dfs_iterative(sx, sy)

        # If imperfect → break random walls
        if not perfect:
            self._break_random_walls()

    # -----------------------------
    def generate_animated(self, perfect: bool = True):
        """Generate maze with animation, yields grid each step."""

        visited = set()
        blocked = self.blocked.copy()
        blocked.discard(self.entry)
        blocked.discard(self.exit)

        stack = [self.entry]
        visited.add(self.entry)

        while stack:
            cx, cy = stack[-1]

            neighbors = []
            for d in [N, E, S, W]:
                nx, ny = cx + DX[d], cy + DY[d]
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited and (nx, ny) not in blocked:
                        neighbors.append((nx, ny))

            if neighbors:
                nx, ny = self.rng.choice(neighbors)
                self.remove_wall((cx, cy), (nx, ny))
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

            yield [row[:] for row in self.grid], (cx, cy)

        if not perfect:
            self._break_random_walls()
            yield [row[:] for row in self.grid], None

    # -----------------------------
    def get_cells(self) -> List[List[int]]:
        """Return a copy of the grid, keeping blocked cells fully walled."""
        grid_copy = [row[:] for row in self.grid]
        for x, y in self.blocked:
            grid_copy[y][x] = N | E | S | W
        return grid_copy
