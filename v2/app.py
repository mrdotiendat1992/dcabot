from tkinter import *
from tkinter import messagebox, filedialog
from threading import Thread
from time import sleep
from configparser import ConfigParser
import MetaTrader5 as mt5
import json

def lay_du_lieu_cau_hinh():
    with open('config/acc_1.json', 'r') as file_1:
        config_acc_1= json.load(file_1)

    with open('config/acc_2.json', 'r') as file_2:
        config_acc_2= json.load(file_2)

    with open('config/acc_3.json', 'r') as file_3:
        config_acc_3= json.load(file_3)
    return {"acc_1":config_acc_1,"acc_2":config_acc_2,"acc_3":config_acc_3}

class GiaoDien:
    def __init__(self):
        self.cuaso = Tk()
        self.cuaso.title("BOT DCA")

        cauhinh = lay_du_lieu_cau_hinh()

        self.khungtaikhoan1 = Frame(self.cuaso)
        self.khungtaikhoan1.pack(padx=5, pady=5, anchor=N, fill=X)
        self.nhantaikhoan1 = Label(self.khungtaikhoan1, text="TÀI KHOẢN 1",width=10,font=("Helvetica",14,"bold"))
        self.nhantaikhoan1.pack(fill=X)
        cauhinh_acc1 = cauhinh["acc_1"]
        self.chiavol1 = Frame(self.khungtaikhoan1)
        self.chiavol1.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)
        self.nhanchiavol1 = Button(self.chiavol1, text="LIST VOLUMES",width=10)
        self.nhanchiavol1.pack(fill=X)
        self.chiavol1trai = Frame(self.chiavol1)
        self.chiavol1trai.pack(side=LEFT)
        self.chiavol1phai = Frame(self.chiavol1)
        self.chiavol1phai.pack(side=LEFT, anchor=N)
        for vol in cauhinh_acc1["list_vol"][:6]:
            Label(self.chiavol1trai, text=vol,relief=SUNKEN,width=10).pack(fill=X)
        for vol in cauhinh_acc1["list_vol"][6:]:
            Label(self.chiavol1phai, text=vol,relief=SUNKEN,width=10).pack(fill=X)
        self.dulieutaikhoan1 = Frame(self.khungtaikhoan1)
        self.dulieutaikhoan1.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)
        self.khungcacnhan1 = Frame(self.dulieutaikhoan1)
        self.khungcacnhan1.pack(fill=X)
        Button(self.khungcacnhan1, text="PRICE",width=10).pack(side=LEFT)
        Button(self.khungcacnhan1, text="VOLUME",width=10).pack(side=LEFT)
        Button(self.khungcacnhan1, text="STOPLOSS",width=10).pack(side=LEFT)
        Button(self.khungcacnhan1, text="TAKEPROFIT",width=10).pack(side=LEFT)
        Button(self.khungcacnhan1, text="DCA",width=10).pack(side=LEFT)
        Button(self.khungcacnhan1, text="MAXPROFIT",width=10).pack(side=LEFT)
        self.khungcacthamso1 = Frame(self.dulieutaikhoan1)
        self.khungcacthamso1.pack(fill=X)
        self.gianhapvao1 = Entry(self.khungcacthamso1,width=11)
        self.gianhapvao1.pack(side=LEFT,padx=5,pady=5)
        self.gianhapvao1.insert(0,cauhinh_acc1["price_open"])
        self.volnhapvao1 = Entry(self.khungcacthamso1,width=11)
        self.volnhapvao1.pack(side=LEFT,padx=5,pady=5)
        self.volnhapvao1.insert(0,cauhinh_acc1["start_vol"])
        self.stoploss1 = Entry(self.khungcacthamso1,width=11)
        self.stoploss1.pack(side=LEFT,padx=5,pady=5)
        self.stoploss1.insert(0,cauhinh_acc1["default_sl"])
        self.takeprofit1 = Entry(self.khungcacthamso1,width=11)
        self.takeprofit1.pack(side=LEFT,padx=5,pady=5)
        self.takeprofit1.insert(0,cauhinh_acc1["default_tp"])
        self.dca1 = Entry(self.khungcacthamso1,width=11)
        self.dca1.pack(side=LEFT,padx=5,pady=5)
        self.dca1.insert(0,cauhinh_acc1["default_dca"])
        self.maxprofit1 = Entry(self.khungcacthamso1,width=11)
        self.maxprofit1.pack(side=LEFT,padx=5,pady=5)
        self.maxprofit1.insert(0,cauhinh_acc1["max_profit"])

        self.khungcacnutbam1 = Frame(self.dulieutaikhoan1)
        self.khungcacnutbam1.pack(fill=X,pady=5)
        Button(self.khungcacnutbam1, text="BUY LIMIT",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam1, text="SELL LIMIT",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam1, text="SET TP",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam1, text="SET SL",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam1, text="CLOSE ALL",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam1, text="CONNECT",width=10).pack(side=LEFT)

        self.khungnhapduongdan1 = Frame(self.dulieutaikhoan1)
        self.khungnhapduongdan1.pack(fill=X, pady=10)
        self.nhapduongdan1 = Entry(self.khungnhapduongdan1,width=50)
        self.nhapduongdan1.pack(side=LEFT,padx=10)
        Button(self.khungnhapduongdan1, text="CHOOSE",width=10).pack(side=LEFT)
        

        self.khungtaikhoan2 = Frame(self.cuaso)
        self.khungtaikhoan2.pack(padx=5, pady=5, anchor=N, fill=X)
        self.nhantaikhoan2 = Label(self.khungtaikhoan2, text="TÀI KHOẢN 2",width=10,font=("Helvetica",14,"bold"))
        self.nhantaikhoan2.pack()
        cauhinh_acc2 = cauhinh["acc_2"]
        self.chiavol2 = Frame(self.khungtaikhoan2)
        self.chiavol2.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)
        self.nhanchiavol2 = Button(self.chiavol2, text="LIST VOLUMES",width=10)
        self.nhanchiavol2.pack(fill=X)
        self.chiavol2trai = Frame(self.chiavol2)
        self.chiavol2trai.pack(side=LEFT)
        self.chiavol2phai = Frame(self.chiavol2)
        self.chiavol2phai.pack(side=LEFT, anchor=N)
        for vol in cauhinh_acc2["list_vol"][:6]:
            Label(self.chiavol2trai, text=vol,relief=SUNKEN,width=10).pack(fill=X)
        for vol in cauhinh_acc2["list_vol"][6:]:
            Label(self.chiavol2phai, text=vol,relief=SUNKEN,width=10).pack(fill=X)

        self.dulieutaikhoan2 = Frame(self.khungtaikhoan2)
        self.dulieutaikhoan2.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)

        self.khungcacnhan2 = Frame(self.dulieutaikhoan2)
        self.khungcacnhan2.pack(fill=X)
        Button(self.khungcacnhan2, text="PRICE",width=10).pack(side=LEFT)
        Button(self.khungcacnhan2, text="VOLUME",width=10).pack(side=LEFT)
        Button(self.khungcacnhan2, text="STOPLOSS",width=10).pack(side=LEFT)
        Button(self.khungcacnhan2, text="TAKEPROFIT",width=10).pack(side=LEFT)
        Button(self.khungcacnhan2, text="DCA",width=10).pack(side=LEFT)
        Button(self.khungcacnhan2, text="MAXPROFIT",width=10).pack(side=LEFT)

        self.khungcacthamso2 = Frame(self.dulieutaikhoan2)
        self.khungcacthamso2.pack(fill=X)

        self.gianhapvao2 = Entry(self.khungcacthamso2,width=11)
        self.gianhapvao2.pack(side=LEFT,padx=5,pady=5)
        self.gianhapvao2.insert(0,cauhinh_acc2["price_open"])

        self.volnhapvao2 = Entry(self.khungcacthamso2,width=11)
        self.volnhapvao2.pack(side=LEFT,padx=5,pady=5)
        self.volnhapvao2.insert(0,cauhinh_acc2["start_vol"])

        self.stoploss2 = Entry(self.khungcacthamso2,width=11)
        self.stoploss2.pack(side=LEFT,padx=5,pady=5)
        self.stoploss2.insert(0,cauhinh_acc2["default_sl"])

        self.takeprofit2 = Entry(self.khungcacthamso2,width=11)
        self.takeprofit2.pack(side=LEFT,padx=5,pady=5)
        self.takeprofit2.insert(0,cauhinh_acc2["default_tp"])

        self.dca2 = Entry(self.khungcacthamso2,width=11)
        self.dca2.pack(side=LEFT,padx=5,pady=5)
        self.dca2.insert(0,cauhinh_acc2["default_dca"])

        self.maxprofit2 = Entry(self.khungcacthamso2,width=11)
        self.maxprofit2.pack(side=LEFT,padx=5,pady=5)
        self.maxprofit2.insert(0,cauhinh_acc2["max_profit"])

        self.khungcacnutbam2 = Frame(self.dulieutaikhoan2)
        self.khungcacnutbam2.pack(fill=X,pady=5)

        Button(self.khungcacnutbam2, text="BUY LIMIT",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam2, text="SELL LIMIT",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam2, text="SET TP",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam2, text="SET SL",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam2, text="CLOSE ALL",width=10).pack(side=LEFT)
        Button(self.khungcacnutbam2, text="CONNECT",width=10).pack(side=LEFT)

        self.khungnhapduongdan2 = Frame(self.dulieutaikhoan2)
        self.khungnhapduongdan2.pack(fill=X, pady=10)
        self.nhapduongdan2 = Entry(self.khungnhapduongdan2,width=50)
        self.nhapduongdan2.pack(side=LEFT,padx=10)
        Button(self.khungnhapduongdan2, text="CHOOSE",width=10).pack(side=LEFT)


        self.khungtakhoan3 = Frame(self.cuaso)
        self.khungtakhoan3.pack(padx=5, pady=5, anchor=N, fill=X)
        self.nhantakhoan3 = Label(self.khungtakhoan3, text="TÀI KHOẢN 3",width=10,font=("Helvetica",14,"bold"))
        self.nhantakhoan3.pack()
        cauhinh_acc3 = cauhinh["acc_3"]
        self.chiavol3 = Frame(self.khungtakhoan3)
        self.chiavol3.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)
        self.nhanchiavol3 = Label(self.chiavol3, text="VOLUMES",width=10)
        self.nhanchiavol3.pack(fill=X)
        self.chiavol3trai = Frame(self.chiavol3)
        self.chiavol3trai.pack(side=LEFT)
        self.chiavol3phai = Frame(self.chiavol3)
        self.chiavol3phai.pack(side=LEFT, anchor=N)
        for vol in cauhinh_acc3["list_vol"][:6]:
            Label(self.chiavol3trai, text=vol,relief=SUNKEN,width=10).pack(fill=X)
        for vol in cauhinh_acc3["list_vol"][6:]:
            Label(self.chiavol3phai, text=vol,relief=SUNKEN,width=10).pack(fill=X)
        
        self.cuaso.mainloop()

GiaoDien()