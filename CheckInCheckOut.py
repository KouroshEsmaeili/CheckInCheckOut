import pandas as pd
import jdatetime
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox


# Function to get or set employee name based on identifier
def get_employee_name(filename, identifier):
    if os.path.exists(filename):
        employees_df = pd.read_csv(filename)
    else:
        employees_df = pd.DataFrame(columns=['Identifier', 'Employee Name'])

    existing_employee = employees_df[employees_df['Identifier'] == identifier]

    if not existing_employee.empty:
        return existing_employee.iloc[0]['Employee Name']
    else:
        return None


def save_employee_name(filename, identifier, employee_name):
    if os.path.exists(filename):
        employees_df = pd.read_csv(filename)
    else:
        employees_df = pd.DataFrame(columns=['Identifier', 'Employee Name'])

    new_entry = pd.DataFrame([[identifier, employee_name]], columns=['Identifier', 'Employee Name'])
    employees_df = pd.concat([employees_df, new_entry], ignore_index=True)
    employees_df.to_csv(filename, index=False)


# Function to log start and end times
def log_time(filename, employee_name, start_time=None, end_time=None):
    today = jdatetime.date.today().strftime('%Y-%m-%d')

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'Employee Name', 'Start Time', 'End Time'])

    existing_entry = df[(df['Date'] == today) & (df['Employee Name'] == employee_name)]

    if not existing_entry.empty:
        if start_time:
            df.loc[existing_entry.index, 'Start Time'] = start_time
        if end_time:
            df.loc[existing_entry.index, 'End Time'] = end_time
    else:
        new_entry = pd.DataFrame([[today, employee_name, start_time, end_time]],
                                 columns=['Date', 'Employee Name', 'Start Time', 'End Time'])
        df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(filename, index=False)


# Function to handle logging start time
def start_time_action():
    start_time = datetime.now().strftime('%H:%M:%S')
    log_time(schedule_filename, employee_name_var.get(), start_time=start_time)
    messagebox.showinfo("CheckInCheckOut", f"Start time logged: {start_time}")


# Function to handle logging end time
def end_time_action():
    end_time = datetime.now().strftime('%H:%M:%S')
    log_time(schedule_filename, employee_name_var.get(), end_time=end_time)
    messagebox.showinfo("CheckInCheckOut", f"End time logged: {end_time}")


# Function to save the employee name and proceed
def save_name_action():
    employee_name = employee_name_var.get()
    if employee_name:
        save_employee_name(employees_filename, identifier, employee_name)
        start_button.config(state=tk.NORMAL)
        end_button.config(state=tk.NORMAL)
        name_entry.config(state=tk.DISABLED)
        save_name_button.config(state=tk.DISABLED)
    else:
        messagebox.showwarning("CheckInCheckOut", "Please enter your name before proceeding.")


# GUI Setup
app = tk.Tk()
app.title("CheckInCheckOut")

identifier = os.getenv('USER', 'unknown_user')
employees_filename = 'employees.csv'

# Variable to store the employee name
employee_name_var = tk.StringVar()

# Check if the name is already stored
stored_name = get_employee_name(employees_filename, identifier)
if stored_name:
    employee_name_var.set(stored_name)

# Labels and Buttons
name_label = tk.Label(app, text="Enter your name:", font=("Helvetica", 14))
name_label.pack(pady=10)

name_entry = tk.Entry(app, textvariable=employee_name_var, font=("Helvetica", 14))
name_entry.pack(pady=10)

save_name_button = tk.Button(app, text="Save Name", command=save_name_action, font=("Helvetica", 14))
save_name_button.pack(pady=10)

start_button = tk.Button(app, text="Log Start Time", command=start_time_action, font=("Helvetica", 14),
                         state=tk.NORMAL if stored_name else tk.DISABLED)
start_button.pack(pady=10)

end_button = tk.Button(app, text="Log End Time", command=end_time_action, font=("Helvetica", 14),
                       state=tk.NORMAL if stored_name else tk.DISABLED)
end_button.pack(pady=10)

schedule_filename = 'work_schedule.csv'

app.mainloop()
