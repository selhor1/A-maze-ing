from mazegen.generator import MazeGenerator
from maze.pathfinder import pathfinder

# -------------------------------
# Console visualization function
# -------------------------------
def print_maze(maze):
    for row in maze:
        line = ""
        for cell in row:
            if cell._42_path:
                line += "42"  # 42 pattern
            elif cell.north or cell.south or cell.east or cell.west:
                line += "##"  # wall exists somewhere → treat as blocked
            else:
                line += "  "  # open path
        print(line)
    print("\n")
# -------------------------------
def main():
    cols, rows = 15, 15
    entry = (0, 0)
    exit = (14, 14)

    # Generate perfect maze
    generator_perfect = MazeGenerator(cols, rows, entry, exit, "perfect_maze.txt")
    generator_perfect.perfect = True
    generator_perfect.generate()
    path = pathfinder(generator_perfect.maze, entry, exit, cols, rows)
    generator_perfect.save(path)
    print("Perfect maze generated and saved!")
    print_maze(generator_perfect.maze)  # <-- visualize in console

    # Generate imperfect maze
    generator_imperfect = MazeGenerator(cols, rows, entry, exit, "imperfect_maze.txt")
    generator_imperfect.perfect = False
    generator_imperfect.generate()
    path2 = pathfinder(generator_imperfect.maze, entry, exit, cols, rows)
    generator_imperfect.save(path2)
    print("Imperfect maze generated and saved!")
    print_maze(generator_imperfect.maze)  # <-- visualize in console

if __name__ == "__main__":
    main()