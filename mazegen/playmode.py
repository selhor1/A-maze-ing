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
        theme: Dict[str, str],
    ) -> None:
        """
        Start interactive play mode.
        Move with WASD, lose hearts on invalid moves.
        """
        os.system("clear")

        px, py = entry
        goal_x, goal_y = exit_
        hearts = ["\033[1;31m\u2665\033[0m"] * 3

        while True:
            os.system("clear")
            maze_cells = maze.get_cells()
            p42 = get_42_pattern_coords(maze.width, maze.height)
            visited_temp = [[None for _ in range(maze.width)] for _ in range(maze.height)]
            for x, y in p42:
                visited_temp[y][x] = "•"        
            visited_temp[py][px] = "@"        
            hearts_display = " ".join(hearts)
            status_bar = f"hearts: [ {hearts_display} ] -- Move with (W/A/S/D -- leave with 'ex' "
            border = "═" * 59
        
            print("Guide the mouse 🐁 to the end. Can you escape to the cheese 🧀?")     
            print(f"     ╔{border}╗")
            print(f"     ║{status_bar}║")
            print(f"     ╚{border}╝")
            render_ascii(
                maze_cells,
                entry=(px, py),
                exit_=exit_,
                origin_theme=theme,
                show_42=True,
                visited=visited_temp
            )        
            current_cell = maze_cells[py][px]        
            if (px, py) == (goal_x, goal_y):
                print("\033[92mCongrats! You reached the exit!\033[0m")
                os.system("aplay win.wav &")
                time.sleep(1.5)
                break            
            move = input("> ").strip().lower()
        
            if move == "w" and not (current_cell & N):
                py -= 1
            elif move == "s" and not (current_cell & S):
                py += 1
            elif move == "a" and not (current_cell & W):
                px -= 1
            elif move == "d" and not (current_cell & E):
                px += 1
            elif move == "ex":
                print("Exiting play mode.")
                break
            else:
                print("\033[91mInvalid move! You lose a heart.\033[0m")
                if hearts:
                    hearts.pop()
                    time.sleep(0.5)
                if not hearts:
                    print("\033[91mGame Over! You ran out of hearts.\033[0m")
                    os.system("aplay lose.wav &")
                    break

