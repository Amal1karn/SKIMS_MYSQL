from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import openpyxl
import sqlite3


class compare_class:
    def __init__(self, root, enable_button):
        self.root = root
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.title("COMPARE LIST")
        self.root.config(bg="white")
        self.enable_button = enable_button

        # =============================Connect to the database==================================
        self.columns = (
        "Manufacturing Number", "Category", "Database", "Quantity (Excel)", "Actual Quantity (DB)", "Status")

        # Create separate tables for each category if they don't exist
        categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                      "Connectors", "Voltage_n_Regulator", "LEDs",
                      "Diodes_n_Rectifiers", "Others"]

        # ==================================TITLE FRAME ===============================================================
        # title frame
        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.title_frame.pack(side=TOP, fill=X)

        Label(self.title_frame, text="COMPARE YOUR LIST", font=("times new roman", 30, "bold"),
              bg="#03B4E6", fg="white", bd=10, relief=GROOVE).pack(side=TOP, fill=X)

        self.closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), bg="#0F148C",
                               cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.close_compare)
        self.closebtn.place(x=1090, y=15, width=100, height=37)

        # ========================================================================

        self.button_frame = Frame(self.root, bd=10, relief=RIDGE, bg="#63B8FF")
        self.button_frame.place(x=4, y=77, width=1220, height=70)

        self.import_file_button = Button(self.button_frame, text="Import File", font=("arial", 10, "bold"),
                                         bg="#0F148C", width=9,
                                         cursor="hand2", relief=RAISED, fg="white", bd=8,
                                         command=self.select_excel_file)  # Removed the lambda function here
        self.import_file_button.grid(row=0, column=1, pady=5, padx=15)

        self.export_button = Button(self.button_frame, text="Export File", font=("arial", 10, "bold"), bg="#0F148C",
                                    width=9,
                                    cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.export_results)
        self.export_button.grid(row=0, column=3, padx=15, pady=5)

        self.clear_button = Button(self.button_frame, text="CLEAR", font=("arial", 10, "bold"), bg="#0F148C", width=7,
                                   cursor="hand2", relief=RAISED, fg="white", bd=8,
                                   command=self.clear_results)
        self.clear_button.grid(row=0, column=4, padx=15, pady=5)

        # Step 11: Visual Improvements
        self.error_label = Label(self.button_frame, text="", fg="red", bg="#63B8FF")
        self.error_label.grid(row=0, column=5, padx=15, pady=5)

        # Progress Bar widget setup
        self.progress = ttk.Progressbar(self.button_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=0, column=2, padx=30, pady=5, )

        # ==================================TREEVIEW FRAME ===============================================================

        self.table_frame = Frame(self.root, bd=15, relief=RIDGE, bg="#63B8FF")
        self.table_frame.place(x=3, y=150, width=1220, height=442)

        # ==========================TREEVIEW====================================
        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.compare_table = ttk.Treeview(self.table_frame, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.compare_table.xview)
        scroll_y.config(command=self.compare_table.yview)

        columns = (
        "Category", "Manufacturing Number", "Quantity (Excel)", "Actual Quantity (DB)", "Status", "Database",)
        self.compare_table = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), foreground='#0F148C', background='black')

        # Column headings
        self.compare_table.heading("#0", text="CHECKING")
        self.compare_table.heading("#1", text="Category")
        self.compare_table.heading("#2", text="Manufacturing Number")
        self.compare_table.heading("#3", text="Quantity (Excel)")
        self.compare_table.heading("#4", text="Actual Quantity (DB)")
        self.compare_table.heading("#5", text="Status")
        self.compare_table.heading("#6", text="Database")

        # Column widths
        self.compare_table.column("#0", width=150)
        self.compare_table.column("#1", width=150)
        self.compare_table.column("#2", width=100)
        self.compare_table.column("#3", width=100)
        self.compare_table.column("#4", width=100)
        self.compare_table.column("#5", width=150)
        self.compare_table.column("#6", width=100)

        # Adding tag configuration for colored rows
        self.compare_table.tag_configure("ENOUGH", background="white", foreground="green")
        self.compare_table.tag_configure("NEED_TO_ORDER", background="white", foreground="red")
        self.compare_table.tag_configure("NOT_ENOUGH", background="yellow", foreground="black")

        self.compare_table.pack(fill=BOTH, expand=1)

        self.col_sort_dict = {col: False for col in columns}
        for col in columns:
            self.compare_table.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))

        self.compare_table.bind("<<TreeviewSelect>>")

        # =============================== UPDATE Treeview FUNCTIOn============================

    def select_excel_file(self):
        messagebox.showwarning("Warning",
                             f"Make sure your file 1st column has Manufacturing number and 2nd column has Quantity", parent=self.root)
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.process_excel_data(file_path, 'flight.db', 'nonflight.db')


    def process_excel_data(self, file_path, flight, nonflight):
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        component_data = []
        total_rows = sheet.max_row - 1
        self.progress["maximum"] = total_rows

        # Open the connections
        conn_db1 = sqlite3.connect(flight)
        conn_db2 = sqlite3.connect(nonflight)

        cursor_db1 = conn_db1.cursor()
        cursor_db2 = conn_db2.cursor()

        # Initialize flightDB and nonflightDB dictionaries outside the loop
        categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                      "Connectors", "Voltage_n_Regulator", "LEDs",
                      "Diodes_n_Rectifiers", "Others"]

        flightDB = {}  # Dictionary to store main database data for each category
        nonflightDB = {}  # Dictionary to store data from another database

        for category in categories:
            # Query the Main Database
            cursor_db1.execute(f"SELECT mfgnum, total_quantity FROM `{category}_summary`")
            main_db_data = cursor_db1.fetchall()

            # Convert main_db_data to a dictionary with uppercase mfgnum as key and total_quantity as value
            flightDB[category] = {mfgnum.upper(): total_quantity for mfgnum, total_quantity in main_db_data}

            # Query the Second Database (Replace '`{category}_summary`' with the correct table name)
            cursor_db2.execute(f"SELECT mfgnum, total_quantity FROM `{category}_summary`")
            another_db_data = cursor_db2.fetchall()

            # Convert another_db_data to a dictionary with uppercase mfgnum as key and total_quantity as value
            nonflightDB[category] = {mfgnum.upper(): total_quantity for mfgnum, total_quantity in another_db_data}

        result_data = []
        for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=1):
            # Ensure that the row contains enough elements before accessing specific indices
            if len(row) >= 4:  # Assuming description at index 2 and supplier at index 3
                component_data.append((row[0], row[1], row[2], row[3]))
            elif len(row) == 3:
                component_data.append((row[0], row[1], row[2], None))  # Supplier information not available
            elif len(row) == 2:
                component_data.append(
                    (row[0], row[1], None, None))  # Description and supplier information not available

            # Update progress bar
            self.progress["value"] = i
            self.root.update_idletasks()

        for data_tuple in component_data:
            excel_mfgnum, excel_quantity, *_ = data_tuple

            # Check if excel_mfgnum is not None before performing the comparison
            if excel_mfgnum is not None and excel_mfgnum.strip():  # Use .strip() to check for non-empty strings

                quantity_status = "NEED TO ORDER"  # Default status
                total_quantity = None
                category = None
                database = None
                found_category = None  # Initialize found_category
                found_database = None  # Initialize found_database

                # Check in the first database
                for category, data_dict in flightDB.items():
                    if excel_mfgnum.upper() in data_dict:  # Ignore case sensitivity
                        total_quantity = data_dict[excel_mfgnum.upper()]
                        found_category = category  # Update found_category
                        found_database = flight  # Update found_database

                        if total_quantity == excel_quantity:
                            quantity_status = "ORDER MORE PLEASE"
                        elif total_quantity > excel_quantity:
                            quantity_status = "ENOUGH"

                        break  # Stop searching if found in any category

                # Check in the second database if not found in the first database
                if total_quantity is None:
                    for category, data_dict in nonflightDB.items():
                        if excel_mfgnum.upper() in data_dict:  # Ignore case sensitivity
                            total_quantity = data_dict[excel_mfgnum.upper()]
                            found_category = category  # Update found_category
                            found_database = nonflight  # Update found_database

                            if total_quantity == excel_quantity:
                                quantity_status = "ORDER MORE PLEASE"
                            elif total_quantity > excel_quantity:
                                quantity_status = "ENOUGH"

                            break  # Stop searching if found in any category

                # If not found in any database or category, set status to "NOT FOUND"
                if total_quantity is None and not all(value is None for value in data_tuple):
                    quantity_status = "NOT FOUND"

                result_data.append(
                    (found_category, excel_mfgnum, excel_quantity, total_quantity, quantity_status, found_database))

        # Close the connections and cursors
        cursor_db1.close()
        cursor_db2.close()
        conn_db1.close()
        conn_db2.close()

        self.display_results(result_data)

    def display_results(self, result_data):
        for row in self.compare_table.get_children():
            self.compare_table.delete(row)

        for data in result_data:
            category, manufacturing_number, excel_quantity, db_quantity, quantity_status, database = data

            # Color coding based on quantity_status
            if quantity_status == "ENOUGH":
                self.compare_table.insert("", "end",
                                          values=(
                                              category, manufacturing_number, excel_quantity, db_quantity,
                                              quantity_status, database),
                                          tags=("ENOUGH",))
            elif quantity_status == "NEED TO ORDER":
                self.compare_table.insert("", "end",
                                          values=(
                                              category, manufacturing_number, excel_quantity, db_quantity,
                                              quantity_status, database),
                                          tags=("NEED_TO_ORDER",))
            else:  # "NOT ENOUGH"
                self.compare_table.insert("", "end",
                                          values=(
                                              category, manufacturing_number, excel_quantity, db_quantity,
                                              quantity_status, database),
                                          tags=("NOT_ENOUGH",))

        # Configure custom tag colors
        self.compare_table.tag_configure("ENOUGH", background="white", foreground="green")
        self.compare_table.tag_configure("NEED_TO_ORDER", background="white", foreground="red")
        self.compare_table.tag_configure("NOT_ENOUGH", background="yellow", foreground="black")

    def sort_by_column(self, col):
        data = [(self.compare_table.set(child, col), child) for child in self.compare_table.get_children('')]
        data.sort(reverse=self.col_sort_dict[col])
        for index, (val, child) in enumerate(data):
            self.compare_table.move(child, '', index)
        self.col_sort_dict[col] = not self.col_sort_dict[col]

    def export_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(self.columns)
            for item in self.compare_table.get_children():
                values = self.compare_table.item(item)['values']
                sheet.append(values)
            wb.save(file_path)

    # Step 7: Handle Exceptions
    def show_error(self, message):
        self.error_label.config(text=message)

    def clear_error(self):
        self.error_label.config(text="")

    # Step 8: Test the Application
    def clear_results(self):
        for row in self.compare_table.get_children():
            self.compare_table.delete(row)
        self.clear_error()

    def close_compare(self):
        self.enable_button()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = compare_class(root, None)
    root.mainloop()
