import MetaTrader5 as  mt5
from multiprocessing import Process
from time import sleep
from tkinter import *

app = Tk()

accounts = {}

list_path = [
    r"c:\Program Files\MetaTrader 5\terminal64.exe",
    r"c:\Program Files\MetaTrader 5 acc1\terminal64.exe",
    r"c:\Program Files\MetaTrader 5 acc2\terminal64.exe"
]

def place_order(path):
    for x in range(10):
        mt5.initialize(path=path)
        symbol_name = mt5.symbols_get("XAUUSD")[0].name
        mt5.order_send({
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol_name,
            "volume": (x+1)*0.1,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "price": 2010.0,
            "sl": 0.0,
            "tp": 0.0,
            "deviation": 10,
            "magic": 234000,
            "comment": "python script order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        })
        mt5.shutdown()
        x+=1

def remove_order(path):
    mt5.initialize(path=path)
    positions = mt5.positions_get()
    if positions:
        for position in positions:
            mt5.Close(symbol=position.symbol,ticket=position.ticket)
    orders = mt5.orders_get()
    if orders:
        for order in mt5.orders_get():
            mt5.order_send({"action":mt5.TRADE_ACTION_REMOVE,"order":order.ticket})
    
    mt5.shutdown()

def place_orders():
    for path in list_path:
        thread = Process(target=place_order, args=(path,))
        thread.start()

def remove_orders():
    for path in list_path:
        thread = Process(target=remove_order, args=(path,))
        thread.start()

Button(app, text="start", command=place_orders).pack()
Button(app, text="stop", command=remove_orders).pack()

if __name__ == "__main__":
    app.mainloop()