
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk

import mysql.connector

class supplier_class:
    def __init__(self, root, enable_button):
        self.root = root
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.title("SUPPLIERS")
        self.root.config(bg="white")
        self.enable_button = enable_button

        # ============================VARIABLE===================================================================
        # ============================VARIABLE=======================================
        self.var_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_description = StringVar()
        self.var_search_invoice = StringVar

        # ==================================TITLE FRAME ===============================================================
        # title frame
        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.title_frame.pack(side=TOP, fill=X)

        Label(self.title_frame, text="Suppliers Details", font=("times new roman", 30, "bold"),
              bg="#63B8FF", fg="white", bd=10, relief=GROOVE).pack(side=TOP, fill=X)



        self.closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), bg="#104E8B", cursor="hand2",
                          fg="white", relief= RAISED, command=self.close_supply)
        self.closebtn.place(x=1090, y=15, width=100, height=37)



        # ==================================Frame 1==================================================================

        details_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        details_frame.place(x=5, y=80, width=440, height=500)

        # =============================================Invoice Label and Entry===============================
        manage_title = Label(details_frame, text="Entries", font=("times new roman", 30, "bold"), bg="#63B8FF",
                             fg="red", justify=CENTER)
        manage_title.grid(row=0, columnspan=2, padx=(50, 45), pady=20)

        # =============================================Invoice Label and Entry=============================
        invoiceSup_label = Label(details_frame, text="Invoice No:", font=("times new roman", 15, "bold"),
                                 bg="#63B8FF", fg="black", anchor='w')
        invoiceSup_label.grid(row=1, column=0, padx=20, sticky="w")
        self.invoiceSup_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                      bd=5, relief=RIDGE, textvariable=self.var_invoice)
        self.invoiceSup_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        # ===========================================NAME========================================================
        # ===========================================NAME======================================================

        nameSup_label = Label(details_frame, text="Name", font=("times new roman", 15, "bold"),
                              bg="#63B8FF", fg="black", anchor='w')
        nameSup_label.grid(row=2, column=0, padx=20, sticky="w")
        self.nameSup_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                   bd=5, relief=RIDGE, textvariable=self.var_name)
        self.nameSup_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # ============================================CONTACT========================================================
        # ============================================CONTACT==================================================
        contactSup_label = Label(details_frame, text="Contact", font=("times new roman", 15, "bold"),
                                 bg="#63B8FF", fg="black", anchor='w')
        contactSup_label.grid(row=3, column=0, padx=20, sticky="w")
        self.contactSup_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                      bd=5, relief=RIDGE, textvariable=self.var_contact)
        self.contactSup_entry.grid(row=3, column=1, pady=10, padx=20, sticky="w")

        # ============================================Email=============================================
        emailSup_label = Label(details_frame, text="Email", font=("times new roman", 15, "bold"),
                               bg="#63B8FF", fg="black", anchor='w')
        emailSup_label.grid(row=4, column=0, padx=20, sticky="w")
        self.emailSup_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                    bd=5, relief=RIDGE, textvariable=self.var_email)
        self.emailSup_entry.grid(row=4, column=1, pady=10, padx=20, sticky="w")

        # ============================================DESCRIPTION================================================
        # ============================================DESCRIPTION=================================================
        descriptionSup_label = Label(details_frame, text="Description", font=("times new roman", 15, "bold"),
                                     bg="#63B8FF", fg="black", anchor='w')
        descriptionSup_label.grid(row=5, column=0, padx=20, sticky="w")
        self.descriptionSup_entry = Entry(details_frame, font=("times new roman", 15, "bold"),
                                          bd=5, relief=RIDGE, textvariable=self.var_description)
        self.descriptionSup_entry.grid(row=5, column=1, pady=10, padx=20, sticky="w")

        # ============================================BUTTONs=====================================================
        # ============================================BUTTONs======================================================
        button_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        button_frame.place(x=17, y=470, width=413, height=80)

        saveSup_button = Button(button_frame, text="Save", font=("times new roman", 15, "bold"), bd=2,
                                cursor="hand2", relief=RAISED, fg="black", justify=CENTER, width=6,
                                command=self.save)
        saveSup_button.grid(row=0, column=0, padx=10, pady=10)
        updateSup_button = Button(button_frame, text="Update", font=("times new roman", 15, "bold"),
                                  command=self.update,
                                  bd=2, cursor="hand2", relief=RAISED, fg="black", width=6, justify=CENTER)
        updateSup_button.grid(row=0, column=1, padx=10, pady=10)
        deleteSup_button = Button(button_frame, text="Delete", font=("times new roman", 15, "bold"),
                                  command=self.delete,
                                  bd=2, cursor="hand2", relief=RAISED, fg="black", width=6, justify=CENTER)
        deleteSup_button.grid(row=0, column=2, padx=10, pady=10)
        clearSup_button = Button(button_frame, text="Clear", font=("times new roman", 15, "bold"), command=self.clear,
                                 bd=2, cursor="hand2", relief=RAISED, fg="black", width=6, justify=CENTER)
        clearSup_button.grid(row=0, column=3, padx=10, pady=10)

        # =================================ENTRY and LABELS==========================================================

        self.search_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.search_frame.place(x=460, y=80, width=760, height=500)

        search_label = Label(self.search_frame, text="Search by Invoice no:", font=("times new roman", 15, "bold"),
                             bg="#63B8FF", fg="black", anchor='w')
        search_label.grid(row=0, column=0, padx=(20, 5), pady=15)

        self.search_entry = Entry(self.search_frame, font=("times new roman", 15, "bold"),
                                  bd=2, relief=RIDGE, textvariable=self.var_search_invoice)
        self.search_entry.grid(row=0, column=1, padx=17, pady=15)

        search_button = Button(self.search_frame, text="Search", font=("times new roman", 15, "bold"),
                               command=self.search, fg="black", justify=CENTER)
        search_button.grid(row=0, column=2, padx=15, pady=15)

        showall_button = Button(self.search_frame, text="Show All", font=("times new roman", 15, "bold"),
                               fg="black", justify=CENTER, command=self.show_all)
        showall_button.grid(row=0, column=3, padx=90, pady=15)

        # ============================Search FRAME  TreeView===============================================
        tree_frame = Frame(self.root, bd=4, relief=RIDGE)
        tree_frame.place(x=475, y=155, width=730, height=415)

        scrollx = Scrollbar(tree_frame, orient=HORIZONTAL)
        scrolly = Scrollbar(tree_frame, orient=VERTICAL)

        self.suppliertable = ttk.Treeview(tree_frame, columns=("invoice", "name", "contact", "email", "description"),
                                          xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.suppliertable.xview)
        scrolly.config(command=self.suppliertable.yview)

        self.suppliertable.heading("invoice", text="INVOICE")
        self.suppliertable.heading("name", text="NAME")
        self.suppliertable.heading("contact", text="CONTACT")
        self.suppliertable.heading("email", text="Email")
        self.suppliertable.heading("description", text="DESCRIPTION")

        self.suppliertable["show"] = "headings"

        self.suppliertable.column("invoice", width=50)
        self.suppliertable.column("name", width=50)
        self.suppliertable.column("contact", width=100)
        self.suppliertable.column("email", width=70)
        self.suppliertable.column("description", width=200)

        self.suppliertable.pack(fill=BOTH, expand=1)

        self.show()

        self.suppliertable.bind("<ButtonRelease-1>", self.get_data)

    # =====================================# Update the database connection========================================

        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1223334444@SK",
            database="suppliers"
        )

        self.cur = self.con.cursor()


    # ===========================================SAVE METHODS=============================================

    def save(self):
       try:
            if self.var_invoice.get() == "":
                messagebox.showerror("Error", f"Invoice Number must be required", parent=self.root)
            else:
                self.cur.execute(f"INSERT INTO supplier (invoice,name,contact, email, description) VALUES (%s, %s, %s, %s, %s)",
                            (
                                self.var_invoice.get(),
                                self.var_name.get(),
                                self.var_contact.get(),
                                self.var_email.get(),
                                self.var_description.get(),
                            )
                                 )
                self.con.commit()
                messagebox.showinfo("Success", f"SUPPLIER SAVED SUCCESSFULLY", parent=self.root)
                self.clear()
                self.show()
       except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # ====================================SHOW FUNCTION =====================================================
    def show(self):
        try:
            self.cur.execute(f"SELECT * FROM supplier")
            rows = self.cur.fetchall()
            # Clear the treeview
            for item in self.suppliertable.get_children():
                self.suppliertable.delete(item)

            # Insert data into the treeview
            for row in rows:
                self.suppliertable.insert('', 'end', values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # =======================================GET DATA===========================================================

    def get_data(self, ev):
        f = self.suppliertable.focus()
        values = self.suppliertable.item(f, 'values')

        # Populate the entry boxes with selected data
        # row = content['values']
        # print(row)
        self.invoiceSup_entry.delete(0, tk.END)
        self.nameSup_entry.delete(0, tk.END)
        self.contactSup_entry.delete(0, tk.END)
        self.emailSup_entry.delete(0, tk.END)
        self.descriptionSup_entry.delete(0, tk.END)

        self.invoiceSup_entry.insert(0, values[0])
        self.nameSup_entry.insert(0, values[1])
        self.contactSup_entry.insert(0, values[2])
        self.emailSup_entry.insert(0, values[3])
        self.descriptionSup_entry.insert(0, values[4])

    # ============================================UPDATE FUNCTION=============================================

    def update(self):
        selected_items = self.suppliertable.focus()
        values = self.suppliertable.item(selected_items, 'values')

        try:
            if not values:
                return

            self.cur.execute("UPDATE supplier SET invoice=%s, name=%s,contact=%s,email=%s,description=%s WHERE "
                        "invoice=%s AND name=%s AND contact=%s AND email=%s AND description=%s",
                        (
                            self.var_invoice.get(),
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.var_email.get(),
                            self.var_description.get(), values[0], values[1], values[2], values[3], values[4]

                        ))
            self.con.commit()
            messagebox.showinfo("Success", "Suppliers Info Updated Successfully", parent=self.root)
            self.show()
            self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    # ============================================DELETE FUNCTION====================================================
    def delete(self):
        selected_items = self.suppliertable.focus()
        values = self.suppliertable.item(selected_items, 'values')

        try:
            if not values:
                return

            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op == True:
                self.cur.execute(
                    "DELETE FROM supplier WHERE invoice=%s AND name=%s AND contact=%s AND email=%s AND description=%s",
                    (values[0], values[1], values[2], values[3], values[4]))
                self.con.commit()
                messagebox.showinfo("Success", "Deleted Successfully", parent=self.root)
            self.show()
            self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    # ============================================SEARCH FUNCTION==================================================
    def search(self):
        search_invoice_detail = self.var_search_invoice.get()

        for item in self.suppliertable.get_children():
            self.suppliertable.delete(item)

        try:
            if self.var_search_invoice == "":
                messagebox.showerror("Error", "Invoice Number must required", parent=self.root)
            else:
                self.cur.execute("SELECT * FROM supplier WHERE invoice=%s", (search_invoice_detail,))
                rows = self.cur.fetchall()
                # Insert data into the treeview
                for row in rows:
                    self.suppliertable.insert('', 'end', values=row)

                # messagebox.showerror("Error", "No item found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # ============================================SHOW ALL FUNCTION==================================================
    def show_all(self):
        try:
            self.cur.execute(f"SELECT * FROM supplier")
            rows = self.cur.fetchall()

            # self.suppliertable.delete(*self.suppliertable.get_children())

            # Clear the treeview
            for item in self.suppliertable.get_children():
                self.suppliertable.delete(item)

            # Insert data into the treeview
            for row in rows:
                self.suppliertable.insert('', 'end', values=row)
            self.con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    # ============================================CLEAR FUNCTION==================================================
    def clear(self):
        self.var_invoice.set('')
        self.var_name.set('')
        self.var_contact.set('')
        self.var_email.set('')
        self.var_description.set('')
        self.var_search_invoice.set('')

    def close_supply(self):

        self.con.close()  # Close the MySQL connection
        self.enable_button()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = supplier_class(root,None)
    root.mainloop()
