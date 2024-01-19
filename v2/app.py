import json
from tkinter import *
from tkinter import messagebox, dialog

def load_config():
    return json.loads(open('config.json').read())

def save_config(config):
    open('config.json', 'w').write(json.dumps(config))

class DcaBot:
    def __init__(self):
        self.root = Tk()
        self.root.title("DCA BOT V2.0")
        self.root.config(padx=10, pady=10, bg="skyblue1")

        self.leftframe = Frame(self.root, padx=10, bg="skyblue2")
        self.leftframe.pack(side=LEFT, pady=10, fill=Y, expand=True, anchor=N)

        self.rightframe = Frame(self.root, padx=10, bg="white")
        self.rightframe.pack(side=LEFT, pady=10, fill=Y, expand=True, anchor=N)

        self.accountnameframe = Frame(self.root, padx=10, bg="white")
        self.accountnameframe.pack(side=LEFT, pady=10, fill=Y, expand=True, anchor=N)

        self.config = load_config()

        self.symbol = StringVar()
        self.symbol.set(self.config['symbols'][0])

        self.volumes = self.config['volumes']

        Label(self.leftframe, text="SYMBOL", width=10, bg="skyblue2", font=("Helvetica", 10, "bold")).pack()
        self.symbol_choose = OptionMenu(self.leftframe, self.symbol, *self.config['symbols'])
        self.symbol_choose.pack()
        Label(self.leftframe, text="", width=10, bg="skyblue2").pack(pady=15)
        Label(self.leftframe, text="VOLUMES", width=10, bg="skyblue2", font=("Helvetica", 10, "bold")).pack()
        for volume in self.volumes:
            Label(self.leftframe, text=volume, width=10,relief=GROOVE, font=("Helvetica", 12, "bold"), bg="skyblue2").pack()

        Button(self.leftframe, text="CONFIG", width=10, bg="yellow", fg="red", font=("Helvetica", 10, "bold")).pack(pady=5)

        self.acc1frame = Frame(self.rightframe, padx=10, bg="white")
        self.acc1frame.pack(pady=10,fill=X)

        self.acc1labelframe = Frame(self.acc1frame, padx=10, bg="white")
        self.acc1labelframe.pack(fill=X)
        
        Label(self.acc1labelframe, text="Vol", width=10, bg="white").pack(side=LEFT)
        Label(self.acc1labelframe, text="Price", width=10, bg="white").pack(side=LEFT)
        Label(self.acc1labelframe, text="TP", width=10, bg="white").pack(side=LEFT)
        Label(self.acc1labelframe, text="SL", width=10, bg="white").pack(side=LEFT)
        Label(self.acc1labelframe, text="DCA", width=10, bg="white").pack(side=LEFT)
        Label(self.acc1labelframe, text="Profit", width=10, bg="white").pack(side=LEFT)

        self.acc1entryframe = Frame(self.acc1frame, padx=10, bg="white")
        self.acc1entryframe.pack(fill=X)

        self.startvol1 = Entry(self.acc1frame, width=12, bg="white")
        self.startvol1.pack(side=LEFT)
        self.startprice1 = Entry(self.acc1frame, width=12, bg="white")
        self.startprice1.pack(side=LEFT)
        self.defaulttp1 = Entry(self.acc1frame, width=12, bg="white")
        self.defaulttp1.pack(side=LEFT)
        self.defaultsl1 = Entry(self.acc1frame, width=12, bg="white")
        self.defaultsl1.pack(side=LEFT)
        self.dca1 = Entry(self.acc1frame, width=12, bg="white")
        self.dca1.pack(side=LEFT)
        self.maxprofit1 = Entry(self.acc1frame, width=12, bg="white")
        self.maxprofit1.pack(side=LEFT)

        self.path1frame = Frame(self.rightframe, padx=10, bg="white")
        self.path1frame.pack(pady=10,fill=X)
        self.path1label = Label(self.path1frame, text="Path: ", bg="white")
        self.path1label.pack(anchor=W)
        self.path1entryframe = Frame(self.path1frame, bg="white")
        self.path1entryframe.pack(fill=X, padx=10)
        self.path1entry = Entry(self.path1entryframe, width=50, bg="white")
        self.path1entry.pack(side=LEFT)
        Button(self.path1entryframe, text="Browse", bg="white").pack(side=LEFT, padx=10)
        
        self.acc1buttonframe = Frame(self.rightframe, padx=10, bg="white")
        self.acc1buttonframe.pack(pady=10,fill=X)
        Button(self.acc1buttonframe, text="Buy", width=10, bg="white").pack(side=LEFT)   
        Button(self.acc1buttonframe, text="Sell", width=10, bg="white").pack(side=LEFT)
        Button(self.acc1buttonframe, text="SL", width=10, bg="white").pack(side=LEFT)
        Button(self.acc1buttonframe, text="TP", width=10, bg="white").pack(side=LEFT)
        Button(self.acc1buttonframe, text="Close", width=10, bg="white").pack(side=LEFT)
        Button(self.acc1buttonframe, text="Connect", width=10, bg="white").pack(side=LEFT)
        

        self.acc2frame = Frame(self.rightframe, bg="white")
        self.acc2frame.pack(pady=10,fill=X)

        self.acc2labelframe = Frame(self.acc2frame, padx=10, bg="white")
        self.acc2labelframe.pack(fill=X)
        
        Label(self.acc2labelframe, text="Vol", width=10, bg="white", font=("Helvetica", 8, "bold")).pack(side=LEFT)
        Label(self.acc2labelframe, text="Price", width=10, bg="white", font=("Helvetica", 8, "bold")).pack(side=LEFT)
        Label(self.acc2labelframe, text="TP", width=10, bg="white", font=("Helvetica", 8, "bold")).pack(side=LEFT)
        Label(self.acc2labelframe, text="SL", width=10, bg="white", font=("Helvetica", 8, "bold")).pack(side=LEFT)
        Label(self.acc2labelframe, text="DCA", width=10, bg="white", font=("Helvetica", 8, "bold")).pack(side=LEFT)
        Label(self.acc2labelframe, text="Profit", width=10, bg="white", font=("Helvetica", 8, "bold")).pack(side=LEFT)

        self.acc2entryframe = Frame(self.acc2frame, padx=10, bg="white")
        self.acc2entryframe.pack(fill=X)

        self.startvol2 = Entry(self.acc2frame, width=12, bg="white")
        self.startvol2.pack(side=LEFT)
        self.startprice2 = Entry(self.acc2frame, width=12, bg="white")
        self.startprice2.pack(side=LEFT)
        self.defaulttp2 = Entry(self.acc2frame, width=12, bg="white")
        self.defaulttp2.pack(side=LEFT)
        self.defaultsl2 = Entry(self.acc2frame, width=12, bg="white")
        self.defaultsl2.pack(side=LEFT)
        self.dca2 = Entry(self.acc2frame, width=12)
        self.dca2.pack(side=LEFT)
        self.maxprofit2 = Entry(self.acc2frame, width=12, bg="white")
        self.maxprofit2.pack(side=LEFT)

        self.path2frame = Frame(self.rightframe, bg="white")
        self.path2frame.pack(pady=10,fill=X)
        self.path2label = Label(self.path2frame, text="Path: ", bg="white")
        self.path2label.pack(anchor=W)
        self.path2entryframe = Frame(self.path2frame, padx=10, bg="white")
        self.path2entryframe.pack(fill=X)
        self.path2entry = Entry(self.path2entryframe, width=50, bg="white")
        self.path2entry.pack(side=LEFT)
        Button(self.path2entryframe, text="Browse", bg="white").pack(side=LEFT, padx=10)
        
        self.acc2buttonframe = Frame(self.rightframe, padx=10, bg="white")
        self.acc2buttonframe.pack(pady=10,fill=X)
        Button(self.acc2buttonframe, text="Buy", width=10, bg="white").pack(side=LEFT)
        Button(self.acc2buttonframe, text="Sell", width=10, bg="white").pack(side=LEFT)
        Button(self.acc2buttonframe, text="SL", width=10, bg="white").pack(side=LEFT)
        Button(self.acc2buttonframe, text="TP", width=10, bg="white").pack(side=LEFT)
        Button(self.acc2buttonframe, text="Close", width=10, bg="white").pack(side=LEFT)
        Button(self.acc2buttonframe, text="Connect", width=10, bg="white").pack(side=LEFT)

        self.acc3frame = Frame(self.rightframe, padx=10)
        self.acc3frame.pack(pady=10,fill=X)

        self.acc3labelframe = Frame(self.acc3frame, padx=10)
        self.acc3labelframe.pack(fill=X)
        
        Label(self.acc3labelframe, text="Vol", width=10).pack(side=LEFT)
        Label(self.acc3labelframe, text="Price", width=10).pack(side=LEFT)
        Label(self.acc3labelframe, text="TP", width=10).pack(side=LEFT)
        Label(self.acc3labelframe, text="SL", width=10).pack(side=LEFT)
        Label(self.acc3labelframe, text="DCA", width=10).pack(side=LEFT)
        Label(self.acc3labelframe, text="Profit", width=10).pack(side=LEFT)

        self.acc3entryframe = Frame(self.acc3frame, padx=10)
        self.acc3entryframe.pack(fill=X)

        self.startvol3 = Entry(self.acc3frame, width=12)
        self.startvol3.pack(side=LEFT)
        self.startprice3 = Entry(self.acc3frame, width=12)
        self.startprice3.pack(side=LEFT)
        self.defaulttp3 = Entry(self.acc3frame, width=12)
        self.defaulttp3.pack(side=LEFT)
        self.defaultsl3 = Entry(self.acc3frame, width=12)
        self.defaultsl3.pack(side=LEFT)
        self.dca3 = Entry(self.acc3frame, width=12)
        self.dca3.pack(side=LEFT)
        self.maxprofit3 = Entry(self.acc3frame, width=12)
        self.maxprofit3.pack(side=LEFT)

        self.path3frame = Frame(self.rightframe, padx=10)
        self.path3frame.pack(pady=10,fill=X)
        self.path3label = Label(self.path3frame, text="Path: ")
        self.path3label.pack(anchor=W)
        self.path3entryframe = Frame(self.path3frame, padx=10)
        self.path3entryframe.pack(fill=X)
        self.path3entry = Entry(self.path3entryframe, width=50)
        self.path3entry.pack(side=LEFT)
        Button(self.path2entryframe, text="Browse").pack(side=LEFT, padx=10)
        
        self.acc3buttonframe = Frame(self.rightframe, padx=10)
        self.acc3buttonframe.pack(pady=10,fill=X)
        Button(self.acc3buttonframe, text="Buy", width=10).pack(side=LEFT)
        Button(self.acc3buttonframe, text="Sell", width=10).pack(side=LEFT)
        Button(self.acc3buttonframe, text="SL", width=10).pack(side=LEFT)
        Button(self.acc3buttonframe, text="TP", width=10).pack(side=LEFT)
        Button(self.acc3buttonframe, text="Close", width=10).pack(side=LEFT)
        Button(self.acc3buttonframe, text="Connect", width=10).pack(side=LEFT)

        
        Label(self.accountnameframe, text="A", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="C", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="C", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="O", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="U", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="N", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="T", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="1", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="", bg="white").pack()

        Label(self.accountnameframe, text="A", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="C", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="C", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="O", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="U", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="N", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="T", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="2", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="", bg="white").pack()

        Label(self.accountnameframe, text="A", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="C", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="C", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="O", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="U", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="N", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="T", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="3", bg="white", font=("Helvetica", 9, "bold")).pack()
        Label(self.accountnameframe, text="", bg="white").pack()

        self.root.mainloop()

DcaBot()