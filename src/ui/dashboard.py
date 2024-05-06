import curses
import os
from .logs_module import logs_module
import time
import locale

# Set the locale to support Unicode characters in the terminal
locale.setlocale(locale.LC_ALL, '')


# Function to count warnings in log files
def count_warnings_in_logs(log_directory):
    warnings_count = 0
    for log_file in os.listdir(log_directory):
        if log_file.endswith(".log"):
            with open(os.path.join(log_directory, log_file), 'r') as file:
                for line in file:
                    if 'WARNING' in line:
                        warnings_count += 1
    return warnings_count



def draw_monitoring_screen(stdscr, log_directories):
    # Setup color pairs for better visual distinction
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # For titles and highlights
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # For data
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # For instructions

    def center_text(width, text):
        return (width - len(text)) // 2

    # Function to draw a single log section
    def draw_log_section(y, x, width, title, count):
        centered_x = center_text(width, title)
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(y, x + centered_x, title, curses.A_BOLD)
        stdscr.attroff(curses.color_pair(4))

        data_text = f"Warnings: {count}"
        centered_data_x = center_text(width, data_text)
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(y + 1, x + centered_data_x, data_text)
        stdscr.attroff(curses.color_pair(5))

    stdscr.clear()
    stdscr.nodelay(True)  # Non-blocking input
    key = None

    main_title = "Guardify Surveillance Mode"

    while key != ord('q'):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Center the main title
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        main_title_x = center_text(width, main_title)
        stdscr.addstr(1, main_title_x, main_title)
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

        # Dynamically calculate layout based on terminal size
        section_width = width // 2 - 4
        x_positions = [2, width // 2 + 1]
        y_position = 4

        # Display log sections
        for i, (title, directory) in enumerate(log_directories.items()):
            count = count_warnings_in_logs(directory)
            draw_log_section(y_position + (i // 2) * 3 + 2, x_positions[i % 2], section_width, title, count)
            
        # Instructions (left-aligned at the bottom in yellow)
        stdscr.attron(curses.color_pair(6))
        stdscr.addstr(height - 1, 1, "Press 'q' to return", curses.A_DIM)
        stdscr.attroff(curses.color_pair(6))

        stdscr.refresh()
        time.sleep(1)  # Refresh the data every second
        stdscr.nodelay(True)
        key = stdscr.getch()

    stdscr.nodelay(False)


def check_terminal_size(stdscr, min_width, min_height):
    h, w = stdscr.getmaxyx()
    if w < min_width or h < min_height:
        stdscr.clear()
        stdscr.addstr(0, 0, "Please resize the terminal window to at least {}x{} and restart the application.".format(min_width, min_height))
        stdscr.refresh()
        stdscr.getkey()
        return False
    return True

def draw_title(stdscr):
    title = [
        "\u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2557   \u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2557   \u2588\u2588\u2557",
        "\u2588\u2588\u2554\u2550\u2550\u2550\u2550\u255d \u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2550\u2550\u255d\u255a\u2588\u2588\u2557 \u2588\u2588\u2554\u255d",
        "\u2588\u2588\u2551  \u2588\u2588\u2588\u2557\u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2557   \u255a\u2588\u2588\u2588\u2588\u2554\u255d ",
        "\u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u255d    \u255a\u2588\u2588\u2554\u255d  ",
        "\u255a\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u255a\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2551\u2588\u2588\u2551        \u2588\u2588\u2551   ",
        " \u255a\u2550\u2550\u2550\u2550\u2550\u255d  \u255a\u2550\u2550\u2550\u2550\u2550\u255d \u255a\u2550\u255d  \u255a\u2550\u255d\u255a\u2550\u255d  \u255a\u2550\u255d\u255a\u2550\u2550\u2550\u2550\u2550\u255d \u255a\u2550\u255d\u255a\u2550\u255d        \u255a\u2550\u255d   "
    ]

    subtitle = "Real-Time System Surveillance Powered with eBPF"

    h, w = stdscr.getmaxyx()
    y_offset = h//2 - len(title) - 2
    for idx, line in enumerate(title):
        x = w//2 - len(line)//2
        y = y_offset + idx
        stdscr.addstr(y, x, line, curses.color_pair(2))

    # Print subtitle below the title
    subtitle_x = w//2 - len(subtitle)//2
    subtitle_y = y_offset + len(title) + 1  # Positioning the subtitle
    stdscr.addstr(subtitle_y, subtitle_x, subtitle, curses.color_pair(3))  # Using a different color pair

def draw_status_bar(stdscr, msg):
    h, w = stdscr.getmaxyx()
    status_bar_str = msg
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(h-1, 0, status_bar_str)
    stdscr.addstr(h-1, len(status_bar_str), " " * (w - len(status_bar_str) - 1))
    stdscr.attroff(curses.color_pair(3))

def draw_menu(stdscr, menu_items, selected_idx, title_length):
    h, w = stdscr.getmaxyx()
    y_start = title_length + 3  # Adjust based on title + subtitle height and desired spacing
    for idx, item in enumerate(menu_items):
        x = w//2 - len(item)//2
        y = y_start + idx  # Starting position adjusted for menu items
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)

def run_tui(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    menu_items = ["Monitor", "Logs", "Info", "Exit"]
    current_row = 0

    # Set title_length based on the title, subtitle, and desired spacing
    title_length = 22 # Adjust this based on your actual title, subtitle, and spacing
    
    if not check_terminal_size(stdscr, 80, 24):  # Minimum terminal size of 80x24
        return  # Exit if the terminal is too small

    while True:
        stdscr.clear()
        draw_title(stdscr)
        draw_menu(stdscr, menu_items, current_row, title_length)
        draw_status_bar(stdscr, "Press Arrow keys to navigate, Enter to select.")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:  # "Monitor" selected
                log_directories = {
                            "File Path Access": "./logs/file_path_access_logs/",
                            "Network Activity": "./logs/network_activity_logs/",
                            "Obfuscation": "./logs/obfuscation_logs/",
                            "Typosquatting": "./logs/typo_squatting_logs/"
                            }
                draw_monitoring_screen(stdscr, log_directories)
            elif current_row == 1:  # "Logs" selected
                logs_module(stdscr)  # Make sure you've imported this at the top
            elif current_row == 2: # "Info" selected
                display_info(stdscr)
            elif current_row == 3: # "Exit" selected
                break

        stdscr.refresh()
        
def display_info(stdscr):
    stdscr.clear()
    info_text = [
        "Guardify Tool Information:",
        "Guardify is a tool which actively monitors and intercepts syscalls for",
        "advanced monitoring using eBPF. It provides real-time insights into",
        "system behavior and helps in detecting potential security threats.",
        "",
        "Developed by QUT-Trusted-Networks-Lab",
        "",
        "License: Still under consideration.",
        "",
        "Press any key to return."
    ]
    h, w = stdscr.getmaxyx()
    for idx, line in enumerate(info_text):
        x = w//2 - len(line)//2
        y = h//2 - len(info_text)//2 + idx
        stdscr.addstr(y, x, line)
    stdscr.refresh()
    stdscr.getkey()  # Wait for any key press

