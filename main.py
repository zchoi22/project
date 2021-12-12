from stock import stock
from screener import screener as sc
from tkinter import *

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

if __name__ == '__main__':
    #configuring gui window with tkinter
    root = Tk()
    root.configure(background = 'white')
    root.title('Rapstar')
    root.geometry('500x450')

    #feature for gui
    title = Label(root, text = "Welcome to Rapstar!")
    title.pack()

    mb = Menu(root)
    filemenu = Menu(mb, tearoff = 0)
    filemenu.add_command(label = 'Screener', command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label = 'Exit', command = root.quit)
    mb.add_cascade(label = 'File', menu = filemenu)

    root.config(menu=mb)
    root.mainloop()