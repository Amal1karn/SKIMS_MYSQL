
import sqlite3
from datetime import date
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk

from GenerateReport import Generate_report_class


class TrackingSN_class:
    def __init__(self, root, enable_trackSN):
        self.root = root
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.title("CONFIGURATION MANAGEMENT")
        self.root.config(bg="white")
        self.enable_trackSN = enable_trackSN
        self.root.focus_force()
        # ==================================TITLE FRAME ===============================================================
        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.title_frame.pack(side=TOP, fill=X)

        Label(self.title_frame, text="SERIAL TRACKING", font=("times new roman", 30, "bold"),
              bg="#03B4E6", fg="white", bd=10, relief=GROOVE).pack(side=TOP, fill=X)

        self.closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), bg="#0F148C",
                               cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.close_configmgm)
        self.closebtn.place(x=1090, y=15, width=100, height=37)
        # =============================================================================================================

        self.tree_title_frame = tk.Frame(self.root, bd=0, relief=tk.RIDGE, bg="#63B8FF")
        self.tree_title_frame.place(x=3, y=80, width=1220, height=50)

        # Create the label inside the title frame
        self.title = tk.Label(self.tree_title_frame, text="Integration Stages", bd=5, relief=tk.GROOVE,
                              font=("times new roman", 21, "bold"), bg="#63B8FF", fg="white")
        self.title.pack(side=tk.TOP, fill=tk.BOTH)
        # =-====================================================================================================

        # Create frames for GUI components
        self.manage_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="#63B8FF")
        self.manage_frame.place(x=3, y=130, width=1220, height=450)

        # Create an "Update Item" button
        subsystem_test_btn = Button(self.manage_frame, text=" SUBSYSTEM\nTEST\nSTATUS",
                                    font=("arial", 16, "bold"), relief=RAISED, bd=8,
                                    bg="#0F148C", cursor="hand2", fg="white", width=15,
                                    height=8, command=self.subsystem_test)
        subsystem_test_btn.grid(row=0, column=0, padx=100, pady=90)

        # Create an "SAVE Item" button
        stage1_integration_btn = Button(self.manage_frame, text=" SATELLITE\nINTEGRATION\nSTATUS",
                                        font=("arial", 16, "bold"), relief=RAISED, bd=8,
                                        bg="#0F148C", cursor="hand2", fg="white", width=15,
                                        height=8, command=self.stage1_integration)
        stage1_integration_btn.grid(row=0, column=1, padx=100, pady=90)

        # Create an "SAVE Item" button
        report_generation_btn = Button(self.manage_frame, text=" GENERATE\nREPORT",
                                       font=("arial", 16, "bold"), relief=RAISED, bd=8,
                                       bg="#0F148C", cursor="hand2", fg="white", width=15,
                                       height=8, command=self.report_generate)
        report_generation_btn.grid(row=0, column=2, padx=100, pady=90)

        # ==========================================================================================================
        # ==========================================================================================================
        # ==============STAGE 1 INTEGRATION=========================================================================
        # ==========================================================================================================
        # ==========================================================================================================

    def stage1_integration(self):

        self.si = Toplevel(self.root)
        self.si.title('Satellite Integration Status')
        self.si.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.si.focus_force()
        self.si.lift()
        self.root.withdraw()

        # =============

        self.s_title_frame = tk.Frame(self.si, bd=4, relief=RIDGE, bg="#03B4E6")
        self.s_title_frame.pack(side=TOP, fill=X)

        # Create the label inside the title frame
        self.s_title = Label(self.s_title_frame, text="Satellite Integration Status",
                             font=("times new roman", 30, "bold"),
                             bg="#03B4E6", fg="white", bd=10, relief=GROOVE)
        self.s_title.pack(side=TOP, fill=X)

        # Create "Close" button
        s3_exit_btn = Button(self.s_title_frame, text="Close", font=("arial", 15, "bold"), bg="#0F148C",
                             cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.s_close_window)
        s3_exit_btn.place(x=1090, y=15, width=100, height=37)
        # ==================================Frame 1=====================================================

        self.s_integration_details = Frame(self.si, bd=10, relief=RIDGE, bg="#03B4E6")
        self.s_integration_details.place(x=5, y=80, width=1220, height=315)

        # =================Create labels Vertically===================

        # Create the label inside the title frame
        self.s_stage1satellite_lbl = Label(self.s_integration_details, text="Satellite", bd=5, relief=GROOVE,
                                           font=("times new roman", 13, "bold"), width=10, bg="#63B8FF", fg="black")
        self.s_stage1satellite_lbl.grid(row=0, column=0, padx=10, pady=(8, 2), sticky="w")

        self.fm_satellite = ["SK4-FM-01", "SK4-FM-02", "SK4-FM03", "SK4-FM04", "SK4-FM05", "SK4-FM06", "SK4-FM07",
                             "SK4-FM08", "FM-Ground Station"]

        self.edm_satellite = ["SK4-EDM01", "SK4-EDM02", "SK4-EDM03", "SK4-EDM04", "SK4-EDM05", "SK4-EDM06", "SK4-EDM07",
                              "SK4-EDM08", "EDM-Ground Station"]

        self.s_stage1satellitecombo = ttk.Combobox(self.s_integration_details, values=self.fm_satellite,
                                                   font=("times new roman", 12, "bold"),
                                                   state="readonly", width=18, justify=tk.CENTER, background="#FFE7BA")
        self.s_stage1satellitecombo.grid(row=0, column=1, padx=10, sticky="e", pady=(8, 2))

        # Create the label inside the title frame
        self.s_stage1system_lbl = Label(self.s_integration_details, text="System", bd=5, relief=GROOVE,
                                        font=("times new roman", 13, "bold"), width=10, bg="#63B8FF", fg="black")
        self.s_stage1system_lbl.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        # ============= Entry widget for the TESTED BY ============

        self.s3_entry_setup()

    def s3_entry_setup(self):
        conn = sqlite3.connect("SerialTracking.db")  # Replace with your database file
        cursor = conn.cursor()

        Finals = ["FM_SatelliteIntegration", "EDM_SatelliteIntegration"]

        s3_unique_items = []

        for final_table in Finals:
            cursor.execute(f"SELECT System FROM {final_table}")
            s3_column_data = cursor.fetchall()
            s3_unique_items.extend([item[0] for item in s3_column_data])

        s3entry_var = tk.StringVar()
        self.s_subcomponent_txt = tk.Entry(self.s_integration_details,
                                           font=("times new roman", 12, "bold"), bd=5, relief=tk.GROOVE,
                                           textvariable=s3entry_var, bg="#FFE7BA", width=20, justify=tk.CENTER)
        self.s_subcomponent_txt.grid(row=1, column=1, padx=10, sticky="e", pady=5)

        def s3on_entry_change(*args):
            s3_search_text = s3entry_var.get().upper()

            s3_filtered_items = [item for item in s3_unique_items if item and s3_search_text in item.upper()]

            self.s3_listbox.delete(0, tk.END)
            for item in s3_filtered_items:
                self.s3_listbox.insert(tk.END, item)

            if s3_filtered_items:
                self.s3_listbox.lift()
                self.s3_listbox.place(x=self.s_subcomponent_txt.winfo_x(),
                                 y=self.s_subcomponent_txt.winfo_y() + self.s_subcomponent_txt.winfo_height() + 5)
            else:
                self.s3_listbox.place_forget()

        s3entry_var.trace_add("write", s3on_entry_change)

        self.s3_listbox = tk.Listbox(self.s_integration_details, font=("times new roman", 12, "bold"),
                                bd=5, relief=tk.GROOVE, takefocus=True)

        self.s3_listbox_scrollbar = tk.Scrollbar(self.s_integration_details, orient="vertical", command=self.s3_listbox.yview)
        self.s3_listbox.config(yscrollcommand=self.s3_listbox_scrollbar.set)

        self.s3_listbox_scrollbar.place(x=self.s3_listbox.winfo_x() + self.s3_listbox.winfo_width() - 2, y=self.s3_listbox.winfo_y(),
                                   height=self.s3_listbox.winfo_height())

        self.s3_listbox.place_forget()

        def s3on_listbox_select(event):
            s3_selection = self.s3_listbox.curselection()
            if s3_selection:
                s3_selected_item = self.s3_listbox.get(s3_selection)
                s3entry_var.set(s3_selected_item)
                self.s3_listbox.place_forget()

        self.s3_listbox.bind("<<ListboxSelect>>", s3on_listbox_select)

        # =================Create labels Vertically===================

        Label(self.s_integration_details, text="Serial No:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=2, column=0, padx=10, pady=2, sticky="w")
        self.s1_txt_serial = Entry(self.s_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                   relief=GROOVE, justify=CENTER)
        self.s1_txt_serial.grid(row=2, column=1, padx=10, sticky="e", pady=5)
        # =====================================================================
        Label(self.s_integration_details, text="Tested Date:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=3, column=0, padx=10, pady=2, sticky="w")
        self.s1_txt_testedDate = Entry(self.s_integration_details, font=("times new roman", 12, "bold"),
                                       bd=5, relief=GROOVE, justify=CENTER)
        self.s1_txt_testedDate.grid(row=3, column=1, padx=10, sticky="e", pady=5)
        # ========================================================================================
        Label(self.s_integration_details, text="Part No:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w', justify=CENTER).grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.s1_txt_partnum = Entry(self.s_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                    relief=GROOVE, justify=CENTER)
        self.s1_txt_partnum.grid(row=4, column=1, padx=10, sticky="e", pady=5)
        # ======================================================================
        Label(self.s_integration_details, text="Revision:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=5, column=0, padx=10, pady=2, sticky="w")
        self.s1_txt_revision = Entry(self.s_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                     relief=GROOVE, justify=CENTER)
        self.s1_txt_revision.grid(row=5, column=1, padx=10, sticky="e", pady=5)
        # =================================================================
        Label(self.s_integration_details, text="Tested By:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=6, column=0, padx=10, pady=2, sticky="w")
        self.s1_txt_testedBy = Entry(self.s_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                     relief=GROOVE, justify=CENTER)
        self.s1_txt_testedBy.grid(row=6, column=1, padx=10, sticky="e", pady=5)
        # ================================================================
        Label(self.s_integration_details, text="Test Report Link:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=1, column=2, padx=(25, 10), pady=2, sticky="w")
        self.s1_txt_reportLink = Entry(self.s_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                       relief=GROOVE)
        self.s1_txt_reportLink.grid(row=1, column=3, padx=10, sticky="e", pady=5)
        # ================================================================
        Label(self.s_integration_details, text="Comment:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=2, column=2, padx=(25, 10), pady=2, sticky="w")
        self.s1_txt_comment = Entry(self.s_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                    relief=GROOVE)
        self.s1_txt_comment.grid(row=2, column=3, padx=10, sticky="e", pady=5)
        # ====================================================================================================
        # =======================OptionMENU BUTTON=================================================================
        # ====================================================================================================
        s_optionmenu_frame = Frame(self.s_integration_details, bd=0, relief=RIDGE, bg="#03B4E6")
        s_optionmenu_frame.place(x=400, y=125, width=240, height=50)

        status = ["Work In Progress", "Complete"]

        self.status_var = tk.StringVar()
        self.status_var.set("Status")  # Set the default status

        self.status_menu = OptionMenu(s_optionmenu_frame, self.status_var, *status)
        self.status_menu.grid(row=0, column=0, pady=0, padx=0)
        self.status_menu.config(font=("arial", 17, "bold"), width= 15, bg="#03B4E6", fg="black", relief=GROOVE,bd=5,
                               anchor='center')

        self.status_var.trace_add('write', self.on_dropdown_select)  # Bind the event


        # ====================================================================================================
        # =======================RADIO BUTTON=================================================================
        # ====================================================================================================

        s_radio_frame = Frame(self.s_integration_details, bd=0, relief=RIDGE, bg="#03B4E6")
        s_radio_frame.place(x=390, y=185, width=260, height=60)

        # Create radio buttons
        self.radio_var = tk.StringVar()
        self.radio_var.set("FM")  # Default selection

        self.s_fm_table = tk.Radiobutton(s_radio_frame, text="FM", font=("arial", 17, "bold"), variable=self.radio_var,
                                         value="FM", bg="#03B4E6", relief=GROOVE, bd=4,command=self.s_update_satellite_combo)
        self.s_fm_table.grid(row=1, column=0, pady=2, padx=30)

        self.s_edm_table = tk.Radiobutton(s_radio_frame, text="EDM", font=("arial", 17, "bold"),relief=GROOVE, bd=4,
                                          variable=self.radio_var, value="EDM", bg="#03B4E6",
                                          command=self.s_update_satellite_combo)
        self.s_edm_table.grid(row=1, column=1, pady=2, padx=30)
        # ====================================================================================================
        # ====================================================================================================
        # ======================================================================================================

        s_btn_frame = Frame(self.s_integration_details, bd=0, relief=RIDGE, bg="#03B4E6")
        s_btn_frame.place(x=350, y=240, width=330, height=50)
        # =================================================================================================
        s3_save_btn = Button(s_btn_frame, text="SAVE", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                             bg="#0F148C", cursor="hand2", fg="white", width=8, command=self.add_si)
        s3_save_btn.grid(row=0, column=0, padx=8, pady=0)

        # Create an "Update Item" button
        s3_udpate_btn = Button(s_btn_frame, text="UPDATE", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                               bg="#0F148C", cursor="hand2", fg="white", width=8, command=self.update_si)
        s3_udpate_btn.grid(row=0, column=1, padx=8, pady=0)

        # Create an "Update Item" button
        s3_clear_btn = Button(s_btn_frame, text="CLEAR", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                              bg="#0F148C", cursor="hand2", fg="white", width=8, command=self.s_clear_entry_fields)
        s3_clear_btn.grid(row=0, column=2, padx=8, pady=0)

        # ===========================================================================================

        s_btn_frame = Frame(self.s_integration_details, bd=3, relief=RIDGE, bg="#03B4E6")
        s_btn_frame.place(x=730, y=20, width=440, height=250)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.s_table_frame = Frame(self.si, bd=10, relief=RIDGE, bg="#03B4E6")
        self.s_table_frame.place(x=5, y=395, width=1220, height=200)

        # ==========================TREEVIEW====================================
        s_scroll_x = Scrollbar(self.s_table_frame, orient=HORIZONTAL)
        s_scroll_y = Scrollbar(self.s_table_frame, orient=VERTICAL)
        self.stage1_table = ttk.Treeview(self.s_table_frame, xscrollcommand=s_scroll_x.set,
                                         yscrollcommand=s_scroll_y.set)
        s_scroll_x.pack(side=BOTTOM, fill=X)
        s_scroll_y.pack(side=RIGHT, fill=Y)
        s_scroll_x.config(command=self.stage1_table.xview)
        s_scroll_y.config(command=self.stage1_table.yview)

        self.stage1_table["columns"] = (
            "Id", "Tested_Date", "Satellite_SN", "System", "Subsystem_SN", "Part_number", "Revision", "Tested_By",
            "Status", "Test_Report_Link", "Comments", "Timestamp")

        # Configure the Treeview columns
        self.stage1_table.heading("#0", text="Table")
        self.stage1_table.heading("Id", text="Id")
        self.stage1_table.heading("Satellite_SN", text="SATELLITE")
        self.stage1_table.heading("Tested_Date", text="TESTED DATE")
        self.stage1_table.heading("System", text="SYSTEM")
        self.stage1_table.heading("Subsystem_SN", text="SERIAL NO.")
        self.stage1_table.heading("Part_number", text="PART NO.")
        self.stage1_table.heading("Revision", text="REVISION")
        self.stage1_table.heading("Tested_By", text="TESTED BY")
        self.stage1_table.heading("Status", text="Status")
        self.stage1_table.heading("Test_Report_Link", text="REPORT LINK")
        self.stage1_table.heading("Comments", text="COMMENT")
        self.stage1_table.heading("Timestamp", text="TIMESTAMP")

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), foreground='#0F148C', background='black')

        # Configure the Treeview headings

        # Configure the Treeview headings
        # self.stage1_table['show'] = 'headings'
        self.stage1_table.column("#0", width=0, stretch=tk.NO)
        self.stage1_table.column("Id", width=0, stretch=tk.NO)
        self.stage1_table.column("Tested_Date", width=100)
        self.stage1_table.column("Satellite_SN", width=70)
        self.stage1_table.column("System", width=70)
        self.stage1_table.column("Subsystem_SN", width=70)
        self.stage1_table.column("Part_number", width=70)
        self.stage1_table.column("Revision", width=70)
        self.stage1_table.column("Tested_By", width=120)
        self.stage1_table.column("Status", width=90)
        self.stage1_table.column("Test_Report_Link", width=200)
        self.stage1_table.column("Comments", width=200)
        self.stage1_table.column("Timestamp", width=0, stretch=tk.NO)

        self.stage1_table.pack(fill=BOTH, expand=1)

        self.stage1_table.bind("<<TreeviewSelect>>", self.s_fetch_data)

        self.s_set_current_date()
        self.s_update_treeview()

    def s_close_window(self):
        self.si.destroy()  # Close the integration frame
        self.root.deiconify()

    # ===========================================================================================
    def on_dropdown_select(self, *args):
        self.status_update()

    def status_update(self):
        selected_status = self.status_var.get()

        if selected_status == "Status":
            self.status_menu.config(font=("arial", 17, "bold"), bg="#03B4E6", fg="black")
        elif selected_status == "Work In Progress":
            self.status_menu.config(font=("arial", 17, "bold"), bg="yellow", fg="black")
        else:
            self.status_menu.config(font=("arial", 17, "bold"), bg="green", fg="black")

    def deselect_status(self):
        self.status_var.set("Status")
        self.status_menu.config(text="Status", font=("arial", 17, "bold"), width=15, bg="#03B4E6", fg="black", relief=GROOVE, bd=5,
                                anchor='center')
        #self.status_menu.config(text="Status", font=("arial", 17, "bold"), bg="#03B4E6", fg="black")

    # ===========================================================================================

    def s_update_satellite_combo(self):
        selection = self.radio_var.get()
        if selection == "FM":
            self.s_stage1satellitecombo['values'] = self.fm_satellite
            self.s_stage1satellitecombo.set(self.fm_satellite[0])
        elif selection == "EDM":
            self.s_stage1satellitecombo['values'] = self.edm_satellite
            self.s_stage1satellitecombo.set(self.edm_satellite[0])

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def s_set_current_date(self):
        try:
            current_date = date.today().strftime("%Y/%m/%d")
            self.s1_txt_testedDate.delete(0, tk.END)  # Clear any existing text
            self.s1_txt_testedDate.insert(0, current_date)  # Insert the current date into the widget
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to date: {str(ex)}", parent=self.root)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def s_clear_entry_fields(self):
        # Clear input fields
        self.s_set_current_date()
        self.s_stage1satellitecombo.set("")
        self.s1_txt_serial.delete(0, tk.END)
        self.s1_txt_testedBy.delete(0, tk.END)
        self.s1_txt_partnum.delete(0, tk.END)
        self.s1_txt_revision.delete(0, tk.END)
        self.s1_txt_reportLink.delete(0, tk.END)
        self.s_subcomponent_txt.delete(0, tk.END)
        self.s1_txt_comment.delete(0, tk.END)
        self.s_update_treeview()
        self.deselect_status()
        self.s3_listbox.place_forget()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def add_si(self):
        try:
            # Extract input values
            input_fields = {
                'testdate_var': self.s1_txt_testedDate.get(),
                'satellite_var': self.s_stage1satellitecombo.get(),
                'sn_var': self.s1_txt_serial.get().upper(),
                'testby_var': self.s1_txt_testedBy.get(),
                'partnum_var': self.s1_txt_partnum.get(),
                'revision_var': self.s1_txt_revision.get(),
                'status_var' : self.status_var.get(),
                'reportlink_var': self.s1_txt_reportLink.get(),
                'entrystage1_var': self.s_subcomponent_txt.get().upper(),
                'comments_var': self.s1_txt_comment.get()
            }

            required_fields = ['satellite_var', 'entrystage1_var', 'sn_var']

            if not input_fields['satellite_var']:
                messagebox.showerror("Error", "Select the Satellite", parent=self.si)
                return

            if not input_fields['sn_var']:
                messagebox.showerror("Error", "Enter the Serial number", parent=self.si)
                return
            if input_fields['entrystage1_var'] == "":
                messagebox.showerror("Error", "Enter the system abbrebiation", parent=self.si)
                return

            if input_fields['status_var'] == "Status":
                messagebox.showerror("Error", "Select Status", parent=self.si)
                return

            # Map radio button values to table names
            table_names = {'FM': 'FM_SatelliteIntegration', 'EDM': 'EDM_SatelliteIntegration'}
            selected_radio = self.radio_var.get()
            if selected_radio not in table_names:
                messagebox.showerror("Error", "Select either FM or EDM", parent=self.si)
                return

            # Connect to the database and start a transaction
            with sqlite3.connect("SerialTracking.db") as connection:
                cursor = connection.cursor()

                table_name = table_names[selected_radio]

                # Check for existing entry
                cursor.execute(
                    f"SELECT Id FROM {table_name} WHERE Satellite_SN = ? AND System = ? AND Subsystem_SN = ?",
                    (input_fields['satellite_var'], input_fields['entrystage1_var'], input_fields['sn_var']))
                existing_entry = cursor.fetchone()

                # Define the query template for inserting or updating
                query_template = f"""
                    INSERT INTO {table_name} (Tested_Date, Satellite_SN, System, Subsystem_SN, Part_number, Revision, 
                    Tested_By, Status, Test_Report_Link, Comments)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                if existing_entry:
                    query_template = f"""
                        UPDATE {table_name}
                        SET Tested_Date = ?, Part_number = ?, Tested_By = ?, Status = ?, Test_Report_Link = ?, Comments = ?
                        WHERE Id = ?
                    """

                # Execute the query
                query_params = (
                    input_fields['testdate_var'], input_fields['satellite_var'], input_fields['entrystage1_var'],
                    input_fields['sn_var'], input_fields['partnum_var'], input_fields['revision_var'],
                    input_fields['testby_var'], input_fields['status_var'], input_fields['reportlink_var'],
                    input_fields['comments_var']
                )

                if existing_entry:
                    query_params = query_params + (existing_entry[0],)

                cursor.execute(query_template, query_params)
                connection.commit()

                # Clear input fields and update GUI display
                self.s_clear_entry_fields()
                self.stage1_table.delete(*self.stage1_table.get_children())

                # Fetch and update the table
                cursor.execute(
                    f"SELECT Id, Tested_Date, Satellite_SN, System, Subsystem_SN, Part_Number, Revision, Tested_By, "
                    f"Status, Test_Report_Link, Comments FROM {table_name} ORDER BY Id DESC LIMIT 1")
                item = cursor.fetchone()
                if item:
                    id, testdate_var, satellite_var, entrystage1_var, sn_var, \
                        partnum_var, revision_var, testby_var, status_var, comments_var, reportlink_var = item
                    self.stage1_table.insert("", 0, text=selected_radio,
                                             values=(
                                                 id, testdate_var, satellite_var, entrystage1_var,
                                                 sn_var, partnum_var, revision_var,
                                                 testby_var,status_var, comments_var, reportlink_var))

                    # Display success message
                    messagebox.showinfo("Success", f"Stage I: {selected_radio} Integration details added successfully",
                                        parent=self.si)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.si)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def update_si(self):
        testdate_var = self.s1_txt_testedDate.get()
        satellite_var = self.s_stage1satellitecombo.get()
        sn_var = self.s1_txt_serial.get().upper()
        testby_var = self.s1_txt_testedBy.get()
        partnum_var = self.s1_txt_partnum.get()
        revision_var = self.s1_txt_revision.get()
        status_var = self.status_var.get()
        reportlink_var = self.s1_txt_reportLink.get()
        entrystage1_var = self.s_subcomponent_txt.get().upper()
        comments_var = self.s1_txt_comment.get()

        selected_item_id = self.stage1_table.selection()
        if not selected_item_id:
            messagebox.showwarning("Warning", "Please select an item to update.", parent=self.si)
            return

        if not satellite_var or not sn_var or entrystage1_var == "":
            messagebox.showerror("Error", "Fill in all required fields", parent=self.si)
            return

        if status_var == "Status":
            messagebox.showerror("Error", "Select Status", parent=self.si)
            return

        unique_id = self.stage1_table.item(selected_item_id, "values")[0]
        selection = self.radio_var.get()

        if selection not in ["FM", "EDM"]:
            messagebox.showerror("Error", "Select either FM or EDM", parent=self.si)
            return

        connection = sqlite3.connect("SerialTracking.db")
        cursor = connection.cursor()

        table_name = f"{selection}_SatelliteIntegration"

        cursor.execute(f"SELECT Id, Tested_Date, Satellite_SN, System, Subsystem_SN, Part_number, Revision, "
                       f"Tested_By, Status, Test_Report_Link, Comments FROM {table_name} WHERE Id = ?", (unique_id,))
        existing_item = cursor.fetchone()

        if existing_item:
            update_columns = ["Tested_Date", "Satellite_SN", "System", "Subsystem_SN", "Part_number", "Revision",
                              "Tested_By", "Status", "Test_Report_Link", "Comments"]
            update_query = f"UPDATE {table_name} SET " + ", ".join(
                f"{col} = ?" for col in update_columns) + " WHERE Id = ?"

            update_values = (testdate_var, satellite_var, entrystage1_var, sn_var, partnum_var, revision_var,
                             testby_var, status_var, reportlink_var, comments_var, unique_id)

            cursor.execute(update_query, update_values)
            connection.commit()

            self.s_clear_entry_fields()
            self.stage1_table.delete(*self.stage1_table.get_children())

            cursor.execute(f"SELECT Id, Tested_Date, Satellite_SN, System, Subsystem_SN, Part_number, Revision, "
                           f"Tested_By, Status, Test_Report_Link, Comments FROM {table_name} ORDER BY Timestamp DESC LIMIT 1")
            item = cursor.fetchone()

            if item:
                id, testdate_var, satellite_var, entrystage1_var, sn_var, partnum_var, revision_var, testby_var, \
                    status_var, comments_var, reportlink_var = item
                self.stage1_table.insert("", 0, text=selection,
                                         values=(id, testdate_var, satellite_var, entrystage1_var, sn_var, partnum_var,
                                                 revision_var, testby_var, status_var, comments_var, reportlink_var))
                messagebox.showinfo("Success", f"Satellite: {selection} Integration details Updated successfully",
                                    parent=self.si)
        else:
            messagebox.showwarning("Warning", f"No component with ID {unique_id} found.", parent=self.si)

        connection.close()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def s_fetch_data(self, event):
        try:
            selected_item = self.stage1_table.selection()
            if not selected_item:
                return

            # Get the values of the selected item
            values = self.stage1_table.item(selected_item, "values")

            # Store the value of column 0 temporarily for later use
            temp_id = values[0]

            # Fetch the value of the first column (name of the table)
            table_type = temp_id

            # Populate the entry boxes with the fetched data
            testeddate, category_type, subcomponent, serial, partnum, \
                revision, testedby, status, reportlink, comments = values[1:11]

            text = self.stage1_table.item(selected_item, "text")
            print(text)
            if text == "FM_SatelliteIntegration":
                self.radio_var.set("FM")
                print(self.radio_var.get())  # This will print the value, not set it again
            elif text == "EDM_SatelliteIntegration":
                self.radio_var.set("EDM")
                print(self.radio_var.get())  # This will print the value, not set it again


            if status == "None":
                self.status_var.set("Status")
                self.status_menu.config(font=("arial", 17, "bold"), bg="#03B4E6", fg="black")
            elif status == "Work In Progress":
                self.status_var.set("Work In Progress")
                self.status_menu.config(font=("arial", 17, "bold"), bg="yellow", fg="black")
            else:
                self.status_var.set("Complete")
                self.status_menu.config(font=("arial", 17, "bold"), bg="green", fg="black")

            self.s1_txt_testedDate.delete(0, tk.END)
            self.s1_txt_testedDate.insert(0, testeddate)

            self.s_stage1satellitecombo.set(category_type)

            self.s_subcomponent_txt.delete(0, tk.END)
            self.s_subcomponent_txt.insert(0, subcomponent)

            self.s1_txt_serial.delete(0, tk.END)
            self.s1_txt_serial.insert(0, serial)

            self.s1_txt_partnum.delete(0, tk.END)
            self.s1_txt_partnum.insert(0, partnum)

            self.s1_txt_revision.delete(0, tk.END)
            self.s1_txt_revision.insert(0, revision)

            self.s1_txt_testedBy.delete(0, tk.END)
            self.s1_txt_testedBy.insert(0, testedby)

            self.s1_txt_reportLink.delete(0, tk.END)
            self.s1_txt_reportLink.insert(0, reportlink)

            self.s1_txt_comment.delete(0, tk.END)
            self.s1_txt_comment.insert(0, comments)

            self.s3_listbox.place_forget()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.si)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def s_update_treeview(self):

        global data
        try:
            # Check if the selected item exists in the register table based on the unique ID
            connection = sqlite3.connect("SerialTracking.db")

            # Clear the existing data in the Treeview
            self.stage1_table.delete(*self.stage1_table.get_children())

            Finals = ["FM_SatelliteIntegration", "EDM_SatelliteIntegration"]

            for final_table in Finals:
                cursor = connection.execute(f"SELECT * FROM {final_table}")
                data = cursor.fetchall()

                # Insert data into the Treeview
                for item in data:
                    item_id = item[0]  # Assuming the ID is the first value in the item tuple
                    item_data = item[0:]  # The rest of the data for the item
                    self.stage1_table.insert("", 0, text=final_table, values=item_data, tags=(item_id,))

            connection.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.si)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++SubSystem Test Status++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def subsystem_test(self):

        self.ssi = Toplevel(self.root)
        self.ssi.title('SUBSYSTEM TEST STATUS')
        self.ssi.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.ssi.focus_force()
        self.ssi.lift()
        self.root.withdraw()

        # =============

        self.ss_title_frame = tk.Frame(self.ssi, bd=4, relief=RIDGE, bg="#03B4E6")
        self.ss_title_frame.pack(side=TOP, fill=X)

        # Create the label inside the title frame
        self.ss_title = Label(self.ss_title_frame, text="SubSystem Test Status", font=("times new roman", 30, "bold"),
                              bg="#03B4E6", fg="white", bd=10, relief=GROOVE)
        self.ss_title.pack(side=TOP, fill=X)

        # Create "Close" button
        ss3_exit_btn = Button(self.ss_title_frame, text="Close", font=("arial", 15, "bold"), bg="#0F148C",
                              cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.ss_close_window)
        ss3_exit_btn.place(x=1090, y=15, width=100, height=37)
        # ==================================Frame 1=====================================================

        self.ss_integration_details = Frame(self.ssi, bd=10, relief=RIDGE, bg="#03B4E6")
        self.ss_integration_details.place(x=5, y=80, width=1220, height=315)

        # =================Create labels Vertically===================

        # Create the label inside the title frame
        self.ss_subsystem_lbl = Label(self.ss_integration_details, text="System", bd=5, relief=GROOVE,
                                      font=("times new roman", 13, "bold"), width=10, bg="#63B8FF", fg="white")
        self.ss_subsystem_lbl.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        # ============= Entry widget for the TESTED BY ============
        self.ss3_entry_setup()

    def ss3_entry_setup(self):
        conn = sqlite3.connect("SerialTracking.db")  # Replace with your database file
        cursor = conn.cursor()

        Finals = ["FM_SubsystemTest", "EDM_SubsystemTest"]

        ss3_unique_items = []

        for final_table in Finals:
            cursor.execute(f"SELECT System FROM {final_table}")
            ss3_column_data = cursor.fetchall()
            ss3_unique_items.extend([item[0] for item in ss3_column_data])

        ss3entry_var = tk.StringVar()
        self.ss_subcomponent_txt = tk.Entry(self.ss_integration_details,
                                            font=("times new roman", 12, "bold"), bd=5, relief=tk.GROOVE,
                                            textvariable=ss3entry_var, bg="#FFE7BA", width=20, justify=tk.CENTER)
        self.ss_subcomponent_txt.grid(row=1, column=1, padx=10, sticky="e", pady=5)

        def ss3on_entry_change(*args):
            ss3_search_text = ss3entry_var.get().upper()

            ss3_filtered_items = [item for item in ss3_unique_items if item and ss3_search_text in item.upper()]

            self.ss3_listbox.delete(0, tk.END)
            for item in ss3_filtered_items:
                self.ss3_listbox.insert(tk.END, item)

            if ss3_filtered_items:
                self.ss3_listbox.lift()
                self.ss3_listbox.place(x=self.ss_subcomponent_txt.winfo_x(),
                                  y=self.ss_subcomponent_txt.winfo_y() + self.ss_subcomponent_txt.winfo_height() + 5)
            else:
                self.ss3_listbox.place_forget()

        ss3entry_var.trace_add("write", ss3on_entry_change)

        self.ss3_listbox = tk.Listbox(self.ss_integration_details, font=("times new roman", 12, "bold"),
                                 bd=5, relief=tk.GROOVE, takefocus=True)

        self.ss3_listbox_scrollbar = tk.Scrollbar(self.ss_integration_details, orient="vertical", command=self.ss3_listbox.yview)
        self.ss3_listbox.config(yscrollcommand=self.ss3_listbox_scrollbar.set)

        self.ss3_listbox_scrollbar.place(x=self.ss3_listbox.winfo_x() + self.ss3_listbox.winfo_width() - 2, y=self.ss3_listbox.winfo_y(),
                                    height=self.ss3_listbox.winfo_height())

        self.ss3_listbox.place_forget()

        def ss3on_listbox_select(event):
            ss3_selection = self.ss3_listbox.curselection()
            if ss3_selection:
                ss3_selected_item = self.ss3_listbox.get(ss3_selection)
                ss3entry_var.set(ss3_selected_item)
                self.ss3_listbox.place_forget()

        self.ss3_listbox.bind("<<ListboxSelect>>", ss3on_listbox_select)

        # =================Create labels Vertically===================

        Label(self.ss_integration_details, text="Serial No:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=2, column=0, padx=10, pady=2, sticky="w")
        self.ss1_txt_serial = Entry(self.ss_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                    relief=GROOVE, justify=CENTER)
        self.ss1_txt_serial.grid(row=2, column=1, padx=10, sticky="e", pady=5)
        # =====================================================================
        Label(self.ss_integration_details, text="Tested Date:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=3, column=0, padx=10, pady=2, sticky="w")
        self.ss1_txt_testedDate = Entry(self.ss_integration_details, font=("times new roman", 12, "bold"),
                                        bd=5, relief=GROOVE, justify=CENTER)
        self.ss1_txt_testedDate.grid(row=3, column=1, padx=10, sticky="e", pady=5)
        # ========================================================================================
        Label(self.ss_integration_details, text="Part No:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w', justify=CENTER).grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.ss1_txt_partnum = Entry(self.ss_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                     relief=GROOVE, justify=CENTER)
        self.ss1_txt_partnum.grid(row=4, column=1, padx=10, sticky="e", pady=5)
        # ======================================================================
        Label(self.ss_integration_details, text="Revision:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=5, column=0, padx=10, pady=2, sticky="w")
        self.ss1_txt_revision = Entry(self.ss_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                      relief=GROOVE, justify=CENTER)
        self.ss1_txt_revision.grid(row=5, column=1, padx=10, sticky="e", pady=5)
        # =================================================================
        Label(self.ss_integration_details, text="Tested By:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=6, column=0, padx=10, pady=2, sticky="w")
        self.ss1_txt_testedBy = Entry(self.ss_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                      relief=GROOVE, justify=CENTER)
        self.ss1_txt_testedBy.grid(row=6, column=1, padx=10, sticky="e", pady=5)
        # ================================================================
        Label(self.ss_integration_details, text="Test Report Link:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=1, column=2, padx=(25, 10), pady=2, sticky="w")
        self.ss1_txt_reportLink = Entry(self.ss_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                        relief=GROOVE)
        self.ss1_txt_reportLink.grid(row=1, column=3, padx=10, sticky="e", pady=5)
        # ================================================================
        Label(self.ss_integration_details, text="Comment:", font=("times new roman", 13, "bold"),
              bg="#03B4E6", fg="black", anchor='w').grid(row=2, column=2, padx=(25, 10), pady=2, sticky="w")
        self.ss1_txt_comment = Entry(self.ss_integration_details, font=("times new roman", 12, "bold"), bd=5,
                                     relief=GROOVE)
        self.ss1_txt_comment.grid(row=2, column=3, padx=10, sticky="e", pady=5)
        # ====================================================================================================
        # =======================PASS/FAIL SWITCH=================================================================
        # ====================================================================================================

        ss_radio_frame = Frame(self.ss_integration_details, bd=0, relief=RIDGE, bg="#03B4E6")
        ss_radio_frame.place(x=370, y=100, width=330, height=120)

        # Create radio buttons
        self.ss_result_var = tk.StringVar()
        self.ss_result_var.set(None)  # Default selection should be None

        self.pass_radio = tk.Radiobutton(ss_radio_frame, text="PASS", value="PASS", bg="#03B4E6", fg="black", bd=4,
                                         relief=tk.GROOVE,
                                         command=lambda: self.ss_pass_fail_selection("PASS"),
                                         font=("arial", 17, "bold"),
                                         width=4, variable=self.ss_result_var)
        self.pass_radio.grid(row=0, column=0, pady=10, padx=0)

        self.fail_radio = tk.Radiobutton(ss_radio_frame, text="FAIL", value="FAIL", bg="#03B4E6", fg="black", bd=4,
                                         relief=tk.GROOVE,
                                         command=lambda: self.ss_pass_fail_selection("FAIL"),
                                         font=("arial", 17, "bold"),
                                         width=4, variable=self.ss_result_var)
        self.fail_radio.grid(row=0, column=1, pady=10, padx=0)



        # ====================================================================================================
        # =======================RADIO BUTTON=================================================================
        # ====================================================================================================

        # Create radio buttons
        self.ss_radio_var = tk.StringVar()
        self.ss_radio_var.set("FM")  # Default selection

        self.ss_fm_table = tk.Radiobutton(ss_radio_frame, text="FM", font=("arial", 17, "bold"),
                                          variable=self.ss_radio_var, width=4,
                                          value="FM", bg="#63B8FF" ,bd=4, relief=GROOVE)

        self.ss_fm_table.grid(row=1, column=0, pady=5, padx=30)

        self.ss_edm_table = tk.Radiobutton(ss_radio_frame, text="EDM", font=("arial", 17, "bold"), bd=4,
                                           variable=self.ss_radio_var, value="EDM", bg="#63B8FF", relief=GROOVE,
                                           width=4)
        self.ss_edm_table.grid(row=1, column=1, pady=5, padx=30)
        # ====================================================================================================
        # ====================================================================================================
        # ======================================================================================================

        ss_btn_frame = Frame(self.ss_integration_details, bd=0, relief=RIDGE, bg="#03B4E6")
        ss_btn_frame.place(x=350, y=240, width=330, height=50)
        # =================================================================================================
        ss3_save_btn = Button(ss_btn_frame, text="SAVE", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                              bg="#0F148C", cursor="hand2", fg="white", width=8, command=self.add_ssi)
        ss3_save_btn.grid(row=0, column=0, padx=8, pady=0)

        # Create an "Update Item" button
        ss3_udpate_btn = Button(ss_btn_frame, text="UPDATE", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                                bg="#0F148C", cursor="hand2", fg="white", width=8, command=self.update_ssi)
        ss3_udpate_btn.grid(row=0, column=1, padx=8, pady=0)

        # Create an "Update Item" button
        ss3_clear_btn = Button(ss_btn_frame, text="CLEAR", font=("arial", 11, "bold"), relief=RAISED, bd=8,
                               bg="#0F148C", cursor="hand2", fg="white", width=8, command=self.ss_clear_entry_fields)
        ss3_clear_btn.grid(row=0, column=2, padx=8, pady=0)

        # ===========================================================================================

        ss_btn_frame = Frame(self.ss_integration_details, bd=3, relief=RIDGE, bg="#03B4E6")
        ss_btn_frame.place(x=730, y=20, width=440, height=250)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.ss_table_frame = Frame(self.ssi, bd=10, relief=RIDGE, bg="#03B4E6")
        self.ss_table_frame.place(x=5, y=395, width=1220, height=200)

        # ==========================TREEVIEW====================================
        ss_scroll_x = Scrollbar(self.ss_table_frame, orient=HORIZONTAL)
        ss_scroll_y = Scrollbar(self.ss_table_frame, orient=VERTICAL)
        self.subSystem_table = ttk.Treeview(self.ss_table_frame, xscrollcommand=ss_scroll_x.set,
                                            yscrollcommand=ss_scroll_y.set)
        ss_scroll_x.pack(side=BOTTOM, fill=X)
        ss_scroll_y.pack(side=RIGHT, fill=Y)
        ss_scroll_x.config(command=self.subSystem_table.xview)
        ss_scroll_y.config(command=self.subSystem_table.yview)

        self.subSystem_table["columns"] = (
            "Id", "Tested_Date", "System", "Subsystem_SN", "Part_number", "Revision", "Tested_By", "Result",
            "Test_Report_Link", "Comments", "Timestamp")

        # Configure the Treeview columns
        self.subSystem_table.heading("#0", text="Table")
        self.subSystem_table.heading("Id", text="Id")
        self.subSystem_table.heading("Tested_Date", text="TESTED DATE")
        self.subSystem_table.heading("System", text="SYSTEM")
        self.subSystem_table.heading("Subsystem_SN", text="SERIAL NO.")
        self.subSystem_table.heading("Part_number", text="PART NO.")
        self.subSystem_table.heading("Revision", text="REVISION")
        self.subSystem_table.heading("Tested_By", text="TESTED BY")
        self.subSystem_table.heading("Result", text="RESULT")
        self.subSystem_table.heading("Test_Report_Link", text="REPORT LINK")
        self.subSystem_table.heading("Comments", text="COMMENT")
        self.subSystem_table.heading("Timestamp", text="TIMESTAMP")

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), foreground='#0F148C', background='black')

        # Configure the Treeview headings
        # self.subSystem_table['show'] = 'headings'
        self.subSystem_table.column("#0", width=0, stretch=tk.NO)
        self.subSystem_table.column("Id", width=0, stretch=tk.NO)
        self.subSystem_table.column("Tested_Date", width=100)
        self.subSystem_table.column("System", width=70)
        self.subSystem_table.column("Subsystem_SN", width=70)
        self.subSystem_table.column("Part_number", width=70)
        self.subSystem_table.column("Revision", width=70)
        self.subSystem_table.column("Tested_By", width=120)
        self.subSystem_table.column("Result", width=60)
        self.subSystem_table.column("Test_Report_Link", width=200)
        self.subSystem_table.column("Comments", width=200)
        self.subSystem_table.column("Timestamp", width=0, stretch=tk.NO)

        self.subSystem_table.pack(fill=BOTH, expand=1)

        self.subSystem_table.bind("<<TreeviewSelect>>", self.ss_fetch_data)

        self.ss_set_current_date()
        self.ss_update_treeview()

    def ss_close_window(self):
        self.ssi.destroy()  # Close the integration frame
        self.root.deiconify()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    def ss_pass_fail_selection(self, option):
        self.ss_result_var.set(option)  # Update the selected value

        if option == "PASS":
            self.pass_radio.config(text="PASS", font=("arial", 17, "bold"), bg="green", fg="white", bd=5,
                                   width=4, height=1, anchor='center', selectcolor="green")
            self.fail_radio.config(bg="#03B4E6", fg="black", selectcolor="#03B4E6")
        elif option == "FAIL":
            self.pass_radio.config(bg="#03B4E6", fg="black", selectcolor="#03B4E6")
            self.fail_radio.config(text="FAIL", font=("arial", 17, "bold"), bg="RED", fg="white", bd=5,
                                   width=4, height=1, anchor='center',  selectcolor="red")

    def ss_deselect_pass_fail(self):
        self.ss_result_var.set(None)  # Update the selected value

        self.pass_radio.config(text="PASS", font=("arial", 17, "bold"), bg="#03B4E6", fg="black", bd=5,
                               width=4, height=1, anchor='center', selectcolor="white")

        self.fail_radio.config(text="FAIL", font=("arial", 17, "bold"), bg="#03B4E6", fg="black", bd=5,
                               width=4, height=1, anchor='center', selectcolor="white")
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def ss_set_current_date(self):
        try:
            current_date = date.today().strftime("%Y/%m/%d")
            self.ss1_txt_testedDate.delete(0, tk.END)  # Clear any existing text
            self.ss1_txt_testedDate.insert(0, current_date)  # Insert the current date into the widget
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to dateSS: {str(ex)}", parent=self.root)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def ss_clear_entry_fields(self):
        # Clear input fields
        self.ss_set_current_date()
        self.ss1_txt_serial.delete(0, tk.END)
        self.ss1_txt_testedBy.delete(0, tk.END)
        self.ss1_txt_partnum.delete(0, tk.END)
        self.ss1_txt_revision.delete(0, tk.END)
        self.ss_deselect_pass_fail()
        self.ss1_txt_reportLink.delete(0, tk.END)
        self.ss_subcomponent_txt.delete(0, tk.END)
        self.ss1_txt_comment.delete(0, tk.END)
        self.ss_update_treeview()
        self.ss3_listbox.place_forget()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def add_ssi(self):
        try:
            # Extract input values
            input_fields = {
                'testdate_var': self.ss1_txt_testedDate.get(),
                'sn_var': self.ss1_txt_serial.get().upper(),
                'testby_var': self.ss1_txt_testedBy.get(),
                'partnum_var': self.ss1_txt_partnum.get(),
                'revision_var': self.ss1_txt_revision.get(),
                'reportlink_var': self.ss1_txt_reportLink.get(),
                'result_var' : self.ss_result_var.get(),
                'entrysubsystem_var': self.ss_subcomponent_txt.get().upper(),
                'comments_var': self.ss1_txt_comment.get()
            }
            if input_fields['entrysubsystem_var'] == "":
                messagebox.showerror("Error", "Enter the System.", parent=self.ssi)
                return
            if not input_fields['sn_var']:
                messagebox.showerror("Error", "Enter the Serial number", parent=self.ssi)
                return

            if self.ss_result_var.get() == "None":
                messagebox.showerror("Error", "Select PASS or FAIL", parent=self.ssi)
                return# Exit the loop if a valid selection is made


            # Map radio button values to table names
            table_names = {'FM': 'FM_SubsystemTest', 'EDM': 'EDM_SubsystemTest'}
            selected_radio = self.ss_radio_var.get()
            if selected_radio not in table_names:
                messagebox.showerror("Error", "Select either FM or EDM", parent=self.ssi)
                return
            # Connect to the database and start a transaction
            with sqlite3.connect("SerialTracking.db") as connection:
                cursor = connection.cursor()

                table_name = table_names[selected_radio]

                # Check for existing entry
                cursor.execute(
                    f"SELECT Id FROM {table_name} WHERE System = ? AND Subsystem_SN = ?",
                    (input_fields['entrysubsystem_var'], input_fields['sn_var']))
                existing_entry = cursor.fetchone()

                # Construct query template for insertion or updating
                if existing_entry:
                    query_template = f"""
                                    UPDATE {table_name}
                                    SET Tested_Date = ?, System = ?, Subsystem_SN = ?, Part_number = ?, Revision = ?, 
                                    Tested_By = ?, Result = ?, Test_Report_Link = ?, Comments = ?
                                    WHERE Id = ?
                                """
                else:
                    query_template = f"""
                                    INSERT INTO {table_name} (Tested_Date, System, Subsystem_SN, Part_number, Revision, 
                                    Tested_By, Result, Test_Report_Link, Comments)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """

                # Construct query parameters
                query_params = (
                    input_fields['testdate_var'], input_fields['entrysubsystem_var'],
                    input_fields['sn_var'], input_fields['partnum_var'], input_fields['revision_var'],
                    input_fields['testby_var'], input_fields['result_var'],
                    input_fields['reportlink_var'],
                    input_fields['comments_var']
                )

                if existing_entry:
                    query_params = query_params + (existing_entry[0],)

                # Execute the query and commit the transaction
                cursor.execute(query_template, query_params)
                connection.commit()

                # Clear input fields and update GUI display
                self.ss_clear_entry_fields()
                self.subSystem_table.delete(*self.subSystem_table.get_children())

                # Fetch and update the table
                cursor.execute(
                    f"SELECT Id, Tested_Date, System, Subsystem_SN, Part_Number, Revision, Tested_By, Result, "
                    f"Test_Report_Link, Comments FROM {table_name} ORDER BY Id DESC LIMIT 1")
                item = cursor.fetchone()
                if item:
                    id, testdate_var, entrysubsystem_var, sn_var, \
                        partnum_var, revision_var, testby_var, result_var, comments_var, reportlink_var = item
                    self.subSystem_table.insert("", 0, text=selected_radio,
                                                values=(
                                                    id, testdate_var, entrysubsystem_var, sn_var, partnum_var,
                                                    revision_var,
                                                    testby_var, result_var, comments_var, reportlink_var))

                    # Display success message
                    messagebox.showinfo("Success", f"Subsystem: {selected_radio} Test details added successfully",
                                        parent=self.ssi)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurredADDSS: {str(e)}", parent=self.ssi)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def update_ssi(self):
        testdate_var = self.ss1_txt_testedDate.get()
        sn_var = self.ss1_txt_serial.get().upper()
        testby_var = self.ss1_txt_testedBy.get()
        partnum_var = self.ss1_txt_partnum.get()
        revision_var = self.ss1_txt_revision.get()
        result_var = self.ss_result_var.get()
        reportlink_var = self.ss1_txt_reportLink.get()
        entrysubsystem_var = self.ss_subcomponent_txt.get().upper()
        comments_var = self.ss1_txt_comment.get()

        selected_item_id = self.subSystem_table.selection()
        if not selected_item_id:
            messagebox.showwarning("Warning", "Please select an item to update.", parent=self.ssi)
            return

        if not sn_var or entrysubsystem_var == "":
            messagebox.showerror("Error", "Fill in all required fields", parent=self.ssi)
            return

        if self.ss_result_var.get() == "None":
            messagebox.showerror("Error", "Select PASS or FAIL", parent=self.ssi)
            return  # Exit the loop if a valid selection is made

        unique_id = self.subSystem_table.item(selected_item_id, "values")[0]
        selection = self.ss_radio_var.get()

        if selection not in ["FM", "EDM"]:
            messagebox.showerror("Error", "Select either FM or EDM", parent=self.ssi)
            return

        connection = sqlite3.connect("SerialTracking.db")
        cursor = connection.cursor()

        table_name = f"{selection}_SubsystemTest"

        cursor.execute(f"SELECT Id, Tested_Date, System, Subsystem_SN, Part_number, Revision, "
                       f"Tested_By, Result, Test_Report_Link, Comments FROM {table_name} WHERE Id = ?", (unique_id,))
        existing_item = cursor.fetchone()

        if existing_item:
            update_columns = ["Tested_Date", "System", "Subsystem_SN", "Part_number", "Revision",
                              "Tested_By", "Result", "Test_Report_Link", "Comments"]
            update_query = f"UPDATE {table_name} SET " + ", ".join(
                f"{col} = ?" for col in update_columns) + " WHERE Id = ?"

            update_values = (testdate_var, entrysubsystem_var, sn_var, partnum_var, revision_var,
                             testby_var, result_var, reportlink_var, comments_var, unique_id)

            cursor.execute(update_query, update_values)
            connection.commit()

            self.ss_clear_entry_fields()
            self.subSystem_table.delete(*self.subSystem_table.get_children())

            cursor.execute(f"SELECT Id, Tested_Date, System, Subsystem_SN, Part_number, Revision, "
                           f"Tested_By, Result, Test_Report_Link, Comments FROM {table_name} ORDER BY Timestamp DESC LIMIT 1")
            item = cursor.fetchone()

            if item:
                id, testdate_var, entrysubsystem_var, sn_var, partnum_var, revision_var, testby_var, result_var,\
                    comments_var, reportlink_var = item
                self.subSystem_table.insert("", 0, text=selection,
                                            values=(id, testdate_var, entrysubsystem_var, sn_var, partnum_var,
                                                    revision_var, testby_var, result_var, comments_var, reportlink_var))
                messagebox.showinfo("Success", f"Subsystem: {selection} Test details Updated successfully",
                                    parent=self.ssi)
        else:
            messagebox.showwarning("Warning", f"No component with ID {unique_id} found.", parent=self.ssi)

        connection.close()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def ss_fetch_data(self, event):
        try:
            selected_item = self.subSystem_table.selection()
            if not selected_item:
                return

            # Get the values of the selected item
            values = self.subSystem_table.item(selected_item, "values")

            # Store the value of column 0 temporarily for later use
            temp_id = values[0]

            # Fetch the value of the first column (name of the table)
            table_type = temp_id

            # Populate the entry boxes with the fetched data
            testeddate, subcomponent, serial, partnum, \
                revision, testedby, result, reportlink, comments = values[1:10]

            text = self.subSystem_table.item(selected_item, "text")
            print(text)
            if text == "FM_SubsystemTest":
                self.ss_radio_var.set("FM")
                print(self.ss_radio_var.get())  # This will print the value, not set it again
            elif text == "EDM_SubsystemTest":
                self.ss_radio_var.set("EDM")
                print(self.ss_radio_var.get())  # This will print the value, not set it again

            # Set the radio buttons based on the fetched result
            if result == "PASS":
                self.ss_result_var.set("PASS")
                self.pass_radio.config(text="PASS", font=("arial", 17, "bold"), bg="green", fg="white", bd=5,
                                       width=4, height=1, anchor='center', selectcolor="green")
                self.fail_radio.config(bg="#03B4E6", fg="black", selectcolor="#03B4E6")
            elif result == "FAIL":
                self.ss_result_var.set("FAIL")
                self.pass_radio.config(bg="#03B4E6", fg="black", selectcolor="#03B4E6")
                self.fail_radio.config(text="FAIL", font=("arial", 17, "bold"), bg="RED", fg="white", bd=5,
                                       width=4, height=1, anchor='center', selectcolor="red")
            else:
                self.ss_deselect_pass_fail()

            self.ss1_txt_testedDate.delete(0, tk.END)
            self.ss1_txt_testedDate.insert(0, testeddate)

            self.ss_subcomponent_txt.delete(0, tk.END)
            self.ss_subcomponent_txt.insert(0, subcomponent)

            self.ss1_txt_serial.delete(0, tk.END)
            self.ss1_txt_serial.insert(0, serial)

            self.ss1_txt_partnum.delete(0, tk.END)
            self.ss1_txt_partnum.insert(0, partnum)

            self.ss1_txt_revision.delete(0, tk.END)
            self.ss1_txt_revision.insert(0, revision)

            self.ss1_txt_testedBy.delete(0, tk.END)
            self.ss1_txt_testedBy.insert(0, testedby)

            self.ss1_txt_reportLink.delete(0, tk.END)
            self.ss1_txt_reportLink.insert(0, reportlink)

            self.ss1_txt_comment.delete(0, tk.END)
            self.ss1_txt_comment.insert(0, comments)

            self.ss3_listbox.place_forget()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.ssi)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def ss_update_treeview(self):

        global data
        try:
            # Check if the selected item exists in the register table based on the unique ID
            connection = sqlite3.connect("SerialTracking.db")

            # Clear the existing data in the Treeview
            self.subSystem_table.delete(*self.subSystem_table.get_children())

            Finals = ["FM_SubsystemTest", "EDM_SubsystemTest"]

            for final_table in Finals:
                cursor = connection.execute(f"SELECT * FROM {final_table}")
                data = cursor.fetchall()

                # Insert data into the Treeview
                for item in data:
                    item_id = item[0]  # Assuming the ID is the first value in the item tuple
                    item_data = item[0:]  # The rest of the data for the item
                    self.subSystem_table.insert("", 0, text=final_table, values=item_data, tags=(item_id,))

            connection.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.ssi)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def report_generate(self):

        self.root.withdraw()  # Hide the main window
        #self.new_win.grab_set()  # Disable the main window
        self.new_win = Toplevel(self.root)  # Create a new Toplevel window
        self.new_win.protocol("WM_DELETE_WINDOW", self.handle_window_close)
        # Create an instance of Generate_report_class
        self.new_obj = Generate_report_class(self.new_win, self.handle_window_close)


    def handle_window_close(self):
        self.new_win.destroy()
        self.root.deiconify()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def close_configmgm(self):
        self.enable_trackSN()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = TrackingSN_class(root, None)
    root.mainloop()
