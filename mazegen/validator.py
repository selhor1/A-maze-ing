"""Maze validation module."""


class MazeValidator:
    """Validates maze connectivity and structure."""
    
    @staticmethod
    def is_fully_connected(maze, entry, width, height):
        """Check if all cells are reachable from entry."""
        visited = [[False for _ in range(width)] for _ in range(height)]
        stack = [entry]
        ex, ey = entry
        visited[ey][ex] = True
        count = 1
        
        while stack:
            x, y = stack.pop()
            cell = maze[y][x]
            
            if not cell.east and x+1 < width and not visited[y][x+1]:
                visited[y][x+1] = True
                count += 1
                stack.append((x+1, y))
            if not cell.west and x-1 >= 0 and not visited[y][x-1]:
                visited[y][x-1] = True
                count += 1
                stack.append((x-1, y))
            if not cell.south and y+1 < height and not visited[y+1][x]:
                visited[y+1][x] = True
                count += 1
                stack.append((x, y+1))
            if not cell.north and y-1 >= 0 and not visited[y-1][x]:
                visited[y-1][x] = True
                count += 1
                stack.append((x, y-1))
        
        return count == width * height
    
    @staticmethod
    def entry_exit_valid(entry, exit, width, height):
        """Check if entry and exit are valid."""
        if entry == exit:
            return False
        ex, ey = entry
        sx, sy = exit
        if not (0 <= ex < width and 0 <= ey < height):
            return False
        if not (0 <= sx < width and 0 <= sy < height):
            return False
        return True