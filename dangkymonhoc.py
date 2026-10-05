"""
dangkymonhoc.py - Hệ thống ĐĂNG KÝ MÔN HỌC (hiện ra sau khi đăng nhập thành công).

Có HAI VAI TRÒ, giao diện khác nhau:
  - Sinh viên (student): xem môn đang mở, ĐĂNG KÝ / HUỶ đăng ký, xem "Môn đã đăng ký".
                         Hệ thống tự chặn khi trùng lịch, vượt tín chỉ tối đa, lớp đã đầy.
  - Quản trị (admin)   : THÊM / SỬA / XOÁ môn học, xem sĩ số từng lớp.

Bố cục:
  - Thanh trên cùng : logo, tên hệ thống, icon, lời chào, nút Đăng xuất
  - Cột trái        : menu điều hướng (theo vai trò)
  - Vùng giữa       : danh sách môn học (nội dung phụ thuộc vai trò)
  - Cột phải        : lịch tháng, ngày hôm nay, thống kê

Dữ liệu lưu trong bộ nhớ (COURSES, REGISTRATIONS): tắt chương trình là mất thay đổi.
Muốn lưu lâu dài hãy ghi ra file JSON hoặc cơ sở dữ liệu.
"""
import calendar
import datetime
import flet as ft

# cấu hình
GREEN_TEXT = "#4CD137"
PANEL_DARK = "#141414"
TOPBAR = "#555555"

# TỈ LỆ GIAO DIỆN: 1.0 = kích thước gốc.
SCALE = 0.7

# Số tín chỉ tối đa một sinh viên được đăng ký
MAX_CREDITS = 20


def s(x):
    return max(1, round(x * SCALE))


LOGO_FILE = "dthu.png"                                              # logo trường, lấy từ thư mục assets

ROLE_LABEL = {"student": "Sinh viên", "admin": "Quản trị"}

# Menu "Liên kết nhanh" theo vai trò (chỉ hiển thị, trừ các mục có gắn chức năng)
QUICK_LINKS = {
    "student": ["Đăng ký môn học", "Thời khóa biểu", "Kết quả học tập",
                "Học phí", "Chương trình đào tạo", "Lịch thi"],
    "admin": ["Quản lý môn học", "Thống kê lượt đăng ký", "Quản lý sinh viên",
              "Quản lý giảng viên", "Thông báo"],
}

MY_PAGES = ["Đại học Đồng Tháp"]

# Các nhóm trong "Hệ thống ứng dụng": {tên nhóm: [các mục con]} theo vai trò
APP_GROUPS = {
    "student": {
        "Đăng ký học phần": ["Danh sách môn học", "Môn đã đăng ký"],
        "Hồ sơ cá nhân": ["Thay đổi mật khẩu", "Bảo mật tài khoản"],
    },
    "admin": {
        "Quản trị": ["Danh sách môn học", "Cấu hình học kỳ"],
        "Hồ sơ cá nhân": ["Thay đổi mật khẩu", "Bảo mật tài khoản"],
    },
}

# dữ liệu
# Thứ trong tuần
THU_LABEL = {2: "Thứ 2", 3: "Thứ 3", 4: "Thứ 4", 5: "Thứ 5",
             6: "Thứ 6", 7: "Thứ 7", 8: "Chủ nhật"}

# Mỗi môn là một dict:
#   ma (mã môn), ten (tên), tc (số tín chỉ), gv (giảng viên),
#   thu (thứ học), tbd / tkt (tiết bắt đầu / kết thúc),
#   siso (sĩ số tối đa), da_dk (số sinh viên khác đã đăng ký sẵn)
COURSES = [
    {"ma": "INF101", "ten": "Nhập môn lập trình", "tc": 3, "gv": "ThS. Nguyễn Văn A",
     "thu": 2, "tbd": 1, "tkt": 3, "siso": 40, "da_dk": 38},
    {"ma": "INF102", "ten": "Cơ sở dữ liệu", "tc": 3, "gv": "ThS. Trần Thị B",
     "thu": 3, "tbd": 4, "tkt": 6, "siso": 40, "da_dk": 25},
    {"ma": "MAT101", "ten": "Toán cao cấp A1", "tc": 3, "gv": "TS. Lê Văn C",
     "thu": 4, "tbd": 1, "tkt": 3, "siso": 60, "da_dk": 40},
    {"ma": "ENG101", "ten": "Tiếng Anh 1", "tc": 2, "gv": "ThS. Phạm Thị D",
     "thu": 5, "tbd": 7, "tkt": 8, "siso": 35, "da_dk": 35},
    {"ma": "PHY101", "ten": "Vật lý đại cương", "tc": 2, "gv": "TS. Võ Văn E",
     "thu": 6, "tbd": 1, "tkt": 2, "siso": 50, "da_dk": 20},
    {"ma": "INF103", "ten": "Lập trình hướng đối tượng", "tc": 3, "gv": "ThS. Hồ Văn P",
     "thu": 2, "tbd": 2, "tkt": 4, "siso": 40, "da_dk": 10},
    {"ma": "INF104", "ten": "Mạng máy tính", "tc": 3, "gv": "ThS. Đặng Thị G",
     "thu": 3, "tbd": 7, "tkt": 9, "siso": 40, "da_dk": 15},
    {"ma": "INF201", "ten": "Cấu trúc dữ liệu và giải thuật", "tc": 3, "gv": "TS. Ngô Văn H",
     "thu": 7, "tbd": 1, "tkt": 4, "siso": 40, "da_dk": 22},
    {"ma": "INF202", "ten": "Hệ điều hành", "tc": 3, "gv": "ThS. Bùi Thị L",
     "thu": 4, "tbd": 7, "tkt": 9, "siso": 40, "da_dk": 18},
]

