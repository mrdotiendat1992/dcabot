from tkinter import *
from tkinter import messagebox,filedialog
import MetaTrader5 as mt5
from threading import Thread
from time import sleep
from configparser import ConfigParser



SYMBOL = "XAUUSD"
helv36 = ("Helvetica",14,"bold")
class BotDca:
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read('vol.ini')
        self.list_volumes = self.get_list_volumes()
        
        # các biến toàn cục
        self.list_orders = []
        self.tp_set = 0.0
        self.side_order = None
        self.run_check_order = False
        self.check_khop_tp = False
        self.position = 0

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
        self.gia = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.gia.grid(row=1, column=0)
        self.vol = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.vol.grid(row=1, column=1)
        self.dca = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.dca.grid(row=1, column=2)
        self.stl = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.stl.grid(row=1, column=3)
        self.tp = Entry(self.cuasovaolenh,width=12,relief=SUNKEN)
        self.tp.grid(row=1, column=4)

        # tạo khoảng trống
        Label(self.cuasovaolenh, text="",bg="white").grid(row=2, column=0)
        Label(self.cuasovaolenh, text="",bg="white").grid(row=3, column=0)

        # các nút vào, thoát lệnh
        Button(self.cuasovaolenh,bg="dark green", fg="white", text="Buy Limit",width=10,font=("Helvetica",10,"bold"),command=self.buy_limit).grid(row=4, column=0)
        Button(self.cuasovaolenh,bg="red3", fg="white", text="Sell Limit",width=10,font=("Helvetica",10,"bold"),command=self.sell_limit).grid(row=4, column=2)
        Button(self.cuasovaolenh,bg="blue2", fg="white", text="Close All",width=10,font=("Helvetica",10,"bold"),command=self.close_all).grid(row=4, column=4)

        # tạo khoảng trống
        Label(self.cuasovaolenh, text="",bg="white").grid(row=5, column=0)
        Label(self.cuasovaolenh, text="",bg="white").grid(row=6, column=0)

        # nút set lại TP/SL
        Button(self.cuasovaolenh,bg="orange red", fg="white",text="STL",width=10,font=("Helvetica",10,"bold"), command=self.set_stl).grid(row=7, column=0)
        self.new_stl_set = Entry(self.cuasovaolenh,width=8)
        self.new_stl_set.grid(row=7, column=1)
        Button(self.cuasovaolenh,bg="royal blue", fg="white", text="TP",width=10,font=("Helvetica",10,"bold"), command=self.set_tp).grid(row=7, column=2)
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

    def get_list_volumes(self):
        list_volumes = [float(vol) for vol in self.parser['default']['list_volumes'].split(",")]
        return list_volumes
    
    def save_list_volumes(self, new_list_volumes):
        self.parser['default']['list_volumes'] = ",".join([str(vol) for vol in new_list_volumes])
        with open('vol.ini', 'w') as configfile:
            self.parser.write(configfile)

    def config_volumes(self):
        self.cuaso_sua_chiavol = Toplevel(self.cuasochinh,bg="white")
        Label(self.cuaso_sua_chiavol, text="VOLUMES",font=("Helvetica",10,"bold"),bg="white",fg="red2").pack(fill=X,padx=5,pady=5)

        self.vol1 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol1.pack()
        self.vol2 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol2.pack()
        self.vol3 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol3.pack()
        self.vol4 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol4.pack()
        self.vol5 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol5.pack()
        self.vol6 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol6.pack()
        self.vol7 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol7.pack()
        self.vol8 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol8.pack()
        self.vol9 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol9.pack()
        self.vol10 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol10.pack()
        self.vol11 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol11.pack()
        self.vol12 = Entry(self.cuaso_sua_chiavol,width=10)
        self.vol12.pack()

        self.list_nhap_volumes = [self.vol1, self.vol2, self.vol3, self.vol4, self.vol5, self.vol6, self.vol7, self.vol8, self.vol9, self.vol10, self.vol11, self.vol12]

        for vol in self.list_volumes:
            index = self.list_volumes.index(vol)
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
        self.list_volumes = self.get_list_volumes()
        self.cuaso_sua_chiavol.destroy()
        self.capnhat_list_volumes()

    def capnhat_list_volumes(self):
        for widget in self.cuasovol.winfo_children():
            widget.destroy()
        cot1=1
        for vol in self.list_volumes[:6]:
            Label(self.cuasovol,text=vol,relief=SUNKEN,width=10,bg="white",fg="black",font=("Helvetica",10,"bold")).grid(column=0, row=cot1)
            cot1+=1
        cot2=1
        for vol in self.list_volumes[6:]:
            Label(self.cuasovol,text=vol,relief=SUNKEN,width=10,bg="white",fg="black",font=("Helvetica",10,"bold")).grid(column=1, row=cot2)
            cot2+=1
        
        Label(self.cuasovol, text="",bg="white").grid(column=0, row=7, columnspan=2)
        Button(self.cuasovol,bg="navy", fg="white", text="Sửa",font=("Helvetica",10,"bold"),width=10,command=self.config_volumes).grid(column=0, row=8, columnspan=2)

    def chon_file(self):
        """Lưu lại đường dẫn đến file exe đã chọn"""
        self.file_path = filedialog.askopenfilename(title="Chọn File", filetypes=[("Application Files", "*.exe")])
        # Kiểm tra xem người dùng đã chọn một file chưa
        if self.file_path:
            self.nhapduongdan.delete(0, 'end')  # Xóa nội dung hiện tại (nếu có)
            self.nhapduongdan.insert(0, self.file_path)  # Hiển thị đường dẫn file trong Entry

    def buy_limit(self):
        """Đọc các thông số nhập vào và đặt các lệnh buy limit"""
        gia = self.gia.get()
        vol = self.vol.get()
        dca = self.dca.get()
        stl = self.stl.get()
        tp = self.tp.get()
        side = "buy"
        self.side_order = "buy"
        self.place_order(gia,vol,dca,stl,tp,side)

    def sell_limit(self):
        """Đọc các thông số nhập vào và đặt các lệnh sell limit"""
        gia = self.gia.get()
        vol = self.vol.get()
        dca = self.dca.get()
        stl = self.stl.get()
        tp = self.tp.get()
        side = "sell"
        self.side_order = "sell"
        self.place_order(gia,vol,dca,stl,tp,side)

    def place_order(self,gia,vol,dca,stl,tp,side):
        """Đặt các lệnh theo thông số đưa vào"""

        # Check các giá trị đưa vào có phù hợp không
        try:
            gia = round(float(gia),3)
            vol = float(vol)
            dca = float(dca)
            stl = float(stl)
            tp = float(tp)
            self.tp_set = tp
        except:
            messagebox.showwarning("Cảnh báo","GIÁ, VOL, DCA, STL, TP phải là số!")
            return
        
        if vol not in self.list_volumes:
            messagebox.showwarning("Cảnh báo","VOL không hợp lệ!")
            return
        
        # Lấy ra các giá trị volume cần đặt
        list_volumes = [vol for vol in self.list_volumes[self.list_volumes.index(vol):]]

        # tính toán các thông số của các lệnh cần đặt
        if side == "buy": # nếu là lệnh mua
            stoploss = gia - stl # sl nhỏ hơn giá trị mua stl giá
            takeprofit = gia + tp # tp lớn hơn giá trị mua tp giá
            for volume in list_volumes:    
                self.list_orders.append( # đưa vào list_orders
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
                self.list_orders.append(
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

        for order in self.list_orders: # đặt các lênh đã tính toán
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
            result = mt5.order_send(request)

        mt5.shutdown()

        # bắt đầu Thread vòng lặp kiểm tra các đơn đã đặt
        self.run_check_order = True
        Thread(target=self.thread_check_order).start()

    def thread_check_order(self):
        """Taọ vong lặp kiểm tra đơn đặt"""
        while self.run_check_order:
            self.check_order()
            sleep(5)

    def close_all(self):
        self.run_check_order = False
        path = self.nhapduongdan.get()
        if not path:
            messagebox.showwarning("Cảnh báo","Chưa chọn file Mt5!")
            return
        
        mt5.initialize(path=path)

        for order in mt5.orders_get():
            mt5.order_send({"action":mt5.TRADE_ACTION_REMOVE,"order":order.ticket})
        for order in mt5.positions_get():
            mt5.Close(symbol=SYMBOL,ticket=order.ticket)

        self.list_orders.clear()
        self.tp_set = 0.0

        mt5.shutdown()

    def check_order(self):
        """Kiểm tra đơn đang đặt"""

        # Kiểm tra đường dẫn đến MT5
        path = self.nhapduongdan.get()
        if not path:
            messagebox.showwarning("Cảnh báo","Chọn file Mt5!")
            return
        mt5.initialize(path=path)
        # print("Kiểm tra positions")
        positions = mt5.positions_get()

        if positions:  
            # Nếu có position tức là đang trong trạng thái kiểm tra có lệnh nào khơp TP không
            if not self.check_khop_tp:
                self.check_khop_tp = True 
            
            # Nếu có thêm position thì tính toán lại TP
            if len(positions) > self.position:
                messagebox.showinfo("Thống báo","Có lệnh khớp mới")
                self.position = len(positions) # lưu lại số position cho lền kiểm tra tiếp
                
                # Tính toán TP cần điều chỉnh khi có lệnh khớp mới
                new_tp = 0.0
                for position in positions: # kiểm tra từng lệnh 1
                    if self.side_order == "buy": # Nếu là lệnh mua 
                        if new_tp == 0.0:
                            new_tp = position.price_open + self.tp_set
                        else:
                            new_tp = max(new_tp, position.price_open + self.tp_set) # TP mới là số lớn hơn giữa TP mới là giá mở cộng TP được nhập vào
                    else: # nếu là lệnh bán
                        if new_tp == 0.0:
                            new_tp = position.price_open - self.tp_set
                        else:
                            new_tp = min(new_tp, position.price_open - self.tp_set) # TP mới là số nhỏ hơn giữa TP mới là giá mở cộng TP được nhập vào

                # orders = mt5.orders_get()

                # self.sua_tatca_order(orders, new_tp)
                # print("Sửa TP các order thành công ")
                for position in positions:
                    self.sua_tp_market(position, new_tp)

            elif len(positions) < self.position: # nếu số lượng position giảm
                messagebox.showwarning("Hit TP/SL", "Đã khớp TP hoặc SL\nĐóng các lệnh!")
                self.close_all()
                self.check_khop_tp = False                

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