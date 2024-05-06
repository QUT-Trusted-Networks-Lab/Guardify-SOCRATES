import os
import yaml
import curses
from src.ui.dashboard import run_tui

def main(stdscr):

    # Run the TUI (Text User Interface), passing the configuration as needed
    run_tui(stdscr)  # Ensure that run_tui is prepared to accept the config argument

if __name__ == "__main__":
    # Start the application using curses.wrapper to handle initialization and cleanup
    curses.wrapper(main)

