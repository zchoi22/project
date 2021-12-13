from stock.stock import stock
from screener.screener import screener as sc
from tkinter import *
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def doNothing():
    pass

def set_screener():
    create_settings()
    print('hi')

def save_settings(settings, screener_name):
    new = sc()
    for i in range(len(settings)):
        new.set_settings(i, settings[i])
    new.save_screener(screener_name)
    clear()

def set_settings(*args):
    answer = simpledialog.askstring("Input", "Enter a screener name: ", parent=root)
    screener_name = '..\\project\\screener\\screeners\\'+ answer
    settings = []

    if args[0] == 'Any':
        settings.append(np.nan)
    elif args[0][:5] == 'Under':
        settings.append(int('1'+args[0][7:]))
    else:
        settings.append(int('2'+args[0][6:]))

    if args[1] == 'Any':
        settings.append(np.nan)
    elif args[0][:5] == 'Under':
        if args[0][-1] == 'K':
            settings.append(int('1' + args[0][7:-1] + '000'))
        else:
            settings.append(int('1' + args[0][7:-1] + '000000'))
    else:
        if args[0][-1] == 'K':
            settings.append(int('2' + args[0][6:-1] + '000'))
        else:
            settings.append(int('2' + args[0][6:-1] + '000000'))

    if args[2] == 'Any':
        settings.append(np.nan)
    else:
        settings.append(int('1'+args.split('%')[0]))

    if args[2] == 'Any':
        settings.append(np.nan)
    else:
        settings.append(int('2'+args.split('%')[0]))
    
    save_settings(settings, screener_name)


def create_settings():
    price_frame = Frame(root)
    price_frame.pack(padx=5, pady=15, side=TOP, anchor=NW)
    price_setting = StringVar(root)
    price_setting.set('Price')
    price_label = Label(price_frame, textvariable = price_setting, relief = RAISED)
    price_label.pack(side=LEFT)
    price_var = StringVar(root)
    price_var.set('Any')
    w = OptionMenu(price_frame, price_var, 'Under $5', 'Under $10', 'Under $20',
                   'Under $30', 'Under $50', 'Under $100', 'Over $5', 'Over $10',
                   'Over $20', 'Over $30', 'Over $50', 'Over $100')
    w.pack(side = LEFT)

    volume_frame = Frame(root)
    volume_frame.pack(padx=5, pady=15, side=TOP, anchor=NW)
    volume_setting = StringVar(root)
    volume_setting.set('Volume')
    volume_label = Label(volume_frame, textvariable=volume_setting, relief=RAISED)
    volume_label.pack(side=LEFT)
    volume_var = StringVar(root)
    volume_var.set('Any')
    w = OptionMenu(volume_frame, volume_var, 'Under 50K', 'Under 100K', 'Under 1M',
                   'Over 100K', 'Over 1M', 'Over 2M')
    w.pack(side=LEFT)

    year_high_frame = Frame(root)
    year_high_frame.pack(padx=5, pady=15, side=TOP, anchor=NW)
    year_high_setting = StringVar(root)
    year_high_setting.set('52 Week High')
    year_high_label = Label(year_high_frame, textvariable=year_high_setting, relief=RAISED)
    year_high_label.pack(side=LEFT)
    year_high_var = StringVar(root)
    year_high_var.set('Any')
    w = OptionMenu(year_high_frame, year_high_var, '05% or more below High', '10% or more below High',
                   '20% or more below High','50% or more below High','90% or more below High',)
    w.pack(side=LEFT)
    
    year_low_frame = Frame(root)
    year_low_frame.pack(padx=5, pady=15, side=TOP, anchor=NW)
    year_low_setting = StringVar(root)
    year_low_setting.set('52 Week Low')
    year_low_label = Label(year_low_frame, textvariable=year_low_setting, relief=RAISED)
    year_low_label.pack(side=LEFT)
    year_low_var = StringVar(root)
    year_low_var.set('Any')
    w = OptionMenu(year_low_frame, year_low_var, '10% or more above High', '20% or more above High',
                   '50% or more above High','100% or more above High','250% or more above High',)
    w.pack(side=LEFT)

    button = Button(root, text="OK", command=lambda : set_settings(price_var.get(),volume_var.get(),
                                                                   year_high_var.get()))
    button.pack(padx=5, pady=15, side=TOP, anchor=NW)

def display_graph():
    df, ticker = ticker_search()
    format_graph(df, ticker)

def format_graph(dataframe, ticker):
    figure = plt.Figure(figsize=(8, 6), dpi=100)
    ax = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, root)
    line.get_tk_widget().pack(side=LEFT, fill=BOTH)
    dataframe.plot(kind='line', x = 'Date', ax=ax)
    ax.set_title(ticker.upper() + ' Chart')

def format_data(data):
    df = data[['Date','Adj Close']].copy()
    return df

def ticker_search():
    answer = simpledialog.askstring("Input", "Enter a ticker below: ", parent = root)
    if answer is not None:
        ticker = stock(answer, '..\\project\\stock\\historical_data\\')
        return format_data(ticker.get_data().reset_index()), answer
    print('Error: Ticker not entered.')

def clear():
    list = return_widgets(root)
    for item in list:
        item.pack_forget()

def return_widgets(window):
    list = window.winfo_children()
    for item in list:
        if item.winfo_children():
            list.extend(item.winfo_children())
    return list

if __name__ == '__main__':
    #configuring gui window with tkinter
    root = Tk()
    root.configure(background = 'white')
    root.title('Rapstar')
    root.geometry('1200x800')

    #feature for gui
    title = Label(root, text = "Welcome to Rapstar!")
    title.pack()

    mb = Menu(root)
    financemenu = Menu(mb, tearoff = 0)
    financemenu.add_command(label = 'Create Chart', command=display_graph)
   # financemenu.add_command(label = 'Screener', command=donothing)
    financemenu.add_separator()
    financemenu.add_command(label = 'Exit', command = root.quit)
    mb.add_cascade(label = 'Finance', menu = financemenu)

    screenermenu = Menu(mb, tearoff = 0)
    screenermenu.add_command(label = 'Set Screener', command=set_screener)
    screenermenu.add_command(label = 'Import Screener')
    screenermenu.add_command(label = 'Run Screener')
    mb.add_cascade(label = 'Screener', menu = screenermenu)

    editmenu = Menu(mb, tearoff=0)
    editmenu.add_command(label='Clear', command=clear)
    mb.add_cascade(label = 'Edit', menu = editmenu)

    root.config(menu=mb)
    root.mainloop()