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

        self.button_submit = tk.Button(self, command=lambda: on_click(self), text="Kehadiran")
        self.button_submit.pack()
    
    def toggle_button(self):
        # TODO : Fix this
        pass
        # if self.is_button_showed:
        #     self.button_submit.lower(self)
        # else:
        #     self.button_submit.lift(self)
        
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
    MAX_ATTENDANCE = 14

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.nimText = tk.StringVar()
        self.courseText = tk.StringVar()
        self.presenceText = tk.StringVar()

        # views
        tk.Label(self, textvariable=self.nimText).pack()
        tk.Label(self, textvariable=self.courseText).pack()
        tk.Label(self, textvariable=self.presenceText).pack()
    
    def setData(self, nim, courses, index):
        self.nimText.set("NIM: " + nim)
        if index > -1:
            count_attendace = courses[index].attendance / float(StudentPage.MAX_ATTENDANCE) * 100
            self.courseText.set("Kode Mata Kuliah: " + courses[index].subject)
            self.presenceText.set("Presensi: " + "0:.2f".format(count_attendace) + " %")

class SubmitPage(Page):
    def __init__(self, *args, **kwargs):
        on_click = args[1]
        Page.__init__(self, *args[:1], **kwargs)
        self.courseText = tk.StringVar()
        self.totalStudentText = tk.StringVar()

        # view
        tk.Label(self, textvariable=self.courseText).pack()
        tk.Label(self, textvariable=self.totalStudentText).pack()
        tk.Button(self, command=lambda: on_click(self), text="Kehadiran").pack()        

    def setData(self, course, total):
        self.courseText.set("Kode Mata Kuliah: " + course)
        self.totalStudentText.set("Jumlah Mahasiswa: " + str(total))
