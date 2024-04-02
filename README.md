# Phân Loại Rác Thải và Phát Hiện Hành Vi Vứt Rác

## Giới Thiệu
Dự án "Phân Loại Rác Thải và Phát Hiện Hành Vi Vứt Rác" sử dụng công nghệ học sâu và xử lý ảnh để tự động phân loại rác thải và phát hiện các hành vi vứt rác không đúng quy định. Dự án này nhằm góp phần vào việc giải quyết vấn đề ô nhiễm môi trường và nâng cao ý thức bảo vệ môi trường trong cộng đồng.

## Cài Đặt
Để cài đặt và chạy dự án, hãy thực hiện theo các bước sau:

1. Clone repo này về máy tính của bạn.
2. Cài đặt các thư viện cần thiết bằng cách chạy `pip install -r requirements.txt`.
3. Đảm bảo bạn có đủ dữ liệu để huấn luyện mô hình trong thư mục `data/`.

## Cấu Trúc Thư Mục
Dưới đây là mô tả ngắn gọn về cấu trúc thư mục trong dự án:

- `src/`: Chứa tất cả mã nguồn.
- `data_preprocessing/`: Scripts tiền xử lý dữ liệu.
- `models/`: Mô hình học sâu và các script liên quan.
- `utilities/`: Các hàm tiện ích hỗ trợ.
- `data/`: Dữ liệu hình ảnh và video.
- `notebooks/`: Jupyter notebooks cho phân tích và thử nghiệm.
- `requirements.txt`: Danh sách các thư viện cần thiết.
- `README.md`: Tài liệu này.

## Cách Sử Dụng
Hướng dẫn cách chạy các script chính:

1. **Tiền Xử Lý Dữ Liệu**: Sử dụng các script trong thư mục `data_preprocessing` để tiền xử lý hình ảnh và video.
2. **Huấn Luyện Mô Hình**: Chạy `src/models/train_model.py` để huấn luyện mô hình phân loại rác và phát hiện hành vi vứt rác.
3. **Sử Dụng Mô Hình Đã Huấn Luyện**: Dùng `src/main.py` để áp dụng các mô hình đã huấn luyện vào việc phân loại rác thải và phát hiện hành vi vứt rác.

## Đóng Góp
Chúng tôi hoan nghênh mọi đóng góp cho dự án. Để biết thêm thông tin, vui lòng xem phần "Đóng Góp" trong tài liệu.

## Liên Hệ
Nếu bạn cần trợ giúp hoặc muốn liên lạc với chúng tôi, vui lòng gửi email đến [địa chỉ email của bạn] hoặc liên hệ qua [phương thức liên lạc khác].
