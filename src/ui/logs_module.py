import os
import curses

# Base and Logs directories setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

def get_log_categories():
    """Get log categories from the logs directory."""
    try:
        return [d for d in os.listdir(LOGS_DIR) if os.path.isdir(os.path.join(LOGS_DIR, d))]
    except FileNotFoundError:
        return ["Error: Log directory not found"]

def get_logs_for_category(category):
    """Get a list of logs for a specific category."""
    category_path = os.path.join(LOGS_DIR, category)
    try:
        return os.listdir(category_path)
    except FileNotFoundError:
        return ["Error: Category not found"]

def draw_menu(stdscr, title, items, selected_idx):
    """Draw menu of items on the screen."""
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(1, w//2 - len(title)//2, title)
    stdscr.attroff(curses.color_pair(2))

    for idx, item in enumerate(items):
        x = w//2 - len(item)//2
        y = h//2 - len(items)//2 + idx
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)

    stdscr.addstr(h-1, 0, "Press 'enter' to select, 'q' to go back")
    stdscr.refresh()

def view_log(stdscr, category, log_name):
    """Display the content of a log with scrolling."""
    log_path = os.path.join(LOGS_DIR, category, log_name)
    stdscr.clear()
    try:
        with open(log_path, 'r') as file:
            log_lines = file.readlines()

        max_y, max_x = stdscr.getmaxyx()
        current_line = 0

        while True:
            stdscr.clear()
            for i in range(max_y - 1):  # Leave a line for instructions or navigation
                if current_line + i < len(log_lines):
                    stdscr.addstr(i, 0, log_lines[current_line + i].strip())

            stdscr.addstr(max_y - 1, 0, "Press 'q' to go back, UP/DOWN to scroll")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_UP and current_line > 0:
                current_line -= 1
            elif key == curses.KEY_DOWN and current_line + max_y - 1 < len(log_lines):
                current_line += 1

    except FileNotFoundError:
        stdscr.addstr(0, 0, "Log file not found.")
        stdscr.getch()


def delete_log(stdscr, category, log_name):
    """Delete a specified log."""
    confirmation = "Are you sure you want to delete {}? [y/N] ".format(log_name)
    stdscr.clear()
    stdscr.addstr(0, 0, confirmation)
    key = stdscr.getch()
    if chr(key).lower() == 'y':
        try:
            os.remove(os.path.join(LOGS_DIR, category, log_name))
            stdscr.addstr(1, 0, "Log deleted successfully.")
        except OSError as e:
            stdscr.addstr(1, 0, "Error deleting log: {}".format(e))
    stdscr.getch()

def log_options(stdscr, category, log_name):
    """Provide options to view or delete a log."""
    options = ["View Log", "Delete Log"]
    current_option = 0
    while True:
        draw_menu(stdscr, f"Log: {log_name}", options, current_option)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(options) - 1:
            current_option += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_option == 0:  # View Log
                view_log(stdscr, category, log_name)
            elif current_option == 1:  # Delete Log
                delete_log(stdscr, category, log_name)
                break  # Exit after deletion to refresh the log list
        elif key == ord('q'):
            break

def view_logs_for_category(stdscr, category):
    """View logs in a specific category and interact with them."""
    logs = get_logs_for_category(category)
    current_row = 0
    while True:
        draw_menu(stdscr, f"Logs in {category}", logs, current_row)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(logs) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            log_options(stdscr, category, logs[current_row])
            logs = get_logs_for_category(category)  # Refresh logs list
        elif key == ord('q'):
            break

def logs_module(stdscr):
    """Main logs module interface."""
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    categories = get_log_categories()
    current_row = 0
    while True:
        draw_menu(stdscr, "Log Categories", categories, current_row)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(categories) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            view_logs_for_category(stdscr, categories[current_row])
        elif key == ord('q'):
            break
