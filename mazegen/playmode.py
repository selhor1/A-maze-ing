import os
import time
from typing import TYPE_CHECKING, Tuple, Dict

from mazegen.generator import E, N, S, W
from renderer import render_ascii, get_42_pattern_coords

if TYPE_CHECKING:
    from mazegen.generator import MazeGenerator


class PlayMode:
    """
    Interactive maze play mode WITHOUT bonuses.
    Player has 3 hearts; wrong moves remove a heart.
    Theme colors are passed dynamically.
    """

    @staticmethod
    def play(
        maze: "MazeGenerator",
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        theme: Dict[str, str],   # <-- pass current theme
    ) -> None:
        """
        Start interactive play mode.
        Move with WASD, lose hearts on invalid moves.
        """
        os.system("cls" if os.name == "nt" else "clear")
        intro_text = "\033[1;31mHurry Up! Find the Exit!\033[0m"
        for c in intro_text:
            print(c, end="", flush=True)
            time.sleep(0.05)
        print()
        time.sleep(1)

        px, py = entry
        goal_x, goal_y = exit_
        steps = 0
        hearts = ["\033[1;31m\u2665\033[0m"] * 3  # fixed 3 hearts

        while True:
            # Clear screen once per loop
            os.system("cls" if os.name == "nt" else "clear")
        
            # --- Maze and status ---
            maze_cells = maze.get_cells()  # single copy for this iteration
        
            # Prepare 42 pattern dots
            p42 = get_42_pattern_coords(maze.width, maze.height)
            visited_temp = [[None for _ in range(maze.width)] for _ in range(maze.height)]
            for x, y in p42:
                visited_temp[y][x] = "•"
        
            # Mark current player position
            visited_temp[py][px] = "@"
        
            # Display hearts and steps
            hearts_display = " ".join(hearts)
            status_bar = f"[ {hearts_display} ]  Steps: {steps}  Exit: ({goal_x},{goal_y})"
            border = "═" * len(status_bar)
        
            print(f"╔{border}╗")
            print(f"║{status_bar}║")
            print(f"╚{border}╝")
        
            # Fun instruction line
            print("Guide the mouse 🐁 with W/A/S/D. Can you escape to the cheese 🧀?\n")
        
            # Render the maze
            render_ascii(
                maze_cells,
                entry=(px, py),
                exit_=exit_,
                origin_theme=theme,
                show_42=True,
                visited=visited_temp
            )
        
            # Current cell for wall checking
            current_cell = maze_cells[py][px]
        
            # Check if reached exit
            if (px, py) == (goal_x, goal_y):
                print("\033[92mCongrats! You reached the exit!\033[0m")
                time.sleep(1.5)
                break
            
            # --- Movement input ---
            move = input("Move (W/A/S/D or 'exit'): ").strip().lower()
            moved = False
        
            if move == "w" and not (current_cell & N):
                py -= 1
                moved = True
            elif move == "s" and not (current_cell & S):
                py += 1
                moved = True
            elif move == "a" and not (current_cell & W):
                px -= 1
                moved = True
            elif move == "d" and not (current_cell & E):
                px += 1
                moved = True
            elif move == "exit":
                print("Exiting play mode.")
                break
            else:
                # Invalid move → lose one heart
                print("\033[91mInvalid move! You lose a heart.\033[0m")
                if hearts:
                    hearts.pop()
                    time.sleep(0.5)
                if not hearts:
                    print("\033[91mGame Over! You ran out of hearts.\033[0m")
                    break

            if moved:
                steps += 1
