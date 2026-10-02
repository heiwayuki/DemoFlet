# 🎓 Hệ Thống Đăng Ký Môn Học (DThU System)

Dự án ứng dụng Desktop/Web **Hệ thống Đăng ký Môn học & Cổng thông tin Sinh viên** được phát triển bằng ngôn ngữ **Python** và thư viện **Flet** (Flutter dành cho Python). Ứng dụng cung cấp giao diện quản lý đăng ký học phần hiện đại, trực quan, hỗ trợ phân quyền người dùng (Sinh viên và Quản trị viên), kiểm tra ràng buộc đăng ký theo thời gian thực và tự động điều chỉnh kích thước theo màn hình (Responsive).

---

## 📌 Các Tính năng Chính

### 1. 🔐 Màn hình Đăng nhập (`login.py`)
- **Đa ngôn ngữ (Multilingual):** Hỗ trợ chuyển đổi ngôn ngữ giao diện linh hoạt giữa **Tiếng Việt (`VI`)** và **Tiếng Anh (`EN`)**.
- **Giao diện tự co giãn (Responsive Layout):**
  - Tự động tính toán lại cỡ chữ hiển thị dạng dọc (`SYSTEM_TITLE = "DThU SYSTEM"`) dựa trên chiều cao cửa sổ khi người dùng kéo giãn.
  - Bố cục 2 cột cân đối (Cột trái: Form nhập liệu; Cột phải: Khung ảnh khuôn viên trường bo góc nghệ thuật).
- **Phân quyền tài khoản:**
  - **Sinh viên (`student`):** Tài khoản `DThU` / Mật khẩu `DThU@123`
  - **Quản trị viên (`admin`):** Tài khoản `admin` / Mật khẩu `admin@123`
- **Tối ưu trải nghiệm (UX):**
  - Nhấn `Enter` tại ô tài khoản để chuyển sang ô mật khẩu, nhấn `Enter` tại ô mật khẩu để đăng nhập.
  - Tích hợp nút bật/tắt ẩn hiện mật khẩu, kiểm tra bỏ trống dữ liệu, hiển thị thông báo lỗi và hướng dẫn cấp lại mật khẩu.

### 2. 👨‍🎓 Giao diện Sinh viên (`dangkymonhoc.py`)
- **Tra cứu môn học:** Hiển thị danh sách các môn học mở trong học kỳ kèm thông tin mã môn, tên môn, số tín chỉ, giảng viên, lịch học và sĩ số hiện tại.
- **Đăng ký & Hủy đăng ký môn học:**
  - **Tự động kiểm tra ràng buộc:** Chặn đăng ký khi **lớp học đã đầy sĩ số**, **vượt quá giới hạn tín chỉ** (tối đa 20 tín chỉ/sinh viên), hoặc **trùng lịch học** (trùng thứ và tiết học).
  - **Chuyển đổi Tab:** Dễ dàng chuyển đổi giữa tab *"Môn đang mở"* và *"Môn đã đăng ký"*.
  - Tô màu nền xanh lá mờ đối với các môn học đã đăng ký thành công.
- **Thống kê cá nhân:** Theo dõi tổng số môn học và tổng số tín chỉ đã đăng ký theo thời gian thực.

### 3. 👨‍💼 Giao diện Quản trị viên (`dangkymonhoc.py`)
- **Quản lý môn học (CRUD):**
  - **Thêm môn học mới:** Nhập thông tin mã môn, tên môn, số tín chỉ, giảng viên, thứ, tiết học và sĩ số tối đa. Hệ thống tự động kiểm tra trùng mã môn hoặc dữ liệu không hợp lệ.
  - **Chỉnh sửa môn học:** Cập nhật thông tin các môn học đã có.
  - **Xóa môn học:** Xóa môn học khỏi hệ thống và tự động cập nhật, loại bỏ môn đó khỏi danh sách đăng ký của tất cả sinh viên.
- **Thống kê hệ thống:** Theo dõi tổng số môn học hiện có và tổng lượt đăng ký môn của toàn bộ sinh viên.

### 4. 📅 Tiện ích & Giao diện Bổ sung
- **Bộ lịch tích hợp (Calendar Widget):** Hiển thị lịch tháng hiện tại, highlight nổi bật ngày hôm nay và ngày cuối tuần.
- **Thanh tìm kiếm linh hoạt:** Tìm kiếm môn học nhanh theo Mã môn, Tên môn học hoặc Tên giảng viên ngay khi gõ.
- **Thanh điều hướng Accordion:** Nhóm menu "Hệ thống ứng dụng" hỗ trợ đóng/mở tiện lợi.

---

## 📁 Cấu trúc Thư mục Dự án

```text
.
├── assets/                  # Thư mục tài nguyên hình ảnh
│   ├── dthu.png             # Logo trường Đại học Đồng Tháp
│   └── daihocdongthap.jpg   # Ảnh đại diện màn hình đăng nhập
├── dangkymonhoc.py          # Module giao diện & logic Đăng ký môn học / Cổng thông tin
├── login.py                 # Module giao diện & logic Đăng nhập (Login)
├── main.py                  # File khởi chạy chính của ứng dụng
└── README.md                # Tài liệu hướng dẫn sử dụng dự án# DemoFlet
