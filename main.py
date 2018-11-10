#!/usr/bin/python

import Tkinter as tk
from PIL import ImageTk, Image
import os
import threading
import time
from pages import *
import MyReader

file_dir = os.path.dirname(os.path.abspath(__file__))

LECTURE = "lecture"
STUDENT = "student"

class AppState(object):
    def __init__(self):
        self.lecture = None
        self.student = None
        self.student_course_index = -1
        self.total_student = 0

        self.wait_for = LECTURE
    
    def reset(self):
        self.lecture = None
        self.student = None
        self.student_course_index = -1
        self.total_student = 0

        self.wait_for = LECTURE
    
    def __repr__(self):
        return str(self.lecture) + "\n" + str(self.student) + "\n" + str(self.student_course_index) + "\n" + self.wait_for

class App(object):
    def __init__(self):

        self.state = AppState()

        # window setup
        self.window = tk.Tk()
        self.window.title("TA Nadya")
        self.window.geometry("800x480")
        self.window.resizable(0,0)

        self.create_pages()
        self.check_for_state_change(True)

    def process_card(self):
        if self.state.wait_for == LECTURE:
            isLecture, result = MyReader.isLecture() # blocking process
            if isLecture: self.state.lecture = result
        elif self.state.wait_for == STUDENT:
            isStudent, result = MyReader.isStudent() # blocking process
            if isStudent: 
                isMatch, idx = MyReader.confirmCourseMatch(self.state.lecture, result)
                if isMatch:
                    self.state.student = result
                    self.state.student_course_index = idx
                    self.state.total_student += 1
        else:
            # stop
            print "Exit App"

        self.check_for_state_change()
        # self.window.after(100, lambda: self.check_for_state_change())

    def create_pages(self):
        # page main
        self.page_main = MainPage(self.window, file_dir+"/logo_telu.jpg", self.handle_click)
        self.page_main.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)
        # self.page_main.toggle_button()

        # failed page
        self.page_failed = FailedPage(self.window, file_dir+"/cross.jpg")
        self.page_failed.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # success page
        self.page_success = SuccessPage(self.window, file_dir+"/check.jpg")
        self.page_success.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # lecture page
        self.page_lecture = LecturePage(self.window)
        self.page_lecture.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # student page
        self.page_student = StudentPage(self.window)
        self.page_student.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)

        # submit page
        self.page_submit = SubmitPage(self.window, self.handle_click)
        self.page_submit.place(in_=self.window, x=0, y=0, relwidth=1, relheight=1)        

    def switch(self, page):
        page.show()

    def check_for_state_change(self, first_time = False):
        print self.state
        if not first_time:
            if self.state.wait_for == LECTURE and self.state.lecture is not None:
                self.switch(self.page_success)
                self.page_lecture.setData(self.state.lecture.name, self.state.lecture.id, self.state.lecture.subject)
                time.sleep(5)
                self.switch(self.page_lecture)
                time.sleep(5)
                self.switch(self.page_main)
                self.state.wait_for = STUDENT

            elif self.state.wait_for == LECTURE and self.state.lecture is None:
                self.switch(self.page_failed)
                time.sleep(5)
                self.switch(self.page_main)

            elif self.state.wait_for == STUDENT and self.state.student is not None:
                self.page_student.setData(self.state.student.id, self.state.student.courses, self.state.student_course_index)
                print "add attendance to card is success:", MyReader.addStudentAttendance(self.state.student, self.state.student_course_index)
                
                self.switch(self.page_success)
                time.sleep(5)

                self.switch(self.page_student)
                time.sleep(5)

                self.switch(self.page_main)

            elif self.state.wait_for == STUDENT and self.state.student is None:
                self.switch(self.page_failed)
                time.sleep(5)
                self.switch(self.page_main)
                self.state.student = None

            if self.state.lecture is not None:
                self.page_submit.setData(self.state.lecture.subject, self.state.total_student)

        self.worker = threading.Thread(target=self.process_card)
        self.worker.start()

    def handle_click(self, source):
        if isinstance(source, MainPage):
            self.switch(self.page_submit)
        else:
            # TODO : Store data
            self.state.reset()
            self.switch(self.page_main)


# main loop
app = App()
app.switch(app.page_main) # select first page
app.window.mainloop()