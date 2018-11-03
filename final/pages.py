import Tkinter as tk
from PIL import ImageTk, Image

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

class MainPage(Page):
    def __init__(self, *args, **kwargs):
        file_dir = args[1]
        on_click = args[2]
        Page.__init__(self, *args[:1], **kwargs)

        # views
        self.img = ImageTk.PhotoImage(Image.open(file_dir))
        tk.Label(self, image=self.img).pack()
        tk.Label(self, text="Silahkan Masukkan Kartu Anda").pack()
        # self.button_submit = tk.Button(self, command=lambda: click_event(self), text="Kehadiran").pack()
    
    def show_button(self, should_show):
        if should_show:
            self.button_submit.lower(self)
        else:
            self.button_submit.lift(self)
        
class FailedPage(Page):
    def __init__(self, *args, **kwargs):
        file_dir = args[1]
        Page.__init__(self, *args[:1], **kwargs)

        # views    
        self.img = ImageTk.PhotoImage(Image.open(file_dir))
        tk.Label(self, image=self.img).pack()

class SuccessPage(Page):
    def __init__(self, *args, **kwargs):
        file_dir = args[1]
        Page.__init__(self, *args[:1], **kwargs)

        # views
        self.img = ImageTk.PhotoImage(Image.open(file_dir))
        tk.Label(self, image=self.img).pack()

class LecturePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.nameText = tk.StringVar()
        self.nipText = tk.StringVar()
        self.course = tk.StringVar()

        # views
        tk.Label(self, textvariable=self.nameText).pack()
        tk.Label(self, textvariable=self.nipText).pack()
        tk.Label(self, textvariable=self.course).pack()
    
    def setData(self, name, nip, course):
        self.nameText.set("Nama Dosen: " + name)
        self.nipText.set("NIP: " + nip)
        self.course.set("Kode Mata Kuliah: " + course)
        # self.master.update()

class StudentPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.nimText = tk.StringVar()
        self.courseText = tk.StringVar()
        self.presenceText = tk.StringVar()

        # views
        tk.Label(self, textvariable=self.nimText).pack()
        tk.Label(self, textvariable=self.courseText).pack()
        tk.Label(self, textvariable=self.presenceText).pack()
    
    def setData(self, nim, course, presence):
        self.nimText.set("NIM: " + nim)
        self.courseText.set("Kode Mata Kuliah: " + course)
        self.presenceText.set("Presensi: " + presence)

class SubmitPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.courseText = tk.StringVar()
        self.totalStudentText = tk.StringVar()

        # view
        tk.Label(self, textvariable=self.courseText).pack()
        tk.Label(self, textvariable=self.totalStudentText).pack()
        tk.Button(self, command=lambda: click_event(self), text="Kehadiran").pack()        

    def setData(self, course, total):
        self.courseText.set("Kode Mata Kuliah: " + course)
        self.totalStudentText.set("Jumlah Mahasiswa: " + total)
