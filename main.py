from main.stock.stock import stock
from main.screener.screener import screener as sc
from tkinter import *
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def doNothing():
    pass

def set_screener(settings, screener_name):
    global base_screener
    for i in range(len(settings)):
        base_screener.set_settings(i, settings[i])
    base_screener.save_screener(screener_name)
    clear()

def import_screener():
    global base_screener
    answer = simpledialog.askstring("Input", "Enter a screener name: ", parent=root)
    screener_name = '..\\project\\main\\screener\\screeners\\'+ answer
    base_screener = sc(False, screener_name)

def run_screener():
    base_screener.run_screener()

def set_settings(*args):
    answer = simpledialog.askstring("Input", "Enter a screener name: ", parent=root)
    screener_name = '..\\project\\main\\screener\\screeners\\'+ answer
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
        settings.append(int('1'+args[2].split('%')[0]))

    if args[3] == 'Any':
        settings.append(np.nan)
    else:
        settings.append(int('2'+args[3].split('%')[0]))

    for arg in args[4:7]:
        setting_components = arg.split(' ')
        string_to_setting = ''
        for component in setting_components:
            if component == "Price":
                string_to_setting+='0'
            elif component == '20-Day-SMA':
                string_to_setting+='1'
            elif component == '50-Day-SMA':
                string_to_setting+='2'
            elif component == '200-Day-SMA':
                string_to_setting+='3'
            elif component == 'below':
                string_to_setting = '1'+string_to_setting
            elif component == 'above':
                string_to_setting = '2'+string_to_setting
        settings.append(string_to_setting)
    
    set_screener(settings, screener_name)


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
    w = OptionMenu(year_high_frame, year_high_var, '5% or more below High', '10% or more below High',
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
    w = OptionMenu(year_low_frame, year_low_var, '10% or more above Low', '20% or more above Low',
                   '50% or more above Low','100% or more above Low','250% or more above Low',)
    w.pack(side=LEFT)
    
    sma20_frame = Frame(root)
    sma20_frame.pack(padx=5, pady=15, side=TOP, anchor=NW)
    sma20_setting = StringVar(root)
    sma20_setting.set('20-Day-SMA')
    sma20_label = Label(sma20_frame, textvariable=sma20_setting, relief=RAISED)
    sma20_label.pack(side=LEFT)
    sma20_var = StringVar(root)
    sma20_var.set('Any')
    w = OptionMenu(sma20_frame, sma20_var, 'Price above 20-Day-SMA', 'Price below 20-Day-SMA',
                   '50-Day-SMA above 20-Day-SMA','50-Day-SMA below 20-Day-SMA','200-Day-SMA above 20-Day-SMA',
                   '200-Day-SMA below 20-Day-SMA')
    w.pack(side=LEFT)
    
    sma50_frame = Frame(root)
    sma50_frame.pack(padx=5, pady=15, side=TOP, anchor=NW)
    sma50_setting = StringVar(root)
    sma50_setting.set('50-Day-SMA')
    sma50_label = Label(sma50_frame, textvariable=sma50_setting, relief=RAISED)
    sma50_label.pack(side=LEFT)
    sma50_var = StringVar(root)
    sma50_var.set('Any')
    w = OptionMenu(sma50_frame, sma50_var, 'Price above 50-Day-SMA', 'Price below 50-Day-SMA',
                   '20-Day-SMA above 50-Day-SMA','20-Day-SMA below 50-Day-SMA','200-Day-SMA above 50-Day-SMA',
                   '200-Day-SMA below 50-Day-SMA')
    w.pack(side=LEFT)
    
    sma200_frame = Frame(root)
    sma200_frame.pack(padx=5, pady=15, side=TOP, anchor=NW)
    sma200_setting = StringVar(root)
    sma200_setting.set('200-Day-SMA')
    sma200_label = Label(sma200_frame, textvariable=sma200_setting, relief=RAISED)
    sma200_label.pack(side=LEFT)
    sma200_var = StringVar(root)
    sma200_var.set('Any')
    w = OptionMenu(sma200_frame, sma200_var, 'Price above 200-Day-SMA', 'Price below 200-Day-SMA',
                   '20-Day-SMA above 200-Day-SMA','20-Day-SMA below 200-Day-SMA','50-Day-SMA above 200-Day-SMA',
                   '50-Day-SMA below 200-Day-SMA')
    w.pack(side=LEFT)

    button = Button(root, text="Save", command=lambda : set_settings(price_var.get(),volume_var.get(),
                                                                   year_high_var.get(), year_low_var.get(),
                                                                   sma20_var.get(), sma50_var.get(), sma200_var.get()))
    button.pack(padx=5, pady=15, side=TOP, anchor=NW)

def advanced_graph():
    features = []
    while True:
        answer = simpledialog.askstring("Input", "Enter features to show: ", parent=root)
        if answer is not None:
            features.append(answer)
        else:
            break
    button = Button(root, text='Done', command = lambda : display_graph(features))
    button.pack()

def display_graph(*args):
    df, ticker = ticker_search()
    data = stock(ticker)
    figure = plt.Figure(figsize=(8, 6), dpi=100)
    ax = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, root)
    df.plot(kind='line', x = 'Date', ax=ax)
    ax.set_title(ticker.upper() + ' Chart')

    if args!=():
        for arg in args[0]:
            if arg in data.get_data().keys():
                df_feature = data.get_data().reset_index()[['Date', arg]].copy()
                df_feature.plot(ax=ax, x='Date')
            elif 'SMA' in arg:
                days = int(arg.split('SMA')[0])
                df_feature = data.get_sma(days)
                df_feature.plot(ax=ax, x='Date')

    line.get_tk_widget().pack(side=LEFT, fill=BOTH)

def format_data(data):
    df = data[['Date','Adj Close']].copy()
    return df

def ticker_search():
    answer = simpledialog.askstring("Input", "Enter a ticker below: ", parent = root)
    if answer is not None:
        ticker = stock(answer)
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

    #configuring screener, base screener is empty
    base_screener = sc(False)

    #title for gui
    title = Label(root, text = "Welcome to Rapstar!")
    title.pack()

    mb = Menu(root)
    financemenu = Menu(mb, tearoff = 0)
    financemenu.add_command(label = 'Create Chart', command=display_graph)
    financemenu.add_command(label='Advanced Chart', command=advanced_graph)
   # financemenu.add_command(label = 'Screener', command=donothing)
    financemenu.add_separator()
    financemenu.add_command(label = 'Exit', command = root.quit)
    mb.add_cascade(label = 'Finance', menu = financemenu)

    screenermenu = Menu(mb, tearoff = 0)
    screenermenu.add_command(label = 'Set Screener', command=create_settings)
    screenermenu.add_command(label = 'Import Screener', command=import_screener)
    screenermenu.add_command(label = 'Run Screener', command=run_screener)
    mb.add_cascade(label = 'Screener', menu = screenermenu)

    editmenu = Menu(mb, tearoff=0)
    editmenu.add_command(label='Clear', command=clear)
    mb.add_cascade(label = 'Edit', menu = editmenu)

    root.config(menu=mb)
    root.mainloop()