import os
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from openpyxl import load_workbook


# Function to handle the "Add to Database" button click
def add_to_database():
    selected_db = db_var.get()
    selected_table = table_var.get()

    # Connect to the selected database
    conn = sqlite3.connect(selected_db)
    cursor = conn.cursor()

    # Check if the selected table exists in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (selected_table,))
    table_exists = cursor.fetchone()
    if not table_exists:
        print(f"Table '{selected_table}' does not exist in the '{selected_db}' database.")
        conn.close()
        return

    # Read data from the Excel file
    file_path = file_var.get()
    if not file_path:
        print("Please select an Excel file.")
        return

    wb = load_workbook(file_path)
    sheet = wb.active

    # Get the column headings from the first row of the Excel file
    excel_column_headings = sheet[1]
    excel_column_headings = [cell.value for cell in excel_column_headings]

    # Get the last id in the table to start incrementing from there
    cursor.execute(f"SELECT MAX(id) FROM {selected_table}")
    last_id = cursor.fetchone()[0]
    if last_id is None:
        last_id = 0

    # Get the current timestamp
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert data from the Excel file into the selected table
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Ignore empty rows in the Excel file
        if not any(row):
            continue

        last_id += 1
        data_with_id = [last_id]

        for heading in excel_column_headings:
            # Check if the heading exists as a column in the table
            if heading in column_names:
                index = excel_column_headings.index(heading)
                data_with_id.append(row[index])
            else:
                # If the heading doesn't match any column in the table, add None as a placeholder
                data_with_id.append(None)

        # Ensure the number of values matches the number of columns in the table
        while len(data_with_id) < len(column_names) + 1:  # Add 1 for the 'id' column
            data_with_id.append(None)

        # Check if 'date' column is missing or has an empty cell
        if 'date' not in excel_column_headings:
            # 'date' column is missing, use the current date as the default value
            data_with_id.insert(1, datetime.now().strftime('%Y-%m-%d'))
        elif data_with_id[1] is None:
            # 'date' column has an empty cell, use the current date as the default value
            data_with_id[1] = datetime.now().strftime('%Y-%m-%d')

        data_with_id.append(current_timestamp)
        placeholders = ', '.join(['?'] * len(data_with_id))
        columns = ', '.join(['id', 'date', *column_names, 'timestamp'])

        cursor.execute(f"INSERT INTO {selected_table} ({columns}) VALUES ({placeholders})", data_with_id)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Data added to the database successfully.")


# Define column names
column_names = ["mfgnum", "partnum", "custPO", "description", "quantity"]

# Create the GUI
root = tk.Tk()
root.title("Excel to Database Upload")

# Database and Table Selection
db_var = tk.StringVar()
db_var.set("flight.db")  # Default database selection
db_label = tk.Label(root, text="Select Database")
db_label.pack()
db_options = ["flight.db", "nonflight.db", "suppliers.db"]  # Add your database options here
db_dropdown = tk.OptionMenu(root, db_var, *db_options)
db_dropdown.pack()

# Create separate tables for each category if they don't exist
categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
              "Connectors", "Voltage_n_Regulator", "LEDs",
              "Diodes_n_Rectifiers", "Others"]

table_var = tk.StringVar()
table_var.set("Choose Table")  # Default table selection
table_label = tk.Label(root, text="Select Table:")
table_label.pack()
table_options = categories  # Add your table options here
table_dropdown = tk.OptionMenu(root, table_var, *table_options)
table_dropdown.pack()

# Upload Excel File
file_label = tk.Label(root, text="Select Excel File:")
file_label.pack()


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        file_var.set(file_path)


file_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_var, state='readonly', width=50)
file_entry.pack()
file_button = tk.Button(root, text="Browse", command=open_file)
file_button.pack()

# Add to Database Button
add_button = tk.Button(root, text="Add to Database", command=add_to_database)
add_button.pack()

root.mainloop()
