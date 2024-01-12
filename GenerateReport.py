from tkinter import *
from tkinter import ttk, scrolledtext
import tkinter as tk

import mysql.connector
import win32print
import win32ui


class Generate_report_class:
    def __init__(self, root, enable_button):
        self.root = root
        self.root.geometry("1230x600+260+165")
        self.root.minsize(1230, 600)  # Set minimum dimensions
        self.root.maxsize(1230, 600)  # Set maximum dimensions
        self.root.title("CONFIGURATION MANAGEMENT")
        self.root.config(bg="white")
        self.enable_button = enable_button
        self.root.focus_force()
        # ==================================TITLE FRAME ===============================================================
        self.title_frame = Frame(self.root, bd=4, relief=RIDGE, bg="#63B8FF")
        self.title_frame.pack(side=TOP, fill=X)

        Label(self.title_frame, text="REPORT GENERATION", font=("times new roman", 30, "bold"),
              bg="#63B8FF", fg="white", bd=10, relief=GROOVE).pack(side=TOP, fill=X)

        self.closebtn = Button(self.title_frame, text="Close", font=("arial", 15, "bold"), bg="#0F148C",
                               cursor="hand2", relief=RAISED, fg="white", bd=8, command=self.close_configmgm)
        self.closebtn.place(x=1090, y=15, width=100, height=37)
        # ====================================================================

        self.tree_title_frame = tk.Frame(self.root, bd=0, relief=tk.RIDGE, bg="#63B8FF")
        self.tree_title_frame.place(x=293, y=80, width=930, height=50)

        # Create the label inside the title frame
        self.title = tk.Label(self.tree_title_frame, text="Reports", bd=5, relief=tk.GROOVE,
                              font=("times new roman", 21, "bold"), bg="#63B8FF", fg="white")
        self.title.pack(side=tk.TOP, fill=tk.BOTH)

        # ===============================================================================

        # Create frames for GUI components
        self.manage_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="#03B4E6")
        self.manage_frame.place(x=293, y=130, width=930, height=450)

        # Create a text area to display existing data
        self.preview_text = tk.Text(self.manage_frame, state=tk.NORMAL, background="#FFFAFA",
                                    height=25, width=100, wrap=tk.WORD)
        self.preview_text.grid(row=0, column=0, padx=60, pady=20)
        # ===============================================================================
        # ===============================================================================
        self.tree_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="#63B8FF")
        self.tree_frame.place(x=5, y=80, width=285, height=500)

        # Create scrollbars and Treeview
        scroll_x = tk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self.tree_frame, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)
        self.tree.heading('#0', text='BLOCK IV', anchor='center')

        # Set heading style using ttk.Style() for "Treeview.Heading" element
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 15, 'bold'), foreground='#0F148C', background='black')
        # Customize the entire treeview widget
        style.configure("Treeview", font=('Helvetica', 11, 'bold'))
        style.map("Treeview", background=[('selected', '#63B8FF')])

        self.tree.pack(expand=True, fill='both')
        self.tree.bind("<<TreeviewSelect>>", self.show_preview)

        self.load_data_from_database()
        self.load_tables()
        # Collapse all items in the Treeview
        self.collapse_all_tree_items()

        # ===============================================================================

        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                           database="serialtracking")
        self.cur = self.con.cursor()

    def collapse_all_tree_items(self):
        for item in self.tree.get_children():
            self.tree.item(item, open=False)

        # ===============================================================================

        # Add buttons to add, update, and delete nodes
        add_button = Button(self.tree_frame, text="Add")
        add_button.pack(side=LEFT)

        update_button = Button(self.tree_frame, text="Update")
        update_button.pack(side=LEFT)

        report_button = Button(self.tree_frame, text="Report")
        report_button.pack(side=LEFT)

        delete_button = Button(self.tree_frame, text="Delete")
        delete_button.pack(side=LEFT)

        delete_button = Button(self.tree_frame, text="Delete")
        delete_button.pack(side=LEFT)

    # ===============================================================================
    def load_data_from_database(self):
        # Connect to the database
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                               database="serialtracking")
            self.cur = self.con.cursor()


        except EXCEPTION as e:
            print("Error connecting to the database:", e)
            return

        selected_item = self.tree.selection()

        # Create a parent node called "Systems"
        systems_node = self.tree.insert("", "end", text="Systems", open=True)

        # Dictionary to store unique systems and their subsystems
        unique_systems = {}

        # Fetch distinct values from "System" column for both tables
        for table_name in ["FM_SubsystemTest", "EDM_SubsystemTest"]:
            try:
                self.cur.execute(f"SELECT DISTINCT SystemName FROM {table_name};")
                system_values = self.cur.fetchall()

                for system_value in system_values:
                    system_name = system_value[0]
                    if system_name not in unique_systems:
                        unique_systems[system_name] = []

                    # Fetch distinct values from "Subsystem_SN" column for this system
                    self.cur.execute(f"SELECT DISTINCT Subsystem_SN FROM {table_name} WHERE System = ?;",
                                        (system_name,))
                    subsystem_values = self.cur.fetchall()
                    unique_systems[system_name].extend(subsystem_values)

            except EXCEPTION as e:
                print("Error fetching data:", e)
                return

        # Populate tree view using the unique_systems dictionary
        for system_name, subsystems in unique_systems.items():
            system_node = self.tree.insert(systems_node, "end", text=system_name)

            for subsystem_value in subsystems:
                subsystem_sn = subsystem_value[0]
                subsystem_node = self.tree.insert(system_node, "end", text=subsystem_sn)

                # Fetch distinct content of columns for this subsystem
                for table_name in ["FM_SubsystemTest", "EDM_SubsystemTest"]:
                    try:
                        self.cur.execute(f"PRAGMA table_info({table_name});")
                        columns = self.cur.fetchall()

                        if len(columns) > 2:
                            for column_index in range(2, len(columns)):
                                column_name = columns[column_index][1]

                                self.cur.execute(
                                    f"SELECT DISTINCT {column_name} FROM {table_name} WHERE SystemName = ? AND Subsystem_SN = ?;",
                                    (system_name, subsystem_sn))
                                distinct_values = self.cur.fetchall()

                    except EXCEPTION as e:
                        print("Error fetching data:", e)
                        return

    # ===============================================================================
    def load_tables(self):
        # Connect to the database
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                               database="serialtracking")
            self.cur = self.con.cursor()

        except EXCEPTION as e:
            print("Error connecting to the database:", e)
            return

        # Fetch table names from the database
        try:
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cur.fetchall()
        except EXCEPTION as e:
            print("Error fetching table names:", e)
            return

        # Dictionary to map actual table names to user-friendly names
        table_name_mapping = {
            "FM_SubsystemTest": "Subsystem Test (FM)",
            "EDM_SubsystemTest": "Subsystem Test (EDM)",
            "FM_SatelliteIntegration": "Satellite Integration (FM)",
            "EDM_SatelliteIntegration": "Satellite Integration (EDM)",
            "sqlite_sequence": "Sequence Table"
            # Add more mappings as needed
        }

        # Nested dictionary to store unique items
        unique_nodes = {}

        # Populate the tree with table names as root nodes
        for table in tables:
            table_name = table[0]

            # Skip certain table names
            if table_name in ["sqlite_sequence", "FM_SubsystemTest", "EDM_SubsystemTest"]:
                continue

            # Use user-friendly names if available in the mapping, else use the original table name
            user_friendly_name = table_name_mapping.get(table_name, table_name)

            table_node = self.tree.insert("", "end", text=user_friendly_name, open=True)

            # Fetch and add distinct content of columns
            try:
                self.cur.execute(f"PRAGMA table_info({table_name});")
                columns = self.cur.fetchall()

                if len(columns) > 2:
                    column_name = columns[2][1]
                    # for column_index in range(2, len(columns)):
                    #    column_name = columns[column_index][1]
                    self.cur.execute(f"SELECT DISTINCT {column_name} FROM {table_name};")
                    distinct_values = self.cur.fetchall()

                    for value in distinct_values:
                        parent_key = (table_name, value[0])

                        if parent_key not in unique_nodes:
                            parent_node = self.tree.insert(table_node, "end", text=f"{value[0]}")
                            unique_nodes[parent_key] = parent_node
                        else:
                            parent_node = unique_nodes[parent_key]

                        if len(columns) > 3:  # Make sure there's a next following column
                            next_column_name = columns[3][1]

                            self.cur.execute(
                                f"SELECT DISTINCT {next_column_name} FROM {table_name} WHERE {column_name} = ?;",
                                (value[0],))
                            next_distinct_values = self.cur.fetchall()

                            for next_value in next_distinct_values:
                                child_key = (table_name, value[0], next_value[0])

                                if child_key not in unique_nodes:
                                    child_node = self.tree.insert(parent_node, "end",
                                                                  text=f"{next_value[0]}")
                                    unique_nodes[child_key] = child_node

                                    if len(columns) > 3:  # Make sure there's a next following column
                                        next_childcolumn_name = columns[4][1]

                                        self.cur.execute(
                                            f"SELECT DISTINCT {next_childcolumn_name} FROM {table_name} "
                                            f"WHERE {next_column_name} = ?;",
                                            (next_value[0],))
                                        next_granddistinct_values = self.cur.fetchall()

                                        for next_grand_value in next_granddistinct_values:
                                            grandchild_key = (table_name, value[0],
                                                              next_value[0],
                                                              next_grand_value[0])
                                            if grandchild_key not in unique_nodes:
                                                grandchild_node = self.tree.insert(child_node, "end",
                                                                                   text=f"{next_grand_value[0]}")
                                                unique_nodes[grandchild_key] = grandchild_node

            except EXCEPTION as e:
                print("Error fetching data:", e)
                return

    # =================================================================================
    def show_preview(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_text = self.tree.item(selected_item, "text")

        # Fetch data from the database based on the selected item

        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                           database="serialtracking")
        self.cur = self.con.cursor()

        tables = ["FM_SubsystemTest", "EDM_SubsystemTest"]
        fetched_data = None

        for table_name in tables:
            self.cur.execute(f"SELECT * FROM {table_name} WHERE Subsystem_SN = ?;", (item_text,))
            fetched_data = self.cur.fetchone()

            if fetched_data:
                break  # Exit the loop once data is fetched
        try:
            # Update the preview_text widget with the fetched data
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"\t\t\t\tFetched data for: {item_text}\n", )
            self.preview_text.tag_configure("header", font=("Aerial", 17, "bold", "underline"), foreground="black")
            self.preview_text.tag_add("header", "1.0", "end linestart+1c")

            self.preview_text.insert(tk.END, f"________________________________________________________________________________________\n")
            self.preview_text.insert(tk.END, f"________________________________________________________________________________________\n\n")
            self.preview_text.insert(tk.END, f"\tTested Date\t\t:   {fetched_data[1]}\n")
            self.preview_text.insert(tk.END, f"\tSystem\t\t:   {fetched_data[2]}\n")
            self.preview_text.insert(tk.END, f"\tSerial No.\t\t:   {fetched_data[3]}\n")
            self.preview_text.insert(tk.END, f"\tPart No.\t\t:   {fetched_data[4]}\n")
            self.preview_text.insert(tk.END, f"\tRevision\t\t:   {fetched_data[5]}\n")
            self.preview_text.insert(tk.END, f"\tTested By\t\t:   {fetched_data[6]}\n")
            self.preview_text.insert(tk.END, f"\tResult\t\t:   {fetched_data[7]}\n")
            self.preview_text.insert(tk.END, f"\tComments\t\t:   {fetched_data[9]}\n")
            self.preview_text.insert(tk.END, f"\tReport Link\t\t:   {fetched_data[8]}\n")
            self.preview_text.insert(tk.END, f"________________________________________________________________________________________\n")
            self.preview_text.insert(tk.END, f"________________________________________________________________________________________\n")

            self.preview_text.tag_configure("gray", foreground="#0F148C", font=("Helvetica", 13, "bold"))
            self.preview_text.tag_add("gray", "2.0", "end linestart+1c")
            self.preview_text.config(state=tk.DISABLED)

        except Exception as e:
            self.preview_text.insert(tk.END, f"\n\n\t\t\t\t***NO DATA FOUND***\n\n\n\n")
            self.preview_text.insert(tk.END, f"________________________________________________________________________________________\n")
            self.preview_text.insert(tk.END, f"________________________________________________________________________________________\n")

            if e:
                self.preview_text.tag_configure("colored", foreground="red", font=("Helvetica", 13, "bold"))
                self.preview_text.tag_add("colored", "2.0", "end linestart+1c")

        self.preview_text.tag_configure("thick_border", borderwidth=2, relief="solid")
        self.preview_text.tag_add("thick_border", "1.0", "end")

        if item_text == "Satellite Integration (FM)":
            print("Fm")
            self.tab_satellite_Integration_fm()

        elif item_text == "Satellite Integration (EDM)":
            print("EDM")
            self.tab_satellite_Integration_edm()

    # ====================================================================================
    # ====================================================================================
    # ====================================================================================
    # ====================================================================================
    # ====================================================================================
    def tab_satellite_Integration_fm(self):
        self.sifm = Toplevel(self.root)
        self.sifm.title("Satellite Integration (FM)")
        self.sifm.geometry("931x483+553+275")
        self.sifm.minsize(931, 483)  # Set minimum dimensions
        self.sifm.maxsize(931, 483)  # Set maximum dimensions
        self.sifm.focus_force()
        self.sifm.lift()
        self.sifm.grab_set()  # Disable the main window

        # Create a custom style
        custom_style = ttk.Style()
        custom_style.configure("Custom.TNotebook.Tab", background="white", fg="#0F148C",
                               font=("Helvetica", 10, "bold"), padding=[10, 5])

        self.tab_control = ttk.Notebook(self.sifm, style="Custom.TNotebook", takefocus=False)
        self.tab_control.pack(fill="both", expand=True)

        def populate_tabs():
            self.cur.execute("SELECT DISTINCT Satellite_SN FROM FM_SatelliteIntegration")
            satellite_sns = self.cur.fetchall()

            for satellite_sn in satellite_sns:
                satellite_tab = ttk.Frame(self.tab_control)
                self.tab_control.add(satellite_tab, text=satellite_sn[0], )

                satellite_notebook = ttk.Notebook(satellite_tab)
                satellite_notebook.pack(fill="both", expand=True)

                self.cur.execute("SELECT DISTINCT System FROM FM_SatelliteIntegration WHERE Satellite_SN=?",
                               (satellite_sn[0],))
                systems = self.cur.fetchall()

                for system in systems:
                    system_tab = ttk.Frame(satellite_notebook)
                    satellite_notebook.add(system_tab, text=system[0])

                    self.cur.execute("SELECT Subsystem_SN FROM FM_SatelliteIntegration WHERE Satellite_SN=? AND System=?",
                                   (satellite_sn[0], system[0]))
                    subsystem_sns = self.cur.fetchall()

                    subsystem_frame = ttk.Frame(system_tab)
                    subsystem_frame.place(x=2, y=10, width=160, height=400)
                    # Create an "CLOSE" button

                    for subsystem_sn in subsystem_sns:
                        subsystem_label = ttk.Label(subsystem_frame, text=f"Subsystem: {subsystem_sn[0]}",
                                                    cursor="hand2",
                                                    font=("Arial", 11, "bold"), foreground="red")
                        subsystem_label.bind("<Button-1>",
                                             lambda event, sn=subsystem_sn[0]: self.show_satellite_fm_preview(sn))
                        subsystem_label.pack()

                    self.full_report_button = tk.Button(subsystem_frame, text="Full Report", font=("arial", 9, "bold"),
                                                        relief=RAISED, bd=5, bg="#0F148C", cursor="hand2", fg="white",
                                                         command=self.show_full_report_fm)
                    self.full_report_button.pack(pady=5)

                    self.print_content_btn = tk.Button(subsystem_frame, text="Print", font=("arial", 9, "bold"),
                                                       relief=RAISED, bd=5, bg="#0F148C", cursor="hand2", fg="white",
                                                       width=5, command=self.print_content)
                    self.print_content_btn.pack(pady=5)
                    self.close_sifm_btn = tk.Button(subsystem_frame, text="Close", font=("arial", 9, "bold"),
                                                    relief=RAISED, bd=5, bg="#0F148C", cursor="hand2", fg="white",
                                                    width=5, command=self.close_sifm)
                    self.close_sifm_btn.pack(pady=5)

        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                           database="serialtracking")
        self.cur = self.con.cursor()

        self.fm_preview_text = scrolledtext.ScrolledText(self.sifm, background="#FFF8DC", font=("Arial", 13, "bold"),
                                       wrap=tk.WORD)
        self.fm_preview_text.place(x=165, y=60, width=755, height=405)


        populate_tabs()

    # ====================================================================================

    def close_sifm(self):
        self.sifm.destroy()

    # ====================================================================================

    def show_satellite_fm_preview(self, subsystem_sn):
        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                           database="serialtracking")
        self.cur = self.con.cursor()

        tables = ["FM_SatelliteIntegration", "EDM_SatelliteIntegration"]
        fetched_data = None

        for table_name in tables:
            self.cur.execute(f"SELECT * FROM {table_name} WHERE Subsystem_SN = ?;", (subsystem_sn,))
            fetched_data = self.cur.fetchone()

            if fetched_data:
                break  # Exit the loop once data is fetched

        self.fm_preview_text.config(state=tk.NORMAL)
        self.fm_preview_text.delete(1.0, tk.END)

        if fetched_data:
            self.fm_preview_text.insert(tk.END, f"\t\t\tFetched data for: {subsystem_sn}\n")
            self.fm_preview_text.insert(tk.END,
                                     f"_________________________________________________________________________________\n")
            self.fm_preview_text.insert(tk.END,
                                     f"_________________________________________________________________________________\n\n")

            self.fm_preview_text.tag_configure("header", font=("Helvetica", 17, "bold", "underline"), foreground="#0F148C")
            self.fm_preview_text.tag_add("header", "1.0", "end linestart+1c")

            self.fm_preview_text.insert(tk.END, f"\tTested Date\t\t:   {fetched_data[1]}\n")
            self.fm_preview_text.insert(tk.END, f"\tSatellite SN\t\t:   {fetched_data[2]}\n")
            self.fm_preview_text.insert(tk.END, f"\tSystem\t\t:   {fetched_data[3]}\n")
            self.fm_preview_text.insert(tk.END, f"\tSerial No.\t\t:   {fetched_data[4]}\n")
            self.fm_preview_text.insert(tk.END, f"\tPart No.\t\t:   {fetched_data[5]}\n")
            self.fm_preview_text.insert(tk.END, f"\tRevision\t\t:   {fetched_data[6]}\n")
            self.fm_preview_text.insert(tk.END, f"\tTested By\t\t:   {fetched_data[7]}\n")
            self.fm_preview_text.insert(tk.END, f"\tStatus\t\t:   {fetched_data[8]}\n")
            self.fm_preview_text.insert(tk.END, f"\tComments\t\t:   {fetched_data[10]}\n")
            self.fm_preview_text.insert(tk.END, f"\tReport Link\t\t:   {fetched_data[9]}\n")
            self.fm_preview_text.insert(tk.END,
                                     f"_________________________________________________________________________________\n")
            self.fm_preview_text.insert(tk.END,
                                     f"_________________________________________________________________________________\n")
            self.fm_preview_text.tag_configure("gray", foreground="#0F148C", font=("Helvetica", 13, "bold"))
            self.fm_preview_text.tag_add("gray", "2.0", "end linestart+1c")
        else:
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t\t\tNo data found for Subsystem: {subsystem_sn}\n")
            self.fm_preview_text.insert(tk.END, f"\n\n\t\t\t\t***NO DATA FOUND***\n\n\n\n")
            self.fm_preview_text.insert(tk.END,
                                     f"_________________________________________________________________________________\n")
            self.fm_preview_text.insert(tk.END,
                                     f"_________________________________________________________________________________\n")

            self.fm_preview_text.tag_configure("colored", foreground="red", font=("Helvetica", 13, "bold"))
            self.fm_preview_text.tag_add("colored", "2.0", "end linestart+1c")

        self.fm_preview_text.tag_configure("thick_border", borderwidth=2, relief="solid")
        self.fm_preview_text.tag_add("thick_border", "1.0", "end")
        self.fm_preview_text.config(state=tk.DISABLED)

    # ====================================================================================
    def show_full_report_fm(self):
        selected_tab_index = self.tab_control.index(self.tab_control.select())
        selected_tab = self.tab_control.tabs()[selected_tab_index]
        satellite_sn = self.tab_control.tab(selected_tab, "text")  # Get the text attribute of the selected tab

        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                           database="serialtracking")
        self.cur = self.con.cursor()

        self.cur.execute("SELECT DISTINCT System FROM FM_SatelliteIntegration WHERE Satellite_SN=?", (satellite_sn,))
        systems = self.cur.fetchall()

        self.fm_preview_text.config(state=tk.NORMAL)
        self.fm_preview_text.delete(1.0, tk.END)

        self.fm_preview_text.insert(tk.END, f"\t\tFull Report for SATELLITE SN: {satellite_sn}\n\n")

        self.fm_preview_text.tag_configure("header", font=("Helvetica", 17, "bold", "underline"), foreground="#0F148C")
        self.fm_preview_text.tag_add("header", "1.0", "end linestart+1c")

        self.fm_preview_text.insert(tk.END, "*SYSTEMS:")
        self.fm_preview_text.tag_configure("system", font=("Helvetica", 15, "bold", "underline"), foreground="red")
        self.fm_preview_text.tag_add("system", "2.0", "end linestart+1c")
        self.fm_preview_text.insert(tk.END,
                                 f"________________________________________________________\n")

        for system in systems:
            self.fm_preview_text.insert(tk.END, f"\t*{system[0]}\n")
            self.fm_preview_text.tag_configure("systemheader", font=("Helvetica", 14, "bold", "underline"),
                                               foreground="#0F148C")
            self.fm_preview_text.tag_add("systemheader", "4.0", "end linestart+1c")

            self.cur.execute(
                "SELECT Subsystem_SN, Tested_Date, Tested_By, Status FROM FM_SatelliteIntegration WHERE Satellite_SN=? AND System=?",
                (satellite_sn, system[0]))
            subsystems = self.cur.fetchall()

            for subsystem in subsystems:
                self.fm_preview_text.insert(tk.END, f"\t\tSubsystem SN\t\t: {subsystem[0]}\n")
                self.fm_preview_text.insert(tk.END, f"\t\tTested Date\t\t: {subsystem[1]}\n")
                self.fm_preview_text.insert(tk.END, f"\t\tTested By\t\t: {subsystem[2]}\n")
                self.fm_preview_text.insert(tk.END, f"\t\tStatus\t\t: {subsystem[3]}\n")
                self.fm_preview_text.insert(tk.END, f"{self.ss_serial_detail(subsystem)}\n")
                self.fm_preview_text.insert(tk.END, f"\t\t________________________________________________________________\n")

                self.fm_preview_text.tag_configure("rest", font=("Helvetica", 13, "bold"), foreground="black")
                self.fm_preview_text.tag_add("rest", "6.0", "end")

        self.fm_preview_text.tag_configure("thick_border", borderwidth=2, relief="solid")
        self.fm_preview_text.tag_add("thick_border", "1.0", "end")
        self.fm_preview_text.config(state=tk.DISABLED)

    def ss_serial_detail(self, subsystem):
        self.con = mysql.connector.connect(host="localhost", user="root", password="1223334444@SK",
                                           database="serialtracking")
        self.cur = self.con.cursor()

        tables = ["FM_SubsystemTest", "EDM_SubsystemTest"]
        fetched_data = None

        for table_name in tables:
            self.cur.execute(f"SELECT * FROM {table_name} WHERE Subsystem_SN = ?;", (subsystem[0],))
            fetched_data = self.cur.fetchone()  # Use fetchone to get a single row

            if fetched_data:
                break  # Exit the loop once data is fetched



        if fetched_data:
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Fetched for Subsystem\t\t: {subsystem[0]}\n")
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Tested Date\t\t: {fetched_data[1]}\n")
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Part No.\t\t: {fetched_data[4]}\n")
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Revision\t\t: {fetched_data[5]}\n")
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Tested By\t\t: {fetched_data[6]}\n")
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Result\t\t: {fetched_data[7]}\n")
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Comments\t\t: {fetched_data[9]}\n")
            self.fm_preview_text.insert(tk.END, f"\t\t\t\t       Report Link\t\t: {fetched_data[8]}")
            self.fm_preview_text.tag_configure("rest", font=("Helvetica", 13, "bold"), foreground="red")
            self.fm_preview_text.tag_add("rest", "8.0", "11.0")
        else:
            self.fm_preview_text.insert(tk.END, "\t\t\t\tData not found\n")

    def print_content(self):
        content = self.fm_preview_text.get("1.0", "end-1c")
        printer_name = win32print.GetDefaultPrinter()

        hprinter = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(hprinter, 2)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_name)

        font = win32ui.CreateFont({
            "name": "Arial",
            "height": 12,
            "weight": 400,
        })

        pdc.SelectObject(font)
        pdc.StartDoc(content[:255])
        pdc.StartPage()
        pdc.TextOut(100, 100, content)
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()

        win32print.ClosePrinter(hprinter)

    # ====================================================================================
    # ==========================EDM TAB==========================================
    # ====================================================================================
    # ====================================================================================
    # ====================================================================================
    '''def tab_satellite_Integration_edm(self):
        self.siedm = Toplevel(self.root)
        self.siedm.title("Satellite Integration (FM)")
        self.siedm.geometry("931x483+553+275")
        self.siedm.minsize(931, 483)  # Set minimum dimensions
        self.siedm.maxsize(931, 483)  # Set maximum dimensions
        self.siedm.focus_force()
        self.siedm.lift()
        self.siedm.grab_set()  # Disable the main window

        def populate_tabs():
            cursor.execute("SELECT DISTINCT Satellite_SN FROM EDM_SatelliteIntegration")
            satellite_sns = cursor.fetchall()

            for satellite_sn in satellite_sns:
                satellite_tab = ttk.Frame(tab_control)
                tab_control.add(satellite_tab, text=satellite_sn[0])

                satellite_notebook = ttk.Notebook(satellite_tab)
                satellite_notebook.pack(fill="both", expand=True)

                cursor.execute("SELECT DISTINCT System FROM EDM_SatelliteIntegration WHERE Satellite_SN=?",
                               (satellite_sn[0],))
                systems = cursor.fetchall()

                for system in systems:
                    system_tab = ttk.Frame(satellite_notebook)
                    satellite_notebook.add(system_tab, text=system[0])

                    cursor.execute(
                        "SELECT Subsystem_SN FROM EDM_SatelliteIntegration WHERE Satellite_SN=? AND System=?",
                        (satellite_sn[0], system[0]))
                    subsystem_sns = cursor.fetchall()

                    subsystem_frame = ttk.Frame(system_tab)
                    subsystem_frame.pack()

                    for subsystem_sn in subsystem_sns:
                        subsystem_label = ttk.Label(subsystem_frame, text=f"Subsystem: {subsystem_sn[0]}",
                                                    cursor="hand2",
                                                    font=("Arial", 12, "bold"), foreground="red")
                        subsystem_label.bind("<Button-1>",
                                             lambda event, sn=subsystem_sn[0]: self.show_satellite_edm_preview(sn))
                        subsystem_label.pack()

        # Create a custom style
        custom_style = ttk.Style()
        custom_style.configure("Custom.TNotebook.Tab", background="lightgray", fg="#0F148C",
                               font=("Helvetica", 14, "bold"), padding=[10, 5])

        tab_control = ttk.Notebook(self.siedm, style="Custom.TNotebook")
        tab_control.pack(fill="both", expand=True)

        conn = sqlite3.connect('SerialTracking.db')
        cursor = conn.cursor()

        self.edm_preview_text = tk.Text(self.siedm, background="#FFF8DC",
                                        height=15, width=65, wrap=tk.WORD,)
        self.edm_preview_text.pack()

        populate_tabs()

    # ====================================================================================
    # ====================================================================================
    # ====================================================================================

    def show_satellite_edm_preview(self, subsystem_sn):
        connection = sqlite3.connect('SerialTracking.db')
        cur = connection.cur()

        tables = ["FM_SatelliteIntegration", "EDM_SatelliteIntegration"]
        fetched_data = None

        for table_name in tables:
            cur.execute(f"SELECT * FROM {table_name} WHERE Subsystem_SN = ?;", (subsystem_sn,))
            fetched_data = cur.fetchone()

            if fetched_data:
                break  # Exit the loop once data is fetched

        self.edm_preview_text.config(state=tk.NORMAL)
        self.edm_preview_text.delete(1.0, tk.END)

        if fetched_data:
            self.edm_preview_text.insert(tk.END, f"\t\t\t[[Fetched data for: {subsystem_sn} ]]\n")
            self.edm_preview_text.insert(tk.END,
                                         f" _________________________________________________________________\n")
            self.edm_preview_text.insert(tk.END,
                                         f"||________________________________________________________________||\n")
            self.edm_preview_text.insert(tk.END, f"||\tTested Date\t\t:   {fetched_data[1]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tSystem\t\t:   {fetched_data[2]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tSerial No.\t\t:   {fetched_data[3]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tPart No.\t\t:   {fetched_data[4]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tRevision\t\t:   {fetched_data[5]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tTested By\t\t:   {fetched_data[6]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tResult\t\t:   {fetched_data[7]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tComments\t\t:   {fetched_data[8]}\n")
            self.edm_preview_text.insert(tk.END, f"||\tReport Link\t\t:   {fetched_data[9]}\n")
            self.edm_preview_text.insert(tk.END,
                                         f"||________________________________________________________________\n")
            self.edm_preview_text.insert(tk.END,
                                         f"||________________________________________________________________||\n")
            self.edm_preview_text.tag_configure("gray", foreground="black")
            self.edm_preview_text.tag_add("gray", "1.0", "end-1c linestart+1c")
        else:
            self.edm_preview_text.insert(tk.END, f"\t\t\t\t\t\tNo data found for Subsystem: {subsystem_sn}\n")
            self.edm_preview_text.insert(tk.END, f"||\n\n\t\t\t\t***NO DATA FOUND***\n\n")
            self.edm_preview_text.insert(tk.END,
                                         f" _________________________________________________________________\n")
            self.edm_preview_text.insert(tk.END,
                                         f"||________________________________________________________________||\n")
            self.edm_preview_text.tag_configure("colored", foreground="red", font=("Helvetica", 10, "bold"))
            self.edm_preview_text.tag_add("colored", "1.0", "end-1c linestart+1c lineend")

        self.edm_preview_text.tag_configure("bold", font=("Helvetica", 15, "bold"))
        self.edm_preview_text.tag_add("bold", "1.0", "end")
        self.edm_preview_text.tag_configure("thick_border", borderwidth=2, relief="solid")
        self.edm_preview_text.tag_add("thick_border", "1.0", "end")
        self.edm_preview_text.config(state=tk.DISABLED)'''

    # ====================================================================================

    def close_configmgm(self):
        self.con.close()
        self.enable_button()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = Generate_report_class(root, None)
    root.mainloop()
