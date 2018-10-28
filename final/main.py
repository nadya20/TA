#!/usr/bin/python

# import Tkinter as tkinter

# # window setup
# main_window = tkinter.Tk()
# main_window.title("TA Nadya")
# main_window.geometry("800x480")
# main_window.resizable(0,0)

# # Code to add widgets will go here...
# imageObj = open('./telu-logo.png', 'r')
# label = tkinter.Label(main_window, text="alif", image=imageObj)
# label.pack()

# # main loop
# main_window.mainloop()


import MyReader as mr


if __name__ == "__main__" :
    print mr.isLecture()
