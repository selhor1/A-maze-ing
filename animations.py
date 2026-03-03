from a_maze_ing import clear_screen
import time


BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"

BIG_TEXT = [
    (" █████╗       ███╗   ███╗ █████╗ ███████╗███████╗    ██╗"
     "███╗   ██╗ ██████╗ "),
    ("██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝    ██║"
     "████╗  ██║██╔════╝ "),
    ("███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗█████╗██║"
     "██╔██╗ ██║██║  ███╗"),
    ("██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝╚════╝██║"
     "██║╚██╗██║██║   ██║"),
    ("██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗    ██║"
     "██║ ╚████║╚██████╔╝"),
    ("╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝"
     "╚═╝  ╚═══╝ ╚═════╝ "),
]

team = "Created by masselgu & selhor\nTeam: Wlad lkhayriya"


def animate_big_text(text_lines: list, delay: float = 0.1) -> None:
    """Show big anamation without return nothing"""
    for i, line in enumerate(text_lines, start=5):
        print(f"\033[{i};5H{BLUE}{line}{RESET}")
        time.sleep(delay)
    time.sleep(0.5)
    print("\n\n")
    for c in team:
        print(f"{YELLOW}{c}", end="", flush=True)
        time.sleep(delay)
    time.sleep(0.5)


def animate_loading_bar(width: int = 75, delay: float = 0.02) -> None:
    """Show loding bar anamation without return nothing"""
    print("\n\n")
    for i in range(width + 1):
        bar = f"[{'#' * i}{' ' * (width - i)}]"
        print(f"\r\033[30mLoading Maze {bar}{RESET}", end="", flush=True)
        time.sleep(delay)
    print("\n")


def show_intro() -> None:
    """call for the anamation function"""
    clear_screen()
    animate_big_text(BIG_TEXT)
    animate_loading_bar()
