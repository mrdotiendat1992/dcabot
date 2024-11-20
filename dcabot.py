from tkinter import *
from tkinter import messagebox, filedialog
from threading import Thread
from time import sleep
from configparser import ConfigParser
import MetaTrader5 as mt5
from datetime import datetime
import os

class GiaoDien:
    def __init__(self):
        try:
            self.docconfig = ConfigParser()
            if not os.path.exists('config.ini'):
                with open('config.ini', 'w') as configfile:
                    configfile.write('[default]\nlist_volumes = 0.5,1,2,3,4,5,6,7,8,9,10\nlist_tp = 0.5,1,2,3,4,5,6,7,8,9,10')
                        
            self.docconfig.read('config.ini')
            self.danhsachvolume = self.lay_danhsach_volume()
            self.danhsachtp = self.lay_danhsach_tp()
            
            self.cacaccount = {}
            self.kiemtrabuy = False
            self.kiemtrasell = False
            self.solenhbuy = []
            self.solenhsell = []

            self.cuasochinh = Tk()
            self.cuasochinh.title("BOT DCA")
            self.cuasochinh.config(bg="white")

            self.cuasochiavol = Frame(self.cuasochinh,bg="white")
            self.cuasochiavol.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)

            self.cuasoconfig = Frame(self.cuasochiavol,bg="white")
            self.cuasoconfig.pack()
            self.cuasovol = Frame(self.cuasoconfig,bg="white")
            self.cuasovol.pack(side=LEFT)
            self.cuasotp = Frame(self.cuasoconfig,bg="white")
            self.cuasotp.pack(side=LEFT)
            self.capnhat_list_volumes()
            self.capnhat_list_tp()

            option_symbols = ["XAUUSD","BTCUSD"]
            self.value_inside = StringVar(self.cuasochinh)
            self.value_inside.set(option_symbols[0])
            self.symbol_menu = OptionMenu(self.cuasochiavol, self.value_inside, *option_symbols) 
            self.symbol_menu.pack() 

            Button(self.cuasochiavol, text="Tài khoản gốc",font=("Helvetica",10,"bold"),width=10,command=lambda:self.chon_file(self.duongdangoc)).pack(fill=X,pady=10)
            self.duongdangoc = Entry(self.cuasochiavol,width=12,relief=SUNKEN)
            self.duongdangoc.pack(fill=X,pady=10)
            Button(self.cuasochiavol, text="Bắt đầu",width=10,font=("Helvetica",14,"bold"),bg="white",command=self.khoidongtkgoc).pack()

            self.manhinhchinh = Frame(self.cuasochinh,bg="white")
            self.manhinhchinh.pack(side=RIGHT, padx=5, pady=5 , anchor=N)
            
            self.manhinhketnoi = Frame(self.manhinhchinh,bg="white")
            self.manhinhketnoi.pack(padx=5, pady=5 , anchor=N)
            Button(self.manhinhketnoi,bg="white", text="Connect",width=10,font=("Helvetica",10,"bold"),command=self.connect_client).pack(side=LEFT,padx=5, pady=5)
            Button(self.manhinhketnoi,bg="white", text="Close All",width=10,font=("Helvetica",10,"bold"),command=self.close_all).pack(side=RIGHT,padx=5, pady=5)

            self.cuasovaolenh = Frame(self.manhinhchinh,bg="white")
            self.cuasovaolenh.pack(padx=5, pady=5 , anchor=N)

            self.cuasovaolenhtrai = Frame(self.cuasovaolenh,bg="white")
            self.cuasovaolenhtrai.pack(side=LEFT, padx=5, pady=5 , anchor=N)

            self.cuasovaolenhphai = Frame(self.cuasovaolenh,bg="white")
            self.cuasovaolenhphai.pack(side=RIGHT, padx=5, pady=5 , anchor=N)
            
            Label(self.cuasovaolenhtrai, text="Giá",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=0)
            Label(self.cuasovaolenhtrai, text="N",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=1)
            Label(self.cuasovaolenhtrai, text="DCA",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=2)
            Label(self.cuasovaolenhtrai, text="STL",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=3)

            self.gianhapvaobuy = Entry(self.cuasovaolenhtrai,width=12,relief=SUNKEN)
            self.gianhapvaobuy.grid(row=2, column=0)
            self.nnhapvaobuy = Entry(self.cuasovaolenhtrai,width=12,relief=SUNKEN)
            self.nnhapvaobuy.grid(row=2, column=1)
            self.dcanhapvaobuy = Entry(self.cuasovaolenhtrai,width=12,relief=SUNKEN)
            self.dcanhapvaobuy.grid(row=2, column=2)
            self.stlnhapvaobuy = Entry(self.cuasovaolenhtrai,width=12,relief=SUNKEN)
            self.stlnhapvaobuy.grid(row=2, column=3)

            Label(self.cuasovaolenhphai, text="Giá",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=0)
            Label(self.cuasovaolenhphai, text="N",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=1)
            Label(self.cuasovaolenhphai, text="DCA",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=2)
            Label(self.cuasovaolenhphai, text="STL",width=10,font=("Helvetica",10,"bold"),bg="white").grid(row=1, column=3)

            self.gianhapvaosell = Entry(self.cuasovaolenhphai,width=12,relief=SUNKEN)
            self.gianhapvaosell.grid(row=2, column=0)
            self.nnhapvaosell = Entry(self.cuasovaolenhphai,width=12,relief=SUNKEN)
            self.nnhapvaosell.grid(row=2, column=1)
            self.dcanhapvaosell = Entry(self.cuasovaolenhphai,width=12,relief=SUNKEN)
            self.dcanhapvaosell.grid(row=2, column=2)
            self.stlnhapvaosell = Entry(self.cuasovaolenhphai,width=12,relief=SUNKEN)
            self.stlnhapvaosell.grid(row=2, column=3)

            Button(self.cuasovaolenhtrai, bg="green", fg="white", text="Buy Limit",width=10,font=("Helvetica",10,"bold"),command=self.buy_limit).grid(row=0, column=0, padx=5, pady=5)
            Button(self.cuasovaolenhtrai, bg="green", fg="white", text="Close Buy",width=10,font=("Helvetica",10,"bold"),command=self.close_all_buy).grid(row=0, column=3, padx=5, pady=5)
            Button(self.cuasovaolenhphai, bg="red", fg="white", text="Sell Limit",width=10,font=("Helvetica",10,"bold"),command=self.sell_limit).grid(row=0, column=0, padx=5, pady=5)
            Button(self.cuasovaolenhphai, bg="red", fg="white", text="Close Sell",width=10,font=("Helvetica",10,"bold"),command=self.close_all_sell).grid(row=0, column=3, padx=5, pady=5)

            Button(self.cuasovaolenhtrai, bg="white",text="STL",width=10,font=("Helvetica",10,"bold"), command=self.set_stl_buy).grid(row=3, column=0, padx=5, pady=5)
            self.new_stl_set_buy = Entry(self.cuasovaolenhtrai,width=8)
            self.new_stl_set_buy.grid(row=3, column=1)
            Button(self.cuasovaolenhtrai, bg="white", text="TP",width=10,font=("Helvetica",10,"bold"), command=self.set_tp_buy).grid(row=3, column=2, padx=5, pady=5)
            self.new_tp_set_buy = Entry(self.cuasovaolenhtrai,width=8)
            self.new_tp_set_buy.grid(row=3, column=3)

            Button(self.cuasovaolenhphai, bg="white",text="STL",width=10,font=("Helvetica",10,"bold"), command=self.set_stl_sell).grid(row=3, column=0, padx=5, pady=5)
            self.new_stl_set_sell = Entry(self.cuasovaolenhphai,width=8)
            self.new_stl_set_sell.grid(row=3, column=1)
            Button(self.cuasovaolenhphai, bg="white", text="TP",width=10,font=("Helvetica",10,"bold"), command=self.set_tp_sell).grid(row=3, column=2, padx=5, pady=5)
            self.new_tp_set_sell = Entry(self.cuasovaolenhphai,width=8)
            self.new_tp_set_sell.grid(row=3, column=3)

            Label(self.cuasovaolenhtrai, text="",bg="white").grid(row=9, column=0)
            Label(self.cuasovaolenhphai, text="",bg="white").grid(row=9, column=0)
            
            self.nhapduongdan1 = Entry(self.cuasovaolenhtrai, width=50)
            self.nhapduongdan1.grid(row=10, column=0,columnspan=4, pady=5)
            self.button_browse1 = Button(self.cuasovaolenhtrai, bg="white", text="Tài khoản 1",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan1))
            self.button_browse1.grid(row=10, column=4, pady=5)

            self.nhapduongdan2 = Entry(self.cuasovaolenhtrai, width=50)
            self.nhapduongdan2.grid(row=11, column=0,columnspan=4, pady=5)
            self.button_browse2 = Button(self.cuasovaolenhtrai, bg="white", text="Tài khoản 2",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan2))
            self.button_browse2.grid(row=11, column=4, pady=5)

            self.nhapduongdan3 = Entry(self.cuasovaolenhtrai, width=50)
            self.nhapduongdan3.grid(row=12, column=0,columnspan=4, pady=5)
            self.button_browse3 = Button(self.cuasovaolenhtrai, bg="white", text="Tài khoản 3",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan3))
            self.button_browse3.grid(row=12, column=4, pady=5)

            self.nhapduongdan4 = Entry(self.cuasovaolenhtrai, width=50)
            self.nhapduongdan4.grid(row=13, column=0,columnspan=4, pady=5)
            self.button_browse4 = Button(self.cuasovaolenhtrai, bg="white", text="Tài khoản 4",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan4))
            self.button_browse4.grid(row=13, column=4, pady=5)

            self.nhapduongdan5 = Entry(self.cuasovaolenhtrai, width=50)
            self.nhapduongdan5.grid(row=14, column=0,columnspan=4, pady=5)
            self.button_browse5 = Button(self.cuasovaolenhtrai, bg="white", text="Tài khoản 5",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan5))
            self.button_browse5.grid(row=14, column=4, pady=5)

            self.nhapduongdan6 = Entry(self.cuasovaolenhphai, width=50)
            self.nhapduongdan6.grid(row=10, column=0,columnspan=4, pady=5)
            self.button_browse6 = Button(self.cuasovaolenhphai, bg="white", text="Tài khoản 6",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan6))
            self.button_browse6.grid(row=10, column=4, pady=5)

            self.nhapduongdan7 = Entry(self.cuasovaolenhphai, width=50)
            self.nhapduongdan7.grid(row=11, column=0,columnspan=4, pady=5)
            self.button_browse7 = Button(self.cuasovaolenhphai, bg="white", text="Tài khoản 7",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan7))
            self.button_browse7.grid(row=11, column=4, pady=5)

            self.nhapduongdan8 = Entry(self.cuasovaolenhphai, width=50)
            self.nhapduongdan8.grid(row=12, column=0,columnspan=4, pady=5)
            self.button_browse8 = Button(self.cuasovaolenhphai, bg="white", text="Tài khoản 8",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan8))
            self.button_browse8.grid(row=12, column=4, pady=5)

            self.nhapduongdan9 = Entry(self.cuasovaolenhphai, width=50)
            self.nhapduongdan9.grid(row=13, column=0,columnspan=4, pady=5)
            self.button_browse9 = Button(self.cuasovaolenhphai, bg="white", text="Tài khoản 9",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan9))
            self.button_browse9.grid(row=13, column=4, pady=5)

            self.nhapduongdan10 = Entry(self.cuasovaolenhphai, width=50)
            self.nhapduongdan10.grid(row=14, column=0,columnspan=4, pady=5)
            self.button_browse10 = Button(self.cuasovaolenhphai, bg="white", text="Tài khoản 10",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan10))
            self.button_browse10.grid(row=14, column=4, pady=5)

            self.manhinhduoi = Frame(self.manhinhchinh,bg="white")
            self.manhinhduoi.pack(padx=5, pady=5, anchor=N, fill=X)

            self.thongbaoloi = Label(self.manhinhduoi, text="ERROR: ",fg="red",font=("Helvetica",10,"bold"),bg="white")
            self.thongbaoloi.pack(side=LEFT, anchor=S, padx=5, pady=5)

            with open('log.txt', 'w') as f:
                f.write("")

            self.cuasochinh.mainloop()
        except Exception as e:
            mainwindow = Tk()
            mainwindow.title("ERROR")
            mainwindow.geometry("300x100")
            Label(mainwindow, text=e,font=("Helvetica",10,"bold")).pack()
            mainwindow.mainloop()
    
    def khoidongtkgoc(self):
        try:
            path = self.duongdangoc.get()
            if path != "":
                mt5.initialize(path=path)
                thongtintaikhoan = mt5.account_info()
                Label(self.cuasochiavol, text=f"ID: {thongtintaikhoan.login}",font=("Helvetica",10,"bold"),bg="white").pack(anchor=W)
                Label(self.cuasochiavol, text=f"SERVER: {thongtintaikhoan.server}",font=("Helvetica",10,"bold"),bg="white").pack(anchor=W)
                Label(self.cuasochiavol, text=f"BALANCE: {thongtintaikhoan.balance}",font=("Helvetica",10,"bold"),bg="white").pack(anchor=W)

                number_order = mt5.orders_get()
                if number_order: 
                    Label(self.cuasochiavol, text=f"NTicket: {str(number_order[0].ticket)}",font=("Helvetica",10,"bold"),bg="white").pack(anchor=W)
                else:
                    Label(self.cuasochiavol, text=f"NTicket: ",font=("Helvetica",10,"bold"),bg="white").pack(anchor=W)
        except Exception as e:
            print(e)
    def ghilog(self,noidung):
        self.savelog(noidung)

    def savelog(self,noidung):
        with open('log.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {noidung}\n")

    def lay_danhsach_volume(self):
        list_volumes = [float(vol) for vol in self.docconfig['default']['list_volumes'].split(",")]
        return list_volumes
    
    def lay_danhsach_tp(self):
        list_tp = [float(vol) for vol in self.docconfig['default']['list_tp'].split(",")]
        return list_tp
    
    def save_list_volumes(self, new_list_volumes):

        self.docconfig['default']['list_volumes'] = ",".join([str(vol) for vol in new_list_volumes])
        with open('config.ini', 'w') as configfile:
            self.docconfig.write(configfile)

    def save_list_tp(self, new_list_tp):
        
        self.docconfig['default']['list_tp'] = ",".join([str(vol) for vol in new_list_tp])
        with open('config.ini', 'w') as configfile:
            self.docconfig.write(configfile)

    def config_volumes(self):

        self.cuaso_sua_chiavol = Toplevel(self.cuasochinh,bg="white")
        
        Label(self.cuaso_sua_chiavol, text="VOLUMES",font=("Helvetica",10,"bold"),bg="white").pack(fill=X,padx=5,pady=5)

        self.volnhapvao1 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao1.pack()
        self.volnhapvao2 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao2.pack()
        self.volnhapvao3 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao3.pack()
        self.volnhapvao4 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao4.pack()
        self.volnhapvao5 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao5.pack()
        self.volnhapvao6 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao6.pack()
        self.volnhapvao7 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao7.pack()
        self.volnhapvao8 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao8.pack()
        self.volnhapvao9 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao9.pack()
        self.volnhapvao10 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao10.pack()
        self.volnhapvao11 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao11.pack()
        self.volnhapvao12 = Entry(self.cuaso_sua_chiavol,width=10)
        self.volnhapvao12.pack()

        self.list_nhap_volumes = [self.volnhapvao1, self.volnhapvao2, self.volnhapvao3, self.volnhapvao4, self.volnhapvao5, self.volnhapvao6, self.volnhapvao7, self.volnhapvao8, self.volnhapvao9, self.volnhapvao10, self.volnhapvao11, self.volnhapvao12]

        for i in range(len(self.list_nhap_volumes)):
            self.list_nhap_volumes[i].insert(0, self.danhsachvolume[i])

        Button(self.cuaso_sua_chiavol, bg="white", text="Lưu",font=("Helvetica",10,"bold"), command=self.luu_list_volumes).pack(padx=5,pady=5,fill=X)

    def config_tp(self):
        self.cuaso_sua_tp = Toplevel(self.cuasochinh,bg="white")
        
        Label(self.cuaso_sua_tp, text="TP",font=("Helvetica",10,"bold"),bg="white").pack(fill=X,padx=5,pady=5)

        self.tpnhapvao1 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao1.pack()
        self.tpnhapvao2 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao2.pack()
        self.tpnhapvao3 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao3.pack()
        self.tpnhapvao4 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao4.pack()
        self.tpnhapvao5 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao5.pack()
        self.tpnhapvao6 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao6.pack()
        self.tpnhapvao7 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao7.pack()
        self.tpnhapvao8 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao8.pack()
        self.tpnhapvao9 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao9.pack()
        self.tpnhapvao10 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao10.pack()
        self.tpnhapvao11 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao11.pack()
        self.tpnhapvao12 = Entry(self.cuaso_sua_tp,width=10)
        self.tpnhapvao12.pack()

        self.list_nhap_tp = [self.tpnhapvao1, self.tpnhapvao2, self.tpnhapvao3, self.tpnhapvao4, self.tpnhapvao5, self.tpnhapvao6, self.tpnhapvao7, self.tpnhapvao8, self.tpnhapvao9, self.tpnhapvao10, self.tpnhapvao11, self.tpnhapvao12]

        for i in range(len(self.list_nhap_tp)):
            self.list_nhap_tp[i].insert(0, self.danhsachtp[i])
        Button(self.cuaso_sua_tp, bg="white", text="Lưu",font=("Helvetica",10,"bold"), command=self.luu_list_tp).pack(padx=5,pady=5,fill=X)

    def chon_file(self,nhapduongdan):
        filepath = filedialog.askopenfilename(title="Tài khoản", filetypes=[("Application Files", "*.exe")])
        self.chon_terminal(filepath, nhapduongdan)

    def chon_terminal(self, filepath:str, nhapduongdan:Entry):

        if filepath:
            nhapduongdan.delete(0, 'end')
            nhapduongdan.insert(0, filepath)

    def luu_list_volumes(self):

        new_list_volumes = []
        for nhap_volume in self.list_nhap_volumes:
            new_vol = nhap_volume.get()
            if new_vol:
                new_list_volumes.append(new_vol)
        self.save_list_volumes(new_list_volumes)
        self.danhsachvolume = self.lay_danhsach_volume()
        self.cuaso_sua_chiavol.destroy()
        self.capnhat_list_volumes()
    
    def luu_list_tp(self):

        new_list_tp = []
        for nhap_tp in self.list_nhap_tp:
            new_tp = nhap_tp.get()
            if new_tp:
                new_list_tp.append(new_tp)
        self.save_list_tp(new_list_tp)
        self.danhsachtp = self.lay_danhsach_tp()
        self.cuaso_sua_tp.destroy()
        self.capnhat_list_tp()

    def capnhat_list_volumes(self):

        for widget in self.cuasovol.winfo_children():
            widget.destroy()

        for i in range(len(self.danhsachvolume)):
            Label(self.cuasovol,text=self.danhsachvolume[i],relief=SUNKEN,width=10,bg="white",fg="black",font=("Helvetica",10,"bold")).pack()
        Button(self.cuasovol, bg="white", text="Sửa",font=("Helvetica",10,"bold"),width=10,command=self.config_volumes).pack()

    def capnhat_list_tp(self):
        for widget in self.cuasotp.winfo_children():
            widget.destroy()

        for i in range(len(self.danhsachtp)):
            Label(self.cuasotp,text=self.danhsachtp[i],relief=SUNKEN,width=10,bg="white",fg="black",font=("Helvetica",10,"bold")).pack()

        Button(self.cuasotp, bg="white", text="Sửa",font=("Helvetica",10,"bold"),width=10,command=self.config_tp).pack()

    def connect_client(self):
        try:
            self.cacaccount = {}
            path1 = self.nhapduongdan1.get()
            path2 = self.nhapduongdan2.get()
            path3 = self.nhapduongdan3.get()
            path4 = self.nhapduongdan4.get()
            path5 = self.nhapduongdan5.get()
            path6 = self.nhapduongdan6.get()
            path7 = self.nhapduongdan7.get()
            path8 = self.nhapduongdan8.get()
            path9 = self.nhapduongdan9.get()
            path10 = self.nhapduongdan10.get()
            x = 1
            for path in [path1, path2, path3, path4, path5, path6, path7, path8, path9, path10]:
                if path:
                    mt5.initialize(path=path)
                    self.cacaccount[f"account{x}"]={
                        "path":path,
                        "trangthaibuy":0,
                        "trangthaisell":0,
                        "solenhbuycu":0,
                        "solenhbuymoi":0,
                        "solenhsellcu":0,
                        "solenhsellmoi":0,
                        }
                    x+=1
            
        except Exception as e:
            print(e)
        
    def close_all(self):
        for acc in self.cacaccount:
            self.close_all_path(acc, 'buy')
            self.close_all_path(acc, 'sell')     
        self.kiemtrabuy = False
        self.kiemtrasell = False
        self.solenhbuy.clear()
        self.solenhsell.clear()
    
    def close_all_buy(self):
        # print(self.cacaccount)
        for acc in self.cacaccount:
            self.close_all_path(acc,'buy')     
        self.kiemtrabuy = False
        self.solenhbuy.clear()

    def close_all_sell(self):
        for acc in self.cacaccount:
            self.close_all_path(acc,'sell')     
        self.kiemtrasell = False
        self.solenhsell.clear()

    def buy_limit(self):
        try:
            self.kiemtrabuy = False
            self.solenhbuy.clear()
            symbolnhapvao = self.value_inside.get()
            if not symbolnhapvao:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn cặp tiền !!!")
                return
            try:
                gianhapvaobuy = round(float(self.gianhapvaobuy.get()),3)
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn giá mua là số !!!")
                return
            try:
                nnhapvaobuy = int(self.nnhapvaobuy.get())
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn volume bắt đầu là số !!!")
                return
            try:
                dcanhapvaobuy = float(self.dcanhapvaobuy.get())
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn DCA bắt đầu là số !!!")
                return
            try:
                stlnhapvaobuy = float(self.stlnhapvaobuy.get())
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn SL bắt đầu là số !!!")
                return
            side = "buy"
            self.close_all_buy()
            for acc in self.cacaccount:
                self.batdaudatlenh(acc,symbolnhapvao,gianhapvaobuy,nnhapvaobuy,dcanhapvaobuy,stlnhapvaobuy,side)
            for acc in self.cacaccount:    
                self.cacaccount[acc]['trangthaibuy'] = 1
            self.kiemtrabuy = True
            Thread(target=lambda:self.quansatbuy()).start()
        except Exception as e:
            print(e)

    def sell_limit(self):
        try:
            self.kiemtrasell = False
            self.solenhsell.clear()
            symbolnhapvao = self.value_inside.get()
            if not symbolnhapvao:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn cặp tiền !!!")
                return
            try:
                gianhapvaosell = round(float(self.gianhapvaosell.get()),3)
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn giá mua là số !!!")
                return
            try:
                nnhapvaosell = int(self.nnhapvaosell.get())
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn volume bắt đầu là số !!!")
                return
            try:
                dcanhapvaosell = float(self.dcanhapvaosell.get())
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn DCA bắt đầu là số !!!")
                return
            try:
                stlnhapvaosell = float(self.stlnhapvaosell.get())
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn SL bắt đầu là số !!!")
                return
            side = "sell"
            self.close_all_sell()
            for acc in self.cacaccount:
                self.batdaudatlenh(acc,symbolnhapvao,gianhapvaosell,nnhapvaosell,dcanhapvaosell,stlnhapvaosell,side)
            for acc in self.cacaccount:
                self.cacaccount[acc]['trangthaisell'] = 1
            self.kiemtrasell = True
            Thread(target=lambda:self.quansatsell()).start()
        except Exception as e:
            print(e)

    def datlenh(self,acc,symbol,gia,vol,sl,tp,side):
        try:
            mt5.initialize(path=self.cacaccount[acc]['path'])
            symbol_name = mt5.symbols_get(symbol)[0].name
            result = mt5.order_send({
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol_name,
                "volume": vol,
                "type": mt5.ORDER_TYPE_BUY_LIMIT if side == "buy" else mt5.ORDER_TYPE_SELL_LIMIT,
                "sl": sl,
                "tp": tp,
                "price": gia,
                "comment": "DCABOT",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK
            })
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                return result.order
            else:
                return 0
        except Exception as e:
            print(e)

    def batdaudatlenh(self,acc,symbolnhapvao,gianhapvao,nnhapvao,dcanhapvao,stlnhapvao,side):
        try:
            listvol = self.lay_danhsach_volume()
            listtp = self.lay_danhsach_tp()
            for i in range(len(listvol)):
                if side == "buy":
                    self.solenhbuy.append({"acc":acc, "index":i, "volume": listvol[i], "tp": listtp[i], "ticket": 0})
                else:
                    self.solenhsell.append({"acc":acc, "index":i, "volume": listvol[i], "tp": listtp[i], "ticket": 0})
            # print(self.solenh)
            sl = gianhapvao - stlnhapvao if side == "buy" else gianhapvao + stlnhapvao
            if side == "buy":
                for lenh in self.solenhbuy:
                    if lenh['acc'] == acc and lenh['index'] >= nnhapvao:
                        tp = gianhapvao + lenh['tp']
                        ticket = self.datlenh(acc,symbolnhapvao,gianhapvao,lenh['volume'],sl,tp,side)
                        lenh['ticket'] = ticket
                        gianhapvao = gianhapvao - dcanhapvao
            else:
                for lenh in self.solenhsell:
                    if lenh['acc'] == acc and lenh['index'] >= nnhapvao:
                        tp = gianhapvao - lenh['tp']
                        ticket = self.datlenh(acc,symbolnhapvao,gianhapvao,lenh['volume'],sl,tp,side)
                        lenh['ticket'] = ticket
                        gianhapvao = gianhapvao + dcanhapvao
            # print(self.solenhbuy,self.solenhsell)
        except Exception as e:
            print(e)

    def thaydoi_tp(self, position, new_tp):
        try:
            if new_tp != position.tp and position.comment == "DCABOT":
                request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol":  position.symbol,
                        "position": position.ticket,
                        "price": position.price_open,
                        "sl": position.sl,
                        "tp": new_tp,
                        "comment": "DCABOT",
                        "type_time": mt5.ORDER_TIME_GTC,
                    }
                mt5.order_send(request)
            self.ghilog(f"Thay doi tp lenh {position.ticket} thanh cong")
        except Exception as e:
            print(e)
            
    def thaydoi_sl(self, position, new_sl):
        try:
            if new_sl != position.tp and position.comment == "DCABOT":
                request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol":  position.symbol,
                        "position": position.ticket,
                        "price": position.price_open,
                        "sl": new_sl,
                        "tp": position.tp,
                        "comment": "DCABOT",
                        "type_time": mt5.ORDER_TIME_GTC,
                    }
                mt5.order_send(request)
            self.ghilog(f"Thay doi sl lenh {position.ticket} thanh cong")
        except Exception as e:
            print(e)

    def set_stl_buy(self):
        try:
            new_sl = self.new_stl_set_buy.get()
            if new_stl:
                try:
                    new_stl = float(new_stl)
                except:
                    messagebox.showerror("Cảnh báo", "Vui lòng chọn sl là số !!!")
                for path in self.cacaccount:
                    mt5.initialize(path=path['path'])
                    for position in mt5.positions_get():
                        if position.comment == "DCABOT" and position.type == 0:
                            self.thaydoi_sl(position, new_sl)
                    
            else:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn sl mới !!!")
        except Exception as e:
            print(e)

    def set_stl_sell(self):
        try:
            new_sl = self.new_stl_set_sell.get()
            if new_stl:
                try:
                    new_stl = float(new_stl)
                except:
                    messagebox.showerror("Cảnh báo", "Vui lòng chọn sl là số !!!")
                for path in self.cacaccount: 
                    mt5.initialize(path=path['path'])
                    for position in mt5.positions_get():
                        if position.comment == "DCABOT" and position.type == 1:
                            self.thaydoi_sl(position, new_sl)
                    
            else:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn sl mới !!!")
        except Exception as e:
            print(e)

    def set_tp_buy(self):
        try:
            new_tp = self.new_tp_set_buy.get()
            if new_tp:
                try:
                    new_tp = float(new_tp)
                except:
                    messagebox.showerror("Cảnh báo", "Vui lòng chọn tp là số !!!")
                for path in self.cacaccount:
                    mt5.initialize(path=self.cacaccount[path]['path'])
                    for position in mt5.positions_get():
                        if position.comment == "DCABOT" and position.type == 0:
                            self.thaydoi_tp(position, new_tp)
                    
            else:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn tp mới !!!")

        except Exception as e:  
            print(e)

    def set_tp_sell(self):
        try:
            new_tp = self.new_tp_set_sell.get()
            if new_tp:
                try:
                    new_tp = float(new_tp)
                except:
                    messagebox.showerror("Cảnh báo", "Vui lòng chọn tp là số !!!")
                for path in self.cacaccount:
                    mt5.initialize(path=self.cacaccount[path]['path'])
                    for position in mt5.positions_get():
                        if position.comment == "DCABOT":
                            self.thaydoi_tp(position, new_tp)
                    
            else:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn tp mới !!!")

        except Exception as e: 
            print(e)

    def close_all_path(self, acc, side):
        try:
            if side == "buy":
                self.kiemtrabuy = False  
                self.cacaccount[acc]['trangthaibuy'] = 0
            else:
                self.kiemtrasell = False
                self.cacaccount[acc]['trangthaisell'] = 0
            
            type_position = 0 if side == "buy" else 1
            type_order = 2 if side == "buy" else 3
            mt5.initialize(path=self.cacaccount[acc]['path'])
            positions = mt5.positions_get()
            # print(acc, positions)
            if positions:
                for position in positions:
                    if position.comment == "DCABOT" and position.type == type_position:
                        mt5.Close(symbol=position.symbol,ticket=position.ticket)

            orders = mt5.orders_get()
            # print(acc, orders)
            if orders:
                for order in mt5.orders_get():
                    if order.comment == "DCABOT" and order.type == type_order:
                        mt5.order_send({'action':mt5.TRADE_ACTION_REMOVE,'order':order.ticket})

        except Exception as e:
            print(e)

    def quansatbuy(self):
        """
        Mỗi 5 giây kiểm tra các vị thế trên sàn của từng account.
        Nếu số lượng vị thế tăng, tức là có lệnh khớp mới, tính toán tp mới theo lệnh mới nhất này, thay đổi tp các vị thế còn lại theo tp mới.
        Nếu số lượng giảm, tức là có lệnh hit SL/TP, đóng hết lệnh còn lại.
        """
        while self.kiemtrabuy:
            
            # print(f"accounts: {self.cacaccount}")
            # print(f"so lenh buy: {self.solenhbuy}")
            for account in self.cacaccount:
                print(self.cacaccount[account])
                # Nếu trạng thái là đã đặt lệnh
                if self.cacaccount[account]['trangthaibuy'] == 1:
                    # profit = 0.0
                    mt5.initialize(path=self.cacaccount[account]['path'])
                    positions = mt5.positions_get()
                    # if positions:
                    #     self.ghilog(f"{account}: positions {len(positions)}")
                    bot_positions = [pos for pos in positions if pos.comment == "DCABOT" and pos.type == 0] if positions else []
                    if bot_positions:
                        print(f"{account}: byt bot positions {len(bot_positions)}")
                    so_lenhmoi = len(bot_positions) if bot_positions else 0
                    self.cacaccount[account]['solenhbuymoi'] = so_lenhmoi
                    if so_lenhmoi > 0:
                        if so_lenhmoi > self.cacaccount[account]['solenhbuycu']:
                            print(f"{account} - BUY Co lenh khop moi, thay doi TP cac lenh")
                            new_position = bot_positions[-1]
                            for lenh in self.solenhbuy:
                                if lenh['ticket'] == new_position.ticket and lenh['acc'] == account:
                                    tp = lenh['tp']
                                    if new_position.type == 0:
                                        new_tp = new_position.price_open + tp  
                                    else:
                                        new_tp = new_position.tp

                                    for position in bot_positions:
                                        self.thaydoi_tp(position, new_tp) 

                        if so_lenhmoi < self.cacaccount[account]['solenhbuycu']:
                            print(f"{account} - BUY Co lenh hit SL/TP, dong tat ca lenh")
                            self.close_all_path(account, "buy")

                    else:
                        if so_lenhmoi < self.cacaccount[account]['solenhbuycu']:
                            print(f"{account} - BUY Co lenh hit SL/TP, dong tat ca lenh")
                            self.close_all_path(account, "buy")

                    self.cacaccount[account]['solenhbuycu'] = self.cacaccount[account]['solenhbuymoi'] 
                    # profit = 0.0

                else:
                    self.cacaccount[account]['solenhbuycu'] = 0

            sleep(5)
    def quansatsell(self):
        """
        Mỗi 5 giây kiểm tra các vị thế trên sàn của từng account.
        Nếu số lượng vị thế tăng, tức là có lệnh khớp mới, tính toán tp mới theo lệnh mới nhất này, thay đổi tp các vị thế còn lại theo tp mới.
        Nếu số lượng giảm, tức là có lệnh hit SL/TP, đóng hết lệnh còn lại.
        """
        while self.kiemtrasell:
            # print(f"accounts: {self.cacaccount}")
            # print(f"so lenh sell: {self.solenhsell}")
            for account in self.cacaccount:
                print(self.cacaccount[account])
                # Nếu trạng thái là đã đặt lệnh
                if self.cacaccount[account]['trangthaisell'] == 1:
                    # profit = 0.0
                    mt5.initialize(path=self.cacaccount[account]['path'])
                    positions = mt5.positions_get()
                    # if positions:
                    #     self.ghilog(f"{account}: positions {len(positions)}")
                    bot_positions = [pos for pos in positions if pos.comment == "DCABOT" and pos.type == 1] if positions else []
                    if bot_positions:
                        print(f"{account}: sell bot positions {len(bot_positions)}")
                    so_lenhmoi = len(bot_positions) if bot_positions else 0
                    self.cacaccount[account]['solenhsellmoi'] = so_lenhmoi
                    if so_lenhmoi > 0:
                        if so_lenhmoi > self.cacaccount[account]['solenhsellcu']:
                            print(f"{account} SELL - Co lenh khop moi, thay doi TP cac lenh")
                            new_position = bot_positions[-1]
                            for lenh in self.solenhsell:
                                if lenh['ticket'] == new_position.ticket and lenh['acc'] == account:
                                    tp = lenh['tp']
                                    if new_position.type == 0:
                                        new_tp = new_position.price_open + tp  
                                    else:
                                        new_tp = new_position.tp

                                    for position in bot_positions:
                                        self.thaydoi_tp(position, new_tp) 

                        if so_lenhmoi < self.cacaccount[account]['solenhsellcu']:
                            print(f"{account} SELL - Co lenh hit SL, dong tat ca lenh")
                            self.close_all_path(account, "sell")

                    else:
                        if so_lenhmoi < self.cacaccount[account]['solenhsellcu']:
                            print(f"{account} - Co lenh hit SL, dong tat ca lenh")
                            self.close_all_path(account, "sell")

                    self.cacaccount[account]['solenhsellcu'] = self.cacaccount[account]['solenhsellmoi'] 

                else:
                    self.cacaccount[account]['solenhsellcu'] = 0

            sleep(5)

if __name__ == "__main__":
    giaodien = GiaoDien()
