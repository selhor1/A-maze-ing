"""Maze export module - Hex format and file output."""

class MazeExporter:
    """Exports maze to hex format and files."""
    
    @staticmethod
    def cell_to_hex(cell):
        """Convert cell walls to hex digit."""
        value = 0
        if cell.north: value |= 8
        if cell.east: value |= 4
        if cell.south: value |= 2
        if cell.west: value |= 1
        return f"{value:X}"
    
    @staticmethod
    def path_to_directions(path):
        """Convert coordinate path to direction string."""
        if not path or len(path) < 2:
            return ""
        d = ""
        x1, y1 = path[0]
        for i in range(1, len(path)):
            x2, y2 = path[i]
            if x1 == x2 and y1 - 1 == y2: d += "N"
            elif x1 == x2 and y1 + 1 == y2: d += "S"
            elif x1 - 1 == x2 and y1 == y2: d += "W"
            elif x1 + 1 == x2 and y1 == y2: d += "E"
            x1, y1 = path[i]
        return d
    
    @staticmethod
    def save_to_file(filename, maze, width, height, entry, exit, path):
        """Save maze to file in required format."""
        with open(filename, "w") as f:
            for y in range(height):
                for x in range(width):
                    f.write(MazeExporter.cell_to_hex(maze[y][x]))
                f.write("\n")
            f.write(f"\n{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(f"{MazeExporter.path_to_directions(path)}\n")