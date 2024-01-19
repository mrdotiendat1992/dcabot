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
        
        self.docvol = ConfigParser()
        self.docvol.read('vol.ini')
        self.danhsachvolume = self.lay_danhsach_volume()
        
        self.cacaccount = {}
        self.kiemtra = 0

        self.cuasochinh = Tk()
        self.cuasochinh.title("BOT DCA")
        self.cuasochinh.resizable(0,0)
        self.cuasochinh.config(bg="white")

        self.cuasochiavol = Frame(self.cuasochinh,bg="white")
        self.cuasochiavol.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)

        Label(self.cuasochiavol, text="CHIA VOL",width=10,font=("Helvetica",14,"bold"),bg="white",fg="red2").pack()
        self.cuasovol = Frame(self.cuasochiavol,bg="white")
        self.cuasovol.pack()
        self.capnhat_list_volumes()

        Label(self.cuasochiavol, text="SYMBOL",width=10,font=("Helvetica",14,"bold"),bg="white",fg="red2").pack(pady=10)
        option_symbols = ["XAUUSD","BTCUSD"]
        self.value_inside = StringVar(self.cuasochinh)
        self.value_inside.set("Select an Symbol")
        self.symbol_menu = OptionMenu(self.cuasochiavol, self.value_inside, *option_symbols) 
        self.symbol_menu.pack() 
 
        self.cuasovaolenh = Frame(self.cuasochinh,bg="white")
        self.cuasovaolenh.pack(side=LEFT, padx=5, pady=5 , anchor=N)
        
        Label(self.cuasovaolenh, text="Giá",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=0)
        Label(self.cuasovaolenh, text="Vol",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=1)
        Label(self.cuasovaolenh, text="DCA",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=2)
        Label(self.cuasovaolenh, text="STL",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=3)
        Label(self.cuasovaolenh, text="TP",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=4)

        self.gianhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.gianhapvao.grid(row=1, column=0)
        self.volnhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.volnhapvao.grid(row=1, column=1)
        self.dcanhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.dcanhapvao.grid(row=1, column=2)
        self.stlnhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.stlnhapvao.grid(row=1, column=3)
        self.tpnhapvao = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.tpnhapvao.grid(row=1, column=4)

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
        self.button_browse1 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(1))
        self.button_browse1.grid(row=10, column=4, pady=5)

        self.nhapduongdan2 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan2.grid(row=11, column=0,columnspan=4, pady=5)
        self.button_browse2 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(2))
        self.button_browse2.grid(row=11, column=4, pady=5)

        self.nhapduongdan3 = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan3.grid(row=12, column=0,columnspan=4, pady=5)
        self.button_browse3 = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=lambda:self.chon_file(3))
        self.button_browse3.grid(row=12, column=4, pady=5)

        with open('log.txt', 'w') as f:
            f.write("")

        self.cuasochinh.mainloop()

    def ghilog(self,noidung):
        self.savelog(noidung)

    def savelog(self,noidung):
        with open('log.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {noidung}\n")

    def lay_danhsach_volume(self):
        list_volumes = [float(vol) for vol in self.docvol['default']['list_volumes'].split(",")]
        return list_volumes
    
    def save_list_volumes(self, new_list_volumes):

        self.docvol['default']['list_volumes'] = ",".join([str(vol) for vol in new_list_volumes])
        with open('vol.ini', 'w') as configfile:
            self.docvol.write(configfile)

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

        for vol in self.danhsachvolume:
            index = self.danhsachvolume.index(vol)
            self.list_nhap_volumes[index].insert(0, vol)               
        Label(self.cuaso_sua_chiavol, text="",).pack()
        Button(self.cuaso_sua_chiavol,bg="navy", fg="white", text="Lưu",font=("Helvetica",10,"bold"), command=self.luu_list_volumes).pack(padx=5,pady=5,fill=X)

    def chon_file(self,number):
        if number == 1:
            filepath1 = filedialog.askopenfilename(title="Chọn File", filetypes=[("Application Files", "*.exe")])
            self.chon_terminal(filepath1, self.nhapduongdan1)
        elif number == 2:
            filepath2 = filedialog.askopenfilename(title="Chọn File", filetypes=[("Application Files", "*.exe")])
            self.chon_terminal(filepath2, self.nhapduongdan2)
        elif number == 3:
            filepath3 = filedialog.askopenfilename(title="Chọn File", filetypes=[("Application Files", "*.exe")])
            self.chon_terminal(filepath3, self.nhapduongdan3)

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

    def capnhat_list_volumes(self):

        for widget in self.cuasovol.winfo_children():
            widget.destroy()
        cot1=1
        for vol in self.danhsachvolume[:6]:
            Label(self.cuasovol,text=vol,relief=SUNKEN,width=10,bg="white",fg="black",font=("Helvetica",10,"bold")).grid(column=0, row=cot1)
            cot1+=1
        cot2=1
        for vol in self.danhsachvolume[6:]:
            Label(self.cuasovol,text=vol,relief=SUNKEN,width=10,bg="white",fg="black",font=("Helvetica",10,"bold")).grid(column=1, row=cot2)
            cot2+=1
        
        Label(self.cuasovol, text="",bg="white").grid(column=0, row=7, columnspan=2)
        Button(self.cuasovol,bg="navy", fg="white", text="Sửa",font=("Helvetica",10,"bold"),width=10,command=self.config_volumes).grid(column=0, row=8, columnspan=2)

    def connect_client(self):
        self.cacaccount = {}
        path1 = self.nhapduongdan1.get()
        path2 = self.nhapduongdan2.get()
        path3 = self.nhapduongdan3.get()
        x = 1
        for path in [path1, path2, path3]:
            if path:
                mt5.initialize(path=path)
                self.cacaccount[f"account{x}"]={
                    "path":path,
                    "trangthai":DOIDATLENH,
                    "solenhcu":0,
                    "solenhmoi":0,
                    "tp":0.0,
                    "maxprofit":0.0,
                    "maxloss":0.0,
                    "side":None
                    }
                x+=1
        

    def close_all(self):
        for acc in self.cacaccount:
            self.close_all_path(acc)     

    def buy_limit(self):
        self.kiemtra = False
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
            volnhapvao = float(self.volnhapvao.get())
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
        try:
            tpnhapvao = float(self.tpnhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn TP bắt đầu là số !!!")
            return
        side = "buy"
        for acc in self.cacaccount:    
            self.close_all_path(acc)
        for acc in self.cacaccount:
            self.batdaudatlenh(acc,symbolnhapvao,gianhapvao,volnhapvao,dcanhapvao,stlnhapvao,tpnhapvao,side)
        for acc in self.cacaccount:    
            self.cacaccount[acc]['trangthai'] = DADATLENH
            self.cacaccount[acc]['side'] = side
            self.cacaccount[acc]['tp'] = tpnhapvao
        self.kiemtra = True
        Thread(target=lambda:self.quansat()).start()

    def sell_limit(self):
        self.kiemtra = False
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
            volnhapvao = float(self.volnhapvao.get())
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
        try:
            tpnhapvao = float(self.tpnhapvao.get())
        except:
            messagebox.showerror("Cảnh báo", "Vui lòng chọn TP bắt đầu là số !!!")
            return
        side = "sell"
        for path in self.cacaccount:
            self.close_all_path(path)
        for acc in self.cacaccount:
            self.batdaudatlenh(acc,symbolnhapvao,gianhapvao,volnhapvao,dcanhapvao,stlnhapvao,tpnhapvao,side)
        for acc in self.cacaccount:
            self.cacaccount[acc]['trangthai'] = DADATLENH
            self.cacaccount[acc]['side'] = side
            self.cacaccount[acc]['tp'] = tpnhapvao
        self.kiemtra = True
        Thread(target=lambda:self.quansat()).start()

    def datlenh(self,acc,symbol,gia,vol,sl,tp,side):
        mt5.initialize(path=self.cacaccount[acc]['path'])
        symbol_name = mt5.symbols_get(symbol)[0].name
        mt5.order_send({
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
        

    def batdaudatlenh(self,acc,symbolnhapvao,gianhapvao,volnhapvao,dcanhapvao,stlnhapvao,tpnhapvao,side):
        listvol = self.lay_danhsach_volume()
        index = listvol.index(volnhapvao)
        sl = gianhapvao - stlnhapvao if side == "buy" else gianhapvao + stlnhapvao
        for vol in listvol[index:]:
            gia = gianhapvao
            tp = gia + tpnhapvao if side == "buy" else gia - tpnhapvao
            self.datlenh(acc,symbolnhapvao,gia,vol,sl,tp,side)
            if side == "buy":
                gianhapvao -= dcanhapvao
            else:
                gianhapvao += dcanhapvao

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

    def close_all_path(self, path):
        
        mt5.initialize(path=self.cacaccount[path]['path'])
        positions = mt5.positions_get()
        if positions:
            for position in positions:
                if position.comment == "DCABOT":
                    mt5.Close(symbol=position.symbol,ticket=position.ticket)
        orders = mt5.orders_get()
        if orders:
            for order in mt5.orders_get():
                if order.comment == "DCABOT":
                    mt5.order_send({"action":mt5.TRADE_ACTION_REMOVE,"order":order.ticket})
        self.cacaccount[path]['trangthai'] = DOIDATLENH
        self.cacaccount[path]['solenhcu'] = 0

    def quansat(self):
        while self.kiemtra:
            
            maxprofit = self.max_profit.get()
            if maxprofit:
                try:
                    maxprofit = float(maxprofit)
                except:
                    maxprofit = 0.0
                finally:
                    for acc in self.cacaccount:
                        self.cacaccount[acc]['maxprofit'] = maxprofit

            maxloss = self.max_loss.get()
            if maxloss:
                try:
                    maxloss = float(maxloss)
                except:
                    maxloss = 0.0
                finally:
                    for acc in self.cacaccount:
                        self.cacaccount[acc]['maxloss'] = maxloss
            # print(self.cacaccount)
            for account in self.cacaccount:
                if self.cacaccount[account]['trangthai'] == DADATLENH:
                    mt5.initialize(path=self.cacaccount[account]['path'])
                    positions = mt5.positions_get()
                    bot_positions = []
                    profit = 0
                    if positions:
                        for position in positions:
                            if position.comment == "DCABOT":
                                bot_positions.append(position)
                        self.cacaccount[account]['solenhmoi'] = len(bot_positions)
                        if self.cacaccount[account]['solenhmoi'] > self.cacaccount[account]['solenhcu']:
                            self.ghilog(f"{account} - Co lenh khop moi, thay doi TP cac lenh")
                            new_position = bot_positions[-1]
                            new_tp = new_position.price_open + self.cacaccount[account]['tp'] if new_position.type == 0 else new_position.price_open - self.cacaccount[account]['tp']
                            for position in bot_positions:
                                self.thaydoi_tp(position, new_tp)
                        elif self.cacaccount[account]['solenhmoi'] < self.cacaccount[account]['solenhcu']:
                            self.ghilog(f"{account} - Co lenh hit SL/TP, dong tat ca lenh")
                            self.close_all_path(account)
                            self.cacaccount[account]['trangthai'] = DOIDATLENH
                        for position in bot_positions:
                            profit += position.profit
                        if self.cacaccount[account]['maxprofit'] > 0.0:
                            
                            if profit > self.cacaccount[account]['maxprofit']:
                                self.ghilog(f"{account} - Chot loi, dong tat ca lenh")
                                self.close_all_path(account)

                        elif self.cacaccount[account]['maxloss'] > 0.0:
                            if profit < -self.cacaccount[account]['maxloss']:
                                self.ghilog(f"{account} - Cat lo, dong tat ca lenh")
                                self.close_all_path(account)

                        self.cacaccount[account]['solenhcu'] = self.cacaccount[account]['solenhmoi']                
            bot_positions.clear()
            profit = 0
            sleep(3)

if __name__ == "__main__":
    giaodien = GiaoDien()