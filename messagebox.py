from tkinter import *
from tkinter import ttk
from datetime import datetime

# main tkinter GUI class
class Application(Frame):
    def __init__(self, title, master=None):
        ttk.Frame.__init__(self, master)
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.test_button = ttk.Button(self, text='test', width=7, command=self.call_test_press)
        self.test_button.grid()

    def call_test_press(self):
        jumper = jump_to_window()
        self.wait_window(jumper.top)



class jump_to_window(Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        top = self.top = Toplevel(self)
        self.label = Label(top, text='Please enter something')
        self.label.grid(row=0, column=0)
        self.entry = Entry(top)
        self.entry.grid(row=1)
        self.data = 'test'
        self.data = self.entry.get()
        print(self.data)
        self.button = Button(top, text='OK', command=self.top.destroy)
        self.button.grid(row=2)


app = Application('test')
app.mainloop()