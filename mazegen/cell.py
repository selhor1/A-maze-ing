"""Cell class for maze representation."""


class Cell:
    """Represents a single cell in the maze with 4 walls."""
    
    def __init__(self):
        """Initialize with all walls closed and not visited."""
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.visited = False
        self._42_path = False