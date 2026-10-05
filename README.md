# Hệ thống đăng ký môn học – DThU System

Ứng dụng desktop đăng ký môn học viết bằng **Python** và thư viện giao diện **[Flet](https://flet.dev)**. Đây là dự án demo phục vụ giảng dạy.

## Tính năng

- **Đăng nhập** với hai vai trò: sinh viên và quản trị.
- **Sinh viên:** xem danh sách môn học, đăng ký và hủy đăng ký. Hệ thống tự chặn khi lớp đã đầy, vượt quá 20 tín chỉ hoặc trùng lịch học.
- **Quản trị:** thêm, sửa, xoá môn học.
- Tìm kiếm môn học theo mã môn, tên môn hoặc giảng viên.

## Tài khoản dùng thử

| Vai trò | Tài khoản | Mật khẩu |
|---|---|---|
| Sinh viên | `DThU` | `DThU@123` |
| Quản trị | `admin` | `admin@123` |

## Cài đặt và chạy

Yêu cầu Python 3.10 trở lên.

```bash
pip install -r requirements.txt
python main.py
```

## Cấu trúc thư mục

```text
.
├── main.py             # Điểm khởi chạy, chuyển giữa các màn hình
├── login.py            # Màn hình đăng nhập
├── portal.py           # Màn hình đăng ký môn học
├── assets/             # Hình ảnh (logo, ảnh nền)
└── requirements.txt
```

## Lưu ý

Dữ liệu chỉ lưu trong bộ nhớ nên sẽ mất khi tắt chương trình. Tài khoản được viết cố định trong mã nguồn để làm ví dụ, không dùng cho môi trường thật.
