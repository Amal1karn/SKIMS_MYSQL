from tkinter import *
from datetime import date
from tkinter import END
import datetime
import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
import re


class ProductClass:
    def __init__(self, root, enable_button):
        self.root = root
        self.root.title("FLIGHT: STOCK IN")
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.config(bg="white")
        self.enable_button = enable_button
        # =============================Connect to the database==================================

        # Create separate tables for each category if they don't exist
        categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                      "Connectors", "Voltage_n_Regulator", "LEDs",
                      "Diodes_n_Rectifiers", "Others"]

        # ============================title frame============================
        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.title_frame.pack(side=TOP, fill=X)

        title = Label(self.title_frame, text="FLIGHT-STOCK IN", bd=10, relief=GROOVE,
                      font=("times new roman", 30, "bold"), bg="#63B8FF", fg="white")
        title.pack(side=TOP, fill=X)

        closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), relief=RAISED, bd=8,
                          bg="#0F148C", cursor="hand2", fg="white", command=self.close_product)
        closebtn.place(x=1090, y=15, width=100, height=37)

        # ============================menu frame============================
        self.manage_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.manage_frame.place(x=5, y=80, width=385, height=500)

        # Create a label and entry widget for the date
        lbl_date = Label(self.manage_frame, text="Date:", font=("times new roman", 17, "bold"),
                         bg="#63B8FF", fg="black")
        lbl_date.grid(row=0, column=0, pady=8, padx=(13, 5), sticky="w")
        self.txt_date = Entry(self.manage_frame, font=("times new roman", 12, "bold"),
                              bd=5, relief=GROOVE)
        self.txt_date.grid(row=0, column=1, pady=8, padx=8, sticky="w")

        # Create a label and entry widget for the MFG NUMBER
        lbl_mfgnum = Label(self.manage_frame, text="MFG No:", font=("times new roman", 17, "bold"),
                           bg="#63B8FF", fg="black")
        lbl_mfgnum.grid(row=1, column=0, pady=8, padx=(13, 5), sticky="w")
        self.txt_mfgnum = Entry(self.manage_frame, font=("times new roman", 12, "bold"),
                                bd=5, relief=GROOVE)
        self.txt_mfgnum.grid(row=1, column=1, pady=8, padx=8, sticky="w")

        # ========== Create a label and entry widget for the PART NUMBER
        lbl_partnum = Label(self.manage_frame, text="Part No:",
                            font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_partnum.grid(row=2, column=0, pady=8, padx=(13, 5), sticky="w")
        self.txt_partnum = Entry(self.manage_frame,
                                 font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_partnum.grid(row=2, column=1, pady=8, padx=8, sticky="w")

        # ============= Create a label and entry widget for the CUSTOMER PO
        lbl_custpo = Label(self.manage_frame, text="Customer PO:", font=("times new roman", 17, "bold"),
                           bg="#63B8FF", fg="black")
        lbl_custpo.grid(row=3, column=0, pady=8, padx=(13, 5), sticky="w")
        self.txt_custpo = Entry(self.manage_frame,
                                font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_custpo.grid(row=3, column=1, pady=8, padx=8, sticky="w")

        # ========== Create a label and entry widget for the item name
        lbl_des = Label(self.manage_frame, text="Description:",
                        font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_des.grid(row=4, column=0, pady=8, padx=(13, 5), sticky="w")
        self.txt_des = Entry(self.manage_frame,
                             font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_des.grid(row=4, column=1, pady=8, padx=8, sticky="w", )

        # ============= Create a label and entry widget for the QUANTITY
        lbl_qty = Label(self.manage_frame, text="Quantity:",
                        font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_qty.grid(row=5, column=0, pady=8, padx=(13, 5), sticky="w")
        self.txt_qty = Entry(self.manage_frame,
                             font=("times new roman", 12, "bold"), bd=5, relief=GROOVE)
        self.txt_qty.grid(row=5, column=1, pady=8, padx=8, sticky="w")

        # ======================Create a combobox Label===================

        lbl_category = Label(self.manage_frame, text="Category",
                             font=("times new roman", 17, "bold"), bg="#63B8FF", fg="black")
        lbl_category.grid(row=6, column=0, pady=8, padx=(13, 5), sticky="w")

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
                         bg="#0F148C", cursor="hand2", fg="white", width=6, command=self.add_product)
        add_btn.grid(row=0, column=0, padx=8, pady=15)

        # Create an "Update Item" button
        update_btn = Button(btn_frame, text="Update", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                            bg="#0F148C", cursor="hand2", fg="white", width=6, command=self.update_product)
        update_btn.grid(row=0, column=1, padx=8, pady=15)

        # Create an "CLEAR" button
        clear_btn = Button(btn_frame, text="Clear", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                           bg="#0F148C", cursor="hand2", fg="white", width=6, command=self.clear_all)
        clear_btn.grid(row=0, column=2, padx=8, pady=15)

        delete_btn = Button(btn_frame, text="Delete", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                            bg="#0F148C", cursor="hand2", fg="white", width=6,
                            command=self.delete_data)
        delete_btn.grid(row=0, column=3, padx=8, pady=15)

        # =======================================SEARCH FRAME================================#
        self.detail_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.detail_frame.place(x=392, y=80, width=835, height=500)

        lbl_search = Label(self.detail_frame, text="Search by MFG No:",
                           font=("times new roman", 15, "bold"), bg="#63B8FF", fg="black")
        lbl_search.grid(row=0, column=0, pady=10, padx=(250, 3), sticky="w")

        self.txt_search = Entry(self.detail_frame, font=("times new roman", 13, "bold"),
                                bd=5, relief=GROOVE)
        self.txt_search.grid(row=0, column=1, pady=10, padx=(3, 20), sticky="w")

        search_btn = Button(self.detail_frame, text="Search", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                            bg="#0F148C", cursor="hand2", fg="white", width=6, padx=5, command=self.search)
        search_btn.grid(row=0, column=2, padx=18, pady=10)

        # ==========================TREEVIEW FRAME====================================
        self.table_frame = Frame(self.detail_frame, bd=4, relief=RIDGE, bg="black")
        self.table_frame.place(x=0, y=59, width=827, height=430)

        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.product_table = ttk.Treeview(self.table_frame, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.product_table.xview)
        scroll_y.config(command=self.product_table.yview)

        self.product_table["columns"] = (
        "id", "date", "mfgnum", "partnum", "custPO", "description", "quantity", "timestamp")

        # Configure the Treeview columns
        self.product_table.heading("#0", text="Category")
        self.product_table.heading("id", text="id")
        self.product_table.heading("date", text="Date")
        self.product_table.heading("mfgnum", text="Manufacturing No.")
        self.product_table.heading("partnum", text="Part No.")
        self.product_table.heading("custPO", text="Customer PO")
        self.product_table.heading("description", text="Description")
        self.product_table.heading("quantity", text="QTY")
        self.product_table.heading("timestamp", text="TIMESTAMP")

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), foreground='#0F148C', background='black')

        # Configure the Treeview headings
        # self.product_table['show'] = 'headings'
        self.product_table.column("#0", width=80)
        self.product_table.column("id", width=0, stretch=tk.NO)
        self.product_table.column("date", width=80)
        self.product_table.column("mfgnum", width=100)
        self.product_table.column("partnum", width=100)
        self.product_table.column("custPO", width=100)
        self.product_table.column("description", width=200)
        self.product_table.column("quantity", width=50)
        self.product_table.column("timestamp", width=0, stretch=tk.NO)

        self.product_table.pack(fill=BOTH, expand=1)

        self.product_table.bind("<<TreeviewSelect>>", self.fetch_data)

        # Configure tags for even rows
        self.product_table.tag_configure("even_row", background="lightgray")
        # udpate treeview
        self.update_treeview()
        # clear all entries
        self.clear_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1223334444@SK",
            database="flight"
        )

        self.cur = self.con.cursor()

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
            current_date = date.today().strftime("%Y-%m-%d")
            self.txt_date.delete(0, tk.END)  # Clear any existing text
            self.txt_date.insert(0, current_date)  # Insert the current date into the widget
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to date: {str(ex)}", parent=self.root)

    # ===============================unselect FUNCTIOn========================

    def unselect_item(self):
        try:
            selected_item = self.product_table.focus()
            if selected_item:
                self.product_table.selection_remove(selected_item)
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

    # ================================================ADD FUNCTIOn==================================


    # ====================================================UPDATE FUNCTIOn=============================================
    # ====================================================UPDATE FUNCTIOn=============================================
    # ====================================================UPDATE FUNCTIOn=============================================
    def add_product(self):
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

            # Create a temporary table
            temp_table_name = f"temp_{category_var}"

            self.cur.execute(f"CREATE TEMPORARY TABLE `{temp_table_name}` LIKE `{category_var}`")

            for category in categories:
                # Check if the item with the same manufacturing number and ordered by entity exists in the register table
                self.cur.execute(
                    f"SELECT id FROM `{category_var}` WHERE date = %s AND mfgnum = %s AND partnum = %s AND custPO = %s",
                    (date_var, mfgnum_var, partnum_var, custpo_var))
                existing_entry = self.cur.fetchone()

                if existing_entry:
                    # If the item already exists, update the temporary table
                    self.cur.execute(
                        f"UPDATE `{temp_table_name}` SET description = %s, quantity = %s WHERE id = %s",
                        (des_var, quantity, existing_entry[0]))
                else:
                    # If the item doesn't exist, insert into the temporary table
                    self.cur.execute(
                        f"INSERT INTO `{temp_table_name}` (date, mfgnum, partnum, custPO, description, quantity) VALUES (%s, %s, %s, %s, %s, %s)",
                        (date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity))

            # Update the main table with the results from the temporary table
            self.cur.execute(
                f"INSERT INTO `{category_var}` SELECT * FROM `{temp_table_name}` ON DUPLICATE KEY UPDATE `{category_var}`.description = `{temp_table_name}`.description, `{category_var}`.quantity = `{temp_table_name}`.quantity")

            # Drop the temporary table
            self.cur.execute(f"DROP TEMPORARY TABLE IF EXISTS `{temp_table_name}`")

            # Commit changes
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
            messagebox.showerror("Error", f"An error occurred ADDITION: {str(e)}", parent=self.root)

    # ====================================================UPDATE FUNCTIOn=============================================
    # ====================================================UPDATE FUNCTIOn=============================================
    # ====================================================UPDATE FUNCTIOn=============================================
    # ====================================================UPDATE FUNCTIOn=============================================

    def update_product(self):
        date_var = self.txt_date.get()
        mfgnum_var = self.txt_mfgnum.get()
        partnum_var = self.txt_partnum.get().upper()  # Convert to uppercase
        custpo_var = self.txt_custpo.get()
        des_var = self.txt_des.get()
        qty_var = self.txt_qty.get()
        category_var = self.cat_combo.get()
        # Get the selected item from the Treeview
        selected_item_id = self.product_table.selection()
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

        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK", database="flight")
        self.cur = self.con.cursor()

        # Get the unique ID from the selected item's values (index 0 is the ID)
        unique_id = self.product_table.item(selected_item_id, "values")[0]

        # Check if the selected item exists in the register table based on the unique ID
        self.cur.execute(
            f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category_var}` WHERE id = %s",
            (unique_id,))
        existing_item = self.cur.fetchone()
        if existing_item:
            # If the item exists, update its details
            self.cur.execute(
                f"UPDATE `{category_var}` SET date=%s, mfgnum=%s, partnum=%s, custPO=%s, description=%s, quantity=%s WHERE id = %s",
                (date_var, mfgnum_var, partnum_var, custpo_var, des_var, qty_var, unique_id))
            self.con.commit()

            self.clear_entry_fields()
            # Clear the tree inventory
            self.product_table.delete(*self.product_table.get_children())

            # Retrieve the newly added item from the respective category table
            self.cur.execute(
                f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category_var}` "
                f"ORDER BY timestamp DESC LIMIT 1")
            item = self.cur.fetchone()
            if item:
                id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity = item
                self.product_table.insert("", 0, text=category_var,
                                          values=(id, date_var, mfgnum_var, partnum_var, custpo_var, des_var, quantity))
                messagebox.showinfo("Success", "Component updated successfully", parent=self.root)

        else:
            # If the item doesn't exist, show a message
            messagebox.showwarning("Warning", f"No component with ID {unique_id} found.", parent=self.root)

        self.refresh_database()
        self.con.close()

    # ====================================================DELETE FUNCTIOn==============================================
    def delete_data(self):
        selected_item = self.product_table.focus()
        category_var = self.cat_combo.get()

        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                               database="flight")
            self.cur = self.con.cursor()

            if not selected_item:
                messagebox.showerror("Error", "Search for components using the search engine", parent=self.root)
                return

            selected_item_id = self.product_table.selection()
            if not selected_item_id:
                # If no item is selected, show a message and return
                messagebox.showwarning("Warning", "Please DELETE.", parent=self.root)
                return

            # Get the unique ID from the selected item's values (index 0 is the ID)
            unique_id = self.product_table.item(selected_item_id, "values")[0]

            # Check if the selected item exists in the register table based on the unique ID
            self.cur.execute(
                f"SELECT id, date, mfgnum, partnum, custPO, description, quantity, timestamp FROM `{category_var}` WHERE id = %s",
                (unique_id,))
            existing_item = self.cur.fetchone()
            # Ask for confirmation before proceeding with the deletion
            confirmation = messagebox.askyesno("Warning", "Do you want to delete the item?", parent=self.root)
            if not confirmation:
                return

            if existing_item:
                # If the item exists, update its details
                self.cur.execute(
                    f"DELETE FROM `{category_var}` WHERE id = %s",
                    (unique_id,))
                self.con.commit()

                # Remove the item from the tree inventory
                self.product_table.delete(selected_item)
                messagebox.showinfo("Success", "Item has been deleted", parent=self.root)

                self.refresh_database()

                self.con.close()
                self.clear_entry_fields()

            else:
                # No matching item found in the database
                messagebox.showwarning("Warning", "No matching item found in the database for deletion.",
                                       parent=self.root)


        except mysql.connector.Error as ex:
            messagebox.showerror("Error", f"Unexpected Error: {str(ex)}", parent=self.root)

    # ================================================= UPDATE Treeview FUNCTIOn=======================================



    def update_treeview(self):
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                               database="flight")
            self.cur = self.con.cursor()

            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            self.product_table.delete(*self.product_table.get_children())

            for category in categories:
                query = f"SELECT * FROM `{category}`"
                self.cur.execute(query)

                data = self.cur.fetchall()

                for item in data:
                    item_id = item[0]
                    item_data = item[1:]
                    self.product_table.insert("", 0, text=category, values=item_data, tags=(item_id,))

            self.con.commit()

        except mysql.connector.Error as ex:
            # Log the exception details for debugging
            print(f"Error in update_treeview: {ex}")
            messagebox.showerror("Error", "Failed to update Treeview. Check logs for details.", parent=self.root)



    # ========================================Search FUNCTIOn===================================

    def search(self):
        try:

            self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                               database="flight")
            self.cur = self.con.cursor()

            search_query = self.txt_search.get().upper()

            if not search_query:
                messagebox.showerror("Error", "Enter the Manufacturing Number", parent=self.root)
                return

            # Clear the tree inventory
            self.product_table.delete(*self.product_table.get_children())

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            mfgnum_found = False  # Flag to track if any mfgnum is found in the category table

            for category in categories:
                cursor = self.cur.execute(
                    f"SELECT id, date, mfgnum, partnum, custPO, description, quantity FROM `{category}` WHERE UPPER(mfgnum) = UPPER(%s)",
                    (search_query,)
                )
                items = cursor.fetchall()

                # Add items to the tree inventory
                for item in items:
                    id, date, mfgnum, partnum, custPO, description, quantity = item

                    self.product_table.insert("", 0, text=category,
                                              values=(id, date, mfgnum, partnum, custPO, description, quantity))

                    mfgnum_found = True

            if not mfgnum_found:
                messagebox.showinfo("Not Found",
                                    f"Manufacturing Number '{search_query}' not found in any category.",
                                    parent=self.root)

            self.con.commit()
            self.con.close()

        except mysql.connector.Error as ex:
            messagebox.showerror("Error", f"Error due 5: {str(ex)}", parent=self.root)

    # =========================================Fetch Data from Treeview FUNCTIOn===================================

    def fetch_data(self, event):
        try:
            selected_item = self.product_table.selection()

            if not selected_item:
                return

            # Get the values of the selected item
            values = self.product_table.item(selected_item, "values")
            # Store the value of column 0 temporarily for later use
            temp_id = values[0]

            # Populate the entry boxes with the fetched data (excluding the first column)
            date, mfgnum, partnum, custPO, description, quantity = values[1:7]

            # Fill the item type, item name, and quantity fields with the selected item's details
            category_type = self.product_table.item(selected_item, "text")
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
            messagebox.showerror("Error", f"Error fetch data: {str(ex)}", parent=self.root)

    # =========================================Clear DATA FUNCTIOn===================================
    def clear_all(self):
        try:
            # this will refresh the database
            self.refresh_database()
            # Clear the input fields
            self.clear_entry_fields()
            # Clear the Treeview by deleting all items ('all' argument)
            self.product_table.delete(*self.product_table.get_children())

        except Exception as ex:
            messagebox.showerror("Error", f"Error due clear all: {str(ex)}", parent=self.root)

    #############--------------------------Refresh DATABASE FUNCTION-----------------------------------------------



    def refresh_database(self):
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                               database="flight")
            self.cur = self.con.cursor()

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            # Step 1: Update category_summary table with merged quantities
            for category in categories:
                # Get all unique mfgnum values from the category table and their merged quantities
                self.cur.execute(f"SELECT mfgnum, SUM(quantity) FROM `{category}` GROUP BY mfgnum")
                merged_data = self.cur.fetchall()

                # Update or insert the summarized information in the category_summary table
                for mfgnum, total_quantity in merged_data:
                    self.cur.execute(
                        f"REPLACE INTO `{category}_summary` (mfgnum, total_quantity) VALUES (%s, %s)",
                        (mfgnum, total_quantity))

            # Step 2: Check and update total_quantity in category_summary table
            for category in categories:
                # Get all mfgnum and total_quantity from the category_summary table
                self.cur.execute(f"SELECT mfgnum, total_quantity FROM `{category}_summary`")
                summary_data = self.cur.fetchall()

                for mfgnum, total_quantity in summary_data:
                    # Calculate the sum of quantities for the current mfgnum from the category table
                    self.cur.execute(f"SELECT SUM(quantity) FROM `{category}` WHERE mfgnum = %s", (mfgnum,))
                    category_total_quantity = self.cur.fetchone()[0]

                    if category_total_quantity is None:
                        category_total_quantity = 0

                    # Update the total_quantity in the category_summary table if different
                    if total_quantity != category_total_quantity:
                        self.cur.execute(f"UPDATE `{category}_summary` SET total_quantity = %s WHERE mfgnum = %s",
                                         (category_total_quantity, mfgnum))

            self.con.commit()
            # Update the Treeview with the latest data
            self.update_treeview()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"MySQL Error refresh_database: {str(e)}")

    ############--------------------------CLOSE FUNCTION----------------------------------------------

    def close_product(self):
        self.con.close()
        self.enable_button()
        self.root.destroy()

    # ========================================================================


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root, None)
    root.mainloop()
