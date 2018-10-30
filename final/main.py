#!/usr/bin/python

import Tkinter as tk
# from PIL import ImageTk, Image
# import os

# file_dir = os.path.dirname(os.path.abspath(__file__))

# # window setup
# window = tkinter.Tk()
# window.title("TA Nadya")
# window.geometry("800x480")
# window.resizable(0,0)

# # page main
# page_main = tkinter.Frame(window)
# tkinter.Label(page_main, text="Main Page").pack()
# page_main.pack(fill="both", expand=True)

# # failed page
# page_failed = tkinter.Frame(window)
# tkinter.Label(page_failed, text="failed page").pack()
# page_failed.pack(fill="both", expand=True)

# # success page
# page_success = tkinter.Frame(window)
# tkinter.Label(page_success, text="success page").pack()
# page_success.pack(fill="both", expand=True)

# # lecture page
# page_lecture = tkinter.Frame(window)
# tkinter.Label(page_lecture, text="lecture page").pack()
# page_lecture.pack(fill="both", expand=True)

# # student page
# page_student = tkinter.Frame(window)
# tkinter.Label(page_student, text="student page").pack()
# page_student.pack(fill="both", expand=True)

# # submit page
# page_submit = tkinter.Frame(window)
# tkinter.Label(page_submit, text="submit page").pack()

# # img = ImageTk.PhotoImage(Image.open(file_dir+"/logo_telu.png"))
# # main loop
# window.mainloop()

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 1")
       label.pack(side="top", fill="both", expand=True)

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()