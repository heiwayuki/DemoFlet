
import flet as ft

# build_login : hàm dựng giao diện đăng nhập   (file login.py)
# build_htsv  : hàm dựng giao diện hệ thống    (file portal.py)
# ASSETS_DIR  : đường dẫn thư mục chứa hình ảnh
# BLUE_BG     : màu nền xanh của màn hình đăng nhập
from login import ASSETS_DIR, BLUE_BG, build_login
from dangkymonhoc import build_htsv


def main(page: ft.Page):
    # Cấu hình cửa sổ
    page.title = "Hệ thống đăng ký môn học"      # tiêu đề trên thanh cửa sổ
    page.padding = 0                             # bỏ lề để giao diện tràn kín cửa sổ
    page.spacing = 0
    page.window.width = 1280                     # kích thước cửa sổ khi mở
    page.window.height = 800

    # Hiển thị màn hình đăng nhập
    def show_login():
        page.clean()                            # xoá màn hình hiện tại
        page.bgcolor = BLUE_BG                  # nền xanh cho màn hình đăng nhập
        # build_login nhận hàm show_htsv: khi đăng nhập đúng sẽ gọi hàm này
        page.add(build_login(page, show_htsv))
        page.update()

    # Hiển thị màn hình hệ thống (sau khi đăng nhập)
    def show_htsv(username, role):
        page.clean()
        page.bgcolor = "#0F0F0F"                # nền tối cho màn hình hệ thống
        # role ("student" / "admin") quyết định giao diện hiển thị
        # build_htsv nhận hàm show_login: nút "Đăng xuất" sẽ gọi hàm này
        page.add(build_htsv(page, username, role, show_login))
        page.update()

    show_login()                                # khởi động: luôn bắt đầu ở màn hình đăng nhập


# Chỉ chạy khi mở trực tiếp file này (không chạy khi bị import)
if __name__ == "__main__":
    # assets_dir: báo cho Flet biết thư mục ảnh để đọc logo và ảnh nền
    ft.run(main, assets_dir=ASSETS_DIR)