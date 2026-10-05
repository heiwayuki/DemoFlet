
import os
import flet as ft

# cấu hình
# Danh sách tài khoản mặc định
# role: "student" = sinh viên (đăng ký / huỷ môn), "admin" = quản trị (thêm / sửa / xoá môn)
ACCOUNTS = {
    "DThU": {"password": "DThU@123", "role": "student"},
    "admin": {"password": "admin@123", "role": "admin"},
}

BLUE_BG = "#4563A5"
DARK_INPUT = "#111111"

# Ảnh nằm trong thư mục assets.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_FILE = "dthu.png"                  # logo trường
CAMPUS_FILE = "daihocdongthap.jpg"     # ảnh khung bên phải
SYSTEM_TITLE = "DThU SYSTEM"           # chữ dọc trên ảnh

# Toàn bộ văn bản hiển thị, chia theo ngôn ngữ: "vi" (Việt) và "en" (Anh)
TEXTS = {
    "vi": {
        "user": "Tài khoản",
        "pwd": "Mật khẩu",
        "login": "Đăng nhập",
        "forgot": "Quên mật khẩu?",
        "empty": "Vui lòng nhập tài khoản và mật khẩu.",     # khi để trống
        "wrong": "Sai tài khoản hoặc mật khẩu.",             # khi nhập sai
        "forgot_msg": "Vui lòng liên hệ quầy thư viện (mang theo giấy tờ tùy thân) "
                      "hoặc trung tâm máy tính để được cấp lại mật khẩu.",
        "info": "Đăng nhập lần đầu: vui lòng đổi mật khẩu sau khi đăng nhập.\n"
                "Quên mật khẩu: hãy liên hệ quầy thư viện hoặc trung tâm máy tính.",

    },
    "en": {
        "user": "Account",
        "pwd": "Password",
        "login": "Log in",
        "forgot": "Forgot password?",
        "empty": "Please enter your account and password.",
        "wrong": "Wrong account or password.",
        "forgot_msg": "Please visit the library counter (bring your ID) "
                      "or call the computer center.",
        "info": "First login: please change your password after logging in.\n"
                "Forgot password: please contact the library counter or computer center.",
    },
}


