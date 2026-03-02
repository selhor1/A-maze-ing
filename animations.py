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


def animate_big_text(text_lines: list, delay: float = 0.1):
    for i, line in enumerate(text_lines, start=5):
        print(f"\033[{i};5H{BLUE}{line}{RESET}")
        time.sleep(delay)
    time.sleep(0.5)
    print("\n\n")
    for i in team:
        print(f"{YELLOW}{i}", end="", flush=True)
        time.sleep(delay)
    time.sleep(0.5)


def animate_loading_bar(width=75, delay=0.02):
    print("\n\n")
    for i in range(width + 1):
        bar = f"[{'#' * i}{' ' * (width - i)}]"
        print(f"\r\033[30mLoading Maze {bar}{RESET}", end="", flush=True)
        time.sleep(delay)
    print("\n")


def show_intro():
    clear_screen()
    animate_big_text(BIG_TEXT)
    animate_loading_bar()