# Môn mỗi sinh viên đã đăng ký: {tên tài khoản: {tập mã môn}}
REGISTRATIONS = {}


def lich_text(c):
    """Chuỗi lịch học để hiển thị, vd: "Thứ 2, tiết 1-3"."""
    return f"{THU_LABEL[c['thu']]}, tiết {c['tbd']}-{c['tkt']}"


def my_regs(username):
    """Tập mã môn mà sinh viên `username` đã đăng ký."""
    return REGISTRATIONS.setdefault(username, set())


def registered_count(ma):
    """Tổng số sinh viên đã đăng ký môn `ma` (gồm cả số đăng ký sẵn da_dk)."""
    course = next(c for c in COURSES if c["ma"] == ma)
    return course["da_dk"] + sum(1 for regs in REGISTRATIONS.values() if ma in regs)


def credits_of(username):
    """Tổng tín chỉ sinh viên đã đăng ký."""
    regs = my_regs(username)
    return sum(c["tc"] for c in COURSES if c["ma"] in regs)


def find_conflict(username, course):
    """Trả về môn đã đăng ký bị TRÙNG LỊCH với `course`, hoặc None nếu không trùng."""
    regs = my_regs(username)
    for c in COURSES:
        if c["ma"] in regs and c["ma"] != course["ma"] and c["thu"] == course["thu"]:
            if not (c["tkt"] < course["tbd"] or course["tkt"] < c["tbd"]):   # tiết giao nhau
                return c
    return None


# tiện ích
def notify(page, text, error=False):
    """Hiện thông báo nhỏ ở cuối màn hình (error=True: nền đỏ)."""
    page.show_dialog(ft.SnackBar(
        content=ft.Text(text, color="#FFFFFF"),
        bgcolor="#C62828" if error else "#2E7D32"))


# các thành phần nhỏ
def section_header(title, icon=None, label=None):
    """Thanh tiêu đề màu xanh lá, có thể kèm icon. `label`: truyền Text có sẵn nếu muốn đổi chữ về sau."""
    row = [label or ft.Text(title, size=s(22), color="#FFFFFF", weight=ft.FontWeight.W_500)]
    if icon:
        row.append(ft.Icon(icon, color="#BBDEFB", size=s(22)))
    return ft.Container(
        content=ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=s(6)),
        # nền chuyển sắc xanh lá sáng -> xanh lá đậm (từ trên xuống dưới)
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1),
            colors=["#7DB93B", "#4F7D1C"]),
        padding=ft.Padding(left=0, top=s(6), right=0, bottom=s(6)),
    )


def link_item(text, on_click=None):
    """Một dòng menu: chữ in đậm màu xám + đường kẻ mờ bên dưới. Bấm được (on_click)."""
    return ft.Container(
        content=ft.Column(
            [ft.Container(
                content=ft.Text(text, size=s(17), color="#D0D0D0", weight=ft.FontWeight.BOLD),
                padding=ft.Padding(left=s(22), top=s(8), right=s(8), bottom=s(8))),
             ft.Divider(height=1, color="#3A3A3A")],   # đường kẻ phân cách
            spacing=0),
        on_click=on_click, ink=True,    # ink=True: hiệu ứng gợn sóng khi bấm
    )


