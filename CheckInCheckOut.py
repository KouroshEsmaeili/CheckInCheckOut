import pandas as pd
from datetime import datetime
import os


def get_employee_name(filename, identifier):
    # Check if the employees file exists
    if os.path.exists(filename):
        employees_df = pd.read_csv(filename)
    else:
        employees_df = pd.DataFrame(columns=['Identifier', 'Employee Name'])

    # Look for the identifier in the file
    existing_employee = employees_df[employees_df['Identifier'] == identifier]

    if not existing_employee.empty:
        # Return the existing employee name
        return existing_employee.iloc[0]['Employee Name']
    else:
        # Prompt for the employee name and save it
        employee_name = input("Enter your name: ")
        new_entry = pd.DataFrame([[identifier, employee_name]], columns=['Identifier', 'Employee Name'])
        employees_df = pd.concat([employees_df, new_entry], ignore_index=True)
        employees_df.to_csv(filename, index=False)
        return employee_name


def log_time(filename, employee_name, start_time=None, end_time=None):
    today = datetime.now().strftime('%Y-%m-%d')

    try:
        # Read the existing CSV file into a DataFrame
        df = pd.read_csv(filename)
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        df = pd.DataFrame(columns=['Date', 'Employee Name', 'Start Time', 'End Time'])

    # Check if there's already an entry for today
    existing_entry = df[(df['Date'] == today) & (df['Employee Name'] == employee_name)]

    if not existing_entry.empty:
        # Update existing entry
        if start_time:
            df.loc[existing_entry.index, 'Start Time'] = start_time
        if end_time:
            df.loc[existing_entry.index, 'End Time'] = end_time
    else:
        # Add a new entry
        new_entry = pd.DataFrame([[today, employee_name, start_time, end_time]],
                                 columns=['Date', 'Employee Name', 'Start Time', 'End Time'])
        df = pd.concat([df, new_entry], ignore_index=True)

    # Write the DataFrame back to the CSV
    df.to_csv(filename, index=False)


def main():
    employees_filename = 'employees.csv'
    schedule_filename = 'work_schedule.csv'

    # Use a unique identifier, for example, the user's environment username
    identifier = os.getenv('USER', 'unknown_user')

    # Get the employee name based on the identifier
    employee_name = get_employee_name(employees_filename, identifier)

    while True:
        action = input(
            f"Hello {employee_name}, do you want to log your (S)tart time or (E)nd time? (S/E): ").strip().upper()
        if action == 'S':
            start_time = datetime.now().strftime('%H:%M:%S')
            log_time(schedule_filename, employee_name, start_time=start_time)
            print(f"Start time logged: {start_time}")
        elif action == 'E':
            end_time = datetime.now().strftime('%H:%M:%S')
            log_time(schedule_filename, employee_name, end_time=end_time)
            print(f"End time logged: {end_time}")
        else:
            print("Invalid input, please enter 'S' for start or 'E' for end.")

        more = input("Do you want to log another time? (y/n): ").strip().lower()
        if more != 'y':
            break


if __name__ == "__main__":
    main()
