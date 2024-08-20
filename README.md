# CheckInCheckOut

**CheckInCheckOut** is a simple and efficient tool designed to help employees log their daily work hours. This Python-based application tracks when employees start and finish their workday, saving this data in a CSV file using the Shamsi (Jalali) calendar. The GUI provides an intuitive interface for entering data, and it also displays the most recent log entry for the current day.

## Features

- **Automatic Name Recognition**: The tool remembers employee names after the first login, simplifying the process of logging time.
- **Daily Time Logging**: Employees can easily log their arrival and departure times for each day.
- **Shamsi (Jalali) Calendar Support**: Dates are handled in the Shamsi calendar system.
- **CSV Storage**: All time logs are stored in a CSV file, making the data easy to access, export, and analyze.
- **Real-Time Feedback**: The GUI displays the employee's current day's log entry, updating automatically when new times are logged.
- **Minimal Setup**: The application is simple to set up and use, with no complex configurations required.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- **Python 3.x** installed on your system.
- **pandas** and **jdatetime** packages (install using pip if not already installed).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KouroshEsmaeili/CheckInCheckOut.git
