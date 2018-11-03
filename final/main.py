#!/usr/bin/python

import Tkinter as tk
from PIL import ImageTk, Image
import os

file_dir = os.path.dirname(os.path.abspath(__file__))

# region state
lecture_name = "Alif"
lecture_nip = "1000111100"
lecture_course = "CS012"

student_nim = "1103132163"
student_course = "CS012"
student_presence = "90%"

total_student = "10"
# endregion

# window setup
window = tk.Tk()
window.title("TA Nadya")
window.geometry("800x480")
window.resizable(0,0)

def switch(page):
    page.lift()

# region pages
# page main
page_main = tk.Frame(window)
img = ImageTk.PhotoImage(Image.open(file_dir+"/logo_telu.jpg"))
tk.Label(page_main, image=img).pack()
tk.Label(page_main, text="Silahkan Masukkan Kartu Anda").pack()
tk.Button(page_main, command=lambda: switch(page_submit), text="Kehadiran").pack()
page_main.place(in_=window, x=0, y=0, relwidth=1, relheight=1)

# failed page
page_failed = tk.Frame(window)
img1 = ImageTk.PhotoImage(Image.open(file_dir+"/cross.jpg"))
tk.Label(page_failed, image=img1).pack()
page_failed.place(in_=window, x=0, y=0, relwidth=1, relheight=1)

# success page
page_success = tk.Frame(window)
img2 = ImageTk.PhotoImage(Image.open(file_dir+"/check.jpg"))
tk.Label(page_success, image=img2).pack()
page_success.place(in_=window, x=0, y=0, relwidth=1, relheight=1)

# lecture page
page_lecture = tk.Frame(window)
tk.Label(page_lecture, text="Nama Dosen: " + lecture_name).pack()
tk.Label(page_lecture, text="NIP: " + lecture_nip).pack()
tk.Label(page_lecture, text="Kode Mata Kuliah: " + lecture_course).pack()
page_lecture.place(in_=window, x=0, y=0, relwidth=1, relheight=1)

# student page
page_student = tk.Frame(window)
tk.Label(page_student, text="NIM: " + student_nim).pack()
tk.Label(page_student, text="Kode Mata Kuliah: " + student_course).pack()
tk.Label(page_student, text="Presensi: " + student_presence).pack()
page_student.place(in_=window, x=0, y=0, relwidth=1, relheight=1)

# submit page
page_submit = tk.Frame(window)
tk.Label(page_submit, text="Kode Mata Kuliah: " + lecture_course).pack()
tk.Label(page_submit, text="Jumlah Mahasiswa: " + total_student).pack()
tk.Button(page_submit, command=lambda: switch(page_main), text="Kehadiran").pack()
page_submit.place(in_=window, x=0, y=0, relwidth=1, relheight=1)
# endregion

# main loop
switch(page_main)
window.mainloop()