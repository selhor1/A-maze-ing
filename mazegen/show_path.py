from typing import Dict, List, Tuple


N, E, S, W = 1, 2, 4, 8
DIRECTIONS = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
OPPOSITE = {N: S, S: N, E: W, W: E}


class Solver:
    @staticmethod
    def solve_bfs(
        grid: List[List[int]],
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
    ) -> List[int]:
        """BFS to get directions list (N,E,S,W)"""
        from collections import deque

        queue = deque([entry])
        visited = {entry}
        parent: Dict[Tuple[int, int], Tuple[int, int, int]] = {}

        while queue:
            x, y = queue.popleft()
            if (x, y) == exit_:
                break
            cell = grid[y][x]
            for direction, (dx, dy) in DIRECTIONS.items():
                if cell & direction:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y, direction)
                        queue.append((nx, ny))
        return Solver.generate_path(parent, entry, exit_)

    @staticmethod
    def generate_path(
        parent: Dict,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
    ) -> List[int]:
        """Convert BFS parent dict to direction path"""
        path = []
        current = exit_
        while current != entry:
            x, y, direction = parent[current]
            path.append(direction)
            current = (x, y)
        path.reverse()
        return path

    @staticmethod
    def path_to_cells(
        entry: Tuple[int, int],
        path: List[int],
    ) -> List[Tuple[int, int]]:
        x, y = entry
        cells = [(x, y)]
        for d in path:
            dx, dy = DIRECTIONS[d]
            x += dx
            y += dy
            cells.append((x, y))
        return cells
