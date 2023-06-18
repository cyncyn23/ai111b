import os.path
import datetime
import pickle

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

#Function of button / msg_box / label / recognize 
import util    


class App:
    def __init__(self):
        self.main_window = tk.Tk()  #主視窗
        self.main_window.geometry("1200x520+350+100")   #視窗大小

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'skyblue', self.login)   #login button
        self.login_button_main_window.place(x=750, y=200)   #button location

        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'pink', self.logout)   #logout button
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')     #register button
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)    #webcam label
        self.webcam_label.place(x=10, y=0, width=700, height=500)  

        self.add_webcam(self.webcam_label)      #add webcam to label(opencv)

        self.db_dir = './db'            #用戶資料夾
        if not os.path.exists(self.db_dir):     #if create new folder
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'     #登陸動態存取

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:      #if created
            self.cap = cv2.VideoCapture(0)  #0 for windos sys

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame    #recent capture frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)    #PIL
        self.most_recent_capture_pil = Image.fromarray(img_)    #轉換格式
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk   #put frame in label
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)      #每20ms 獲取一禎(連續)

    def login(self):

        name = util.recognize(self.most_recent_capture_arr, self.db_dir)    #db_dir 存放已登錄用戶資料

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                f.close()


    def logout(self):


        name = util.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Hasta la vista !', 'Goodbye, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},out\n'.format(name, datetime.datetime.now()))
                f.close()



    def register_new_user(self):        #register 視窗
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'skyblue', self.accept_register_new_user)    #accept button
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'pink', self.try_again_register_new_user)      #tryagain button
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)  #new windows
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)   #img label

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)      #blank to enter text(username)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()     #back to main windows

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()    #捕獲新用戶

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):     #get user enter text 
        name = self.entry_text_register_new_user.get(1.0, "end-1c")     #format

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')      #保存圖像
        pickle.dump(embeddings, file)

        util.msg_box('Success!', 'User was registered successfully !')  #視窗-創建新用戶成功

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
