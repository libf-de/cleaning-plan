import time
import schedule
import argparse
from datetime import datetime, date
from escpos.printer import Network
import math
import sys

# Cleaning tasks
WEEKLY_TASKS = [
    "Kuche: Schranke, Kuhlschrank abwischen, Mull runterbringen",
    "Bad: Waschbecken, Duschwanne, WC reinigen"
]

MONTHLY_TASKS = [
    "Kuche+Flur: Fussboden wischen",
    "Bad: Fussboden wischen"
]

QUARTERLY_TASKS = [
    "Kuche: Fenster putzen, Kuhlschrank abtauen"
]

def get_week_number():
    """Get the ISO week number of the current date."""
    return datetime.now().isocalendar()[1]

def get_month_number():
    """Get the month number of the current date."""
    return datetime.now().month

def get_quarter():
    """Get the current quarter of the year (1-4)."""
    return math.ceil(get_month_number() / 3)

def get_assigned_person(period_number):
    """Determine which person is assigned based on odd/even period number."""
    return "Person 1" if period_number % 2 == 1 else "Person 2"

def print_task(printer, task, task_type, assigned_person):
    """Print a single task on a separate printout."""
    # Print header
    current_date = date.today().strftime("%d.%m.%Y")
    printer.set(align='center', bold=False, double_height=False, double_width=False, normal_textsize=True)
    printer.text(f"{current_date}\n")
    printer.set(align='center', bold=True, custom_size=True, width=6, height=6)
    printer.text(f"{assigned_person}")
    printer.set(align='center', bold=False, double_height=False, double_width=False, normal_textsize=True)
    printer.text(f"\n\n")
    
    # Print task type
    # printer.set(align='center', bold=True)
    # printer.text(f"{task_type} TASK\n")
    
    # Print task - use bold instead of text_type
    printer.set(align='center', bold=True, width=2, height=2, custom_size=True)
    printer.text(f"{task}")
    
    # Cut the paper
    printer.cut()

def print_cleaning_plan(print_type=None):
    """
    Print the cleaning plan to the ESC/POS printer.
    
    Args:
        print_type (str, optional): Type of plan to print - 'week', 'month', 
                                   'quarter', or None for all applicable plans
    """
    try:
        # Connect to the network printer
        printer = Network("192.168.188.60")
        
        # Get current period numbers
        week_num = get_week_number()
        month_num = get_month_number()
        quarter = get_quarter()
        
        tasks_printed = 0
        
        # Print weekly tasks if no specific type is requested or 'week' is requested
        if print_type is None or print_type == 'week':
            weekly_person = get_assigned_person(week_num)
            for task in WEEKLY_TASKS:
                print_task(printer, task, "WEEKLY", weekly_person)
                tasks_printed += 1
        
        # Print monthly tasks if it's the first Monday of the month or if 'month' is requested
        if (datetime.now().day <= 7 and print_type is None) or print_type == 'month':
            monthly_person = get_assigned_person(month_num)
            for task in MONTHLY_TASKS:
                print_task(printer, task, "MONTHLY", monthly_person)
                tasks_printed += 1
        
        # Print quarterly tasks if it's the first month of a new quarter or if 'quarter' is requested
        if (month_num in [1, 4, 7, 10] and datetime.now().day <= 7 and print_type is None) or print_type == 'quarter':
            quarterly_person = get_assigned_person(quarter)
            for task in QUARTERLY_TASKS:
                print_task(printer, task, "QUARTERLY", quarterly_person)
                tasks_printed += 1
        
        print(f"Successfully printed {tasks_printed} cleaning tasks")
        
    except Exception as e:
        print(f"Error printing cleaning plan: {e}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Print cleaning schedule')
    parser.add_argument('--print', choices=['week', 'month', 'quarter', 'all'],
                        help='Immediately print specific cleaning plan(s)')
    
    args = parser.parse_args()
    
    # If --print argument is provided, print the requested plan and exit
    if args.print:
        if args.print == 'all':
            print_cleaning_plan()
        else:
            print_cleaning_plan(args.print)
        return
    
    # Otherwise, schedule the task to run every Monday at 11:00
    schedule.every().monday.at("11:00").do(print_cleaning_plan)
    
    # For debugging/testing, print when the script starts
    print(f"Script started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Scheduled to print cleaning plan every Monday at 11:00")
    print("Use --print [week|month|quarter|all] to print immediately")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
