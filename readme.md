# Tính năng

```sh
    1. Đặt hàng loạt lệnh pending với các thông số nhập vào
    2. Xoá các lệnh cũ trước khi đặt
    3. Thay đổi TP của vị thế khớp mới nhất
    4. Thay đổi TP của các vị thế khác theo vị thế khớp mới nhất
    5. Đóng tất cả các lệnh nếu có vị thế hit TP/SL
    6. Đóng tất cả lệnh nếu đạt đến số lãi/lỗ nhất định
    7. Chọn client Mt5 muốn đặt lệnh
    8. Sửa SL/TP tất cả các lệnh theo số nhập vào
    9. Chạy nhiều client 1 lúc (continue...)
```

# Cài đặt tool DCA bot Mt5

```sh
    1. Cài python 3.10.7 ![ ](image-3.png)( Đánh dấu vào ô Add python 3.10 to PATH) ![Alt text](image.png)
    2_1. Cài thư viện python: tại thư mục chưa tool click vào dòng địa chỉ nhập "cmd" ![Alt text](image-1.png)
    2_2. Nhập "pip install -r requirements.txt" ![Alt text](image-2.png)
    2_3. Nếu không chạy nhập lần lượt các lệnh: "pip install MetaTrader5" và "pip install tk"
    3. Chạy file dcabo.bat
    4. Bật chế độ cho phép chạy auto trên client Mt5
    4_1. Chọn Tool ![Alt text](image-4.png)
    4_2. Chọn Options ![Alt text](image-5.png)
    4_3. Chọn One Click Trading ở Tab Trade ![Alt text](image-6.png)
    4_4. Chọn Allow algothimic trading và bỏ chọn các ô Disable ![Alt text](image-7.png)
```