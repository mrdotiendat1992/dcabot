from tkinter import *
from tkinter import messagebox, filedialog
from threading import Thread
from time import sleep
from configparser import ConfigParser
import MetaTrader5 as mt5
from datetime import datetime

DOIDATLENH = 0
DADATLENH = 1

class GiaoDien:
    def __init__(self):
        
        self.docconfig = ConfigParser()
        self.docconfig.read('config.ini')
        self.danhsachvolume = self.lay_danhsach_volume()
        self.danhsachtp = self.lay_danhsach_tp()
        
        self.cacaccount = {}
        self.kiemtra = False
        self.solenh = []

        self.cuasochinh = Tk()
        self.cuasochinh.title("BOT DCA")
        self.cuasochinh.config(bg="white")

        self.cuasochiavol = Frame(self.cuasochinh,bg="white")
        self.cuasochiavol.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)

        Button(self.cuasochiavol, text="START",width=10,font=("Helvetica",14,"bold"),bg="white",fg="red2",command=self.khoidongtkgoc).pack()
        self.cuasoconfig = Frame(self.cuasochiavol,bg="white")
        self.cuasoconfig.pack()
        self.cuasovol = Frame(self.cuasoconfig,bg="white")
        self.cuasovol.pack(side=LEFT)
        self.cuasotp = Frame(self.cuasoconfig,bg="white")
        self.cuasotp.pack(side=LEFT)
        self.capnhat_list_volumes()
        self.capnhat_list_tp()

        Label(self.cuasochiavol, text="SYMBOL",width=10,font=("Helvetica",14,"bold"),bg="white",fg="red2").pack(pady=10)
        option_symbols = ["XAUUSD","BTCUSD"]
        self.value_inside = StringVar(self.cuasochinh)
        self.value_inside.set(option_symbols[0])
        self.symbol_menu = OptionMenu(self.cuasochiavol, self.value_inside, *option_symbols) 
        self.symbol_menu.pack() 

        Button(self.cuasochiavol, text="Path",font=("Helvetica",10,"bold"),width=10,command=lambda:self.chon_file(self.duongdangoc)).pack(fill=X,pady=10)
        self.duongdangoc = Entry(self.cuasochiavol,width=12,relief=SUNKEN)
        self.duongdangoc.pack(fill=X,pady=10)
        self.cuasovaolenh = Frame(self.cuasochinh,bg="white")
        self.cuasovaolenh.pack(side=LEFT, padx=5, pady=5 , anchor=N)
        
        Label(self.cuasovaolenh, text="Giá",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=0)
        Label(self.cuasovaolenh, text="N",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=1)
        Label(self.cuasovaolenh, text="DCA",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=2)
        Label(self.cuasovaolenh, text="STL",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=3)

        self.gianhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.gianhapvao.grid(row=1, column=0)
        self.nnhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.nnhapvao.grid(row=1, column=1)
        self.dcanhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.dcanhapvao.grid(row=1, column=2)
        self.stlnhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.stlnhapvao.grid(row=1, column=3)

        Label(self.cuasovaolenh,font=("Helvetica",10,"bold"),bg="white",fg="red2",text="Max Profit($):").grid(row=2,column=0,padx=5, pady=5)
        self.max_profit = Entry(self.cuasovaolenh,width=8)
        self.max_profit.grid(row=2, column=1)


        Label(self.cuasovaolenh,font=("Helvetica",10,"bold"),bg="white",fg="red2",text="Max Loss($):").grid(row=2,column=2,padx=5, pady=5)
        self.max_loss = Entry(self.cuasovaolenh,width=8)
        self.max_loss.grid(row=2, column=3)

        Button(self.cuasovaolenh,bg="deep pink", fg="white", text="Connect",width=10,font=("Helvetica",10,"bold"),command=self.connect_client).grid(row=3, column=0, padx=5, pady=5)
        Button(self.cuasovaolenh,bg="blue2", fg="white", text="Close All",width=10,font=("Helvetica",10,"bold"),command=self.close_all).grid(row=3, column=2, padx=5, pady=5)
        
        Button(self.cuasovaolenh,bg="dark green", fg="white", text="Buy Limit",width=10,font=("Helvetica",10,"bold"),command=self.buy_limit).grid(row=4, column=1, padx=5, pady=5)
        Button(self.cuasovaolenh,bg="red3", fg="white", text="Sell Limit",width=10,font=("Helvetica",10,"bold"),command=self.sell_limit).grid(row=4, column=3, padx=5, pady=5)
       
        Button(self.cuasovaolenh,bg="orange red", fg="white",text="STL",width=10,font=("Helvetica",10,"bold"), command=self.set_stl).grid(row=7, column=0, padx=5, pady=5)
        self.new_stl_set = Entry(self.cuasovaolenh,width=8)
        self.new_stl_set.grid(row=7, column=1)
        Button(self.cuasovaolenh,bg="royal blue", fg="white", text="TP",width=10,font=("Helvetica",10,"bold"), command=self.set_tp).grid(row=7, column=2, padx=5, pady=5)
        self.new_tp_set = Entry(self.cuasovaolenh,width=8)
        self.new_tp_set.grid(row=7, column=3)
        Label(self.cuasovaolenh, text="",bg="white").grid(row=9, column=0)
        
        self.nhapduongdan1 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan1.grid(row=10, column=0,columnspan=4, pady=5)
        self.button_browse1 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan1))
        self.button_browse1.grid(row=10, column=4, pady=5)

        self.nhapduongdan2 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan2.grid(row=11, column=0,columnspan=4, pady=5)
        self.button_browse2 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan2))
        self.button_browse2.grid(row=11, column=4, pady=5)

        self.nhapduongdan3 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan3.grid(row=12, column=0,columnspan=4, pady=5)
        self.button_browse3 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan3))
        self.button_browse3.grid(row=12, column=4, pady=5)

        self.nhapduongdan4 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan4.grid(row=13, column=0,columnspan=4, pady=5)
        self.button_browse4 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan4))
        self.button_browse4.grid(row=13, column=4, pady=5)

        self.nhapduongdan5 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan5.grid(row=14, column=0,columnspan=4, pady=5)
        self.button_browse5 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan5))
        self.button_browse5.grid(row=14, column=4, pady=5)

        self.nhapduongdan6 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan6.grid(row=15, column=0,columnspan=4, pady=5)
        self.button_browse6 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan6))
        self.button_browse6.grid(row=15, column=4, pady=5)

        self.nhapduongdan7 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan7.grid(row=16, column=0,columnspan=4, pady=5)
        self.button_browse7 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan7))
        self.button_browse7.grid(row=16, column=4, pady=5)

        self.nhapduongdan8 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan8.grid(row=17, column=0,columnspan=4, pady=5)
        self.button_browse8 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan8))
        self.button_browse8.grid(row=17, column=4, pady=5)

        self.nhapduongdan9 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan9.grid(row=18, column=0,columnspan=4, pady=5)
        self.button_browse9 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan9))
        self.button_browse9.grid(row=18, column=4, pady=5)

        self.nhapduongdan10 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan10.grid(row=19, column=0,columnspan=4, pady=5)
        self.button_browse10 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(self.nhapduongdan10))
        self.button_browse10.grid(row=19, column=4, pady=5)

        with open('log.txt', 'w') as f:
            f.write("")

        self.cuasochinh.mainloop()
    
    def khoidongtkgoc(self):
        path = self.duongdangoc.get()
        if path != "":
            mt5.initialize(path=path)
            thongtintaikhoan = mt5.account_info()
            Label(self.cuasochiavol, text=f"ID: {thongtintaikhoan.login}",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(anchor=W)
            Label(self.cuasochiavol, text=f"SERVER: {thongtintaikhoan.server}",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(anchor=W)
            Label(self.cuasochiavol, text=f"BALANCE: {thongtintaikhoan.balance}",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(anchor=W)

            number_order = mt5.orders_get()
            if number_order: 
                Label(self.cuasochiavol, text=f"NTicket: {str(number_order[0].ticket)}",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(anchor=W)
            else:
                Label(self.cuasochiavol, text=f"NTicket: ",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(anchor=W)

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
        
        Label(self.cuaso_sua_chiavol, text="VOLUMES",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(fill=X,padx=5,pady=5)

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

        Button(self.cuaso_sua_chiavol,bg="navy", fg="white", text="Lưu",font=("Helvetica",10,"bold"), command=self.luu_list_volumes).pack(padx=5,pady=5,fill=X)

    def config_tp(self):
        self.cuaso_sua_tp = Toplevel(self.cuasochinh,bg="white")
        
        Label(self.cuaso_sua_tp, text="TP",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(fill=X,padx=5,pady=5)

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
        Button(self.cuaso_sua_tp,bg="navy", fg="white", text="Lưu",font=("Helvetica",10,"bold"), command=self.luu_list_tp).pack(padx=5,pady=5,fill=X)

    def chon_file(self,nhapduongdan):
        filepath = filedialog.askopenfilename(title="Chọn File", filetypes=[("Application Files", "*.exe")])
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
        Button(self.cuasovol,bg="navy", fg="white", text="Sửa",font=("Helvetica",10,"bold"),width=10,command=self.config_volumes).pack()

    def capnhat_list_tp(self):
        for widget in self.cuasotp.winfo_children():
            widget.destroy()

        for i in range(len(self.danhsachtp)):
            Label(self.cuasotp,text=self.danhsachtp[i],relief=SUNKEN,width=10,bg="white",fg="black",font=("Helvetica",10,"bold")).pack()

        Button(self.cuasotp,bg="navy", fg="white", text="Sửa",font=("Helvetica",10,"bold"),width=10,command=self.config_tp).pack()

    def connect_client(self):
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
                    "trangthai":DOIDATLENH,
                    "solenhcu":0,
                    "solenhmoi":0,
                    "maxprofit":0.0,
                    "maxloss":0.0,
                    "side":None
                    }
                x+=1
        
    def close_all(self):
        for acc in self.cacaccount:
            self.close_all_path(acc)     
        self.kiemtra = False
        self.solenh.clear()

    def buy_limit(self):
        self.kiemtra = False
        self.solenh.clear()
        symbolnhapvao = self.value_inside.get()
        if not symbolnhapvao:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn cặp tiền !!!")
            return
        try:
            gianhapvao = round(float(self.gianhapvao.get()),3)
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn giá mua là số !!!")
            return
        try:
            nnhapvao = int(self.nnhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn volume bắt đầu là số !!!")
            return
        try:
            dcanhapvao = float(self.dcanhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn DCA bắt đầu là số !!!")
            return
        try:
            stlnhapvao = float(self.stlnhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn SL bắt đầu là số !!!")
            return
        side = "buy"
        for acc in self.cacaccount:    
            self.close_all_path(acc)
        for acc in self.cacaccount:
            self.batdaudatlenh(acc,symbolnhapvao,gianhapvao,nnhapvao,dcanhapvao,stlnhapvao,side)
        for acc in self.cacaccount:    
            self.cacaccount[acc]['trangthai'] = DADATLENH
            self.cacaccount[acc]['side'] = side
        self.kiemtra = True
        Thread(target=lambda:self.quansat()).start()

    def sell_limit(self):
        self.kiemtra = False
        self.solenh.clear()
        symbolnhapvao = self.value_inside.get()
        if not symbolnhapvao:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn cặp tiền !!!")
            return
        try:
            gianhapvao = round(float(self.gianhapvao.get()),3)
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn giá mua là số !!!")
            return
        try:
            nnhapvao = int(self.nnhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn volume bắt đầu là số !!!")
            return
        try:
            dcanhapvao = float(self.dcanhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn DCA bắt đầu là số !!!")
            return
        try:
            stlnhapvao = float(self.stlnhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn SL bắt đầu là số !!!")
            return
        side = "sell"
        for path in self.cacaccount:
            self.close_all_path(path)
        for acc in self.cacaccount:
            self.batdaudatlenh(acc,symbolnhapvao,gianhapvao,nnhapvao,dcanhapvao,stlnhapvao,side)
        for acc in self.cacaccount:
            self.cacaccount[acc]['trangthai'] = DADATLENH
            self.cacaccount[acc]['side'] = side
        self.kiemtra = True
        Thread(target=lambda:self.quansat()).start()

    def datlenh(self,acc,symbol,gia,vol,sl,tp,side):
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

    def batdaudatlenh(self,acc,symbolnhapvao,gianhapvao,nnhapvao,dcanhapvao,stlnhapvao,side):
        listvol = self.lay_danhsach_volume()
        listtp = self.lay_danhsach_tp()
        for i in range(len(listvol)):
            self.solenh.append({"acc":acc, "index":i, "volume": listvol[i], "tp": listtp[i], "ticket": 0})
        # print(self.solenh)
        sl = gianhapvao - stlnhapvao if side == "buy" else gianhapvao + stlnhapvao
        for lenh in self.solenh:
            if lenh['acc'] == acc and lenh['index'] >= nnhapvao:
                tp = gianhapvao + lenh['tp'] if side == "buy" else gianhapvao - lenh['tp']
                ticket = self.datlenh(acc,symbolnhapvao,gianhapvao,lenh['volume'],sl,tp,side)
                lenh['ticket'] = ticket
                if side == "buy":
                    gianhapvao = gianhapvao - dcanhapvao
                else:
                    gianhapvao = gianhapvao + dcanhapvao

    def thaydoi_tp(self, position, new_tp):
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

    def thaydoi_sl(self, position, new_sl):
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

    def set_stl(self):
        new_sl = self.new_stl_set.get()
        if new_stl:
            try:
                new_stl = float(new_stl)
            except:
                messagebox.showerror("Cảnh báo", "Vui lòng chọn sl là số !!!")
            for path in self.cacaccount:
                mt5.initialize(path=path['path'])
                for position in mt5.positions_get():
                    if position.comment == "DCABOT":
                        self.thaydoi_sl(position, new_sl)
                
        else:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn sl mới !!!")
                
    def set_tp(self):
        new_tp = self.new_tp_set.get()
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

    def close_all_path(self, acc):
        self.kiemtra = False
        self.cacaccount[acc]['trangthai'] = DOIDATLENH

        mt5.initialize(path=self.cacaccount[acc]['path'])
        positions = mt5.positions_get()
        if positions:
            for position in positions:
                if position.comment == "DCABOT":
                    mt5.Close(symbol=position.symbol,ticket=position.ticket)

        orders = mt5.orders_get()
        if orders:
            for order in mt5.orders_get():
                if order.comment == "DCABOT":
                    mt5.order_send({'action':mt5.TRADE_ACTION_REMOVE,'order':order.ticket})

    def quansat(self):
        """
        Mỗi 5 giây kiểm tra các vị thế trên sàn của từng account.
        Nếu số lượng vị thế tăng, tức là có lệnh khớp mới, tính toán tp mới theo lệnh mới nhất này, thay đổi tp các vị thế còn lại theo tp mới.
        Nếu số lượng giảm, tức là có lệnh hit SL/TP, đóng hết lệnh còn lại.
        """
        while self.kiemtra:
            
            maxprofit = self.max_profit.get()
            if maxprofit:
                try:
                    maxprofit = float(maxprofit)
                except:
                    maxprofit = 0.0
            else:
                maxprofit = 0.0
            for acc in self.cacaccount:
                self.cacaccount[acc]['maxprofit'] = maxprofit

            maxloss = self.max_loss.get()
            if maxloss:
                try:
                    maxloss = float(maxloss)
                except:
                    maxloss = 0.0
            else:
                maxloss = 0.0
            for acc in self.cacaccount:
                self.cacaccount[acc]['maxloss'] = maxloss
            # Với mỗi account
            for account in self.cacaccount:
                # Nếu trạng thái là đã đặt lệnh
                if self.cacaccount[account]['trangthai'] == DADATLENH:
                    profit = 0.0
                    mt5.initialize(path=self.cacaccount[account]['path'])
                    positions = mt5.positions_get()
                    if positions:
                        self.ghilog(f"{account}: positions {len(positions)}")
                    bot_positions = [pos for pos in positions if pos.comment == "DCABOT"] if positions else []
                    if bot_positions:
                        self.ghilog(f"{account}: bot_positions {len(bot_positions)}")
                    so_lenhmoi = len(bot_positions) if bot_positions else 0
                    self.cacaccount[account]['solenhmoi'] = so_lenhmoi
                    if so_lenhmoi > 0:
                        if so_lenhmoi > self.cacaccount[account]['solenhcu']:
                            self.ghilog(f"{account} - Co lenh khop moi, thay doi TP cac lenh")
                            new_position = bot_positions[-1]
                            for lenh in self.solenh:
                                if lenh['ticket'] == new_position.ticket and lenh['acc'] == account:
                                    tp = lenh['tp']
                                    if new_position.type == 0:
                                        new_tp = new_position.price_open + tp  
                                    elif new_position.type == 1:
                                        new_tp = new_position.price_open - tp
                                    else:
                                        new_tp = new_position.tp

                            for position in bot_positions:
                                self.thaydoi_tp(position, new_tp) 

                        if so_lenhmoi < self.cacaccount[account]['solenhcu']:
                            self.ghilog(f"{account} - Co lenh hit SL/TP, dong tat ca lenh")
                            self.close_all_path(account)

                        for position in bot_positions:
                            profit += position.profit

                        if self.cacaccount[account]['maxprofit'] > 0.0:
                            
                            if profit > self.cacaccount[account]['maxprofit']:
                                self.ghilog(f"{account} - Chot loi, dong tat ca lenh")
                                self.close_all_path(account)

                        if self.cacaccount[account]['maxloss'] > 0.0:
                            if profit < -self.cacaccount[account]['maxloss']:
                                self.ghilog(f"{account} - Cat lo, dong tat ca lenh")
                                self.close_all_path(account)

                    else:
                        if so_lenhmoi < self.cacaccount[account]['solenhcu']:
                            self.ghilog(f"{account} - Co lenh hit SL/TP, dong tat ca lenh")
                            self.close_all_path(account)

                    self.cacaccount[account]['solenhcu'] = self.cacaccount[account]['solenhmoi'] 
                    profit = 0.0

                else:
                    self.cacaccount[account]['solenhcu'] = 0

            sleep(5)

if __name__ == "__main__":
    giaodien = GiaoDien()
