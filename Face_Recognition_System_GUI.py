import csv
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import simpledialog

import cv2
import face_recognition
import numpy as np
from PIL import ImageTk, Image

import Constants
import webbrowser


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, SetPassword, ChangeChatID, TelegramInfo, Login, ChangePassword, ForgetPassword, NewUser, Dashboard):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            # print(self.frames)

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # first window frame startpage


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        message = tk.Label(
            self, text="Face Recognition System",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        message.place(x=200, y=20)

        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)

        Display_new = tk.Button(self, text="New User", command=lambda: controller.show_frame(NewUser),
                                fg="white",
                                bg="green",
                                width=20, height=3,
                                activebackground="Red", font=('times', 18, ' bold '))
        Display_new.place(x=600, y=280)

        Display_existing = tk.Button(self, text="Existing User", command=lambda: controller.show_frame(Login),
                                     fg="white",
                                     bg="green", width=20, height=3,
                                     activebackground="Red", font=('times', 18, ' bold '))
        Display_existing.place(x=600, y=480)

        Display_setpass = tk.Button(self, text="Set Password", command=lambda: controller.show_frame(SetPassword),
                                    fg="white",
                                    bg="green", width=20, height=2,
                                    activebackground="Red", font=('times', 18, ' bold '))
        Display_setpass.place(x=230, y=670)

        Display_chat_id = tk.Button(self, text="Change Chat ID", command=lambda: controller.show_frame(ChangeChatID),
                                    fg="white",
                                    bg="green", width=20, height=2,
                                    activebackground="Red", font=('times', 18, ' bold '))
        Display_chat_id.place(x=600, y=670)

        Display_changepass = tk.Button(self, text="Change Password",
                                       command=lambda: controller.show_frame(ChangePassword),
                                       fg="white",
                                       bg="green", width=20, height=2,
                                       activebackground="Red", font=('times', 18, ' bold '))
        Display_changepass.place(x=980, y=670)

        description = tk.Label(self, text="***Requires Telegram Application***", height=3,
                               width=50, font=('times', 15, 'bold'))
        description.place(x=450, y=800)


class NewUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)

        self.message = tk.Label(
            self, text="Add New User",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        self.message.place(x=200, y=20)

        self.lbl_back = tk.Button(self, text="<-Back",
                                  command=lambda: [self.clearUp(), controller.show_frame(StartPage)],
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=75, y=50)

        self.lbl_username = tk.Label(self, text="UserName", width=15, height=2, fg="green",
                                     font=('times', 18, ' bold '))
        self.lbl_username.place(x=430, y=300)

        self.username = tk.Entry(self, width=20, fg="green", font=('times', 18, ' bold '))
        self.username.place(x=670, y=315)

        self.Output = tk.Label(self, text="", height=2,
                               width=50, font=('times', 24, ' bold '))
        self.Output.place(x=220, y=450)

        Display = tk.Button(self, text="Get Started!", command=lambda: self.create_user(), fg="white", bg="green",
                            width=15, height=2,
                            activebackground="Red", font=('times', 18, ' bold '))
        Display.place(x=600, y=700)

    def create_user(self):
        with open("C:/Users/...../passwordfile.csv",
                  'r') as readfile:
            myreader = csv.reader(readfile)
            check_list = []
            for row in myreader:
                check_list.append(row)
            readfile.close()
        try:
            master_pass = check_list[0][0]

            username_entry = self.username.get()
            if len(username_entry) != 0:
                s = simpledialog.askstring("Confirm?", "Enter password to add new user:)")
                if s == master_pass:
                    tkinter.messagebox.showinfo("Success", "Password Verified")
                    self.check_user()
                elif len(master_pass) == 0:
                    tkinter.messagebox.showerror("Failed", "You need to set password first!")
                else:
                    tkinter.messagebox.showerror("Failed", "Password does not match")
            else:
                tkinter.messagebox.showwarning("Warning", "Username can't be empty")
        except:
            tkinter.messagebox.showerror("Error", "You need to set password first")

    def clearUp(self):
        self.Output.config(text="")
        self.username.delete(0, 'end')

    def check_user(self):

        global k
        user_name = self.username.get()
        person_name_lower = user_name.lower()
        if len(self.username.get()) != 0:
            if os.path.isfile('C:/Users/...../Images/{}.jpg'.format(user_name)):
                self.Output.config(text="{}! You are an existing user".format(user_name), fg="red")
            elif os.path.isfile('C:/Users/...../Images/{}.jpg'.format(person_name_lower)):
                self.Output.config(text="{}! You are an existing user".format(person_name_lower), fg="red")
            else:
                self.Output.config(text="")
                unknown_face_count = 0
                unknown_count = 5
                image_path = 'Images'
                images = []
                classNames = []
                myList = os.listdir(image_path)
                for cl in myList:
                    curImg = cv2.imread(f'{image_path}/{cl}')
                    images.append(curImg)
                    classNames.append(os.path.splitext(cl)[0])

                def findEncodings(images):
                    encodeList = []
                    for img in images:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        encode = face_recognition.face_encodings(img)[0]
                        encodeList.append(encode)
                    return encodeList

                encodeListKnown = findEncodings(images)

                cam = cv2.VideoCapture(0)
                c, key = 0, 0
                while_flag = True

                while while_flag:
                    ret, frame = cam.read()
                    original_image = frame
                    imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
                    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                    if len(myList) > 0:
                        facesCurFrame = face_recognition.face_locations(imgS)
                        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                            print(matches, faceDis)
                            matchIndex = np.argmin(faceDis)

                            if faceDis[matchIndex] < 0.50:
                                unknown_face_count = 0
                                name = classNames[matchIndex].upper()
                                y1, x2, y2, x1 = faceLoc
                                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                                cv2.putText(frame, name, (x1, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                            else:
                                # IF UNKNOWN PERSON DETECTED....
                                unknown_face_count += 1

                                if len(facesCurFrame) > 1:
                                    unknown_face_count = 0
                                    break

                                if 5 < unknown_face_count < 11:
                                    c += 1
                                    y1, x2, y2, x1 = faceLoc
                                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

                                    # After 5 Seconds, Image will be captured and stored
                                    if c == unknown_count:
                                        cam.release()
                                        cv2.destroyAllWindows()
                                        img_name = "C:/Users/...../Images/{}.jpg".format(user_name)
                                        cv2.imwrite(img_name, original_image)
                                        self.Output.config(text="Welcome aboard {}".format(user_name), fg="green")
                                        while_flag = False
                                        break
                            if c == unknown_count:
                                break
                    else:
                        facesCurFrame = face_recognition.face_locations(imgS)
                        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                            unknown_face_count += 1
                            # print(unknown_face_count)
                            y1, x2, y2, x1 = faceLoc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

                            if len(facesCurFrame) > 1:
                                unknown_face_count = 0
                                break

                            if 5 < unknown_face_count < 11:
                                c += 1

                                # After 5 Seconds, Image will be captured and stored
                                if c == unknown_count:
                                    cam.release()
                                    cv2.destroyAllWindows()

                                    img_name = "C:/Users/...../Images/{}.jpg".format(user_name)
                                    cv2.imwrite(img_name, original_image)
                                    self.Output.config(text="Welcome aboard {}".format(user_name), fg="green")
                                    while_flag = False
                                    break

                            if c == unknown_count:
                                break

                    cv2.imshow("Detecting {}".format(user_name.upper()), frame)
                    key = cv2.waitKey(1)
                    if key % 256 == 27:  # ESC pressed
                        print("Escape hit, closing...")
                        break

                cam.release()
                cv2.destroyAllWindows()
                if key % 256 == 32:
                    tkinter.messagebox.showinfo("Success", "Now, go back and Login")
        else:
            self.Output.config(text="Please enter the username", fg="red")


class SetPassword(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)

        message = tk.Label(
            self, text="Set Password",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))
        message.place(x=200, y=20)

        def check_password(self):
            def clear_up(self):
                try:
                    self.password.delete(0, 'end')
                except:
                    pass
                try:
                    self.ans.delete(0, 'end')
                except:
                    pass
                try:
                    chat_id_entry.delete(0, 'end')
                except:
                    pass

            self.lbl_back = tk.Button(self, text="<-Back",
                                      command=lambda: [clear_up(self), controller.show_frame(StartPage)],
                                      width=7,
                                      height=1, fg="white", bg="green",
                                      activebackground='red',
                                      font=('times', 15, ' bold '))
            self.lbl_back.place(x=75, y=50)

            with open("C:/Users/...../passwordfile.csv",
                      'r') as readfile:
                myreader = csv.reader(readfile)
                check_list = []

                for row in myreader:
                    check_list.append(row)
                readfile.close()
                print(check_list[0], " : ", len(check_list[0]))
            if len(check_list[0]) != 0:
                self.Output = tk.Label(self, text="", height=2,
                                       width=50, font=('times', 26, ' bold '))
                self.Output.place(x=220, y=350)
                self.Output.config(text="Password is already set!", fg='red')
            else:
                self.lbl_Password = tk.Label(self, text="Enter new Password", width=20, height=2, fg="green",
                                             font=('times', 20, ' bold '))
                self.lbl_Password.place(x=400, y=200)

                self.password = tk.Entry(self, width=20, show='*', fg="green", font=('times', 20, ' bold '))
                self.password.place(x=700, y=215)

                lbl_ans = tk.Label(self, text="Enter your Answer", width=20, height=2, fg="green",
                                   font=('times', 20, ' bold '))
                lbl_ans.place(x=400, y=420)

                self.ans = tk.Entry(self, width=20, fg="green", font=('times', 20, ' bold '))
                self.ans.place(x=700, y=435)

                label_chat_id = tk.Label(self, text="Enter your Chat id", width=20, height=2, fg="green",
                                         font=('times', 20, ' bold '))
                label_chat_id.place(x=400, y=520)

                chat_id_entry = tk.Entry(self, width=20, fg="green", font=('times', 20, ' bold '))
                chat_id_entry.place(x=700, y=535)

                info_btn = tk.Button(self, text="<--Click to know how to get chat id", command=lambda: controller.show_frame(TelegramInfo), fg="white", bg="green",
                                     width=27, height=1,
                                     activebackground="Red", font=('times', 18, ' bold '))
                info_btn.place(x=1030, y=520)

                def check_pass_set():
                    check_list = []
                    with open('C:/Users/...../outputdata.csv', 'r') as outfile:
                        pass_writer = csv.reader(outfile)
                        for row in pass_writer:
                            check_list.append(row)
                        outfile.close()

                def show():
                    # label.config(text=clicked.get())
                    print(clicked.get())
                    question = clicked.get()
                    answer = self.ans.get()
                    security_question = [[question, answer]]
                    print(security_question)
                    new_password = [[self.password.get(), chat_id_entry.get()]]
                    print(new_password)
                    print(len(new_password[0][0]))
                    if len(new_password[0][0]) > 4:
                        if len(answer) > 0:
                            with open('C:/Users/...../passwordfile.csv', 'w') as passfile:
                                pass_writer = csv.writer(passfile)
                                for row in new_password:
                                    pass_writer.writerow(row)
                                passfile.close()
                            with open(
                                    'C:/Users/...../outputdata.csv',
                                    'w') as outfile:
                                mywriter = csv.writer(outfile)
                                for d in security_question:
                                    mywriter.writerow(d)
                                outfile.close()
                            tkinter.messagebox.showinfo("Sucess", "Password set successfully!\nRestart the App again "
                                                                  "to take effect")
                        else:
                            tkinter.messagebox.showwarning("Warning", "Answer field can't be empty")
                    else:
                        tkinter.messagebox.showwarning("warning", "Password too short!")

                # Dropdown menu options
                options = [
                    "What is your favourite car?",
                    "what is your daily routine?",
                    "who is your favourite singer?",
                    "what is your first crush name?"
                ]

                # datatype of menu text
                clicked = tk.StringVar()

                # initial menu text
                clicked.set("What is your favourite car?")

                # Create Dropdown menu
                drop = tk.OptionMenu(self, clicked, *options)
                drop.place(x=730, y=320)

                # Create button, it will change label text
                button = tk.Button(self, text="Done", command=show, fg="white", bg="green",
                                   width=15, height=2,
                                   activebackground="Red", font=('times', 18, ' bold '))
                button.place(x=600, y=715)

        check_password(self)


class ChangeChatID(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_password():
            with open("C:/Users/...../passwordfile.csv",
                      'r') as readfile:
                myreader = csv.reader(readfile)
                check_list = []
                for row in myreader:
                    check_list.append(row)
                readfile.close()
            try:
                master_pass = check_list[0][0]
                new_chat_id = self.new_chatid.get()
                new_pass = [[master_pass, new_chat_id]]

                if len(master_pass) != 0:
                    if master_pass == self.login_cur_pass.get():
                        if len(new_chat_id) != 0:
                            with open('C:/Users/...../passwordfile.csv',
                                      'w') as passfile:
                                pass_writer = csv.writer(passfile)
                                for row in new_pass:
                                    pass_writer.writerow(row)
                                passfile.close()
                                tkinter.messagebox.showinfo("Success", "Chat ID changed Successfully")
                        else:
                            tkinter.messagebox.showwarning("Warning", 'Chat ID field can\'t be empty')
                    else:
                        tkinter.messagebox.showerror("Error", "Password doesn't match")
                else:
                    tkinter.messagebox.showwarning("Warning", 'Password field can\'t be empty')
            except:
                tkinter.messagebox.showerror("Error", "You need to set password first")

        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)

        self.message = tk.Label(
            self, text="Change Chat ID",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        self.message.place(x=200, y=20)

        self.lbl_back = tk.Button(self, text="<-Back",
                                  command=lambda: [self.clearUp(), controller.show_frame(StartPage)],
                                  width=7,
                                  height=1, activebackground="Red", fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=75, y=50)

        self.lbl_cur_pass = tk.Label(self, text="Enter current password", width=20, height=2, fg="green",
                                     font=('times', 20, ' bold '))
        self.lbl_cur_pass.place(x=385, y=250)

        self.login_cur_pass = tk.Entry(self, width=20, show='*', fg="green", font=('times', 20, ' bold '))
        self.login_cur_pass.place(x=700, y=265)

        self.lbl_new_chatid = tk.Label(self, text="Enter new Chat ID", width=20, height=2, fg="green",
                                         font=('times', 20, ' bold '))
        self.lbl_new_chatid.place(x=400, y=330)

        self.new_chatid = tk.Entry(self, width=20, fg="green", font=('times', 20, ' bold '))
        self.new_chatid.place(x=700, y=345)

        button = tk.Button(self, text="Done", command=check_password, fg="white", bg="green",
                           width=15, height=2,
                           activebackground="Red", font=('times', 18, ' bold '))
        button.place(x=600, y=615)

    def clearUp(self):
        self.new_chatid.delete(0, 'end')
        self.login_cur_pass.delete(0, 'end')


class TelegramInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.message = tk.Label(
            self, text="Telegram Chat ID",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        self.message.place(x=200, y=20)

        self.lbl_exit = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_exit.place(x=1315, y=50)

        self.lbl_back = tk.Button(self, text="<-Back",
                                  command=lambda: controller.show_frame(SetPassword),
                                  width=7,
                                  height=1, activebackground="Red", fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=75, y=50)

        self.Output = tk.Label(self, text="Chat ID is always unique to each and every Telegram user\n"
                               "So, navigate to the Telegram's \"IDBot\" by clicking the link\n"
                               " provided below. Then follow the steps given in the Bot to get\n"
                               " your Chat ID. It will look something like this - \"987654321\"", font=('Helvetica', 20, ' bold '))
        self.Output.place(x=380, y=200)

        link1 = tk.Label(self, text="Click here to get Chat ID", width=25, height=2, font=('Helvetica', 20, ' bold '), fg="blue", cursor="hand2")
        link1.place(x=520, y=420)
        link1.bind("<Button-1>", lambda e: callback("https://web.telegram.org/#/im?p=@myidbot"))

        self.mob = tk.Label(self, text="Otherwise, you can simply search \"IDBot\" in Telegram app on your phone", font=('Helvetica', 20, ' bold '))
        self.mob.place(x=290, y=600)

        def callback(url):
            webbrowser.open_new(url)


class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)

        self.message = tk.Label(
            self, text="Login",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        self.message.place(x=200, y=20)

        self.lbl_back = tk.Button(self, text="<-Back",
                                  command=lambda: [self.clearUp(), controller.show_frame(StartPage)],
                                  width=7,
                                  height=1, activebackground="Red", fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=75, y=50)

        def check_password():
            with open("C:/Users/...../passwordfile.csv",
                      'r') as readfile:
                myreader = csv.reader(readfile)
                check_list = []
                for row in myreader:
                    check_list.append(row)
                readfile.close()
            try:
                master_pass = check_list[0][0]

                if len(master_pass) != 0:
                    if master_pass == self.login_cur_pass.get():
                        if Constants.login_count == 0:
                            button.destroy()
                            Constants.login_count += 1
                            print("Constants.login_count : ", Constants.login_count)
                            self.ver_button = tk.Button(self, text="Verified! Click Me",
                                                        command=lambda: controller.show_frame(Dashboard), fg="white",
                                                        bg="green",
                                                        width=15, height=3,
                                                        activebackground="Red", font=('times', 17, ' bold '))
                            self.ver_button.place(x=600, y=615)
                        else:
                            tk.Frame(self, command=controller.show_frame(Dashboard))
                    else:
                        tkinter.messagebox.showerror("Error", "Password doesn't match")
                else:
                    tkinter.messagebox.showwarning("Warning", 'Password field can\'t be empty')
            except:
                tkinter.messagebox.showerror("Error", "You need to set password first")

        self.message = tk.Label(
            self, text="Login",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        self.message.place(x=200, y=20)

        self.lbl_back = tk.Button(self, text="<-Back",
                                  command=lambda: [self.clearUp(), controller.show_frame(StartPage)],
                                  width=7,
                                  height=1, activebackground="Red", fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=75, y=50)

        self.lbl_cur_pass = tk.Label(self, text="Enter password", width=20, height=2, fg="green",
                                     font=('times', 20, ' bold '))
        self.lbl_cur_pass.place(x=370, y=250)

        self.login_cur_pass = tk.Entry(self, width=20, show='*', fg="green", font=('times', 20, ' bold '))
        self.login_cur_pass.place(x=670, y=265)

        button = tk.Button(self, text="Done", command=check_password, fg="white", bg="green",
                           width=15, height=2,
                           activebackground="Red", font=('times', 18, ' bold '))
        button.place(x=600, y=615)

    def clearUp(self):
        self.login_cur_pass.delete(0, 'end')


class ChangePassword(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.message = tk.Label(
            self, text="Change Password",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        self.message.place(x=200, y=20)

        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)

        self.lbl_back = tk.Button(self, text="<-Back",
                                  command=lambda: [self.clearUp(), controller.show_frame(StartPage)],
                                  width=7,
                                  height=1, activebackground="Red", fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=75, y=50)

        self.lbl_cur_pass = tk.Label(self, text="Enter current password", width=20, height=2, fg="green",
                                     font=('times', 20, ' bold '))
        self.lbl_cur_pass.place(x=385, y=250)

        self.login_cur_pass = tk.Entry(self, width=20, show='*', fg="green", font=('times', 20, ' bold '))
        self.login_cur_pass.place(x=700, y=265)

        self.lbl_new_Password = tk.Label(self, text="Enter new Password", width=20, height=2, fg="green",
                                         font=('times', 20, ' bold '))
        self.lbl_new_Password.place(x=400, y=330)

        self.login_new_password = tk.Entry(self, width=20, show='*', fg="green", font=('times', 20, ' bold '))
        self.login_new_password.place(x=700, y=345)

        self.reenter_new_Password = tk.Label(self, text="Re-enter new Password", width=20, height=2, fg="green",
                                             font=('times', 20, ' bold '))
        self.reenter_new_Password.place(x=400, y=410)

        self.btnreenter_new_password = tk.Entry(self, width=20, show='*', fg="green", font=('times', 20, ' bold '))
        self.btnreenter_new_password.place(x=700, y=425)

        self.Output = tk.Label(self, text="", height=2,
                               width=50, font=('times', 20, ' bold '))
        self.Output.place(x=420, y=500)

        forget_btn = tk.Button(self, text="Forget Password", command=lambda: controller.show_frame(ForgetPassword),
                               fg="white", bg="green",
                               width=20, height=2,
                               activebackground="Red", font=('times', 20, ' bold '))
        forget_btn.place(x=400, y=600)

        reset_btn = tk.Button(self, text="Reset Password", command=lambda: self.reset_pass(), fg="white", bg="green",
                              width=20, height=2,
                              activebackground="Red", font=('times', 20, ' bold '))
        reset_btn.place(x=800, y=600)

    def clearUp(self):
        self.login_cur_pass.delete(0, 'end')
        self.login_new_password.delete(0, 'end')
        self.btnreenter_new_password.delete(0, 'end')

    def reset_pass(self):
        curr_pass = self.login_cur_pass.get()
        new_pass = self.login_new_password.get()
        re_pass = self.btnreenter_new_password.get()
        with open("C:/Users/...../passwordfile.csv",
                  'r') as readfile:
            myreader = csv.reader(readfile)
            check_list = []
            for row in myreader:
                check_list.append(row)
            readfile.close()
        try:
            master_pass = check_list[0][0]

            if len(curr_pass) == 0:
                if len(new_pass) == 0:
                    if len(re_pass) == 0:
                        if curr_pass == master_pass:
                            if new_pass == re_pass:
                                new_pass = [[new_pass]]
                                try:
                                    with open('C:/Users/...../passwordfile.csv',
                                              'w') as passfile:
                                        pass_writer = csv.writer(passfile)
                                        for row in new_pass:
                                            pass_writer.writerow(row)
                                        passfile.close()
                                        tkinter.messagebox.showinfo("Success", "Password changed successfully")
                                except:
                                    tkinter.messagebox.showerror("Error", "Something not right, try again later:(")
                            else:
                                tkinter.messagebox.showerror("Error", "Re-entered password does not match")
                        else:
                            tkinter.messagebox.showerror("Error", "Current Password does not match")
                    else:
                        tkinter.messagebox.showerror("Error", "Re-enter password field can't be empty")
                else:
                    tkinter.messagebox.showerror("Error", "New password field can't be empty")
            else:
                tkinter.messagebox.showerror("Error", "Current password field can't be empty")
        except:
            tkinter.messagebox.showerror("Error", "You need to set password first")


class ForgetPassword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)
        self.message = tk.Label(
            self, text="Forget Password",
            bg="green", fg="white", width=45,
            height=3, font=('times', 30, 'bold'))

        self.message.place(x=200, y=20)

        self.lbl_back = tk.Button(self, text="<-Back",
                                  command=lambda: [self.clearUp(), controller.show_frame(ChangePassword)],
                                  width=7,
                                  height=1, activebackground="Red", fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=75, y=50)

        self.lbl_new_Password = tk.Label(self, text="Enter new Password", width=20, height=2, fg="green",
                                         font=('times', 20, ' bold '))
        self.lbl_new_Password.place(x=400, y=250)

        self.login_new_password = tk.Entry(self, width=20, show='*', fg="green", font=('times', 20, ' bold '))
        self.login_new_password.place(x=700, y=265)

        def show():
            check_list = []
            with open('C:/Users/...../outputdata.csv',
                      'r') as outfile:
                pass_writer = csv.reader(outfile)
                for row in pass_writer:
                    check_list.append(row)
                outfile.close()
            try:
                master_pass = check_list[0][0]
                print(master_pass)
                question = clicked.get()
                answer = self.ans.get()
                new_pass = [[self.login_new_password.get()]]
                security_question = [[question, answer], []]
                print(security_question)
                with open('C:/Users/...../outputdata.csv',
                          'r') as outfile:
                    my_reader = csv.reader(outfile)
                    check_list = []
                    for d in my_reader:
                        check_list.append(d)
                    outfile.close()
                if len(new_pass) > 3:
                    if check_list == security_question:
                        with open(
                                'C:/Users/...../passwordfile.csv',
                                'w') as passfile:
                            pass_writer = csv.writer(passfile)
                            for row in new_pass:
                                pass_writer.writerow(row)
                            passfile.close()
                        tkinter.messagebox.showinfo("Success", "Password changed!")
                    else:
                        tkinter.messagebox.showerror("Error", "Please check your security question and answer:(")
                else:
                    tkinter.messagebox.showwarning("Failed", "Password too short!")
            except:
                tkinter.messagebox.showerror("Error", "You need to set password first!")

        # Dropdown menu options
        options = [
            "What is your favourite car?",
            "what is your daily routine?",
            "who is your favourite singer?",
            "what is your first crush name?"
        ]
        # datatype of menu text
        clicked = tk.StringVar()

        # initial menu text
        clicked.set("What is your favourite car?")

        # Create Dropdown menu
        drop = tk.OptionMenu(self, clicked, *options)
        drop.place(x=600, y=350)

        lbl_ans = tk.Label(self, text="Answer", width=20, height=2, fg="green",
                           font=('times', 20, ' bold '))
        lbl_ans.place(x=450, y=450)

        self.ans = tk.Entry(self, width=20, fg="green", font=('times', 20, ' bold '))
        self.ans.place(x=700, y=465)

        # Create button, it will change label text
        button = tk.Button(self, text="Done", command=show, fg="white", bg="green",
                           width=15, height=2,
                           activebackground="Red", font=('times', 20, ' bold '))
        button.place(x=600, y=615)

    def clearUp(self):
        self.login_new_password.delete(0, 'end')
        self.ans.delete(0, 'end')


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl_back = tk.Button(self, text="Exit",
                                  command=lambda: exit(),
                                  width=7,
                                  height=1, fg="white", bg="green",
                                  font=('times', 15, ' bold '))
        self.lbl_back.place(x=1315, y=50)
        self.k = ""

        self.dashboard = tk.Label(self, text="Dashboard",
                                  bg="green", fg="white", width=45,
                                  height=2, font=('times', 30, 'bold'))
        self.dashboard.place(x=200, y=10)

        self.listbox = tk.Listbox(self, bd=2, height=15, width=25, font=('times', 20), activestyle='dotbox')
        self.listbox.place(x=100, y=125)

        self.delete = tk.Button(self, command=lambda: get_password(), text="Delete", fg="white", bg="green",
                                width=10, height=2,
                                activebackground="Red", font=('times', 15, ' bold '))
        self.delete.place(x=700, y=700)

        self.back = tk.Button(self, text="<-Back", command=lambda: controller.show_frame(StartPage), width=7,
                              height=1, fg="white", bg="green",
                              font=('times', 15, ' bold '))
        self.back.place(x=75, y=50)

        self.refresh = tk.Button(self, command=lambda: refresh(), text="Refresh", fg="white",
                                 bg="green",
                                 width=10, height=2,
                                 activebackground="Red", font=('times', 15, ' bold '))
        self.refresh.place(x=1000, y=700)

        def get_password():
            s = simpledialog.askstring("Confirm?", "Enter password to delete")
            print(s)
            with open("C:/Users/...../passwordfile.csv",
                      'r') as readfile:
                myreader = csv.reader(readfile)
                check_list = []
                for row in myreader:
                    check_list.append(row)
                readfile.close()
            master_pass = check_list[0][0]

            if master_pass == s:
                deleteImage()
            else:
                tkinter.messagebox.showinfo('Warning!', 'Incorrect password')

        def insertList():
            self.file_list = os.listdir(self.path)
            for item in self.file_list:
                print(item, "2")
                item = list(item.split('.'))
                self.listbox.insert(tk.END, item[0])

        def showcontents(event):
            self.canvas = tk.Canvas(self, width=1000, height=500)
            self.canvas.place(x=600, y=125)
            self.x = self.listbox.curselection()[0]
            file = self.path + self.listbox.get(self.x) + ".jpg"
            self.k = file
            self.img = ImageTk.PhotoImage(Image.open(file))
            self.canvas.create_image(10, 10, anchor=tk.NW, image=self.img)

        def refresh():
            self.listbox.delete(0, tk.END)
            self.path_name = "C:/Users/...../Images/"
            self.file_name = os.listdir(self.path_name)
            for i in self.file_name:
                print(i, "3")
                i = list(i.split('.'))
                self.listbox.insert(tk.END, i[0])

        def existing_refresh():
            self.path = "C:/Users/...../Images/"

        def deleteImage():
            print(self.k)
            split_image_Name = list(self.k.split('/'))
            print(split_image_Name[len(split_image_Name) - 1])

            def destroy_canvas():
                self.canvas.destroy()
                return 0

            if os.path.isfile(self.k):
                os.remove(self.k)
                tkinter.messagebox.showinfo('Removed!', 'Successfully Removed!')
                self.listbox.delete(0, tk.END)
                destroy_canvas()
                insertList()
            else:
                tkinter.messagebox.showerror('Error!', 'File not found!')

        self.listbox.bind("<<ListboxSelect>>", showcontents)

        existing_refresh()
        insertList()


app = tkinterApp()
app.title("")
app.geometry("1280x800")
# app.state('zoomed')
app.attributes("-fullscreen", "True")
app.mainloop()
