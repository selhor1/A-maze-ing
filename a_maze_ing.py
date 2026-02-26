import sys
import os
import time
import tty
import termios
import random
# from typing import List, Tuple, Dict, Any
from animations import show_intro
from config import load_config, ConfigError
from mazegen import MazeGenerator
from mazegen.show_path import Solver
from mazegen.playmode import PlayMode
# Import PALETTES and render_ascii from your renderer
from renderer import render_ascii, PALETTES
from mazegen.generator import N, E, S, W

# ===== TERMINAL HELPERS =====


def clear_screen() -> None:
    os.system("clear")


def get_key() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == "\x1b":
            sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch3
        return ch1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
# ===== UPDATED GENERATE & RENDER =====


def generate_and_render(config, pal_idx, animate=True):
    seed_to_use = config.seed if config.seed is not None else random.randint(0, 999999)
    
    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        seed=seed_to_use,
    )

    pal = PALETTES[pal_idx]
    theme = {"walls": pal["walls"], "inner": pal["inner"],
             "pattern": pal["pattern"]}

    if animate:
        for grid, current_cell in generator.generate_animated(perfect=config.perfect):
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
    else:
        generator.generate(perfect=config.perfect)

    grid = generator.get_cells()
    return generator, grid


def save_maze_to_file_hex(grid, config):
    """Save maze as hex with size and entry/exit at top."""
    lines = []
    lines.append(f"{config.width} {config.height}")          # width & height
    lines.append(f"{config.entry[0]} {config.entry[1]}")    # entry
    lines.append(f"{config.exit[0]} {config.exit[1]}")      # exit

    for row in grid:
        line = " ".join(f"{cell:X}" for cell in row)        # hex for each cell
        lines.append(line)

    with open(config.output_file, "w") as f:
        f.write("\n".join(lines))
    print(f"\033[32mMaze saved to {config.output_file} in subject format\033[0m")

# ANSI color codes
BLUE = "\033[34m"    # walls
RED = "\033[31m"     # some text
GREEN = "\033[32m"   # other text
RESET = "\033[0m"    # reset
YELLOW = "\033[33m"

# ===== MAIN =====


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        config = load_config(sys.argv[1])
        pal_idx = 0
        # Show intro animation first
        show_intro()
        generator, grid = generate_and_render(config, pal_idx, animate=True)
        save_maze_to_file_hex(grid, config)
        path_cells = None
        pal = PALETTES[pal_idx]
        theme = {
            "walls": pal["walls"],
            "inner": pal["inner"],
            "pattern": pal["pattern"],
        }
        while True:
            print(f"\n{YELLOW}Created by masselgu & selhor"
                  "\nTeam: Wlad Lkhayriya")
            print(f"\n\n\n\n {GREEN}Theme: {PALETTES[pal_idx]['name']}")
            print(f"{BLUE} ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
                  f"▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
            print(f"{BLUE} ▌            ▌            ▌           ▌          "
                  f"  ▌           ▌{RESET}")
            print(f"{BLUE} ▌{RESET} [R]{RED} Regen{RESET}  {BLUE}▌{RESET} [S]"
                  f"{RED} Solve{RESET}  {BLUE}▌{RESET} [P]{RED} Play{RESET}  "
                  f"{BLUE}▌{RESET} [C]{RED} Theme{RESET}  {BLUE}▌{RESET} [Q]"
                  f"{RED} Quit{RESET}  {BLUE}▌{RESET}")
            print(f"{BLUE} ▌            ▌            ▌           ▌          "
                  f"  ▌           ▌{RESET}")
            print(f"{BLUE} ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
                  f"▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}")
            choice = input("> ").strip().lower()   # ← wait Enter
            if choice == "q":
                break
            elif choice == "r":
                # regenerate maze
                generator, grid = generate_and_render(config, pal_idx)
                path_cells = None
            elif choice == "s":
                # 🔹 If path already visible → hide it
                if path_cells:
                    path_cells = None
                    clear_screen()
                    render_ascii(grid, config.entry, config.exit, theme,
                                 show_42=True)
                    continue
                # 🔹 Compute path
                path_dirs = Solver.solve_bfs(
                    grid=grid,
                    entry=config.entry,
                    exit_=config.exit
                )
                cells = Solver.path_to_cells(config.entry, path_dirs)
                visible = set()
                # 🔹 Animate one point after another
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
                # 🔹 Remember path so next S hides it
                path_cells = set(cells)
            elif choice == "p":
                PlayMode.play(
                    maze=generator,  # pass your MazeGenerator object
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
            else:
                continue
    except ConfigError as error:
        print(f"Configuration error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