def small_pill(text, bg="#000000", fg="#FFFFFF"):
    """Nút nhỏ bo tròn dạng "▶xem thêm..." (bg: màu nền, fg: màu chữ)."""
    return ft.Container(
        content=ft.Text("▶" + text, size=s(13), color=fg),
        bgcolor=bg, border_radius=s(12),
        padding=ft.Padding(left=s(10), top=s(2), right=s(10), bottom=s(2)),
    )


def collapsible(title, items, page, open_state=True, handlers=None):
    """Nhóm menu đóng/mở được. handlers: {tên mục: hàm} để gắn chức năng cho mục con."""
    handlers = handlers or {}
    state = {"open": open_state}    # trạng thái hiện tại (đang mở hay đóng)
    body = ft.Column([link_item(i, handlers.get(i)) for i in items],
                     spacing=0, visible=open_state)
    icon = ft.Text("⊟" if open_state else "⊞", color="#FFFFFF", size=s(18))

    def toggle(e):
        # Đảo trạng thái, ẩn/hiện phần thân, đổi icon ⊟ <-> ⊞
        state["open"] = not state["open"]
        body.visible = state["open"]
        icon.value = "⊟" if state["open"] else "⊞"
        page.update()

    head = ft.Container(
        content=ft.Row(
            [ft.Text(title, size=s(19), color=GREEN_TEXT), icon],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor="#0B2B0B",
        padding=ft.Padding(left=s(6), top=s(4), right=s(8), bottom=s(4)),
        on_click=toggle,
    )
    return ft.Column([head, body], spacing=0)


def action_btn(text, icon, bg, on_click):
    """Nút hành động lớn có icon + chữ (vd: "Thêm môn học")."""
    return ft.Container(
        content=ft.Row(
            [ft.Icon(icon, color="#FFFFFF", size=s(22)),
             ft.Text(text, size=s(17), color="#FFFFFF", weight=ft.FontWeight.BOLD)],
            spacing=s(6), tight=True),
        bgcolor=bg, border_radius=s(8), on_click=on_click, ink=True,
        padding=ft.Padding(left=s(14), top=s(8), right=s(14), bottom=s(8)),
    )


def row_btn(text, bg, on_click=None):
    """Nút nhỏ nằm trong từng dòng (vd: "Đăng ký", "Huỷ"). on_click=None -> nút bị vô hiệu."""
    return ft.Container(
        content=ft.Text(text, size=s(15), color="#FFFFFF", weight=ft.FontWeight.BOLD),
        bgcolor=bg, border_radius=s(6), on_click=on_click, ink=on_click is not None,
        padding=ft.Padding(left=s(12), top=s(5), right=s(12), bottom=s(5)),
    )


def build_calendar(today: datetime.date):
    """Vẽ lịch của tháng chứa ngày `today`; ngày hôm nay được tô vàng."""
    cal = calendar.Calendar(firstweekday=6)    # tuần bắt đầu từ Chủ nhật
    heads = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"]
    cell_w, cell_h = s(46), s(30)              # kích thước mỗi ô ngày
    gap = max(1, s(2))                         # khoảng cách giữa các ô

    # Hàng đầu tiên: tên các thứ trong tuần
    rows = [
        ft.Row(
            [ft.Container(ft.Text(h, size=s(13), color="#FFFFFF", weight=ft.FontWeight.BOLD),
                          width=cell_w, alignment=ft.Alignment(0, 0)) for h in heads],
            spacing=gap)
    ]

    # Mỗi tuần của tháng là một hàng, mỗi ngày là một ô
    for week in cal.monthdatescalendar(today.year, today.month):
        cells = []
        for d in week:
            in_month = d.month == today.month    # ngày có thuộc tháng đang xem không
            is_today = d == today                # có phải hôm nay không
            weekend = d.weekday() >= 5           # thứ 7 hoặc Chủ nhật
            if not in_month:
                color, bg = "#555555", "#2A2A2A"     # ngày của tháng khác: chữ xám mờ
            elif is_today:
                color, bg = "#222222", "#FFF59D"     # hôm nay: nền vàng
            else:
                color = "#29B6F6" if not weekend else "#E1A0FF"   # ngày thường xanh, cuối tuần tím
                bg = "#2A2A2A"
            cells.append(ft.Container(
                content=ft.Text(str(d.day), size=s(14), color=color),
                width=cell_w, height=cell_h, bgcolor=bg, alignment=ft.Alignment(1, 0),
                padding=ft.Padding(left=0, top=0, right=s(4), bottom=0)))
        rows.append(ft.Row(cells, spacing=gap))

    # Thanh tiêu đề màu cam: mũi tên trái - "Tháng X năm Y" - mũi tên phải
    header = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.CHEVRON_LEFT, color="#FFFFFF", size=s(24)),
             ft.Text(f"Tháng {today.month} năm {today.year}", size=s(16),
                     color="#FFFFFF", weight=ft.FontWeight.BOLD),
             ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#FFFFFF", size=s(24))],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor="#F5A623",
        padding=ft.Padding(left=s(8), top=s(6), right=s(8), bottom=s(6)),
        # chỉ bo hai góc trên
        border_radius=ft.BorderRadius(top_left=s(8), top_right=s(8), bottom_left=0, bottom_right=0),
    )
    return ft.Container(
        content=ft.Column(
            [header, ft.Container(ft.Column(rows, spacing=gap), padding=s(6))], spacing=0),
        bgcolor="#3A3A3A", border_radius=s(8),
        width=cell_w * 7 + gap * 6 + s(6) * 2,    # rộng vừa đúng 7 ô + khoảng cách + lề
    )


