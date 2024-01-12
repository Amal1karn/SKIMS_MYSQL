import sqlite3
from datetime import date
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import re


class stockOUT_class:
    def __init__(self, root, enable_button):
        self.root = root
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.title("STOCK-OUT")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.lift()
        self.enable_button = enable_button

        # ==================================TITLE FRAME ===============================================================

        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#03B4E6")
        self.title_frame.pack(side=TOP, fill=X)

        Label(self.title_frame, text="Stock-Out", font=("times new roman", 30, "bold"),
              bg="#03B4E6", fg="white", bd=10, relief=GROOVE).pack(side=TOP, fill=X)

        self.closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), bg="#0F148C",
                               cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.close_stock_out)
        self.closebtn.place(x=1090, y=15, width=100, height=37)

        # ==================================Frame 1==================================================================

        details_frame = Frame(self.root, bd=10, relief=RIDGE, bg="#03B4E6")
        details_frame.place(x=5, y=80, width=1220, height=310)

        # =============================================Invoice Label and Entry===============================
        manage_title = Label(details_frame, text="", font=("times new roman", 25, "bold"), bg="#03B4E6",
                             bd=8, fg="#0F148C", justify=CENTER)
        manage_title.grid(row=0, column=2, padx=0, pady=0)

        # =============================================MFG Number Label and Entry=============================
        self.date_label = Label(details_frame, text="Date:", font=("times new roman", 17, "bold"),
                                bg="#03B4E6", fg="black", anchor='w')
        self.date_label.grid(row=1, column=0, pady=10, padx=20, sticky="e")

        self.date_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                bd=5, relief=RIDGE, justify=CENTER)
        self.date_entry.grid(row=1, column=1, pady=10, padx=30, sticky="w")

        # =============================================MFG Number Label and Entry=============================
        self.mfgnum_label = Label(details_frame, text="MFG Number:", font=("times new roman", 17, "bold"),
                                  bg="#03B4E6", fg="black", anchor='w')
        self.mfgnum_label.grid(row=2, column=0, pady=10, padx=20, sticky="e")

        self.mfgnum_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                  bd=5, relief=RIDGE, justify=CENTER)
        self.mfgnum_entry.grid(row=2, column=1, pady=10, padx=30, sticky="w")

        # =============================================MFG Number Label and Entry=============================
        self.usedBy_label = Label(details_frame, text="Used By:", font=("times new roman", 17, "bold"),
                                  bg="#03B4E6", fg="black", anchor='w')
        self.usedBy_label.grid(row=3, column=0, pady=10, padx=20, sticky="e")

        self.usedBy_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                  bd=5, relief=RIDGE, justify=CENTER)
        self.usedBy_entry.grid(row=3, column=1, pady=10, padx=30, sticky="w")

        # ===========================================Quantity entry and label======================================================

        self.description_label = Label(details_frame, text="Description:", font=("times new roman", 17, "bold"),
                                       bg="#03B4E6", fg="black", anchor='w')
        self.description_label.grid(row=1, column=2, pady=10, padx=20, sticky="e")

        self.description_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                       bd=5, relief=RIDGE, justify=CENTER)
        self.description_entry.grid(row=1, column=3, pady=10, padx=30, sticky="w")

        # =============================================MFG Number Label and Entry=============================
        self.quantity_label = Label(details_frame, text="Quantity:", font=("times new roman", 17, "bold"),
                                    bg="#03B4E6", fg="black", anchor='w')
        self.quantity_label.grid(row=2, column=2, pady=10, padx=20, sticky="e")

        self.quantity_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                    bd=5, relief=RIDGE, justify=CENTER)
        self.quantity_entry.grid(row=2, column=3, pady=10, padx=30, sticky="w")

        # ============================================BUTTONs======================================================
        self.button_frame = Frame(details_frame, bd=0, relief=FLAT, bg="#03B4E6")
        self.button_frame.place(x=950, y=50, width=150, height=200)

        self.used_button = Button(self.button_frame, text="OUT", font=("arial", 15, "bold"), bg="#0F148C", width=7,
                                  cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.perform_stock_out)
        self.used_button.grid(row=0, column=0, pady=25, padx=10)

        self.clear_button = Button(self.button_frame, text="CLEAR", font=("arial", 15, "bold"), bg="#0F148C", width=7,
                                   cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.clear_entry_fields)
        self.clear_button.grid(row=1, column=0, padx=10, pady=25)

        # =================================Treeview Frame==========================================================

        self.table_frame = Frame(self.root, bd=10, relief=RIDGE, bg="#03B4E6")
        self.table_frame.place(x=5, y=390, width=1220, height=200)

        # ==========================TREEVIEW====================================
        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.stockOUT_table = ttk.Treeview(self.table_frame, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.stockOUT_table.xview)
        scroll_y.config(command=self.stockOUT_table.yview)

        self.stockOUT_table["columns"] = ("date", "mfgnum", "custPO", "description", "quantity", "totalQTY")

        # Configure the Treeview columns
        self.stockOUT_table.heading("#0", text="CATEGORY")
        self.stockOUT_table.heading("date", text="DATE")
        self.stockOUT_table.heading("mfgnum", text="MFG NO.")
        self.stockOUT_table.heading("custPO", text="USED BY")
        self.stockOUT_table.heading("description", text="DESCRIPTION")
        self.stockOUT_table.heading("quantity", text="QTY")
        self.stockOUT_table.heading("totalQTY", text="TOTAL QTY")

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), foreground='#0F148C', background='black')

        # Configure the Treeview headings

        self.stockOUT_table.column("#0", width=60)
        self.stockOUT_table.column("date", width=60)
        self.stockOUT_table.column("mfgnum", width=60)
        self.stockOUT_table.column("custPO", width=100)
        self.stockOUT_table.column("description", width=200)
        self.stockOUT_table.column("quantity", width=40)
        self.stockOUT_table.column("totalQTY", width=40)

        self.stockOUT_table.pack(fill=BOTH, expand=1)

        self.stockOUT_table.bind("<<TreeviewSelect>>")

        self.clear_entry_fields()

    # =========================================DATE FUNCTIOn===================================
    def set_current_date(self):
        try:
            current_date = date.today().strftime("%Y/%m/%d")
            self.date_entry.delete(0, tk.END)  # Clear any existing text
            self.date_entry.insert(0, current_date)  # Insert the current date into the widget
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to date: {str(ex)}", parent=self.root)

    # ====================================================================================

    def perform_stock_out(self):
        date = self.date_entry.get()
        mfgnum = self.mfgnum_entry.get().upper()  # Convert to uppercase
        des = self.description_entry.get()
        usedby = self.usedBy_entry.get()
        quantity_used = self.quantity_entry.get()

        if not date or not mfgnum or not des or not usedby or not quantity_used:
            messagebox.showerror("Error", "Must enter all details.", parent=self.root)
            return

        try:
            # Check if the quantity is a valid positive integer
            if not re.match(r'^\d+$', str(quantity_used)):
                messagebox.showerror("Error", "Quantity must be a positive integer.", parent=self.root)
                return
            quantity = int(quantity_used)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive number.", parent=self.root)
            return

        try:
            # Save the item details to the register table in the database
            self.connection = sqlite3.connect("flight.db")
            cursor = self.connection.cursor()

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            found_in_category = False
            category = ""

            # Check if the mfgnum exists in the category_summary table
            for category in categories:
                cursor.execute(f"SELECT total_quantity FROM `{category}_summary` WHERE mfgnum=?", (mfgnum,))
                row = cursor.fetchone()
                if row is not None:
                    total_quantity = row[0]
                    found_in_category = True
                    break

            if not found_in_category:
                messagebox.showerror("Error", f"MFG Number {mfgnum} not found in the system.", parent=self.root)
                self.connection.close()
                return

            if total_quantity < quantity:
                messagebox.showerror("Error", f"Only {total_quantity} available in stock. Please order more.",
                                     parent=self.root)
                self.connection.close()
                return

            elif total_quantity == quantity:
                # Subtract the quantity used from category_summary table by mfgnum
                cursor.execute(f"UPDATE `{category}_summary` SET total_quantity=? WHERE mfgnum=?",
                               (total_quantity - quantity, mfgnum))

                # Add the entries to the category table with the quantity in negative
                cursor.execute(
                    f"INSERT INTO `{category}` (date, mfgnum, custPO, description, quantity, partnum) "
                    f"VALUES (?, ?, ?, ?, ?, ?)",
                    (date, mfgnum, usedby, des, -quantity, ""))

                cursor.execute(f"SELECT * FROM `{category}_summary`")
                rows = cursor.fetchall()
                self.stockOUT_table.delete(*self.stockOUT_table.get_children())
                for row in rows:
                    self.stockOUT_table.insert("", 0, text=category,
                                               values=(date, row[0], usedby, des, -quantity, row[1]))

                # self.stockOUT_table.insert("", 0, text=category,
                # values=(date, mfgnum, usedby, des, -quantity))

                messagebox.showinfo("Success", f"Stock out operation successful. No more stock left, please order.",
                                    parent=self.root)
                self.clear_entry_fields()
            else:
                # Subtract the quantity used from category_summary table by mfgnum
                cursor.execute(f"UPDATE `{category}_summary` SET total_quantity=? WHERE mfgnum=?",
                               (total_quantity - quantity, mfgnum))

                # Add the entries to the category table with the quantity in negative
                cursor.execute(
                    f"INSERT INTO `{category}` (date, mfgnum, custPO, description, quantity, partnum) "
                    f"VALUES (?, ?, ?, ?, ?, ?)",
                    (date, mfgnum, usedby, des, -quantity, ""))

                remaining_quantity = total_quantity - quantity

                # self.stockOUT_table.insert("", 0, text=category,
                # values=(date, mfgnum, usedby, des, -quantity))

                cursor.execute(f"SELECT * FROM `{category}_summary`")
                rows = cursor.fetchall()
                self.stockOUT_table.delete(*self.stockOUT_table.get_children())
                for row in rows:
                    self.stockOUT_table.insert("", 0, text=category,
                                               values=(date, row[0], usedby, des, -quantity, row[1]))
                messagebox.showinfo("Success",
                                    f"Stock out operation successful. Remaining quantity: {remaining_quantity}.", parent=self.root)

                self.clear_entry_fields()

            self.connection.commit()
            self.refresh_database()
            self.connection.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error stockout: {str(ex)}", parent=self.root)

    #############--------------------------Refresh DATABASE FUNCTION-----------------------------------------------

    def refresh_database(self):
        try:
            self.connection = sqlite3.connect("flight.db")
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
            # self.update_treeview()

        except Exception as ex:
            print(f"Error refreshing the database: {str(ex)}")

    # ==================Clear all entries FUNCTIOn========================
    def clear_entry_fields(self):
        # Clear input fields
        self.set_current_date()
        self.mfgnum_entry.delete(0, tk.END)
        self.usedBy_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.stockOUT_table.delete(*self.stockOUT_table.get_children())
        # self.cat_combo.set("Select Category")

    # ==================CLOSE FUNCTIOn========================

    def close_stock_out(self):
        self.enable_button()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = stockOUT_class(root, None)
    root.mainloop()
