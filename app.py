from tkinter import *
from tkinter import messagebox,filedialog
import MetaTrader5 as mt5
from threading import Thread
from time import sleep
from configparser import ConfigParser

SYMBOL = "XAUUSD"

class BotDca:
    def __init__(self):

        self.docvol = ConfigParser()
        self.docvol.read('vol.ini')
        self.danhsachvolume = self.lay_danhsach_volume()
        
        # các biến toàn cục
        self.danhsachdondat = []
        self.tpmacdinh = 0.0
        self.kiemtravithe = False
        self.kiemtrakhoptp = False
        self.soluongvithe = 0

        # giao diện
        self.cuasochinh = Tk()
        self.cuasochinh.title("BOT DCA")
        self.cuasochinh.resizable(0,0)
        self.cuasochinh.config(bg="white")
        # phần chia vol
        self.cuasochiavol = Frame(self.cuasochinh,bg="white")
        self.cuasochiavol.pack(side=LEFT, padx=5, pady=5, anchor=N, fill=X)

        Label(self.cuasochiavol, text="CHIA VOL",width=10,font=("Helvetica",14,"bold"),bg="white",fg="red2").pack()
        self.cuasovol = Frame(self.cuasochiavol,bg="white")
        self.cuasovol.pack()
        self.capnhat_list_volumes()

        # phần nhập thông số 
        self.cuasovaolenh = Frame(self.cuasochinh,bg="white")
        self.cuasovaolenh.pack(side=LEFT, padx=5, pady=5 , anchor=N)
        
        # các nhãn 
        Label(self.cuasovaolenh, text="Giá",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=0)
        Label(self.cuasovaolenh, text="Vol",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=1)
        Label(self.cuasovaolenh, text="DCA",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=2)
        Label(self.cuasovaolenh, text="STL",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=3)
        Label(self.cuasovaolenh, text="TP",width=10,font=("Helvetica",10,"bold"),bg="white",fg="red2").grid(row=0, column=4)

        # các ô nhập vào
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

        Label(self.cuasovaolenh,font=("Helvetica",10,"bold"),bg="white",fg="red2",text="Max Profit/Loss($):").grid(row=2,column=0,padx=5, pady=5)
        self.max_profit_loss = Entry(self.cuasovaolenh,width=8)
        self.max_profit_loss.grid(row=2, column=1)

        Button(self.cuasovaolenh,bg="deep pink", fg="white", text="Connect",width=10,font=("Helvetica",10,"bold"),command=self.connect_client).grid(row=3, column=0, padx=5, pady=5)
        Button(self.cuasovaolenh,bg="blue2", fg="white", text="Close All",width=10,font=("Helvetica",10,"bold"),command=self.close_all).grid(row=3, column=2, padx=5, pady=5)
        
        Button(self.cuasovaolenh,bg="dark green", fg="white", text="Buy Limit",width=10,font=("Helvetica",10,"bold"),command=self.buy_limit).grid(row=4, column=1, padx=5, pady=5)
        Button(self.cuasovaolenh,bg="red3", fg="white", text="Sell Limit",width=10,font=("Helvetica",10,"bold"),command=self.sell_limit).grid(row=4, column=3, padx=5, pady=5)
       
        # nút set lại TP/SL
        Button(self.cuasovaolenh,bg="orange red", fg="white",text="STL",width=10,font=("Helvetica",10,"bold"), command=self.set_stl).grid(row=7, column=0, padx=5, pady=5)
        self.new_stl_set = Entry(self.cuasovaolenh,width=8)
        self.new_stl_set.grid(row=7, column=1)
        Button(self.cuasovaolenh,bg="royal blue", fg="white", text="TP",width=10,font=("Helvetica",10,"bold"), command=self.set_tp).grid(row=7, column=2, padx=5, pady=5)
        self.new_tp_set = Entry(self.cuasovaolenh,width=8)
        self.new_tp_set.grid(row=7, column=3)
        Label(self.cuasovaolenh, text="",).grid(row=9, column=0)
        
        # Đường dẫn tới client Mt5 đăng nhập acount có số lệnh cần đếm
        self.nhapduongdan = Entry(self.cuasovaolenh, width=50)
        self.nhapduongdan.grid(row=10, column=0,columnspan=4)
        self.button_browse = Button(self.cuasovaolenh,bg="purple4", fg="white", text="Chọn File",font=("Helvetica",10,"bold"), command=self.chon_file)
        self.button_browse.grid(row=10, column=4)

        # chạy giao diện
        self.cuasochinh.mainloop()

    def connect_client(self):

        path = self.nhapduongdan.get()
        if not path:
            messagebox.showwarning("Cảnh báo","Chọn file Mt5!")
            return
        mt5.initialize(path=path)

    def set_stl(self):

        new_stl = self.new_stl_set.get()
        if new_stl:
            for position in mt5.positions_get():
                self.sua_sl_market(position, float(new_stl))
    
    def set_tp(self):

        new_tp = self.new_tp_set.get()
        if new_tp:
            for position in mt5.positions_get():
                self.sua_tp_market(position, float(new_tp))

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

    def chon_file(self):

        self.file_path = filedialog.askopenfilename(title="Chọn File", filetypes=[("Application Files", "*.exe")])
        # Kiểm tra xem người dùng đã chọn một file chưa
        if self.file_path:
            self.nhapduongdan.delete(0, 'end')  # Xóa nội dung hiện tại (nếu có)
            self.nhapduongdan.insert(0, self.file_path)  # Hiển thị đường dẫn file trong Entry

    def buy_limit(self):

        gianhapvao = self.gianhapvao.get()
        volnhapvao = self.volnhapvao.get()
        dcanhapvao = self.dcanhapvao.get()
        stlnhapvao = self.stlnhapvao.get()
        tpnhapvao = self.tpnhapvao.get()
        side = "buy"
        self.side_order = "buy"
        self.place_order(gianhapvao,volnhapvao,dcanhapvao,stlnhapvao,tpnhapvao,side)

    def sell_limit(self):

        gianhapvao = self.gianhapvao.get()
        volnhapvao = self.volnhapvao.get()
        dcanhapvao = self.dcanhapvao.get()
        stlnhapvao = self.stlnhapvao.get()
        tpnhapvao = self.tpnhapvao.get()
        side = "sell"
        self.side_order = "sell"
        self.place_order(gianhapvao,volnhapvao,dcanhapvao,stlnhapvao,tpnhapvao,side)

    def place_order(self,gia,vol,dca,stl,tp,side):
        self.close_all()

        # Check các giá trị đưa vào có phù hợp không
        try:
            gia = round(float(gia),3)
            vol = float(vol)
            dca = float(dca)
            stl = float(stl)
            tp = float(tp)
            self.tpmacdinh = tp
        except:
            messagebox.showwarning("Cảnh báo","GIÁ, VOL, DCA, STL, TP phải là số!")
            return
        
        if vol not in self.danhsachvolume:
            messagebox.showwarning("Cảnh báo","VOL không hợp lệ!")
            return    
        
        # Lấy ra các giá trị volume cần đặt
        list_volumes = [vol for vol in self.danhsachvolume[self.danhsachvolume.index(vol):]]

        # tính toán các thông số của các lệnh cần đặt
        if side == "buy": # nếu là lệnh mua
            stoploss = gia - stl # sl nhỏ hơn giá trị mua stl giá
            takeprofit = gia + tp # tp lớn hơn giá trị mua tp giá
            for volume in list_volumes:    
                self.danhsachdondat.append( # đưa vào list_orders
                    {"side":"buy",
                    "vol":volume,
                    "price":gia,
                    "stoploss":stoploss,
                    "takeprofit":takeprofit,
                    "sl": stoploss,
                    }
                )
                gia -= dca # lệnh sau sẽ thấp hơn lệnh trước dca giá

        elif side == "sell": # nếu là lệnh bán
            stoploss = gia + stl # sl lớn hơn giá trị mua stl giá
            takeprofit = gia - tp # tp lớn nhỏ giá trị mua tp giá
            for volume in list_volumes: 
                self.danhsachdondat.append(
                    {"side":"sell",
                    "vol":volume,
                    "price":gia,
                    "stoploss":stoploss,
                    "takeprofit":takeprofit,
                    "sl": stoploss,
                    }
                )
                gia += dca # lệnh sau sẽ cao hơn lệnh trước dca giá

        path = self.nhapduongdan.get()

        if not path:

            messagebox.showwarning("Cảnh báo","Chưa chọn file Mt5!")
            return
        
        mt5.initialize(path=path)

        for order in self.danhsachdondat: # đặt các lênh đã tính toán
            request = {
                "action" : mt5.TRADE_ACTION_PENDING, # lệnh pending
                "symbol" : SYMBOL ,
                "volume" : order["vol"], 
                "type" : mt5.ORDER_TYPE_BUY_LIMIT if order["side"] == "buy" else mt5.ORDER_TYPE_SELL_LIMIT,
                "price" : order["price"],
                "sl" : order["stoploss"],
                "tp" : order["takeprofit"],
                "type_filling" : mt5.ORDER_FILLING_FOK, # kiểu khớp đặt hoặc không đặt, không chờ
                "type_time" : mt5.ORDER_TIME_GTC # thời gian tính theo giờ GTC
            }
            
            mt5.order_send(request)

        mt5.shutdown()

        # bắt đầu Thread vòng lặp kiểm tra các đơn đã đặt
        self.kiemtravithe = True

        Thread(target=self.thread_check_order).start()

    def thread_check_order(self):

        while self.kiemtravithe:
            self.check_order()
            sleep(5)

    def close_all(self):

        self.kiemtravithe = False

        path = self.nhapduongdan.get()

        if not path:
            messagebox.showwarning("Cảnh báo","Chưa chọn file Mt5!")
            return
        
        mt5.initialize(path=path)

        for order in mt5.orders_get():
            mt5.order_send({"action":mt5.TRADE_ACTION_REMOVE,"order":order.ticket})

        for order in mt5.positions_get():
            mt5.Close(symbol=SYMBOL,ticket=order.ticket)

        self.danhsachdondat.clear()

        self.tpmacdinh = 0.0

        mt5.shutdown()

    def check_order(self):
        """Kiểm tra đơn đang đặt"""

        # Kiểm tra đường dẫn đến MT5
        path = self.nhapduongdan.get()

        if not path:
            messagebox.showwarning("Cảnh báo","Chọn file Mt5!")
            return
        
        mt5.initialize(path=path)

        cacvithe = mt5.positions_get()

        if cacvithe:  
            # Nếu có position tức là đang trong trạng thái kiểm tra có lệnh nào khớp TP không
            if not self.kiemtrakhoptp:
                self.kiemtrakhoptp = True 
                
            # Nếu có thêm position thì tính toán lại TP
            if len(cacvithe) > self.soluongvithe: # số lượng vị thế tăng lên, nghĩa là có lệnh khớp mới

                self.soluongvithe = len(cacvithe) # lưu lại số position cho lền kiểm tra tiếp
                
                vithemoinhat = cacvithe[-1]
                # print(vithemoinhat.type ,vithemoinhat.price_open, self.tpmacdinh)
                tp_moi = vithemoinhat.price_open + self.tpmacdinh if vithemoinhat.type == 0 else vithemoinhat.price_open - self.tpmacdinh
                # print(tp_moi)
                for vithe in cacvithe:
                    self.sua_tp_market(vithe, tp_moi)

            elif len(cacvithe) < self.soluongvithe and self.kiemtrakhoptp: # nếu số lượng position giảm đi, tức là có lệnh hit TP/SL

                self.close_all()
                self.kiemtrakhoptp = False  
                self.kiemtravithe = False

            max_profit_loss = 0.0 if not self.max_profit_loss.get() else float(self.max_profit_loss.get())
            profit = 0.0
            if max_profit_loss > 0.0:
                for vithe in cacvithe:
                    profit += vithe.profit
                if profit >= max_profit_loss or profit <= -max_profit_loss:
                    self.close_all()
                    self.kiemtrakhoptp = False  
                    self.kiemtravithe = False
        else:
            # Nếu không có vị thế nào, mà đang kiểm tra khớp TP, tức là đã hit TP/SL hết
            if self.kiemtrakhoptp:

                self.close_all()
                self.kiemtrakhoptp = False  
                self.kiemtravithe = False
            
    def sua_order(self, order, new_tp):

        if new_tp != order.tp:

            request = {
                    "action": mt5.TRADE_ACTION_MODIFY,
                    "symbol": SYMBOL,
                    "order": order.ticket,
                    "price": order.price_open,
                    "sl": order.sl,
                    "tp": new_tp,
                    "type_time": mt5.ORDER_TIME_GTC,
                }

            result = mt5.order_send(request)

            return result.retcode

    def sua_tatca_order(self,list_orders, new_tp):

        for order in list_orders:
            self.sua_order(order, new_tp)

    def sua_tp_market(self, position, new_tp):

        if new_tp != position.tp:

            request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "symbol": SYMBOL,
                    "position": position.ticket,
                    "price": position.price_open,
                    "sl": position.sl,
                    "tp": new_tp,
                    "type_time": mt5.ORDER_TIME_GTC,
                }

            result = mt5.order_send(request)

            return result.retcode
        
    def sua_sl_market(self, position, new_sl):

        if new_sl != position.sl:

            request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "symbol": SYMBOL,
                    "position": position.ticket,
                    "price": position.price_open,
                    "sl": new_sl,
                    "tp": position.tp,
                    "type_time": mt5.ORDER_TIME_GTC,
                }

            result = mt5.order_send(request)

            return result.retcode

if __name__ == "__main__":
    app = BotDca()