# ------------------------------------------------------------------ màn hình chính
def build_htsv(page: ft.Page, username: str, role: str, on_logout):
    """Dựng màn hình hệ thống đăng ký môn học.

    page      : trang Flet hiện tại
    username  : tên tài khoản hiển thị ở lời chào
    role      : "student" (sinh viên) hoặc "admin" (quản trị)
    on_logout : hàm được gọi khi bấm "Đăng xuất" (quay về màn hình đăng nhập)
    """
    today = datetime.date.today()    # ngày hôm nay (dùng cho lịch)
    is_admin = role == "admin"
    tab = {"v": "all"}               # sinh viên: "all" = môn đang mở, "mine" = môn đã đăng ký

    logo = ft.Image(src=LOGO_FILE, width=s(44), height=s(44))    # logo trường

    # ================================================================== DANH SÁCH MÔN HỌC
    # Độ rộng các cột (dùng chung cho dòng tiêu đề và từng dòng dữ liệu để thẳng hàng)
    W_STT, W_TC, W_SISO, W_ACT = s(46), s(60), s(80), s(110)   # cột cố định
    E_MA, E_TEN, E_GV, E_LICH = 2, 5, 4, 4                     # cột co giãn theo tỉ lệ

    def cell(content, width=None, expand=None, center=False):
        """Một ô trong bảng; nhận chữ hoặc control."""
        if isinstance(content, str):
            content = ft.Text(content, size=s(17), color="#E0E0E0",
                              max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)
        return ft.Container(
            content=content, width=width, expand=expand,
            alignment=ft.Alignment(0, 0) if center else ft.Alignment(-1, 0))

    def head_text(t):
        return ft.Text(t, size=s(17), color=GREEN_TEXT, weight=ft.FontWeight.BOLD)

    # Dòng tiêu đề bảng
    table_head = ft.Container(
        content=ft.Row([
            cell(head_text("STT"), width=W_STT, center=True),
            cell(head_text("Mã môn"), expand=E_MA),
            cell(head_text("Tên môn học"), expand=E_TEN),
            cell(head_text("TC"), width=W_TC, center=True),
            cell(head_text("Giảng viên"), expand=E_GV),
            cell(head_text("Lịch học"), expand=E_LICH),
            cell(head_text("Sĩ số"), width=W_SISO, center=True),
            cell(head_text("Thao tác"), width=W_ACT, center=True),
        ], spacing=s(6)),
        bgcolor="#0B2B0B",
        padding=ft.Padding(left=s(8), top=s(8), right=s(8), bottom=s(8)))

    rows_col = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)  # chứa các dòng môn
    stat_a = ft.Text("0", size=s(26), color="#FFFFFF", weight=ft.FontWeight.BOLD)
    stat_b = ft.Text("0", size=s(26), color="#FFFFFF", weight=ft.FontWeight.BOLD)
    count_text = ft.Text("", size=s(15), color="#9E9E9E")   # dòng đếm bên dưới bảng
    title_label = ft.Text("", size=s(22), color="#FFFFFF", weight=ft.FontWeight.W_500)

    # Ô tìm kiếm: gõ đến đâu lọc đến đó (theo mã môn, tên môn, giảng viên)
    search_tf = ft.TextField(
        hint_text="Tìm theo mã môn, tên môn, giảng viên...",
        prefix_icon=ft.Icons.SEARCH, text_size=s(17), color="#FFFFFF",
        bgcolor="#1E1E1E", height=s(48), expand=True,
        content_padding=ft.Padding(left=s(10), top=0, right=s(10), bottom=0),
        border=ft.OutlineInputBorder(border_radius=s(8), side=ft.BorderSide(1, "#3A3A3A")),
        on_change=lambda e: render(),
    )

    def render(update=True):
        """Vẽ lại danh sách theo vai trò / tab / ô tìm kiếm và cập nhật thống kê."""
        regs = my_regs(username)
        kw = (search_tf.value or "").strip().lower()

        # Chọn danh sách gốc: quản trị và tab "all" thấy tất cả, tab "mine" chỉ thấy môn đã đăng ký
        base = COURSES if (is_admin or tab["v"] == "all") else [c for c in COURSES if c["ma"] in regs]
        shown = [c for c in base
                 if kw in c["ma"].lower() or kw in c["ten"].lower() or kw in c["gv"].lower()]

        rows_col.controls = [course_row(i, c) for i, c in enumerate(shown, start=1)]
        if not shown:
            empty = ("Bạn chưa đăng ký môn nào." if (not is_admin and tab["v"] == "mine" and not kw)
                     else "Không có môn học nào.")
            rows_col.controls.append(ft.Container(
                content=ft.Text(empty, size=s(17), color="#9E9E9E"),
                padding=s(20), alignment=ft.Alignment(0, 0)))

        # Tiêu đề, dòng đếm và thống kê
        if is_admin:
            title_label.value = "Quản lý môn học"
            stat_a.value = str(len(COURSES))
            stat_b.value = str(sum(registered_count(c["ma"]) for c in COURSES))
            count_text.value = f"Hiển thị {len(shown)}/{len(COURSES)} môn học"
        else:
            title_label.value = ("Môn học đang mở đăng ký" if tab["v"] == "all"
                                 else "Môn đã đăng ký")
            stat_a.value = str(len(regs))
            stat_b.value = f"{credits_of(username)}/{MAX_CREDITS}"
            count_text.value = (f"Hiển thị {len(shown)}/{len(base)} môn học  •  "
                                f"Đã đăng ký {credits_of(username)}/{MAX_CREDITS} tín chỉ")
        if not is_admin:
            for key, btn in tab_buttons.items():     # tô màu tab đang chọn
                btn.bgcolor = "#2E7D32" if key == tab["v"] else "#2A2A2A"
        if update:
            page.update()

    def course_row(stt, c):
        """Một dòng môn học: thông tin + nút thao tác theo vai trò."""
        used = registered_count(c["ma"])
        full = used >= c["siso"]
        registered = c["ma"] in my_regs(username)

        if is_admin:
            # Quản trị: nút Sửa, Xoá
            action = ft.Row([
                ft.IconButton(icon=ft.Icons.EDIT, icon_color="#FFB300", icon_size=s(24),
                              tooltip="Sửa", on_click=lambda e: open_form(c)),
                ft.IconButton(icon=ft.Icons.DELETE, icon_color="#EF5350", icon_size=s(24),
                              tooltip="Xoá", on_click=lambda e: confirm_delete(c)),
            ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
        elif registered:
            action = row_btn("Huỷ ĐK", "#C62828", lambda e: confirm_unregister(c))
        elif full:
            action = row_btn("Đã đầy", "#616161")          # không bấm được
        else:
            action = row_btn("Đăng ký", "#2E7D32", lambda e: register(c))

        siso_text = ft.Text(f"{used}/{c['siso']}", size=s(17),
                            color="#EF5350" if full else "#E0E0E0")    # đầy -> chữ đỏ
        # sinh viên: môn đã đăng ký được tô nền xanh nhạt để dễ nhận ra
        if not is_admin and registered:
            row_bg = "#143018"
        else:
            row_bg = "#181818" if stt % 2 else "#141414"
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        cell(str(stt), width=W_STT, center=True),
                        cell(c["ma"], expand=E_MA),
                        cell(c["ten"], expand=E_TEN),
                        cell(str(c["tc"]), width=W_TC, center=True),
                        cell(c["gv"], expand=E_GV),
                        cell(lich_text(c), expand=E_LICH),
                        cell(siso_text, width=W_SISO, center=True),
                        cell(action, width=W_ACT, center=True),
                    ], spacing=s(6), vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(left=s(8), top=s(2), right=s(8), bottom=s(2))),
                ft.Divider(height=1, color="#2E2E2E"),
            ], spacing=0),
            bgcolor=row_bg,
        )

    # ---------------------------------------------------------------- SINH VIÊN: ĐĂNG KÝ / HUỶ
    def register(course):
        """Đăng ký một môn, có kiểm tra: đã đủ sĩ số, vượt tín chỉ, trùng lịch."""
        regs = my_regs(username)
        if course["ma"] in regs:
            return
        if registered_count(course["ma"]) >= course["siso"]:
            notify(page, f"Lớp {course['ma']} đã đủ sĩ số.", error=True)
            return
        if credits_of(username) + course["tc"] > MAX_CREDITS:
            notify(page, f"Vượt quá {MAX_CREDITS} tín chỉ tối đa "
                         f"(hiện có {credits_of(username)}, môn này {course['tc']}).", error=True)
            return
        clash = find_conflict(username, course)
        if clash:
            notify(page, f"Trùng lịch với môn {clash['ma']} - {clash['ten']} "
                         f"({lich_text(clash)}).", error=True)
            return
        regs.add(course["ma"])
        render()
        notify(page, f"Đã đăng ký môn {course['ma']} - {course['ten']}")

    def confirm_unregister(course):
        """Hỏi xác nhận trước khi huỷ đăng ký."""
        def do_unregister(e):
            my_regs(username).discard(course["ma"])
            page.pop_dialog()
            render()
            notify(page, f"Đã huỷ đăng ký môn {course['ma']}")

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Huỷ đăng ký"),
            content=ft.Text(f"Bạn có chắc muốn huỷ đăng ký môn "
                            f"\"{course['ten']}\" ({course['ma']}) không?"),
            actions=[
                ft.TextButton("Không", on_click=lambda e: page.pop_dialog()),
                ft.TextButton("Huỷ đăng ký", on_click=do_unregister,
                              style=ft.ButtonStyle(color="#EF5350")),
            ],
        )
        page.show_dialog(dlg)

    # ---------------------------------------------------------------- QUẢN TRỊ: THÊM / SỬA
    def open_form(course=None):
        """Mở hộp thoại nhập môn học. course=None -> THÊM MỚI, có giá trị -> SỬA."""
        is_edit = course is not None

        f_ma = ft.TextField(label="Mã môn", value=course["ma"] if is_edit else "",
                            disabled=is_edit)      # khi sửa không cho đổi mã môn
        f_ten = ft.TextField(label="Tên môn học", value=course["ten"] if is_edit else "")
        f_tc = ft.TextField(label="Số tín chỉ (1-10)", value=str(course["tc"]) if is_edit else "",
                            keyboard_type=ft.KeyboardType.NUMBER)
        f_gv = ft.TextField(label="Giảng viên", value=course["gv"] if is_edit else "")
        f_thu = ft.Dropdown(
            label="Thứ học", value=str(course["thu"]) if is_edit else "2",
            options=[ft.dropdown.Option(key=str(k), text=v) for k, v in THU_LABEL.items()])
        f_tbd = ft.TextField(label="Tiết bắt đầu", value=str(course["tbd"]) if is_edit else "",
                             keyboard_type=ft.KeyboardType.NUMBER, expand=True)
        f_tkt = ft.TextField(label="Tiết kết thúc", value=str(course["tkt"]) if is_edit else "",
                             keyboard_type=ft.KeyboardType.NUMBER, expand=True)
        f_siso = ft.TextField(label="Sĩ số tối đa", value=str(course["siso"]) if is_edit else "40",
                              keyboard_type=ft.KeyboardType.NUMBER)

        def to_int(field, lo, hi, msg):
            """Đọc số nguyên từ ô nhập trong khoảng [lo, hi]; sai thì gắn lỗi và trả None."""
            try:
                v = int((field.value or "").strip())
                if not lo <= v <= hi:
                    raise ValueError
                return v
            except ValueError:
                field.error = msg
                return None

        def save(e):
            # --- Kiểm tra dữ liệu, ô nào sai thì báo lỗi dưới ô đó ---
            for f in (f_ma, f_ten, f_tc, f_tbd, f_tkt, f_siso):
                f.error = None
            ma = (f_ma.value or "").strip().upper()
            ten = (f_ten.value or "").strip()
            if not ma:
                f_ma.error = "Vui lòng nhập mã môn"
            elif not is_edit and any(c["ma"] == ma for c in COURSES):
                f_ma.error = "Mã môn đã tồn tại"      # không cho trùng mã
            if not ten:
                f_ten.error = "Vui lòng nhập tên môn"
            tc = to_int(f_tc, 1, 10, "Tín chỉ phải là số từ 1 đến 10")
            tbd = to_int(f_tbd, 1, 12, "Tiết từ 1 đến 12")
            tkt = to_int(f_tkt, 1, 12, "Tiết từ 1 đến 12")
            if tbd and tkt and tkt < tbd:
                f_tkt.error = "Phải lớn hơn hoặc bằng tiết bắt đầu"
                tkt = None
            # sĩ số tối đa không được nhỏ hơn số sinh viên đang đăng ký
            min_siso = max(1, registered_count(course["ma"])) if is_edit else 1
            siso = to_int(f_siso, min_siso, 500,
                          f"Sĩ số từ {min_siso} đến 500" + (" (đã có người đăng ký)" if is_edit else ""))

            if any(f.error for f in (f_ma, f_ten, f_tc, f_tbd, f_tkt, f_siso)):
                page.update()
                return

            # --- Dữ liệu hợp lệ: cập nhật hoặc thêm mới ---
            data = {"ma": ma, "ten": ten, "tc": tc, "gv": (f_gv.value or "").strip(),
                    "thu": int(f_thu.value or 2), "tbd": tbd, "tkt": tkt, "siso": siso}
            if is_edit:
                course.update(data)          # sửa trực tiếp dict trong COURSES
            else:
                data["da_dk"] = 0
                COURSES.append(data)         # thêm vào cuối danh sách
            page.pop_dialog()
            render()
            notify(page, "Đã cập nhật môn học" if is_edit else "Đã thêm môn học")

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sửa môn học" if is_edit else "Thêm môn học"),
            content=ft.Column([f_ma, f_ten, f_tc, f_gv, f_thu, ft.Row([f_tbd, f_tkt]), f_siso],
                              tight=True, width=420, spacing=12, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Huỷ", on_click=lambda e: page.pop_dialog()),
                ft.TextButton("Lưu", on_click=save),
            ],
        )
        page.show_dialog(dlg)

    # ---------------------------------------------------------------- QUẢN TRỊ: XOÁ
    def confirm_delete(course):
        """Hỏi xác nhận trước khi xoá một môn học."""
        def do_delete(e):
            COURSES.remove(course)
            for regs in REGISTRATIONS.values():      # xoá luôn khỏi danh sách đăng ký của sinh viên
                regs.discard(course["ma"])
            page.pop_dialog()
            render()
            notify(page, f"Đã xoá môn {course['ma']}")

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Xoá môn học"),
            content=ft.Text(f"Bạn có chắc muốn xoá môn \"{course['ten']}\" ({course['ma']}) không?\n"
                            f"Các đăng ký của sinh viên với môn này cũng sẽ bị xoá."),
            actions=[
                ft.TextButton("Huỷ", on_click=lambda e: page.pop_dialog()),
                ft.TextButton("Xoá", on_click=do_delete,
                              style=ft.ButtonStyle(color="#EF5350")),
            ],
        )
        page.show_dialog(dlg)

    # ---------------------------------------------------------------- TAB (chỉ sinh viên)
    def set_tab(key):
        tab["v"] = key
        render()

    def tab_button(text, key):
        return ft.Container(
            content=ft.Text(text, size=s(17), color="#FFFFFF", weight=ft.FontWeight.BOLD),
            bgcolor="#2A2A2A", border_radius=s(8), ink=True, on_click=lambda e: set_tab(key),
            padding=ft.Padding(left=s(14), top=s(8), right=s(14), bottom=s(8)))

    tab_buttons = {}
    if not is_admin:
        tab_buttons = {"all": tab_button("Môn đang mở", "all"),
                       "mine": tab_button("Môn đã đăng ký", "mine")}

    render(update=False)    # vẽ danh sách lần đầu (chưa gắn vào trang nên chưa cần update)

    # ---- Thanh công cụ phía trên bảng ----
    if is_admin:
        toolbar = ft.Row([
            search_tf,
            action_btn("Thêm môn học", ft.Icons.ADD, "#2E7D32", lambda e: open_form()),
        ], spacing=s(10), vertical_alignment=ft.CrossAxisAlignment.CENTER)
    else:
        toolbar = ft.Row([
            tab_buttons["all"], tab_buttons["mine"], search_tf,
        ], spacing=s(10), vertical_alignment=ft.CrossAxisAlignment.CENTER)

    # ---- Vùng giữa: tiêu đề + thanh công cụ + bảng + dòng đếm ----
    content_area = ft.Container(
        expand=True, bgcolor="#0F0F0F", padding=s(14),
        content=ft.Column([
            section_header("", label=title_label),
            toolbar,
            table_head,
            rows_col,                                             # các dòng môn (cuộn được)
            count_text,
        ], spacing=s(8), expand=True))

    # ---- Thanh trên cùng ----
    topbar = ft.Container(
        bgcolor=TOPBAR, height=s(56),
        padding=ft.Padding(left=s(16), top=0, right=s(20), bottom=0),
        content=ft.Row(
            [
                # Nhóm bên trái: logo, tên hệ thống, các icon
                ft.Row([
                    logo,
                    ft.Text("Hệ thống đăng ký môn học", size=s(30), color="#FFFFFF",
                            weight=ft.FontWeight.BOLD),
                    ft.Icon(ft.Icons.APPS, color="#FFFFFF", size=s(26)),            # ứng dụng
                    ft.Icon(ft.Icons.CHAT, color="#FFFFFF", size=s(32)),            # tin nhắn
                    ft.Icon(ft.Icons.CALENDAR_MONTH, color="#FFFFFF", size=s(30)),  # lịch
                ], spacing=s(18), vertical_alignment=ft.CrossAxisAlignment.CENTER),
                # Nhóm bên phải: lời chào (kèm vai trò) và nút đăng xuất
                ft.Row([
                    ft.Text(f"Xin chào, {username} ({ROLE_LABEL[role]})",
                            size=s(20), color="#FFFFFF"),
                    ft.Container(
                        content=ft.Text("Đăng xuất", size=s(14), color="#FFFFFF"),
                        bgcolor="#000000", border_radius=s(12), on_click=lambda e: on_logout(),
                        padding=ft.Padding(left=s(12), top=s(4), right=s(12), bottom=s(4)),
                        ink=True),
                ], spacing=s(14)),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,    # hai nhóm dạt về hai đầu
            vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    # ---- Cột trái: menu theo vai trò ----
    # Sinh viên: các mục "Đăng ký môn học", "Danh sách môn học", "Môn đã đăng ký" bấm được
    handlers = {} if is_admin else {
        "Đăng ký môn học": lambda e: set_tab("all"),
        "Danh sách môn học": lambda e: set_tab("all"),
        "Môn đã đăng ký": lambda e: set_tab("mine"),
    }

    sidebar = ft.Container(
        width=s(310), bgcolor=PANEL_DARK,
        content=ft.Column(
            [
                section_header("Liên kết nhanh"),
                *[link_item(t, handlers.get(t)) for t in QUICK_LINKS[role]],
                section_header("Trang của tôi"),
                *[link_item(t) for t in MY_PAGES],
                ft.Row([small_pill("xem thêm...")], alignment=ft.MainAxisAlignment.END),
                section_header("Hệ thống ứng dụng", icon=ft.Icons.SEARCH),
                *[collapsible(name, items, page, handlers=handlers)
                  for name, items in APP_GROUPS[role].items()],
            ],
            spacing=0, scroll=ft.ScrollMode.AUTO),
    )

    def bar(title):
        # Thanh tiêu đề xanh đậm (vd: "Thống kê đăng ký")
        return ft.Container(
            content=ft.Text(title, size=s(20), color=GREEN_TEXT),
            bgcolor="#0B2B0B",
            padding=ft.Padding(left=s(6), top=s(4), right=s(6), bottom=s(4)))

    def stat_card(label, value_text):
        # Ô thống kê: số lớn + nhãn nhỏ
        return ft.Container(
            content=ft.Column([value_text, ft.Text(label, size=s(15), color="#BDBDBD")],
                              spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#1E1E1E", border_radius=s(8), expand=True,
            padding=ft.Padding(left=s(8), top=s(10), right=s(8), bottom=s(10)))

    # Nhãn thống kê theo vai trò
    label_a, label_b = (("Số môn học", "Lượt đăng ký") if is_admin
                        else ("Môn đã đăng ký", "Tín chỉ"))

    # ---- Cột phải: lịch + thống kê ----
    right_panel = ft.Column(
        [
            build_calendar(today),                                       # lịch tháng
            ft.Container(                                                # ngày hôm nay
                content=ft.Text(f"Ngày {today.day} tháng {today.month} năm {today.year}", size=s(18), color="#7CFC00",
                                text_align=ft.TextAlign.CENTER),
                bgcolor="#0B2B0B", alignment=ft.Alignment(0, 0),
                padding=ft.Padding(left=0, top=s(6), right=0, bottom=s(6))),
            bar("Thống kê đăng ký"),
            ft.Row([stat_card(label_a, stat_a), stat_card(label_b, stat_b)], spacing=s(8)),
        ],
        spacing=s(8), scroll=ft.ScrollMode.AUTO, expand=True)

    right_area = ft.Container(
        width=s(400), bgcolor="#141414",
        padding=ft.Padding(left=s(16), top=0, right=s(16), bottom=s(10)),
        content=right_panel)

    # Thân trang: [cột trái | danh sách môn học | cột phải]
    body = ft.Row([sidebar, content_area, right_area], expand=True, spacing=0)
    # Toàn trang: thanh trên cùng nằm trên, thân trang nằm dưới
    return ft.Column([topbar, body], expand=True, spacing=0)