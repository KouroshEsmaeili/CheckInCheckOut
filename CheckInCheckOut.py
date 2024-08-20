import pandas as pd
import jdatetime
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox


# File and Identifier Setup
def initialize_filenames():
    identifier = os.getenv('USER', 'unknown_user')
    employees_filename = 'employees.csv'
    schedule_filename = 'work_schedule.csv'
    return identifier, employees_filename, schedule_filename


# Employee Name Management
def get_employee_name(filename, identifier):
    if os.path.exists(filename):
        employees_df = pd.read_csv(filename)
    else:
        employees_df = pd.DataFrame(columns=['Identifier', 'Employee Name'])

    existing_employee = employees_df[employees_df['Identifier'] == identifier]
    return existing_employee.iloc[0]['Employee Name'] if not existing_employee.empty else None


def save_employee_name(filename, identifier, employee_name):
    if os.path.exists(filename):
        employees_df = pd.read_csv(filename)
    else:
        employees_df = pd.DataFrame(columns=['Identifier', 'Employee Name'])

    new_entry = pd.DataFrame([[identifier, employee_name]], columns=['Identifier', 'Employee Name'])
    employees_df = pd.concat([employees_df, new_entry], ignore_index=True)
    employees_df.to_csv(filename, index=False)


# Time Logging
def log_time(filename, employee_name, start_time=None, end_time=None):
    today = jdatetime.date.today().strftime('%Y-%m-%d')
    df = load_or_create_dataframe(filename, ['Date', 'Employee Name', 'Start Time', 'End Time'])

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


def load_or_create_dataframe(filename, columns):
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns)
    return df


# GUI Actions
def save_name_action(employee_name_var, identifier, employees_filename, start_button, end_button, name_entry,
                     save_name_button, todays_entry_label, schedule_filename):
    employee_name = employee_name_var.get()
    if employee_name:
        save_employee_name(employees_filename, identifier, employee_name)
        enable_buttons(start_button, end_button, name_entry, save_name_button)
        todays_entry_text = get_todays_entry(schedule_filename, employee_name)
        todays_entry_label.config(text=todays_entry_text)
    else:
        messagebox.showwarning("CheckInCheckOut", "Please enter your name before proceeding.")


def start_time_action(employee_name_var, schedule_filename, todays_entry_label):
    start_time = datetime.now().strftime('%H:%M:%S')
    log_time(schedule_filename, employee_name_var.get(), start_time=start_time)
    messagebox.showinfo("CheckInCheckOut", f"Start time logged: {start_time}")
    todays_entry_text = get_todays_entry(schedule_filename, employee_name_var.get())
    todays_entry_label.config(text=todays_entry_text)


def end_time_action(employee_name_var, schedule_filename, todays_entry_label):
    end_time = datetime.now().strftime('%H:%M:%S')
    log_time(schedule_filename, employee_name_var.get(), end_time=end_time)
    messagebox.showinfo("CheckInCheckOut", f"End time logged: {end_time}")
    todays_entry_text = get_todays_entry(schedule_filename, employee_name_var.get())
    todays_entry_label.config(text=todays_entry_text)


def enable_buttons(start_button, end_button, name_entry, save_name_button):
    start_button.config(state=tk.NORMAL)
    end_button.config(state=tk.NORMAL)
    name_entry.config(state=tk.DISABLED)
    save_name_button.config(state=tk.DISABLED)


# GUI Setup
def setup_gui():
    app = tk.Tk()
    app.title("CheckInCheckOut")
    app.geometry("800x600")
    app.resizable(False, False)

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TEntry", font=("Helvetica", 12))

    frame = ttk.Frame(app, padding="20")
    frame.pack(fill="both", expand=True)

    return app, frame


def create_widgets(app, frame, employee_name_var, stored_name, identifier, employees_filename, schedule_filename):
    title_label = ttk.Label(frame, text="Welcome to CheckInCheckOut", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    name_label = ttk.Label(frame, text="Enter your name:")
    name_label.pack(pady=10)

    # Increase the width of the entry box
    name_entry = ttk.Entry(frame, textvariable=employee_name_var, width=40)
    name_entry.pack(pady=5, padx=20)

    save_name_button = ttk.Button(frame, text="Save Name", command=lambda: save_name_action(
        employee_name_var, identifier, employees_filename, start_button, end_button, name_entry, save_name_button,
        todays_entry_label, schedule_filename))
    save_name_button.pack(pady=10)

    start_button = ttk.Button(frame, text="Log Start Time",
                              command=lambda: start_time_action(employee_name_var, schedule_filename,
                                                                todays_entry_label),
                              state=tk.NORMAL if stored_name else tk.DISABLED)
    start_button.pack(pady=5)

    end_button = ttk.Button(frame, text="Log End Time",
                            command=lambda: end_time_action(employee_name_var, schedule_filename, todays_entry_label),
                            state=tk.NORMAL if stored_name else tk.DISABLED)
    end_button.pack(pady=5)

    # Display today's entry
    todays_entry_text = get_todays_entry(schedule_filename, stored_name)
    todays_entry_label = ttk.Label(frame, text=todays_entry_text, font=("Helvetica", 10))
    todays_entry_label.pack(pady=20)

    return start_button, end_button, name_entry, save_name_button


def get_todays_entry(filename, employee_name):
    if not os.path.exists(filename):
        return "No entries for today."

    df = pd.read_csv(filename)
    today = jdatetime.date.today().strftime('%Y-%m-%d')
    todays_entry = df[(df['Date'] == today) & (df['Employee Name'] == employee_name)]

    if todays_entry.empty:
        return "No entries for today."

    start_time = todays_entry.iloc[0]['Start Time'] if pd.notna(todays_entry.iloc[0]['Start Time']) else "N/A"
    end_time = todays_entry.iloc[0]['End Time'] if pd.notna(todays_entry.iloc[0]['End Time']) else "N/A"

    return f"Today's Entry - Start Time: {start_time}, End Time: {end_time}"


# Main function to run the application
def main():
    identifier, employees_filename, schedule_filename = initialize_filenames()

    # Initialize the GUI before creating any Tkinter variables
    app, frame = setup_gui()

    stored_name = get_employee_name(employees_filename, identifier)
    employee_name_var = tk.StringVar(value=stored_name if stored_name else "")

    start_button, end_button, name_entry, save_name_button = create_widgets(
        app, frame, employee_name_var, stored_name, identifier, employees_filename, schedule_filename)

    app.mainloop()


if __name__ == "__main__":
    main()
