


import os
import time
from tkinter import *

import mysql.connector
from PIL import Image
from PIL import ImageTk

from SNTracking import TrackingSN_class
from ProductsBox import ProductClass
from datetime import datetime
from Suppliers import supplier_class
from login import login_class
from Prohibited_flight import Prohibited_class
from tkinter import Toplevel, messagebox
from StockOut import stockOUT_class
from HighStock import highSTOCK_class
from LowStock import lowSTOCK_class
from CompareExcelFile import compare_class


class IMS:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x770+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.minsize(1500, 770)  # Set minimum dimensions
        self.root.maxsize(1500, 770)  # Set maximum dimensions

        # ======================================TITLE FRAME===================================================
        title_frame = Frame(self.root, bd=6, bg="#03B4E6", relief=GROOVE)
        title_frame.pack(side=TOP, fill=X)

        # Get the path to the script's directory
        # script_dir = sys.path[0]
        # Construct the path to the image file
        # self.image_path = os.path.join(script_dir, "sky2.jpg")
        #self.image_path = "sky2.jpg"

        #self.title_image = Image.open(self.image_path)
        #self.title_image = self.title_image.resize((200, 55))
        #self.icon_title = ImageTk.PhotoImage(self.title_image)///






        #self.title_image = Image.open("images/sky2.jpg")
        #self.resize_image = self.title_image.resize((200, 55), Image.LANCZOS)
        #self.converted_image = ImageTk.PhotoImage(self.resize_image)
        #Label(title_frame, image=self.converted_image).grid(row=0, column=0, padx=50, pady=6)
        Label(title_frame).grid(row=0, column=0, padx=50, pady=6)






        #Label(title_frame, image=self.icon_title).grid(row=0, column=0, padx=50, pady=6)
        # image = Label(title_frame).grid(row=0, column=0, padx=50, pady=6)

        Label(title_frame, text="Inventory Management System", font=("times new roman", 38, "bold"),
              bg="#03B4E6", justify=CENTER, fg="white").grid(row=0, column=2, padx=120, pady=6)

        Button(title_frame, text="Logout", font=("arial", 15, "bold"), bg="#0F148C", cursor="hand2", relief=RAISED,
               fg="white", bd=8, command=self.logout).place(x=1350, y=10, width=100, height=50)

        # ===========================WELCOME FRAME========================================================

        welcome_frame = Frame(self.root, bd=0, bg="white", height=45)
        welcome_frame.pack(side=TOP, padx=7, fill=X)

        self.frame_date = datetime.now().strftime("%d/%m/%Y")
        self.frame_time = datetime.now().strftime("%H:%M:%S")

        # clock
        self.lbl_clock = Label(welcome_frame,
                               text="Welcome to Inventory Management System\t Date:DD-MM-YYY\t Time:HH:MM:SS",
                               font=("arial", 15, "bold"), bg="green", fg="white", justify=CENTER, )
        self.lbl_clock.place(x=0, y=0, relwidth=1, height=45)
        self.lbl_clock.config(
            text=f"Welcome to Inventory Management System\t Date: {self.frame_date} \t Time: {self.frame_time} ")
        # ===========================Frame for menus========================================================

        frame_menu = Frame(self.root, bd=5, relief=GROOVE, bg="#03B4E6")
        frame_menu.place(x=5, y=135, width=250, height=630)

        self.dashboard_btn = Button(frame_menu, text="DASHBOARD", bd=8, relief=RAISED,
                                    font=("times new roman", 20, "bold"), bg="#0F148C", fg="white")
        self.dashboard_btn.place(x=3, y=5, width=235, height=50)
        self.Product_btn = Button(frame_menu, text="STOCK-IN", bd=8, relief=RAISED,
                                  font=("times new roman", 20, "bold"), bg="#0F148C", fg="white",
                                  command=self.products)
        self.Product_btn.place(x=3, y=63, width=235, height=50)

        self.Prohibited_btn = Button(frame_menu, text="NON-FLIGHT", bd=8, relief=RAISED,
                                     font=("times new roman", 20, "bold"), bg="#0F148C", fg="white",
                                     command=self.prohibitedFlight)
        self.Prohibited_btn.place(x=3, y=121, width=235, height=50)

        self.Suppliers_btn = Button(frame_menu, text="SUPPLIERS", bd=8, relief=RAISED,
                                    font=("times new roman", 20, "bold"), bg="#0F148C", fg="white",
                                    command=self.suppliers)
        self.Suppliers_btn.place(x=3, y=179, width=235, height=50)

        self.stock_out_btn = Button(frame_menu, text="STOCK-OUT", bd=8, relief=RAISED,
                                    font=("times new roman", 20, "bold"), bg="#0F148C", fg="white",
                                    command=self.stock_out)
        self.stock_out_btn.place(x=3, y=237, width=235, height=50)

        self.compare_btn = Button(frame_menu, text="COMPARE", bd=8, relief=RAISED,
                                  font=("times new roman", 20, "bold"), bg="#0F148C", fg="white", command=self.compare)
        self.compare_btn.place(x=3, y=295, width=235, height=50)

        self.sntracking_btn = Button(frame_menu, text="S.N. TRACKING", bd=8, relief=RAISED,
                              font=("times new roman", 20, "bold"), bg="#0F148C", fg="white", command=self.sntracking)
        self.sntracking_btn.place(x=3, y=353, width=235, height=50)

        self.exit_btn = Button(frame_menu, text="EXIT", bd=8, relief=RAISED,
                              font=("times new roman", 20, "bold"), bg="#0F148C", fg="white", command=self.root.destroy)
        self.exit_btn.place(x=3, y=411, width=235, height=50)

        ############################################CONTENT====================================

        frame_content = Frame(self.root, bd=20, relief=GROOVE, bg="#03B4E6")  # bg="#03B4E6"
        frame_content.place(x=255, y=135, width=1230, height=630)

        self.Total_category_btn = Button(frame_content, text="Total Category\n\n[ 9 ]",
                                         font=("arial", 20, "bold"), bg="white", justify=CENTER, bd=15,
                                         relief=GROOVE, fg="#03B4E6", padx=16)
        self.Total_category_btn.place(x=100, y=80, width=280, height=170)

        self.Total_supplier_btn = Button(frame_content, text="Total Supplier\n\n[ 0 ]",
                                         font=("arial", 20, "bold"), bg="white", justify=CENTER, bd=15,
                                         relief=GROOVE, fg="#03B4E6", padx=16)
        self.Total_supplier_btn.place(x=460, y=80, width=280, height=170)

        self.Total_product_btn = Button(frame_content, text="Product Stock\n\n[ 0 ]",
                                        font=("arial", 20, "bold"), bg="white", justify=CENTER, bd=15,
                                        relief=GROOVE, fg="#03B4E6", padx=16)
        self.Total_product_btn.place(x=820, y=80, width=280, height=170)

        self.high_stock_btn = Button(frame_content, text="Over Stock\n\n[ 0 ]",
                                     font=("arial", 20, "bold"), bg="white", justify=CENTER, bd=15,
                                     relief=GROOVE, fg="red", padx=16, command=self.high_stock)
        self.high_stock_btn.place(x=100, y=320, width=280, height=170)

        self.low_stock_btn = Button(frame_content, text="Under Stock\n\n[ 0 ]",
                                    font=("arial", 20, "bold"), bg="white", justify=CENTER, bd=15,
                                    relief=GROOVE, fg="red", padx=16, command=self.low_stock)
        self.low_stock_btn.place(x=460, y=320, width=280, height=170)

        self.zzz_btn = Button(frame_content, text="ZZZ\n\n[ 0 ]",
                              font=("arial", 20, "bold"), bg="white", justify=CENTER, bd=15,
                              relief=GROOVE, fg="#03B4E6", padx=16)
        self.zzz_btn.place(x=820, y=320, width=280, height=170)

        self.menu_buttons = [self.dashboard_btn, self.Product_btn, self.Prohibited_btn, self.Suppliers_btn,
                             self.stock_out_btn, self.compare_btn, self.sntracking_btn, self.high_stock_btn,
                             self.low_stock_btn]

        self.update_content()

    # ===========================Frame for menus============================================

    def highlight_dashboard(self):
        self.dashboard_btn.config(state="disabled")

    def products(self):
        self.products_highlight_button(self.Product_btn)

    def prohibitedFlight(self):
        self.prohibited_highlight_button(self.Prohibited_btn)

    def suppliers(self):
        self.supplier_highlight_btn(self.Suppliers_btn)

    def stock_out(self):
        self.stockOut_highlight_btn(self.stock_out_btn)

    def high_stock(self):
        self.highStock_highlight_btn(self.high_stock_btn)

    def low_stock(self):
        self.lowStock_highlight_btn(self.low_stock_btn)

    def compare(self):
        self.compare_highlight_btn(self.compare_btn)

    def sntracking(self):
        self.sntracking_highlight_btn(self.sntracking_btn)

    # =====================================================================================#

    def products_highlight_button(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        # self.new_win.attributes('-topmost', True)  # Make the new window stay on top
        self.new_obj = ProductClass(self.new_win, self.enable_all_button)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)
        #self.root.withdraw()
        #self.new_.deiconify()

    # =====================================================================================#
    def prohibited_highlight_button(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        # self.new_win.attributes('-topmost', True)  # Make the new window stay on top
        self.new_obj = Prohibited_class(self.new_win, self.enable_all_button)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)

    # =====================================================================================#

    def supplier_highlight_btn(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        # self.new_win.attributes("-topmost", True)  # Keep supplier window on top
        self.new_obj = supplier_class(self.new_win, self.enable_all_button)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)

    # ==============================STOCK OUT==================================================#

    def stockOut_highlight_btn(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        #self.new_win.attributes("-topmost", False)  # Keep supplier window on top
        self.new_obj = stockOUT_class(self.new_win, self.enable_all_button)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)


    # ================================HIGH STOCK===========================================#

    def highStock_highlight_btn(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        # self.new_win.attributes("-topmost", True)  # Keep supplier window on top
        self.new_obj = highSTOCK_class(self.new_win, self.enable_all_button)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)

    # ================================LOW STOCK===========================================#

    def lowStock_highlight_btn(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        # self.new_win.attributes("-topmost", True)  # Keep supplier window on top
        self.new_obj = lowSTOCK_class(self.new_win, self.enable_all_button)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)

    # ================================LOW STOCK===========================================#

    def compare_highlight_btn(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        # self.new_win.attributes("-topmost", True)  # Keep supplier window on top
        self.new_obj = compare_class(self.new_win, self.enable_all_button)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)

        # ==============================STOCK OUT==================================================#

    def sntracking_highlight_btn(self, button):

        # Disable all buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="disabled")

        # Highlight the clicked button
        button.config(bg="#03B4E6")

        self.new_win = Toplevel(self.root)
        self.new_win.grab_set()  # Disable the main window
        # self.new_win.attributes("-topmost", True)  # Keep supplier window on top
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_close)
        self.new_obj = TrackingSN_class(self.new_win, self.enable_all_button)

    # =====================================================================================#



    def enable_all_button(self):
        # Enable all the buttons in the frame
        for btn in self.menu_buttons:
            btn.config(state="normal")
            btn.config(bg="#0F148C")

    # =====================================================================================#

    def on_close(self):
        self.enable_all_button()

    # =====================================================================================#

    def login(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = login_class(self.new_win)

    # =====================================================================================#

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    # =====================================================================================#
    # =====================================================================================#

    def update_content(self):
        # Create separate tables for each category if they don't exist
        categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                      "Connectors", "Voltage_n_Regulator", "LEDs",
                      "Diodes_n_Rectifiers", "Others"]

        self.con = mysql.connector.connect(host="localhost",user="root",password="1223334444@SK",database="flight")
        self.cur = self.con.cursor()

        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK", database="nonflight")
        self.cur = self.con.cursor()

        try:
            '''cur.execute("Select * from supplier")
            supplier = cur.fetchall()
            self.Total_supplier_lbl.config(text=f'Total Suppliers\n\n [ {str(len(supplier))} ]')'''

            combined_high_items = []  # Initialize an empty list

            for category in categories:
                # Fetch data from "flight.db" and add a new column with the database name
                self.cur.execute(
                    f"SELECT mfgnum, total_quantity FROM `{category}_summary` WHERE total_quantity >= 100")
                items_high_flight = self.cur.fetchall()
                items_high_flight_with_db = [(item[0], item[1], "Flight") for item in items_high_flight]

                # Fetch data from "nonflight.db" and add a new column with the database name
                self.cur_nonflight.execute(
                    f"SELECT mfgnum, total_quantity FROM `{category}_summary` WHERE total_quantity >= 100")
                items_high_nonflight = self.cur_nonflight.fetchall()
                items_high_nonflight_with_db = [(item[0], item[1], "Non-Flight") for item in items_high_nonflight]

                # Combine data from both databases and add to the Treeview
                combined_high_items.extend(items_high_flight_with_db + items_high_nonflight_with_db)

            # Now, calculate the total count of unique high stock items
            total_high_stock_items = len(set(combined_high_items))
            self.high_stock_btn.config(text=f'High STOCK\n\n [ {str(total_high_stock_items)} ]')

            combined_low_items = []  # Initialize an empty list

            for category in categories:
                # Fetch data from "flight.db" and add a new column with the database name
                self.cur.execute(
                    f"SELECT mfgnum, total_quantity FROM `{category}_summary` WHERE total_quantity <= 10")
                items_low_flight = self.cur.fetchall()
                items_low_flight_with_db = [(item[0], item[1], "Flight") for item in items_low_flight]

                # Fetch data from "nonflight.db" and add a new column with the database name
                self.cur_nonflight.execute(
                    f"SELECT mfgnum, total_quantity FROM `{category}_summary` WHERE total_quantity <= 10")
                items_low_nonflight = self.cur_nonflight.fetchall()
                items_low_nonflight_with_db = [(item[0], item[1], "Non-Flight") for item in items_low_nonflight]

                # Combine data from both databases and add to the Treeview
                combined_low_items.extend(items_low_flight_with_db + items_low_nonflight_with_db)

            # Now, calculate the total count of unique low stock items
            total_low_stock_items = len(set(combined_low_items))
            self.low_stock_btn.config(text=f'Low STOCK\n\n [ {str(total_low_stock_items)} ]')

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)




if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
