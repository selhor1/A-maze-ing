import sys
import os
import time
import random
from config import load_config, ConfigError, Config
from mazegen import MazeGenerator
from mazegen.show_path import Solver
from mazegen.playmode import PlayMode
from renderer import render_ascii, PALETTES
from mazegen.generator import N, E, S, W
from typing import List, Tuple


def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    os.system("clear")


def generate_and_render(
    config: Config,
    pal_idx: int
) -> Tuple[MazeGenerator, List[List[int]], int]:
    """
    Generate a maze and render it step-by-step with animation.

    Parameters:
    - config: Config object containing maze settings
              (width, height, entry, exit, seed, perfect).
    - pal_idx: Index of the selected color palette.

    Returns:
    - Tuple containing:
        - MazeGenerator instance used to generate the maze.
        - Final grid as a 2D list of integers.
        - The seed value used for generation.
    """
    s = config.seed if config.seed is not None else random.randint(0, 999999)
    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        seed=s,
    )
    pal = PALETTES[pal_idx]
    theme = {"walls": pal["walls"], "inner": pal["inner"],
             "pattern": pal["pattern"]}

    for grid, current_cell in generator.generate_animated(
         perfect=config.perfect):
        clear_screen()
        render_ascii(
            grid,
            config.entry,
            config.exit,
            theme,
            show_42=True,
            current_cell=current_cell
        )
        time.sleep(0.03)

    grid = generator.get_cells()
    return generator, grid, s


def save_maze_to_file_hex(
    grid: List[List[int]],
    config: Config
) -> None:
    """Save maze to file using hex digits, then entry, exit, shortest path."""
    lines = []

    for row in grid:
        line = "".join(f"{cell:X}" for cell in row)
        lines.append(line)

    lines.append("")
    lines.append(f"{config.entry[0]} {config.entry[1]}")
    lines.append(f"{config.exit[0]} {config.exit[1]}")
    path_dirs = Solver.solve_bfs(
        grid=grid,
        entry=config.entry,
        exit_=config.exit
    )
    dir_map = {N: "N", E: "E", S: "S", W: "W"}
    path_str = "".join(dir_map[d] for d in path_dirs)
    lines.append(path_str)
    with open(config.output_file, "w") as f:
        f.write("\n".join(lines) + "\n")


BLUE = "\033[34m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
YELLOW = "\033[33m"


def main() -> None:
    """
    Main entry point of the program.
    Loads configuration, generates the maze, displays it,
    and provides a menu for regenerating, solving, or playing the maze.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        from animations import show_intro
        config = load_config(sys.argv[1])
        pal_idx = 0
        show_intro()
        generator, grid, seed = generate_and_render(config, pal_idx)
        save_maze_to_file_hex(grid, config)

        path_cells = None
        pal = PALETTES[pal_idx]
        theme = {
            "walls": pal["walls"],
            "inner": pal["inner"],
            "pattern": pal["pattern"],
        }

        while True:
            print(f"{BLUE} ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
            print(f"{BLUE} ▌            ▌            ▌          ▌{RESET}")
            print(f"{BLUE} ▌{RESET} [R]{RED} Regen{RESET}  {BLUE}▌{RESET} [S]"
                  f"{RED} Solve{RESET}  {BLUE}▌{RESET} [P]{RED} Play{RESET} "
                  f"{BLUE}▌{RESET}")
            print(f"{BLUE} ▌            ▌            ▌          ▌{RESET}")
            print(f"{BLUE} ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")
            print(f"{BLUE} ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
            print(f"{BLUE} ▌            ▌            ▌          ▌{RESET}")
            print(f"{BLUE} ▌{RESET} [C]{RED} Theme {RESET} {BLUE}▌{RESET} [I]"
                  f"{RED} Info  {RESET} {BLUE}▌{RESET} [Q] {RED}Quit{RESET}"
                  f" {BLUE}▌{RESET}")
            print(f"{BLUE} ▌            ▌            ▌          ▌{RESET}")
            print(f"{BLUE} ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}")
            choice = input("> ").strip().lower()
            if choice == "q":
                break
            elif choice == "r":
                generator, grid, seed = generate_and_render(config, pal_idx)
                save_maze_to_file_hex(grid, config)
                path_cells = None
            elif choice == "s":
                if path_cells:
                    path_cells = None
                    clear_screen()
                    render_ascii(grid, config.entry, config.exit, theme,
                                 show_42=True)
                    continue
                path_dirs = Solver.solve_bfs(
                    grid=grid,
                    entry=config.entry,
                    exit_=config.exit
                )
                cells = Solver.path_to_cells(config.entry, path_dirs)
                visible = set()
                for c in cells[1:-1]:
                    visible.add(c)
                    clear_screen()
                    render_ascii(
                        grid,
                        config.entry,
                        config.exit,
                        theme,
                        show_42=True,
                        path_cells=visible
                    )
                    time.sleep(0.05)
                path_cells = set(cells)
            elif choice == "p":
                PlayMode.play(
                    maze=generator,
                    entry=config.entry,
                    exit_=config.exit,
                    theme=theme
                )
            elif choice == "c":
                pal_idx = (pal_idx + 1) % len(PALETTES)
                clear_screen()
                pal = PALETTES[pal_idx]
                theme = {
                    "walls": pal["walls"],
                    "inner": pal["inner"],
                    "pattern": pal["pattern"],
                }
                render_ascii(grid, config.entry, config.exit, theme,
                             show_42=True)
            elif choice == "i":
                text = [
                    "░▀█▀░█▀█░█▀▀░█▀█",
                    "░░█░░█░█░█▀▀░█░█",
                    "░▀▀▀░▀░▀░▀░░░▀▀▀",
                ]
                print()
                for line in text:
                    print(f"{BLUE}{line}{RESET}")
                    time.sleep(0.1)
                time.sleep(0.5)
                print(f"\n\n{YELLOW}Theme: {PALETTES[pal_idx]['name']}")
                print(f"Parametre Configuration:{RESET}\n  - entry: "
                      f"{config.entry}   - exit: {config.exit}\n  - width: "
                      f"{config.width}       - height: {config.height}\n"
                      f"  - Output_file: {config.output_file}")
                if config.perfect:
                    print("  - Perfect maze")
                else:
                    print("  - Non perfect maze")
                print(f"{YELLOW}Seed maze: {seed} {RESET}\n\n")

            else:
                continue
    except ConfigError as error:
        print(f"Configuration error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error {e}")
    except KeyboardInterrupt:
        clear_screen()
        print("Exiting the game")
