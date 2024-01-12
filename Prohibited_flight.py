from tkinter import *
from datetime import date
import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
import re

class Prohibited_class:
    def __init__(self, root, enable_button):
        self.root = root
        self.root.title("NON-FLIGHT: STOCK IN")
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.config(bg="white")
        self.enable_button = enable_button

        #=============================Connect to the database==================================

        '''# Function to make a case-insensitive comparison for the manufacturing number and ordered by entity
        def case_insensitive_equal(str1, str2):
            return str1.upper() == str2.upper()'''

        # Create separate tables for each category if they don't exist
        categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                      "Connectors", "Voltage_n_Regulator", "LEDs",
                      "Diodes_n_Rectifiers", "Others"]

        #============================title frame============================
        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.title_frame.pack(side=TOP, fill=X)

        title = Label(self.title_frame, text="NON-FLIGHT-STOCK IN", bd=10, relief=GROOVE,
                      font=("times new roman", 30, "bold"), bg="#0F148C", fg="white")
        title.pack(side=TOP, fill=X)

        closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), relief=RAISED, bd=8,
                          bg="#63B8FF", cursor="hand2", fg="white", command= self.close_prohibited)
        closebtn.place(x=1090, y=15, width=100, height=37)

        # ============================menu frame============================
        self.manage_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.manage_frame.place(x=5, y=80, width=385, height=500)

        # Create a label and entry widget for the date
        lbl_date = Label(self.manage_frame, text="Date:", font=("times new roman", 17, "bold"),
                         bg="#63B8FF", fg="black")
        lbl_date.grid(row=0, column=0, pady=8, padx=(13,5), sticky="w")
        self.txt_date = Entry(self.manage_frame,font=("times new roman", 12, "bold"),
                              bd=5, relief=GROOVE)
        self.txt_date.grid(row=0, column=1, pady=8, padx=8, sticky="w")

        # Create a label and entry widget for the MFG NUMBER
        lbl_mfgnum = Label(self.manage_frame, text="MFG No:", font=("times new roman", 17, "bold"),
                           bg="#63B8FF", fg="black")
        lbl_mfgnum.grid(row=1, column=0, pady=8, padx=(13,5), sticky="w")
        self.txt_mfgnum = Entry(self.manage_frame, font=("times new roman", 12, "bold"),
                           bd=5, relief=GROOVE)
        self.txt_mfgnum.grid(row=1, column=1, pady=8, padx=8, sticky="w")

        #========== Create a label and entry widget for the PART NUMBER
        lbl_partnum = Label(self.manage_frame, text="Part No:",
                            font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_partnum.grid(row=2, column=0, pady=8, padx=(13,5), sticky="w")
        self.txt_partnum = Entry(self.manage_frame,
                            font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_partnum.grid(row=2, column=1, pady=8, padx=8, sticky="w")

        #============= Create a label and entry widget for the CUSTOMER PO
        lbl_custpo = Label(self.manage_frame, text="Customer PO:", font=("times new roman", 17, "bold"),
                           bg="#63B8FF", fg="black")
        lbl_custpo.grid(row=3, column=0, pady=8, padx=(13,5), sticky="w")
        self.txt_custpo = Entry(self.manage_frame,
                           font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_custpo.grid(row=3, column=1, pady=8, padx=8, sticky="w")

        #========== Create a label and entry widget for the item name
        lbl_des = Label(self.manage_frame, text="Description:",
                        font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_des.grid(row=4, column=0, pady=8, padx=(13,5), sticky="w")
        self.txt_des = Entry(self.manage_frame,
                        font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_des.grid(row=4, column=1, pady=8, padx=8, sticky="w",)

        #============= Create a label and entry widget for the QUANTITY
        lbl_qty = Label(self.manage_frame, text="Quantity:",
                        font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_qty.grid(row=5, column=0, pady=8, padx=(13,5), sticky="w")
        self.txt_qty = Entry(self.manage_frame,
                        font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_qty.grid(row=5, column=1, pady=8, padx=8, sticky="w")

        # ======================Create a combobox Label===================

        lbl_category = Label(self.manage_frame, text="Category",
                             font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_category.grid(row=6, column=0, pady=8, padx=(13,5), sticky="w")


        # Add the default option to the categories list
        categories = ["Select Category"] + categories

        self.cat_combo = ttk.Combobox(self.manage_frame, values=categories,
                                      state="readonly", font=("times new roman", 13, "bold"), width=17)
        self.cat_combo.grid(row=6, column=1, pady=8, padx=8, sticky="w")

        # Set the default value to "Select Category"
        self.cat_combo.current(0)
        # ===============BUttons Menu============================================

        btn_frame = Frame(self.manage_frame, bd=0, relief=RIDGE, bg="#63B8FF")
        btn_frame.place(x=3, y=350, width=370, height=100)

        # Create an "Add Item" button
        add_btn = Button(btn_frame, text="Add", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                          bg="#0F148C", cursor="hand2", fg="white",width=6,command=self.add_prohibited)
        add_btn.grid(row=0, column=0, padx=8, pady=15)

        # Create an "Update Item" button
        update_btn = Button(btn_frame, text="Update",font=("arial", 11, "bold"), relief=RAISED, bd=8,
                          bg="#0F148C", cursor="hand2", fg="white", width=6,command=self.update_prohibited)
        update_btn.grid(row=0, column=1, padx=8, pady=15)

        # Create an "CLEAR" button
        clear_btn = Button(btn_frame, text="Clear",font=("arial", 11, "bold"), relief=RAISED, bd=8,
                          bg="#0F148C", cursor="hand2", fg="white",width=6, command= self.clear_all)
        clear_btn.grid(row=0, column=2, padx=8, pady=15)

        delete_btn = Button(btn_frame, text="Delete", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                          bg="#0F148C", cursor="hand2", fg="white",width=6,
                            command=self.delete_data)
        delete_btn.grid(row=0, column=3, padx=8, pady=15)

        #=======================================SEARCH FRAME================================#
        self.detail_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.detail_frame.place(x=392, y=80, width=835, height=500)

        lbl_search = Label(self.detail_frame, text="Search by MFG No:",
                           font=("times new roman", 15, "bold"), bg="#63B8FF", fg="black")
        lbl_search.grid(row=0, column=0, pady=10, padx=(250,3), sticky="w")

        self.txt_search = Entry(self.detail_frame, font=("times new roman", 13, "bold"),
                           bd=5, relief=GROOVE)
        self.txt_search.grid(row=0, column=1, pady=10, padx=(3,20), sticky="w")

        search_btn = Button(self.detail_frame, text="Search",  font=("arial", 11, "bold"), relief=RAISED, bd=8,
                          bg="#0F148C", cursor="hand2", fg="white",width=6,padx=5,command=self.search)
        search_btn.grid(row=0, column=2, padx=18, pady=10)

       #==========================TREEVIEW FRAME====================================
        self.table_frame = Frame(self.detail_frame, bd=4, relief=RIDGE, bg="black")
        self.table_frame.place(x=0, y=59, width=827, height=430)

        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.prohibited_table = ttk.Treeview(self.table_frame,xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.prohibited_table.xview)
        scroll_y.config(command=self.prohibited_table.yview)

        self.prohibited_table["columns"] = ("id", "date", "mfgnum", "partnum", "custPO", "description", "quantity", "timestamp")

        # Configure the Treeview columns
        self.prohibited_table.heading("#0", text="Category")
        self.prohibited_table.heading("id", text="id")
        self.prohibited_table.heading("date", text="Date")
        self.prohibited_table.heading("mfgnum", text="Manufacturing No.")
        self.prohibited_table.heading("partnum", text="Part No.")
        self.prohibited_table.heading("custPO", text="Customer PO")
        self.prohibited_table.heading("description", text="Description")
        self.prohibited_table.heading("quantity", text="QTY")
        self.prohibited_table.heading("timestamp", text="TIMESTAMP")

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), foreground='#0F148C', background='black')

        # Configure the Treeview headings
        #self.prohibited_table['show'] = 'headings'
        self.prohibited_table.column("#0", width=80)
        self.prohibited_table.column("id", width=0, stretch=tk.NO)
        self.prohibited_table.column("date", width=80)
        self.prohibited_table.column("mfgnum", width=100)
        self.prohibited_table.column("partnum", width=100)
        self.prohibited_table.column("custPO", width=100)
        self.prohibited_table.column("description", width=200)
        self.prohibited_table.column("quantity", width=50)
        self.prohibited_table.column("timestamp", width=0, stretch=tk.NO)

        self.prohibited_table.pack(fill=BOTH, expand=1)

        self.prohibited_table.bind("<<TreeviewSelect>>", self.fetch_data)

        # Configure tags for even rows
        self.prohibited_table.tag_configure("even_row", background="lightgray")
        #udpate treeview
        self.update_treeview()
        #clear all entries
        self.clear_all()

# ===Check valid quantity positive number FUNCTIOn===================================
    def check_quantity(self):
        qty_var = self.txt_qty.get()

        try:
            # Check if the quantity is a valid positive integer
            if not re.match(r'^\d+$', qty_var):
                print("Error: Quantity must be a positive number.")
                return
            quantity = int(qty_var)
            if quantity <= 0:
                print("Error: Quantity must be a positive number.")
                return
            print("Quantity is a valid positive integer.")
        except ValueError:
            print("Error: Quantity must be a positive number.")

    # =========================================DATE FUNCTIOn===================================
    def set_current_date(self):
        try:
            current_date = date.today().strftime("%Y/%m/%d")
            self.txt_date.delete(0, tk.END)  # Clear any existing text
            self.txt_date.insert(0, current_date)  # Insert the current date into the widget
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to date: {str(ex)}", parent=self.root)
    # ===============================unselect FUNCTIOn========================

    def unselect_item(self):
        try:
            selected_item = self.prohibited_table.focus()
            if selected_item:
                self.prohibited_table.selection_remove(selected_item)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to unselected: {str(ex)}", parent=self.root)

    # ==================Clear all entries FUNCTIOn========================
    def clear_entry_fields(self):
        # Clear input fields
        self.set_current_date()
        self.txt_mfgnum.delete(0, tk.END)
        self.txt_partnum.delete(0, tk.END)
        self.txt_custpo.delete(0, tk.END)
        self.txt_des.delete(0, tk.END)
        self.txt_qty.delete(0, tk.END)
        self.cat_combo.set("Select Category")
        self.txt_search.delete(0, tk.END)
        self.refresh_database()

    # ================================================ADD FUNCTIOn==================================
    def add_prohibited(self):
        date_var = self.txt_date.get()
        mfgnum_var = self.txt_mfgnum.get().upper()  # Convert to uppercase
        partnum_var = self.txt_partnum.get().upper()  # Convert to uppercase
        custpo_var = self.txt_custpo.get()
        des_var = self.txt_des.get()
        qty_var = self.txt_qty.get()
        category_var = self.cat_combo.get()
        if not mfgnum_var:
            messagebox.showerror("Error", "Enter the Manufacturing number", parent=self.root)
            return
        if category_var == "Select Category":
            messagebox.showerror("Error", "Select the Component Category", parent=self.root)
            return

        try:
            # Check if the quantity is a valid positive integer
            if not re.match(r'^\d+$', str(qty_var)):
                messagebox.showerror("Error", "Quantity must not be special characters", parent=self.root)
                return
            quantity = int(qty_var)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)

        try:
            # Save the item details to the register table in the database
            self.connection = sqlite3.connect("nonflight.db")
            cursor = self.connection.cursor()
            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]
            for category in categories:
                # Check if the item with the same manufacturing number and ordered by entity exists in the register table
                cursor = self.connection.execute(
                    f"SELECT id FROM `{category_var}` WHERE date = ? AND mfgnum = ? AND partnum = ? AND custPO = ?",
                    (date_var, mfgnum_var, partnum_var, custpo_var))
                existing_entry = cursor.fetchone()
                if existing_entry:
                    # If the item already exists, update the entry
                    self.connection.execute(
                        f"UPDATE `{category_var}` SET description = ?, quantity = ? WHERE id = ?",
                        (des_var, quantity, existing_entry[0]))
                else:
                    # If the item doesn't exist, insert a new entry
                    self.connection.execute(
                        f"INSERT INTO `{category_var}` (date, mfgnum, partnum, custPO, description, quantity) VALUES (?, ?, ?, ?, ?, ?)",
                        (date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity))

                self.connection.commit()
                # Update the total quantity in the register_summary table
                self.connection = sqlite3.connect("nonflight.db")
                cursor = self.connection.execute(
                    f"SELECT mfgnum, SUM(quantity) AS total_quantity FROM `{category_var}` GROUP BY mfgnum")
                summary_data = cursor.fetchall()

                self.connection.execute(f"DELETE FROM `{category_var}_summary`")
                self.connection.executemany(
                    f"INSERT INTO `{category_var}_summary` (mfgnum, total_quantity) VALUES (?, ?)",
                    summary_data)
                self.connection.commit()

            # Clear input fields
            self.clear_entry_fields()
            # Clear the tree inventory
            self.prohibited_table.delete(*self.prohibited_table.get_children())
            self.connection = sqlite3.connect("nonflight.db")
            # Retrieve the newly added item from the respective category table
            cursor = self.connection.execute(
                f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category_var}` "
                f"ORDER BY id DESC LIMIT 1")
            item = cursor.fetchone()
            if item:
                id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity = item
                self.prohibited_table.insert("", 0, text=category_var,
                                          values=(id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity))
                messagebox.showinfo("Success", "Component added successfully", parent=self.root)

            self.connection.commit()
            self.refresh_database()
            self.connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)

    # ====================================================UPDATE FUNCTIOn=============================================

    def update_prohibited(self):
        date_var = self.txt_date.get()
        mfgnum_var = self.txt_mfgnum.get()
        partnum_var = self.txt_partnum.get().upper()  # Convert to uppercase
        custpo_var = self.txt_custpo.get()
        des_var = self.txt_des.get()
        qty_var = self.txt_qty.get()
        category_var = self.cat_combo.get()
        # Get the selected item from the Treeview
        selected_item_id = self.prohibited_table.selection()
        if not selected_item_id:
            # If no item is selected, show a message and return
            messagebox.showwarning("Warning", "Please select an item to update.", parent=self.root)
            return

        if not mfgnum_var:
            messagebox.showerror("Error", "Enter the Manufacturing number", parent=self.root)
            return
        if category_var == "Select Category":
            messagebox.showerror("Error", "Select the Component Category", parent=self.root)
            return

        try:
            # Check if the quantity is a valid positive integer
            if not re.match(r'^\d+$', str(qty_var)):
                messagebox.showerror("Error", "Quantity must not be special characters", parent=self.root)
                return
            quantity = int(qty_var)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)

        # Get the unique ID from the selected item's values (index 0 is the ID)
        unique_id = self.prohibited_table.item(selected_item_id, "values")[0]

        # Save the item details to the register table in the database
        self.connection = sqlite3.connect("nonflight.db")
        cursor = self.connection.cursor()
        # Check if the selected item exists in the register table based on the unique ID
        cursor.execute(f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category_var}` WHERE id = ?", (unique_id,))
        existing_item = cursor.fetchone()
        if existing_item:
            # If the item exists, update its details
            cursor.execute(
                f"UPDATE `{category_var}` SET date=?, mfgnum=?, partnum=?, custPO=?, description=?, quantity=? WHERE id = ?",
                (date_var, mfgnum_var, partnum_var, custpo_var, des_var, qty_var, unique_id))
            self.connection.commit()

            self.clear_entry_fields()
            # Clear the tree inventory
            self.prohibited_table.delete(*self.prohibited_table.get_children())
            self.connection = sqlite3.connect("nonflight.db")
            # Retrieve the newly added item from the respective category table
            cursor = self.connection.execute(
                f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category_var}` "
                f"ORDER BY timestamp DESC LIMIT 1")
            item = cursor.fetchone()
            if item:
                id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity = item
                self.prohibited_table.insert("", 0, text=category_var,
                                          values=(id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity))
                messagebox.showinfo("Success", "Component updated successfully", parent=self.root)

        else:
            # If the item doesn't exist, show a message
            messagebox.showwarning("Warning", f"No component with ID {unique_id} found.", parent=self.root)

        self.refresh_database()
        self.connection.close()

    # ====================================================DELETE FUNCTIOn==============================================
    def delete_data(self):
        selected_item = self.prohibited_table.focus()
        category_var = self.cat_combo.get()

        try:
            if not selected_item:
                messagebox.showerror("Error", "Search for components using the search engine", parent=self.root)
                return

            selected_item_id = self.prohibited_table.selection()
            if not selected_item_id:
                # If no item is selected, show a message and return
                messagebox.showwarning("Warning", "Please DELETE.", parent=self.root)
                return

            # Get the unique ID from the selected item's values (index 0 is the ID)
            unique_id = self.prohibited_table.item(selected_item_id, "values")[0]

            # Save the item details to the register table in the database
            self.connection = sqlite3.connect("nonflight.db")
            cursor = self.connection.cursor()
            # Check if the selected item exists in the register table based on the unique ID
            cursor.execute(
                f"SELECT id, date, mfgnum, partnum, custPO, description, quantity, timestamp FROM `{category_var}` WHERE id = ?",
                (unique_id,))
            existing_item = cursor.fetchone()
            # Ask for confirmation before proceeding with the deletion
            confirmation = messagebox.askyesno("Warning", "Do you want to delete the item?", parent=self.root)
            if not confirmation:
                return

            if existing_item:
                # If the item exists, update its details
                cursor.execute(
                    f"DELETE FROM `{category_var}` WHERE id = ?",
                    (unique_id,))
                self.connection.commit()

                # Remove the item from the tree inventory
                self.prohibited_table.delete(selected_item)
                messagebox.showinfo("Success", "Item has been deleted", parent=self.root)

                self.refresh_database()

                self.connection.close()
                self.clear_entry_fields()

            else:
                # No matching item found in the database
                messagebox.showwarning("Warning", "No matching item found in the database for deletion.", parent=self.root)

        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"SQLite Error: {str(ex)}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Unexpected Error: {str(ex)}", parent=self.root)

    # ================================================= UPDATE Treeview FUNCTIOn=======================================

    def update_treeview(self):

        try:
            # Check if the selected item exists in the register table based on the unique ID
            self.connection = sqlite3.connect("nonflight.db")

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            # Clear the existing data in the Treeview
            self.prohibited_table.delete(*self.prohibited_table.get_children())


            # Fetch data from each database table based on the selected category
            for category in categories:
                cursor = self.connection.execute(f"SELECT * FROM `{category}`")
                data = cursor.fetchall()

                # Insert data into the Treeview
                for item in data:
                    item_id = item[0]  # Assuming the ID is the first value in the item tuple
                    item_data = item[0:]  # The rest of the data for the item
                    self.prohibited_table.insert("", 0, text=category, values=item_data, tags=(item_id,))

            self.connection.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # ========================================Search FUNCTIOn===================================

    def search(self):
        try:
            # Check if the selected item exists in the register table based on the unique ID
            self.connection = sqlite3.connect("nonflight.db")
            cursor = self.connection.cursor()
            search_query = self.txt_search.get().upper()

            if not search_query:
                messagebox.showerror("Error", "Enter the Manufacturing Number", parent=self.root)
                return

            # Clear the tree inventory
            self.prohibited_table.delete(*self.prohibited_table.get_children())

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            mfgnum_found = False  # Flag to track if any mfgnum is found in the category table

            for category in categories:
                cursor.execute(
                    f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category}` WHERE UPPER(mfgnum) = UPPER(?)",
                    (search_query,)
                )
                items = cursor.fetchall()

                # Add items to the tree inventory
                for item in items:
                    id, date, mfgnum, partnum, custPO, description, quantity = item

                    self.prohibited_table.insert("", 0, text=category,
                                              values=(id, date, mfgnum, partnum, custPO, description, quantity))

                    mfgnum_found = True

            if not mfgnum_found:
                messagebox.showinfo("Not Found",
                                    f"Manufacturing Number '{search_query}' not found in any category.", parent=self.root)

            self.connection.commit()
            self.connection.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due 5: {str(ex)}", parent=self.root)


# =========================================Fetch Data from Treeview FUNCTIOn===================================

    def fetch_data(self, event):
        try:
            selected_item = self.prohibited_table.selection()

            if not selected_item:
                return

            # Get the values of the selected item
            values = self.prohibited_table.item(selected_item, "values")
            # Store the value of column 0 temporarily for later use
            temp_id = values[0]

            # Populate the entry boxes with the fetched data (excluding the first column)
            date, mfgnum, partnum, custPO, description, quantity = values[1:7]

            # Fill the item type, item name, and quantity fields with the selected item's details
            category_type = self.prohibited_table.item(selected_item, "text")
            self.cat_combo.set(category_type)

            # Fill the entry boxes with the selected item's details
            self.txt_date.delete(0, tk.END)
            self.txt_date.insert(0, date)

            self.txt_mfgnum.delete(0, tk.END)
            self.txt_mfgnum.insert(0, mfgnum)

            self.txt_partnum.delete(0, tk.END)
            self.txt_partnum.insert(0, partnum)

            self.txt_custpo.delete(0, tk.END)
            self.txt_custpo.insert(0, custPO)

            self.txt_des.delete(0, tk.END)
            self.txt_des.insert(0, description)

            self.txt_qty.delete(0, tk.END)
            self.txt_qty.insert(0, quantity)


        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # =========================================Clear DATA FUNCTIOn===================================
    def clear_all(self):
        try:
            #this will refresh the database
            self.refresh_database()
            # Clear the input fields
            self.clear_entry_fields()
            # Clear the Treeview by deleting all items ('all' argument)
            self.prohibited_table.delete(*self.prohibited_table.get_children())

        except Exception as ex:
            messagebox.showerror("Error", f"Error due 7: {str(ex)}", parent=self.root)


#############--------------------------SHOW ALL FUNCTION-----------------------------------------------

    def refresh_database(self):
        try:
            self.connection = sqlite3.connect("nonflight.db")
            cursor = self.connection.cursor()

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            # Step 1: Update category_summary table with merged quantities
            for category in categories:
                # Get all unique mfgnum values from the category table and their merged quantities
                cursor.execute(f"SELECT mfgnum, SUM(quantity) FROM `{category}` GROUP BY mfgnum")
                merged_data = cursor.fetchall()

                # Update or insert the summarized information in the category_summary table
                for mfgnum, total_quantity in merged_data:
                    cursor.execute(
                        f"INSERT OR REPLACE INTO `{category}_summary` (mfgnum, total_quantity) VALUES (?, ?)",
                        (mfgnum, total_quantity))

            # Step 2: Check and update total_quantity in category_summary table
            for category in categories:
                # Get all mfgnum and total_quantity from the category_summary table
                cursor.execute(f"SELECT mfgnum, total_quantity FROM `{category}_summary`")
                summary_data = cursor.fetchall()

                for mfgnum, total_quantity in summary_data:
                    # Calculate the sum of quantities for the current mfgnum from the category table
                    cursor.execute(f"SELECT SUM(quantity) FROM `{category}` WHERE mfgnum = ?", (mfgnum,))
                    category_total_quantity = cursor.fetchone()[0]

                    if category_total_quantity is None:
                        category_total_quantity = 0

                    # Update the total_quantity in the category_summary table if different
                    if total_quantity != category_total_quantity:
                        cursor.execute(f"UPDATE `{category}_summary` SET total_quantity = ? WHERE mfgnum = ?",
                                       (category_total_quantity, mfgnum))

            self.connection.commit()
            self.connection.close()

            # Update the Treeview with the latest data
            self.update_treeview()

        except Exception as ex:
            print(f"Error refreshing the database: {str(ex)}")





    ############--------------------------CLOSE FUNCTION----------------------------------------------


    def close_prohibited(self):

        self.enable_button()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = Prohibited_class(root, None)
    root.mainloop()




"""def add_product(self):
        date_var = self.txt_date.get()
        mfgnum_var = self.txt_mfgnum.get().upper()  # Convert to uppercase
        partnum_var = self.txt_partnum.get().upper()  # Convert to uppercase
        custpo_var = self.txt_custpo.get()
        des_var = self.txt_des.get()
        qty_var = self.txt_qty.get()
        category_var = self.cat_combo.get()
        if not mfgnum_var:
            messagebox.showerror("Error", "Enter the Manufacturing number", parent=self.root)
            return
        if category_var == "Select Category":
            messagebox.showerror("Error", "Select the Component Category", parent=self.root)
            return

        try:
            # Check if the quantity is a valid positive integer
            if not re.match(r'^\d+$', str(qty_var)):
                messagebox.showerror("Error", "Quantity must not be special characters", parent=self.root)
                return
            quantity = int(qty_var)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)

        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                               database="flight")
            self.cur = self.con.cursor()

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            for category in categories:
                # Check if the item with the same manufacturing number and ordered by entity exists in the register table
                self.cur.execute(
                    f"SELECT id FROM `{category_var}` WHERE date = %s AND mfgnum = %s AND partnum = %s AND custPO = %s",
                    (date_var, mfgnum_var, partnum_var, custpo_var))
                existing_entry = self.cur.fetchone()

                if existing_entry:
                    # If the item already exists, update the entry
                    self.cur.execute(
                        f"UPDATE `{category_var}` SET description = %s, quantity = %s WHERE id = %s",
                        (des_var, quantity, existing_entry[0]))

                else:
                    # If the item doesn't exist, insert a new entry
                    self.cur.execute(
                        f"INSERT INTO `{category_var}` (date, mfgnum, partnum, custPO, description, quantity) VALUES (%s, %s, %s, %s, %s, %s)",
                        (date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity))

                self.con.commit()

                self.cur.execute(
                    f"SELECT mfgnum, SUM(quantity) AS total_quantity FROM `{category_var}` GROUP BY mfgnum")
                summary_data = self.cur.fetchall()

                self.cur.execute(f"DELETE FROM `{category_var}_summary`")
                self.cur.executemany(
                    f"INSERT INTO `{category_var}_summary` (mfgnum, total_quantity) VALUES (%s, %s)",
                    summary_data)
                self.con.commit()

            # Clear input fields
            self.clear_entry_fields()
            # Clear the tree inventory
            self.product_table.delete(*self.product_table.get_children())

            # Retrieve the newly added item from the respective category table
            self.cur.execute(
                f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category_var}` "
                f"ORDER BY id DESC LIMIT 1")
            item = self.cur.fetchone()
            if item:
                id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity = item
                self.product_table.insert("", 0, text=category_var,
                                          values=(id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity))
                messagebox.showinfo("Success", "Component added successfully", parent=self.root)

            self.con.commit()
            self.refresh_database()
            self.con.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"An error occurred ADDITION: {str(e)}", parent=self.root)"""

