import os
import smtplib  # pip install secure-smtplib
import mysql.connector
import sys
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox
# from PIL import Image
# from PIL import ImageTk
import email_pass


def resource_path(relative_path):
    """ GET absolute path to resource, works for dev and for PyInstaller"""

    try:
        # PyInstaller creates a tempo folder and sites path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class login_class:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x770+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # Construct the path to the image file
        # self.image_path = "images/sky2.jpg"

        # ==========================TITLE FRAME===============================================================
        title_frame = Frame(self.root, bd=6, bg="#63B8FF", relief=GROOVE)
        title_frame.pack(side=TOP, fill=X)

        # self.title_image = Image.open(resource_path(self.image_path))
        # self.title_image = self.title_image.resize((200, 55))
        # self.icon_title = ImageTk.PhotoImage(self.title_image)

        # Label(title_frame, image=self.icon_title).grid(row=0, column=0, padx=50, pady=6)
        Label(title_frame).grid(row=0, column=0, padx=50, pady=6)
        Label(title_frame, text="Inventory Management System",
              font=("times new roman", 35, "bold"), bg="#63B8FF", anchor='w',
              fg="white").place(x=450, y=10)

        Button(title_frame, text="Exit", font=("arial", 15, "bold"), bg="#0F148C", cursor="hand2", relief=RAISED,
               fg="white", bd=8, command=self.close).place(x=1350, y=10, width=100, height=50)

        # ===========================WELCOME FRAME========================================================
        self.frame_date = datetime.now().strftime("%d/%m/%Y")
        self.frame_time = datetime.now().strftime("%H:%M:%S")

        welcome_frame = Frame(self.root, bd=0, bg="white", height=45)
        welcome_frame.pack(side=TOP, padx=7, fill=X)

        # clock
        self.lbl_clock = Label(welcome_frame,
                               text="Welcome to Inventory Management System\t Date:DD-MM-YYY\t Time:HH:MM:SS",
                               font=("arial", 15, "bold"), bg="green", fg="white", justify=CENTER, )
        self.lbl_clock.place(x=0, y=0, relwidth=1, height=45)
        self.lbl_clock.config(
            text=f"Welcome to Inventory Management System\t Date: {self.frame_date} \t Time: {self.frame_time} ")

        # ==================================TITLE FRAME ===============================================================
        image_frame = Frame(self.root, bd=5, bg="#191970", relief=GROOVE)
        image_frame.place(x=5, y=130, width=1000, height=635)
        # self.image_path2 = "images/sky1.jpg"

        # self.title_image2 = Image.open(self.image_path2)
        # self.title_image2 = self.title_image2.resize((1000, 645))
        # self.icon_title2 = ImageTk.PhotoImage(self.title_image2)

        # self.title = Label(image_frame, image=self.icon_title2, width=960, height=650)
        self.title = Label(image_frame, width=960, height=650)
        self.title.pack(side=LEFT, fill=BOTH)
        # place(x=20, y=40, width=1000, height=700)

        # ============================VARIABLE===================================================================

        self.var_otp = ''
        # ============================VARIABLE===================================================================

        self.var_username = StringVar()
        self.var_password = StringVar()

        # ==================================Frame 1================================================================

        details_frame = Frame(self.root, bd=15, relief=GROOVE, bg="#63B8FF", width=500, height=600)
        details_frame.place(x=970, y=130, width=530, height=635)

        signin_label = Label(details_frame, text="SIGN IN", font=("times new roman", 40, "bold"), bg="#63B8FF",
                             fg="black", justify=CENTER)
        signin_label.place(x=110, y=40, width=270, height=100)

        # ==================================USERNAME LABELS AND ENTRY=================================================
        username_label = Label(details_frame, text="Username:", font=("arial", 13, "bold"),
                               bg="#63B8FF", fg="black", anchor='w')
        username_label.place(x=100, y=150, width=100, height=40)

        username_entry = Entry(details_frame, font=("arial", 13, "bold"),
                               bd=3, bg="#FFE7BA", relief=GROOVE, width=80, textvariable=self.var_username)
        username_entry.place(x=100, y=190, width=280, height=40)

        # ==================================PASSWORD LABELS AND ENTRY=================================================
        password_label = Label(details_frame, text="Password:", font=("arial", 13, "bold"),
                               bg="#63B8FF", fg="black", anchor='w')
        password_label.place(x=100, y=240, width=100, height=40)
        password_entry = Entry(details_frame, font=("arial", 13, "bold"),
                               bd=3, bg="#FFE7BA", relief=GROOVE, width=80, show="*", textvariable=self.var_password)
        password_entry.place(x=100, y=280, width=280, height=40)

        login_button = Button(details_frame, text="Log In", font=("arial", 13, "bold"), command=self.login,
                              fg="black", justify=CENTER, bd=5, relief=GROOVE, compound=LEFT)
        login_button.place(x=200, y=370, width=80, height=35)

        forget_button = Button(details_frame, text="Forget Password?", font=("arial", 13, "bold"),
                               command=self.forget_window,
                               fg="red", justify=CENTER, bd=5)
        forget_button.place(x=145, y=450, width=200, height=35)

        # ==================================MY SQL CONNECTION=================================================
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1223334444@SK",
            database="suppliers"
        )

        self.cur = self.con.cursor()

    # ==================================login Method=================================================

    def login(self):
        try:
            if self.var_username.get() == "" or self.var_password.get() == "":
                messagebox.showerror("Error", "All field are required", parent=self.root)
            else:
                self.cur.execute(f"SELECT * FROM login WHERE username=%s AND password=%s",
                                 (self.var_username.get(), self.var_password.get(),))
                user = self.cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
                else:
                    self.root.destroy()
                    os.system("python dashboard.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # ====================================SHOW FUNCTION =======================================================

    def forget_window(self):
        try:
            if self.var_username.get() == "":
                messagebox.showerror("Error", "Username is required", parent=self.root)
            else:
                self.cur.execute("SELECT email FROM login WHERE username=%s", (self.var_username.get(),))
                email = self.cur.fetchone()
                if email is None:
                    messagebox.showerror("Error", "Invalid User, try again", parent=self.root)
                else:
                    ####====================VARIABLES======================================

                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_confirm_pass = StringVar()

                    # call send_email_function()
                    chk = self.send_email(email[0])
                    if chk == 'f':
                        messagebox.showerror("Error", "Connection Error,try again", parent=self.root)
                    else:
                        # call send email_function
                        self.forget_win = Toplevel(self.root)
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('500x450+500+200')
                        self.forget_win.focus_force()

                        forget_password_label = Label(self.forget_win, text="Forget Password",
                                                      font=("arial", 16, "bold"),
                                                      bg="#63B8FF", fg="black", justify=CENTER)
                        forget_password_label.pack(side=TOP, fill=X)

                        otp_label = Label(self.forget_win, text="Enter OTP Sent on Registered Email",
                                          font=("arial", 13, "bold"),
                                          anchor='w', fg="black", justify=LEFT)
                        otp_label.place(x=25, y=70, width=300, height=30)

                        otp_entry = Entry(self.forget_win, font=("arial", 13, "bold"),
                                          bd=2, bg="#FFE7BA", relief=RIDGE, width=200, textvariable=self.var_otp)
                        otp_entry.place(x=25, y=100, width=300, height=40)

                        self.confirm_button = Button(self.forget_win, text="Confirm", font=("arial", 13, "bold")
                                                     , bg="#63B8FF", fg="black", justify=CENTER, compound=RIGHT,
                                                     cursor='hand2', command=self.validate_otp)
                        self.confirm_button.place(x=380, y=100, width=100, height=40)

                        ##################################

                        newPass_label = Label(self.forget_win, text="New Password", font=("arial", 13, "bold"),
                                              fg="black", justify=LEFT, anchor='w')
                        newPass_label.place(x=25, y=170, width=200, height=40)

                        newPass_entry = Entry(self.forget_win, font=("arial", 13, "bold"),
                                              bd=2, bg="#FFE7BA", relief=RIDGE, width=200,
                                              textvariable=self.var_new_pass)
                        newPass_entry.place(x=25, y=200, width=200, height=40)

                        ##################################
                        confirmpass_lbl = Label(self.forget_win, text="Confirm Password", font=("arial", 13, "bold"),
                                                fg="black", justify=LEFT, anchor='w')
                        confirmpass_lbl.place(x=25, y=245, width=200, height=40)

                        confirmpass_entry = Entry(self.forget_win, font=("arial", 13, "bold"),
                                                  bd=2, bg="#FFE7BA", relief=RIDGE, width=200,
                                                  textvariable=self.var_confirm_pass)
                        confirmpass_entry.place(x=25, y=275, width=200, height=40)
                        ##################################

                        self.submit_button = Button(self.forget_win, text="Submit", font=("arial", 13, "bold")
                                                    , bg="#63B8FF", fg="black", justify=CENTER, compound=LEFT,
                                                    command=self.update_password, cursor='hand2')
                        self.submit_button.place(x=200, y=355, width=100, height=45)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def send_email(self, to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)  # port number
        s.starttls()  # encript all emails, secure
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_, pass_)

        self.otp = int(time.strftime("%H%M%S")) + int(time.strftime("%S"))
        print(self.otp)

        subj = 'IMS-Reset Password OTP'
        msg = f'Dear Sir/Madam, \n\nYours Reset OTP is {str(self.otp)}. \n\n With Regards, \n IMS Team'
        msg = "Subject: {}\n\n{}".format(subj, msg)
        s.sendmail(email_, to_, msg)
        chk = s.ehlo()
        if chk[0] == 250:
            return 's'
        else:
            return 'f'

    def update_password(self):
        if self.var_new_pass.get() == "" or self.var_confirm_pass.get() == "":
            messagebox.showerror("Error", "Password is required", parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_confirm_pass.get():
            messagebox.showerror("Error", "Password & Confirm Password should be same", parent=self.forget_win)
        else:
            try:
                self.cur.execute("Update login SET password=%s WHERE username=%s",
                                 (self.var_new_pass.get(), self.var_username.get()))
                self.con.commit()
                messagebox.showinfo("Success", "Password updated Successfully", parent=self.forget_win)
                self.forget_win.destroy()

            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def validate_otp(self):
        if int(self.otp) == int(self.var_otp.get()):
            self.submit_button.config(state=NORMAL)
            self.confirm_button.config(state=DISABLED)

        else:
            messagebox.showerror("Error", "Invalid OTP,try again", parent=self.forget_win)

    def close(self):
        self.con.close()  # Close the MySQL connection
        self.root.destroy()
        os.system("dashboard.py")


if __name__ == "__main__":
    root = Tk()
    obj = login_class(root)
    root.mainloop()