# giao diện
def build_login(page: ft.Page, on_success):
    """Dựng màn hình đăng nhập.

    page       : trang Flet hiện tại (dùng để cập nhật giao diện)
    on_success : hàm được gọi khi đăng nhập đúng, nhận vào (tên tài khoản, vai trò)
    """
    lang = {"v": "vi"}   # ngôn ngữ hiện tại (dùng dict để hàm con sửa được giá trị)

    # ---- Logo trường (căn giữa ở phần bố cục bên dưới) ----
    logo = ft.Image(src=LOGO_FILE, width=210, height=210)

    # ---- Các dòng chữ thông báo ----
    msg = ft.Text("", color="#FFD54F", size=14)    # thông báo lỗi (màu vàng)
    info = ft.Text("", color="#FFFFFF", size=15)   # đoạn hướng dẫn phía dưới

    # ---- Ô nhập tài khoản và mật khẩu ----
    user_tf = ft.TextField(
        prefix_icon=ft.Icons.PERSON, bgcolor=DARK_INPUT, color="#FFFFFF",
        border=ft.OutlineInputBorder(
            border_radius=8, side=ft.BorderSide(1, DARK_INPUT)),
        height=56, text_size=18,
        autofocus=True,      # tự đặt con trỏ vào ô này khi mở
    )
    pwd_tf = ft.TextField(
        password=True,               # ẩn ký tự khi gõ
        can_reveal_password=True,    # nút con mắt để hiện/ẩn mật khẩu
        bgcolor="#3F5C9A",
        color="#FFFFFF",
        border=ft.OutlineInputBorder(
            border_radius=8, side=ft.BorderSide(1, "#3F5C9A")),
        height=56, text_size=18,
    )

    # ---- Xử lý khi bấm "Đăng nhập" ----
    def do_login(e=None):
        t = TEXTS[lang["v"]]                  # văn bản theo ngôn ngữ hiện tại
        u = (user_tf.value or "").strip()     # bỏ khoảng trắng thừa ở tài khoản
        p = pwd_tf.value or ""
        if not u or not p:
            msg.value = t["empty"]            # thiếu tài khoản hoặc mật khẩu
        elif u in ACCOUNTS and ACCOUNTS[u]["password"] == p:
            msg.value = ""
            # đúng -> báo cho main.py chuyển màn hình, kèm vai trò của tài khoản
            on_success(u, ACCOUNTS[u]["role"])
            return
        else:
            msg.value = t["wrong"]            # sai thông tin
        page.update()

    # Xử lý khi bấm "Quên mật khẩu?"
    def do_forgot(e):
        msg.value = TEXTS[lang["v"]]["forgot_msg"]
        page.update()

    # Tạo nút bấm màu đen (dùng chung cho 2 nút)
    def make_btn(handler):
        txt = ft.Text("", color="#FFFFFF", size=16)    # chữ được gán khi chọn ngôn ngữ
        box = ft.Container(
            content=txt, bgcolor="#000000", border_radius=8, height=56,
            alignment=ft.Alignment(0, 0), on_click=handler, ink=True,
        )
        return box, txt

    login_box, login_txt = make_btn(do_login)       # nút Đăng nhập
    forgot_box, forgot_txt = make_btn(do_forgot)    # nút Quên mật khẩu

    # Phím Enter: ở ô mật khẩu -> đăng nhập; ở ô tài khoản -> nhảy sang ô mật khẩu
    async def to_password(e):
        await pwd_tf.focus()

    pwd_tf.on_submit = do_login
    user_tf.on_submit = to_password

    # Nút chọn ngôn ngữ VI | EN
    lang_vi = ft.Text("VI", size=20, color="#FFFFFF")
    lang_en = ft.Text("EN", size=20, color="#FFFFFF")

    def apply_lang(code):
        """Đổi toàn bộ chữ trên màn hình sang ngôn ngữ `code` ("vi" hoặc "en")."""
        lang["v"] = code
        t = TEXTS[code]
        user_tf.label = t["user"]
        pwd_tf.label = t["pwd"]
        login_txt.value = t["login"]
        forgot_txt.value = t["forgot"]
        info.value = t["info"]
        msg.value = ""
        # ngôn ngữ đang chọn tô màu vàng, ngôn ngữ còn lại màu trắng
        for txt, c in ((lang_vi, "vi"), (lang_en, "en")):
            txt.color = "#FFD600" if c == code else "#FFFFFF"
        page.update()

    def lang_item(txt, code):
        # Mỗi chữ ngôn ngữ là một vùng bấm được
        return ft.Container(content=txt, on_click=lambda e: apply_lang(code), padding=4)

    lang_bar = ft.Container(
        content=ft.Row(
            [lang_item(lang_vi, "vi"), ft.Text("|", size=20, color="#FFFFFF"),
             lang_item(lang_en, "en")],
            spacing=6, tight=True,
        ),
        padding=ft.Padding(left=14, top=4, right=14, bottom=4),
        bgcolor="#3F5C9A", border_radius=6,
    )

    # Khung ảnh bên phải (tự co giãn theo kích thước cửa sổ)
    # Cột chứa các chữ cái xếp dọc của SYSTEM_TITLE
    title_col = ft.Column(
        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def fill_title():
        """Vẽ lại chữ dọc, tự chọn cỡ chữ (14-44) để luôn vừa chiều cao khung."""
        h = (page.height or 800) - 120
        size = max(14, min(44, int(h / (len(SYSTEM_TITLE) * 1.3))))
        title_col.controls = [
            ft.Container(height=size * 0.6) if ch == " "
            else ft.Text(ch, size=size, weight=ft.FontWeight.BOLD, color="#4563A5")
            for ch in SYSTEM_TITLE
        ]

    fill_title()

    # Bo góc khung: góc trên-trái bo lớn (150), các góc còn lại bo nhẹ (24)
    card_radius = ft.BorderRadius(top_left=150, top_right=24, bottom_left=24, bottom_right=24)
    # Ảnh phủ kín khung (left/top/right/bottom = 0), cắt mép nếu cần (COVER)
    card_bg = ft.Image(src=CAMPUS_FILE, left=0, top=0, right=0, bottom=0, fit=ft.BoxFit.COVER)
    card = ft.Container(
        expand=True, border_radius=card_radius,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,    # cắt ảnh theo bo góc
        content=ft.Stack([
            card_bg,                                                     # lớp dưới: ảnh
            ft.Container(content=title_col, right=24, top=0, bottom=0),  # lớp trên: chữ dọc
        ]),
    )

    def on_resize(e=None):
        # Khi người dùng kéo giãn cửa sổ -> tính lại cỡ chữ dọc
        fill_title()
        page.update()

    page.on_resize = on_resize

    # Bố cục: nửa trái (form) + nửa phải (ảnh)
    left = ft.Container(
        expand=1,                                                       # chiếm 1 phần chiều rộng
        padding=ft.Padding(left=60, top=30, right=40, bottom=20),
        content=ft.Column(
            [
                # logo nằm giữa
                ft.Row([logo], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=30),                                # khoảng trống giữa logo và ô nhập
                user_tf,
                pwd_tf,
                login_box,
                forgot_box,
                ft.Row([lang_bar], alignment=ft.MainAxisAlignment.END),  # VI|EN ở góc phải
                msg,
                info,
            ],
            spacing=18, scroll=ft.ScrollMode.AUTO,
            # kéo giãn mọi ô cho bằng chiều rộng (ô nhập = nút bấm)
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )
    right = ft.Container(
        expand=1,                                                       # chiếm 1 phần còn lại (bằng nửa trái)
        padding=ft.Padding(left=0, top=30, right=40, bottom=30),
        content=ft.Column(
            [card], expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    # Khung ngoài cùng: nền xanh, chứa hai nửa trái - phải
    view = ft.Container(
        bgcolor=BLUE_BG, expand=True,
        content=ft.Row([left, right], expand=True,
                       vertical_alignment=ft.CrossAxisAlignment.STRETCH),
    )
    apply_lang("vi")                                                    # mặc định hiển thị tiếng Việt
    return view