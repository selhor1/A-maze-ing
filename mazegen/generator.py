import random
from typing import List, Tuple, Set, Optional

N, E, S, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}


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

        self.grid: List[List[int]] = [
            [N | E | S | W for _ in range(width)]
            for _ in range(height)
        ]
        self.visited: List[List[bool]] = [
            [False for _ in range(width)]
            for _ in range(height)
        ]

        self.blocked = self._create_42_pattern()

    def _create_42_pattern(self) -> Set[Tuple[int, int]]:
        """Return coordinates for 42 pattern."""
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

    def _break_random_walls(self, extra_paths: int = None) -> None:
        """
        Break random walls to create extra paths, but:
        - corridors stay max 2 cells wide/height
        - avoids merging too many open cells
        """
        if extra_paths is None:
            extra_paths = int((self.width * self.height) / 10)

        added = 0
        attempts = 0
        max_attempts = extra_paths * 20

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
                        # Check if breaking creates a 3x3 open area
                        open_count = 0
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                tx, ty = nx + dx, ny + dy
                                if 0 <= tx < self.width and 0 <= ty < self.height:
                                    if self.grid[ty][tx] != (N | E | S | W):
                                        open_count += 1
                        if open_count > 4:
                            # Too many adjacent open cells → skip
                            continue

                        self.remove_wall((x, y), (nx, ny))
                        added += 1
                        break
            attempts += 1

    def generate_animated(self, perfect: bool = True):
        """Generate maze with animation, yields grid each step."""

        visited = set()
        blocked = self.blocked
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

    def get_cells(self) -> List[List[int]]:
        """Return a copy of the grid, keeping blocked cells fully walled."""
        grid_copy = [row[:] for row in self.grid]
        for x, y in self.blocked:
            grid_copy[y][x] = N | E | S | W
        return grid_copy
