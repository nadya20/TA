#!/usr/bin/python

import Tkinter as tk
from PIL import ImageTk, Image
import os
import threading
from pages import *

file_dir = os.path.dirname(os.path.abspath(__file__))

class AppState(object):
    def __init__(self):
        self.lecture_name = "Alif"
        self.lecture_nip = "1000111100"
        self.lecture_course = "CS012"

        self.student_nim = "1103132163"
        self.student_course = "CS012"
        self.student_presence = "90%"

        self.total_student = "10"

class App(object):
    def __init__(self):

        self.state = AppState()

        # window setup
        self.window = tk.Tk()
        self.window.title("TA Nadya")
        self.window.geometry("800x480")
        self.window.resizable(0,0)

        self.create_pages()
        self.page_main.lift() # select first page

        self.worker = threading.Thread(target=self.process_card)
        self.worker.start()

    def process_card(self):
        print 1000

    def create_pages(self):
        # page main
        self.page_main = MainPage(self.window, file_dir+"/logo_telu.jpg", self.handle_click)
        self.page_main.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # failed page
        self.page_failed = FailedPage(self.window, file_dir+"/cross.jpg")
        self.page_failed.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # success page
        self.page_success = SuccessPage(self.window, file_dir+"/check.jpg")
        self.page_success.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # lecture page
        self.page_lecture = LecturePage(self.window)
        self.page_lecture.setData(self.state.lecture_name, self.state.lecture_nip, self.state.lecture_course)
        self.page_lecture.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # student page
        self.page_student = StudentPage(self.window)
        self.page_student.setData(self.state.student_nim, self.state.student_course, self.state.student_presence)
        self.page_student.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # submit page
        self.page_submit = SubmitPage(self.window)
        self.page_submit.setData(self.state.lecture_course, self.state.total_student)
        self.page_submit.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)        

    def switch(self, page):
        page.lift()

    def handle_click(self, source):
        pass


# main loop
app = App()
app.window.mainloop()