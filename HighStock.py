import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk

import mysql


class highSTOCK_class:
    def __init__(self, root, enable_button):
        self.root = root
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.title("HIGH STOCK")
        self.root.config(bg="white")
        self.enable_button = enable_button

        # =============================Connect to the database==================================
        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK", database="flight")
        self.cur = self.con.cursor()

        # Connect to the second database "nonflight.db"
        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK", database="nonflight")
        self.cur = self.con.cursor()

        # Create separate tables for each category if they don't exist
        categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                      "Connectors", "Voltage_n_Regulator", "LEDs",
                      "Diodes_n_Rectifiers", "Others"]

        # ==================================TITLE FRAME ===============================================================
        # title frame
        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.title_frame.pack(side=TOP, fill=X)

        Label(self.title_frame, text="High On Stock", font=("times new roman", 30, "bold"),
              bg="#03B4E6", fg="white", bd=10, relief=GROOVE).pack(side=TOP, fill=X)

        self.closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), bg="#0F148C",
                               cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.close_high_stock)
        self.closebtn.place(x=1090, y=15, width=100, height=37)

        # ==================================TREEVIEW FRAME ===============================================================

        self.table_frame = Frame(self.root, bd=15, relief=RIDGE, bg="#63B8FF")
        self.table_frame.place(x=3, y=80, width=1220, height=510)

        # ==========================TREEVIEW====================================
        scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.product_table = ttk.Treeview(self.table_frame, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.product_table.xview)
        scroll_y.config(command=self.product_table.yview)

        self.product_table["columns"] = ("mfgnum", "quantity", "database")

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), foreground='#0F148C', background='black')

        # Configure the Treeview columns
        self.product_table.heading("#0", text="Category")
        self.product_table.heading("mfgnum", text="Manufacturing No.")
        self.product_table.heading("quantity", text="QTY")
        self.product_table.heading("database", text="Database")

        # Configure the Treeview headings

        self.product_table.column("#0", width=15)
        self.product_table.column("mfgnum", width=25)
        self.product_table.column("quantity", width=20)
        self.product_table.column("database", width=30)

        self.product_table.pack(fill=BOTH, expand=1)

        self.product_table.bind("<<TreeviewSelect>>")

        self.display_high_stock_items()

    # ================================================= UPDATE Treeview FUNCTIOn=======================================
    def display_high_stock_items(self):
        # Clear the tree inventory
        self.product_table.delete(*self.product_table.get_children())

        # Create separate tables for each category if they don't exist
        categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                      "Connectors", "Voltage_n_Regulator", "LEDs",
                      "Diodes_n_Rectifiers", "Others"]

        for category in categories:
            # Fetch data from "flight.db" and add a new column with the database name
            self.cursor.execute(
                f"SELECT mfgnum, total_quantity FROM `{category}_summary` WHERE total_quantity >= 100")
            items_flight = self.cursor.fetchall()
            items_flight_with_db = [(item[0], item[1], "Flight") for item in items_flight]

            # Fetch data from "nonflight.db" and add a new column with the database name
            self.cursor_nonflight.execute(
                f"SELECT mfgnum, total_quantity FROM `{category}_summary` WHERE total_quantity >= 100")
            items_nonflight = self.cursor_nonflight.fetchall()
            items_nonflight_with_db = [(item[0], item[1], "Non-Flight") for item in items_nonflight]

            # Combine data from both databases and add to the Treeview
            combined_items = items_flight_with_db + items_nonflight_with_db
            for item in combined_items:
                mfgnum, total_quantity, source_db = item
                self.product_table.insert("", 0, text=category, values=(mfgnum, total_quantity, source_db))

    # ================================================= UPDATE Treeview FUNCTIOn=======================================

    def update_treeview(self):
        try:
            # Clear the tree inventory
            self.product_table.delete(*self.product_table.get_children())

            # Create separate tables for each category if they don't exist
            categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                          "Connectors", "Voltage_n_Regulator", "LEDs",
                          "Diodes_n_Rectifiers", "Others"]

            for category in categories:
                self.cursor.execute(
                    f"SELECT date, mfgnum, partnum, custPO, description, quantity FROM `{category}` ORDER BY id DESC")
                items = self.cursor.fetchall()

                # Add items to the tree inventory
                for item in items:
                    date, mfgnum, partnum, custPO, description, quantity = item
                    self.product_table.insert("", 0, text=category,
                                              values=(date, mfgnum, partnum, custPO, description, quantity))

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def close_high_stock(self):
        self.enable_button()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = highSTOCK_class(root, None)
    root.mainloop()
