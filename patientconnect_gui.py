# ============================================================
# PATIENT CONNECT - MODERN BENTO GUI
# ============================================================
# UI:
#   - Modern healthcare SaaS style
#   - Bento dashboard cards
#   - Sidebar navigation
#   - Role-based navigation
#   - Scrollable content
#   - Modern forms
#   - Modern tables
#   - Hover effects
#
# BACKEND:
#   - MySQL
#   - bcrypt
#   - Stored Procedures
#   - Mailtrap
#   - CSV Export
#
# EXISTING BACKEND LOGIC IS NOT CHANGED
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import bcrypt
import csv

from db import get_db_config
from mailer import send_email


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return mysql.connector.connect(**get_db_config())


# ============================================================
# COLORS
# ============================================================

BG = "#F6F8FC"
WHITE = "#FFFFFF"

TEXT = "#172033"
TEXT_LIGHT = "#475569"
MUTED = "#64748B"

BORDER = "#E3E8F0"

PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
PRIMARY_LIGHT = "#EFF6FF"

SUCCESS = "#059669"
SUCCESS_DARK = "#047857"
SUCCESS_LIGHT = "#ECFDF5"

WARNING = "#D97706"
WARNING_LIGHT = "#FFFBEB"

DANGER = "#E11D48"
DANGER_DARK = "#BE123C"
DANGER_LIGHT = "#FFF1F2"

BLUE = "#2563EB"
BLUE_LIGHT = "#EFF6FF"

PURPLE = "#7C3AED"
PURPLE_LIGHT = "#F5F3FF"

FONT = "Segoe UI"


# ============================================================
# ROLE COLORS
# ============================================================

ROLE_COLORS = {
    "ADMIN": (
        PRIMARY,
        PRIMARY_LIGHT
    ),

    "DOCTOR": (
        SUCCESS,
        SUCCESS_LIGHT
    ),

    "STAFF": (
        WARNING,
        WARNING_LIGHT
    )
}


# ============================================================
# LOGIN WINDOW
# ============================================================

class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "PatientConnect | Secure Login"
        )

        self.root.geometry(
            "980x620"
        )

        self.root.resizable(
            False,
            False
        )

        self.root.configure(
            bg=BG
        )

        self.setup_style()

        self.build_login()


    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )

        style.configure(
            "TScrollbar",
            troughcolor=BG,
            background="#CBD5E1",
            borderwidth=0,
            arrowsize=12
        )

        style.configure(
            "Modern.TButton",
            font=(FONT, 9, "bold"),
            padding=(13, 8),
            borderwidth=0
        )

        style.map(
            "Modern.TButton",
            background=[("active", PRIMARY_LIGHT)],
            foreground=[("active", PRIMARY_DARK)]
        )

        # ----------------------------------------------------
        # FRAME
        # ----------------------------------------------------

        style.configure(
            "TFrame",
            background=BG
        )

        # ----------------------------------------------------
        # LABEL
        # ----------------------------------------------------

        style.configure(
            "TLabel",
            background=BG,
            foreground=TEXT,
            font=(
                FONT,
                10
            )
        )

        # ----------------------------------------------------
        # BUTTON
        # ----------------------------------------------------

        style.configure(
            "TButton",
            font=(
                FONT,
                10
            ),
            padding=(
                14,
                8
            )
        )

        # ----------------------------------------------------
        # PRIMARY BUTTON
        # ----------------------------------------------------

        style.configure(
            "Primary.TButton",
            background=PRIMARY,
            foreground=WHITE,
            font=(
                FONT,
                10,
                "bold"
            ),
            padding=(
                16,
                10
            ),
            borderwidth=0
        )

        style.map(
            "Primary.TButton",
            background=[
                (
                    "active",
                    PRIMARY_DARK
                )
            ]
        )

        # ----------------------------------------------------
        # SUCCESS BUTTON
        # ----------------------------------------------------

        style.configure(
            "Success.TButton",
            background=SUCCESS,
            foreground=WHITE,
            font=(
                FONT,
                10,
                "bold"
            ),
            padding=(
                16,
                10
            ),
            borderwidth=0
        )

        style.map(
            "Success.TButton",
            background=[
                (
                    "active",
                    SUCCESS_DARK
                )
            ]
        )

        # ----------------------------------------------------
        # DANGER BUTTON
        # ----------------------------------------------------

        style.configure(
            "Danger.TButton",
            background=DANGER,
            foreground=WHITE,
            font=(
                FONT,
                10,
                "bold"
            ),
            padding=(
                16,
                10
            ),
            borderwidth=0
        )

        style.map(
            "Danger.TButton",
            background=[
                (
                    "active",
                    DANGER_DARK
                )
            ]
        )

        # ----------------------------------------------------
        # BACK BUTTON
        # ----------------------------------------------------

        style.configure(
            "Back.TButton",
            background=BG,
            foreground=MUTED,
            font=(
                FONT,
                9,
                "bold"
            ),
            padding=(
                10,
                7
            ),
            borderwidth=0
        )

        style.map(
            "Back.TButton",
            foreground=[
                (
                    "active",
                    PRIMARY
                )
            ]
        )

        # ----------------------------------------------------
        # ENTRY
        # ----------------------------------------------------

        style.configure(
            "Modern.TEntry",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            borderwidth=1,
            relief="solid",
            padding=8
        )

        style.map(
            "Modern.TEntry",
            bordercolor=[
                (
                    "focus",
                    PRIMARY
                )
            ],

            lightcolor=[
                (
                    "focus",
                    PRIMARY
                )
            ],

            darkcolor=[
                (
                    "focus",
                    PRIMARY
                )
            ]
        )

        # ----------------------------------------------------
        # COMBOBOX
        # ----------------------------------------------------

        style.configure(
            "Modern.TCombobox",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            arrowcolor=PRIMARY,
            padding=7
        )

        # ----------------------------------------------------
        # TREEVIEW
        # ----------------------------------------------------

        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            font=(
                FONT,
                9
            ),
            rowheight=32,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=PRIMARY_LIGHT,
            foreground=PRIMARY_DARK,
            font=(
                FONT,
                9,
                "bold"
            ),
            padding=(
                8,
                8
            )
        )

        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    PRIMARY_LIGHT
                )
            ],

            foreground=[
                (
                    "selected",
                    PRIMARY_DARK
                )
            ]
        )


    # ========================================================
    # LOGIN SCREEN
    # ========================================================

    def build_login(self):

        # Premium, minimal login layout. Authentication logic below is unchanged.
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        left = tk.Frame(outer, bg="#173B72", width=220)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(
            left, text="✚", bg="#173B72", fg=WHITE,
            font=(FONT, 30, "bold")
        ).pack(anchor="w", padx=28, pady=(45, 12))

        tk.Label(
            left, text="PATIENT", bg="#173B72", fg=WHITE,
            font=(FONT, 18, "bold")
        ).pack(anchor="w", padx=28)

        tk.Label(
            left, text="CONNECT", bg="#173B72", fg="#7DD3FC",
            font=(FONT, 18, "bold")
        ).pack(anchor="w", padx=28)

        tk.Frame(left, bg="#3B82F6", height=2).pack(
            fill="x", padx=28, pady=22
        )

        tk.Label(
            left,
            text="Healthcare\nmanagement,\nsimplified.",
            justify="left",
            bg="#173B72",
            fg="#DCEBFF",
            font=(FONT, 15, "bold"),
        ).pack(anchor="w", padx=28)

        tk.Label(
            left,
            text="Secure access for your\nclinical workspace.",
            justify="left",
            bg="#173B72",
            fg="#AFC6E8",
            font=(FONT, 9),
        ).pack(anchor="w", padx=28, pady=(12, 0))

        right = tk.Frame(outer, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right, text="Welcome back", bg=BG, fg=TEXT,
            font=(FONT, 24, "bold")
        ).pack(anchor="w", padx=42, pady=(72, 4))

        tk.Label(
            right, text="Sign in to continue to PatientConnect",
            bg=BG, fg=MUTED, font=(FONT, 10)
        ).pack(anchor="w", padx=42)

        card = tk.Frame(
            right, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="x", padx=42, pady=28)

        inside = tk.Frame(card, bg=WHITE)
        inside.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            inside, text="Account access", bg=WHITE, fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(anchor="w", pady=(0, 20))

        tk.Label(
            inside, text="USERNAME", bg=WHITE, fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w")

        self.username = ttk.Entry(
            inside, style="Modern.TEntry", font=(FONT, 11)
        )
        self.username.pack(fill="x", pady=(6, 18), ipady=5)

        tk.Label(
            inside, text="PASSWORD", bg=WHITE, fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w")

        self.password = ttk.Entry(
            inside, style="Modern.TEntry", show="*", font=(FONT, 11)
        )
        self.password.pack(fill="x", pady=(6, 24), ipady=5)

        ttk.Button(
            inside, text="Sign in  →",
            command=self.login, style="Primary.TButton"
        ).pack(fill="x", ipady=2)

        self.status = tk.Label(
            right, text="", bg=BG, fg=DANGER,
            font=(FONT, 9, "bold")
        )
        self.status.pack(pady=4)

        tk.Label(
            right,
            text="PatientConnect  •  Secure Healthcare Platform",
            bg=BG, fg="#94A3B8", font=(FONT, 8)
        ).pack(pady=18)

        self.root.bind("<Return>", lambda event: self.login())
        self.username.focus_set()


    # ========================================================
    # LOGIN FUNCTION
    # ========================================================

    def login(self):

        username = self.username.get().strip()

        password = self.password.get()

        if not username or not password:

            self.status.config(
                text="Enter username and password."
            )

            return

        conn = None

        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT
                    user_id,
                    username,
                    password_hash,
                    role,
                    active
                FROM users
                WHERE username = %s
                LIMIT 1
                """,
                (username,)
            )

            user = cursor.fetchone()

            if user is None:

                self.status.config(
                    text="Invalid username or password."
                )

                return

            if not user["active"]:

                self.status.config(
                    text="This account is inactive."
                )

                return

            stored_hash = user["password_hash"]

            if isinstance(
                stored_hash,
                str
            ):

                stored_hash = stored_hash.encode()

            if not bcrypt.checkpw(
                password.encode(),
                stored_hash
            ):

                self.status.config(
                    text="Invalid username or password."
                )

                return

            self.open_dashboard(
                user
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


    # ========================================================
    # OPEN DASHBOARD
    # ========================================================

    def open_dashboard(
        self,
        user
    ):

        for widget in self.root.winfo_children():

            widget.destroy()

        Dashboard(
            self.root,
            user,
            self.logout
        )


    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        for widget in self.root.winfo_children():

            widget.destroy()

        self.root.geometry(
            "520x600"
        )

        self.root.resizable(
            False,
            False
        )

        self.build_login()


# ============================================================
# DASHBOARD
# ============================================================

class Dashboard:

    def __init__(
        self,
        root,
        user,
        logout_callback
    ):

        self.window = root

        self.user = user

        self.logout_callback = logout_callback

        self.role = str(
            user.get(
                "role",
                ""
            )
        ).upper()

        self.username = user.get(
            "username",
            "Unknown"
        )

        self.window.configure(
            bg=BG
        )

        self.window.geometry(
            "1320x800"
        )

        self.window.minsize(
            1050,
            650
        )

        self.window.resizable(
            True,
            True
        )

        self.create_layout()

        self.build()


    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = tk.Frame(
            self.window,
            bg=WHITE,
            width=235
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        # ----------------------------------------------------
        # Main area
        # ----------------------------------------------------

        self.main_area = tk.Frame(
            self.window,
            bg=BG
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Scrollable canvas
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            self.main_area,
            bg=BG,
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar = ttk.Scrollbar(
            self.main_area,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.content = tk.Frame(
            self.canvas,
            bg=BG
        )

        self.canvas_window = self.canvas.create_window(
            (
                0,
                0
            ),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mousewheel
        )

        self.build_sidebar()


    # ========================================================
    # SCROLL
    # ========================================================

    def update_scroll_region(
        self,
        event=None
    ):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    def resize_content(
        self,
        event
    ):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    def mousewheel(
        self,
        event
    ):

        self.canvas.yview_scroll(
            int(
                -1 *
                (
                    event.delta / 120
                )
            ),
            "units"
        )


    # ========================================================
    # SIDEBAR
    # ========================================================

    def build_sidebar(self):

        self.sidebar.configure(bg="#FFFFFF")

        logo = tk.Frame(self.sidebar, bg=WHITE)
        logo.pack(fill="x", padx=20, pady=(24, 20))

        mark = tk.Frame(
            logo, bg=PRIMARY, width=38, height=38
        )
        mark.pack(side="left")
        mark.pack_propagate(False)

        tk.Label(
            mark, text="✚", bg=PRIMARY, fg=WHITE,
            font=(FONT, 18, "bold")
        ).pack(expand=True)

        logo_text = tk.Frame(logo, bg=WHITE)
        logo_text.pack(side="left", padx=11)

        tk.Label(
            logo_text, text="PATIENTCONNECT",
            bg=WHITE, fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(anchor="w")

        tk.Label(
            logo_text, text="Healthcare workspace",
            bg=WHITE, fg=MUTED, font=(FONT, 7)
        ).pack(anchor="w", pady=(1, 0))

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x")

        tk.Label(
            self.sidebar, text="WORKSPACE",
            bg=WHITE, fg="#94A3B8",
            font=(FONT, 8, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        if self.role == "ADMIN":
            nav_items = [
                ("⌂", "Dashboard", self.build),
                ("♙", "Patients", self.patient_management),
                ("□", "Appointments", self.appointment_management),
                ("▥", "Reports", self.reports),
                ("◇", "Messages", self.messages),
                ("⚕", "Clinical Info", self.clinical_information),
                ("▣", "Clinics", self.clinic_information),
                ("$", "Insurance", self.insurance),
                ("◈", "Audit Logs", self.audit_logs)
            ]
        elif self.role == "DOCTOR":
            nav_items = [
                ("⌂", "Dashboard", self.build),
                ("♙", "Patients", self.patient_management),
                ("□", "Appointments", self.appointment_management),
                ("⚕", "Clinical Info", self.clinical_information),
                ("◇", "Messages", self.messages),
                ("▥", "Reports", self.reports),
                ("$", "Insurance", self.insurance)
            ]
        else:
            nav_items = [
                ("⌂", "Dashboard", self.build),
                ("♙", "Patients", self.patient_management),
                ("□", "Appointments", self.appointment_management),
                ("◇", "Messages", self.messages),
                ("◷", "Due Reminders", self.due_reminders),
                ("▣", "Clinics", self.clinic_information),
                ("$", "Insurance", self.insurance)
            ]

        for icon, text, command in nav_items:
            self.sidebar_button(icon, text, command)

        spacer = tk.Frame(self.sidebar, bg=WHITE)
        spacer.pack(fill="both", expand=True)

        role_color, role_bg = ROLE_COLORS.get(
            self.role, (PRIMARY, PRIMARY_LIGHT)
        )

        user_card = tk.Frame(
            self.sidebar, bg="#F5F8FD",
            highlightbackground=BORDER, highlightthickness=1
        )
        user_card.pack(fill="x", padx=14, pady=(10, 8))

        avatar = tk.Frame(user_card, bg=PRIMARY, width=34, height=34)
        avatar.pack(side="left", padx=11, pady=11)
        avatar.pack_propagate(False)

        tk.Label(
            avatar, text=str(self.username)[:1].upper(),
            bg=PRIMARY, fg=WHITE, font=(FONT, 11, "bold")
        ).pack(expand=True)

        info = tk.Frame(user_card, bg="#F5F8FD")
        info.pack(side="left", pady=9)

        tk.Label(
            info, text=self.username, bg="#F5F8FD", fg=TEXT,
            font=(FONT, 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            info, text=self.role, bg=role_bg, fg=role_color,
            font=(FONT, 7, "bold"), padx=6
        ).pack(anchor="w", pady=(3, 0))

        tk.Button(
            self.sidebar, text="↪  Sign out",
            command=self.logout,
            bg=WHITE, fg=DANGER,
            activebackground=DANGER_LIGHT,
            activeforeground=DANGER_DARK,
            relief="flat", bd=0,
            font=(FONT, 9, "bold"),
            cursor="hand2", anchor="w",
            padx=20, pady=11
        ).pack(fill="x", padx=8, pady=(2, 10))


    # ========================================================
    # SIDEBAR BUTTON
    # ========================================================

    def sidebar_button(
        self,
        icon,
        text,
        command
    ):

        button = tk.Frame(
            self.sidebar,
            bg=WHITE,
            cursor="hand2"
        )
        button.pack(fill="x", padx=10, pady=2)

        accent = tk.Frame(button, bg=WHITE, width=3)
        accent.pack(side="left", fill="y")

        icon_label = tk.Label(
            button, text=icon, bg=WHITE, fg=MUTED,
            font=(FONT, 12), width=3
        )
        icon_label.pack(side="left", padx=(5, 3), pady=8)

        text_label = tk.Label(
            button, text=text, bg=WHITE, fg=TEXT_LIGHT,
            font=(FONT, 9, "bold"), anchor="w"
        )
        text_label.pack(side="left", fill="x", expand=True, pady=8)

        widgets = (button, icon_label, text_label, accent)

        def enter(event):
            for widget in widgets:
                widget.configure(bg=PRIMARY_LIGHT)
            accent.configure(bg=PRIMARY)
            icon_label.configure(fg=PRIMARY)
            text_label.configure(fg=PRIMARY_DARK)

        def leave(event):
            for widget in widgets:
                widget.configure(bg=WHITE)
            accent.configure(bg=WHITE)
            icon_label.configure(fg=MUTED)
            text_label.configure(fg=TEXT_LIGHT)

        def click(event):
            command()

        for widget in widgets:
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
            widget.bind("<Button-1>", click)


    # ========================================================
    # CLEAR PAGE
    # ========================================================

    def clear(self):

        for widget in self.content.winfo_children():

            widget.destroy()

        self.canvas.yview_moveto(
            0
        )


    # ========================================================
    # TOP HEADER
    # ========================================================

    def top_header(
        self,
        title,
        subtitle
    ):

        header = tk.Frame(self.content, bg=WHITE)
        header.pack(fill="x")

        left = tk.Frame(header, bg=WHITE)
        left.pack(side="left", padx=34, pady=24)

        tk.Label(
            left, text=title, bg=WHITE, fg=TEXT,
            font=(FONT, 21, "bold")
        ).pack(anchor="w")

        tk.Label(
            left, text=subtitle, bg=WHITE, fg=MUTED,
            font=(FONT, 9)
        ).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(header, bg=WHITE)
        right.pack(side="right", padx=30)

        role_color, role_bg = ROLE_COLORS.get(
            self.role, (PRIMARY, PRIMARY_LIGHT)
        )

        badge = tk.Label(
            right, text=f"  {self.role}  ",
            bg=role_bg, fg=role_color,
            font=(FONT, 8, "bold"), padx=5, pady=4
        )
        badge.pack(side="right")

        tk.Label(
            right, text=f"Hi, {self.username}",
            bg=WHITE, fg=TEXT_LIGHT,
            font=(FONT, 9, "bold")
        ).pack(side="right", padx=12)

        tk.Frame(
            self.content, bg=BORDER, height=1
        ).pack(fill="x")


    # ========================================================
    # PAGE TITLE
    # ========================================================

    def page_title(
        self,
        title,
        subtitle=""
    ):

        self.top_header(
            title,
            subtitle
        )


    # ========================================================
    # BENTO CARD
    # ========================================================

    def make_bento_card(
        self,
        parent,
        icon,
        title,
        subtitle,
        command,
        accent=PRIMARY,
        accent_bg=PRIMARY_LIGHT
    ):

        card = tk.Frame(
            parent, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2"
        )

        top = tk.Frame(card, bg=accent, height=4)
        top.pack(fill="x")
        top.pack_propagate(False)

        inner = tk.Frame(card, bg=WHITE)
        inner.pack(fill="both", expand=True, padx=20, pady=18)

        icon_box = tk.Label(
            inner, text=icon,
            bg=accent_bg, fg=accent,
            font=(FONT, 17, "bold"),
            width=3, height=1
        )
        icon_box.pack(anchor="w")

        tk.Label(
            inner, text=title, bg=WHITE, fg=TEXT,
            font=(FONT, 11, "bold"), anchor="w"
        ).pack(fill="x", pady=(14, 3))

        tk.Label(
            inner, text=subtitle, bg=WHITE, fg=MUTED,
            font=(FONT, 8), anchor="w",
            justify="left", wraplength=240
        ).pack(fill="x")

        arrow = tk.Label(
            inner, text="→", bg=WHITE, fg=MUTED,
            font=(FONT, 13, "bold")
        )
        arrow.pack(anchor="e", pady=(12, 0))

        widgets = (card, inner, icon_box, arrow)

        def enter(event):
            card.configure(highlightbackground=accent)
            inner.configure(bg=accent_bg)
            arrow.configure(bg=accent_bg, fg=accent)
            icon_box.configure(bg=WHITE)

        def leave(event):
            card.configure(highlightbackground=BORDER)
            inner.configure(bg=WHITE)
            arrow.configure(bg=WHITE, fg=MUTED)
            icon_box.configure(bg=accent_bg)

        def click(event):
            command()

        for widget in widgets:
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
            widget.bind("<Button-1>", click)

        return card


    # ========================================================
    # BENTO GRID
    # ========================================================

    def bento_grid(
        self,
        items,
        columns=3
    ):

        wrapper = tk.Frame(
            self.content,
            bg=BG
        )

        wrapper.pack(
            fill="x",
            padx=25,
            pady=18
        )

        for column in range(columns):

            wrapper.columnconfigure(
                column,
                weight=1,
                uniform="bento"
            )

        for index, item in enumerate(items):

            row = index // columns

            column = index % columns

            icon = item[0]
            title = item[1]
            subtitle = item[2]
            command = item[3]

            accent = (
                item[4]
                if len(item) > 4
                else PRIMARY
            )

            accent_bg = (
                item[5]
                if len(item) > 5
                else PRIMARY_LIGHT
            )

            card = self.make_bento_card(
                wrapper,
                icon,
                title,
                subtitle,
                command,
                accent,
                accent_bg
            )

            card.grid(
                row=row,
                column=column,
                padx=7,
                pady=7,
                sticky="nsew"
            )


    # ========================================================
    # BACK BUTTON
    # ========================================================

    def back_button(
        self,
        command
    ):

        ttk.Button(
            self.content,
            text="←  Back",
            command=command,
            style="Back.TButton"
        ).pack(
            pady=(
                10,
                28
            )
        )


    # ========================================================
    # DASHBOARD HOME
    # ========================================================

    def build(self):

        self.clear()

        self.page_title(
            "Good evening, " + self.username,
            "Here's your PatientConnect overview"
        )

        # ----------------------------------------------------
        # Welcome section
        # ----------------------------------------------------

        welcome = tk.Frame(
            self.content,
            bg=BG
        )

        welcome.pack(
            fill="x",
            padx=32,
            pady=(
                20,
                5
            )
        )

        tk.Label(
            welcome,
            text="Healthcare Operations",
            bg=BG,
            fg=TEXT,
            font=(
                FONT,
                15,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            welcome,
            text="Manage patients, appointments, clinical information and reports from one place.",
            bg=BG,
            fg=MUTED,
            font=(
                FONT,
                9
            )
        ).pack(
            anchor="w",
            pady=3
        )

        # ----------------------------------------------------
        # KPI cards
        # ----------------------------------------------------

        self.dashboard_kpis()

        # ----------------------------------------------------
        # Role based cards
        # ----------------------------------------------------

        if self.role == "ADMIN":

            items = [
                (
                    "👥",
                    "Patient Management",
                    "View, search and create patient records.",
                    self.patient_management,
                    PRIMARY,
                    PRIMARY_LIGHT
                ),

                (
                    "📅",
                    "Appointments",
                    "Manage bookings and appointment status.",
                    self.appointment_management,
                    BLUE,
                    BLUE_LIGHT
                ),

                (
                    "📊",
                    "Reports",
                    "View analytics and healthcare reports.",
                    self.reports,
                    PURPLE,
                    PURPLE_LIGHT
                ),

                (
                    "💬",
                    "Messages",
                    "View patient communication records.",
                    self.messages,
                    SUCCESS,
                    SUCCESS_LIGHT
                ),

                (
                    "🩺",
                    "Clinical Information",
                    "Conditions, recalls and clinical history.",
                    self.clinical_information,
                    DANGER,
                    DANGER_LIGHT
                ),

                (
                    "🏥",
                    "Clinic Information",
                    "Manage clinics and healthcare providers.",
                    self.clinic_information,
                    WARNING,
                    WARNING_LIGHT
                ),

                (
                    "💳",
                    "Insurance",
                    "View patient insurance records.",
                    self.insurance,
                    BLUE,
                    BLUE_LIGHT
                ),

                (
                    "✅",
                    "Eligibility",
                    "Review insurance eligibility information.",
                    self.eligibility,
                    SUCCESS,
                    SUCCESS_LIGHT
                ),

                (
                    "🔐",
                    "Audit Logs",
                    "Review system audit records.",
                    self.audit_logs,
                    DANGER,
                    DANGER_LIGHT
                ),

                (
                    "📄",
                    "Export Patients",
                    "Export patient records to CSV.",
                    self.export_patients,
                    PRIMARY,
                    PRIMARY_LIGHT
                )
            ]

        elif self.role == "DOCTOR":

            items = [
                (
                    "👥",
                    "Patients",
                    "View and search patient records.",
                    self.patient_management,
                    PRIMARY,
                    PRIMARY_LIGHT
                ),

                (
                    "📅",
                    "Appointments",
                    "Manage patient appointments.",
                    self.appointment_management,
                    BLUE,
                    BLUE_LIGHT
                ),

                (
                    "🩺",
                    "Clinical Information",
                    "View conditions and clinical history.",
                    self.clinical_information,
                    DANGER,
                    DANGER_LIGHT
                ),

                (
                    "💬",
                    "Messages",
                    "View healthcare messages.",
                    self.messages,
                    SUCCESS,
                    SUCCESS_LIGHT
                ),

                (
                    "📊",
                    "Reports",
                    "Review appointment and delivery reports.",
                    self.reports,
                    PURPLE,
                    PURPLE_LIGHT
                ),

                (
                    "💳",
                    "Insurance",
                    "View patient insurance.",
                    self.insurance,
                    BLUE,
                    BLUE_LIGHT
                ),

                (
                    "✅",
                    "Eligibility",
                    "Review insurance eligibility.",
                    self.eligibility,
                    SUCCESS,
                    SUCCESS_LIGHT
                )
            ]

        else:

            items = [
                (
                    "👥",
                    "Patients",
                    "View and search patient records.",
                    self.patient_management,
                    PRIMARY,
                    PRIMARY_LIGHT
                ),

                (
                    "📅",
                    "Appointments",
                    "View and manage appointments.",
                    self.appointment_management,
                    BLUE,
                    BLUE_LIGHT
                ),

                (
                    "💬",
                    "Messages",
                    "View healthcare messages.",
                    self.messages,
                    SUCCESS,
                    SUCCESS_LIGHT
                ),

                (
                    "⏰",
                    "Due Reminders",
                    "Find upcoming reminder candidates.",
                    self.due_reminders,
                    WARNING,
                    WARNING_LIGHT
                ),

                (
                    "🏥",
                    "Clinic Information",
                    "View clinics and providers.",
                    self.clinic_information,
                    PRIMARY,
                    PRIMARY_LIGHT
                ),

                (
                    "💳",
                    "Insurance",
                    "View patient insurance.",
                    self.insurance,
                    BLUE,
                    BLUE_LIGHT
                ),

                (
                    "✅",
                    "Eligibility",
                    "Review insurance eligibility.",
                    self.eligibility,
                    SUCCESS,
                    SUCCESS_LIGHT
                )
            ]

        self.bento_grid(
            items,
            columns=3
        )


    # ========================================================
    # DASHBOARD KPI
    # ========================================================

    def dashboard_kpis(self):

        frame = tk.Frame(
            self.content,
            bg=BG
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        for column in range(3):

            frame.columnconfigure(
                column,
                weight=1,
                uniform="kpi"
            )

        self.kpi_card(
            frame,
            0,
            "👥",
            "Patients",
            "Patient records",
            PRIMARY,
            PRIMARY_LIGHT
        )

        self.kpi_card(
            frame,
            1,
            "📅",
            "Appointments",
            "Appointment records",
            BLUE,
            BLUE_LIGHT
        )

        self.kpi_card(
            frame,
            2,
            "💬",
            "Messages",
            "Message records",
            SUCCESS,
            SUCCESS_LIGHT
        )


    # ========================================================
    # KPI CARD
    # ========================================================

    def kpi_card(
        self,
        parent,
        column,
        icon,
        title,
        subtitle,
        accent,
        accent_bg
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            padx=7,
            sticky="nsew"
        )

        inner = tk.Frame(
            card,
            bg=WHITE
        )

        inner.pack(
            fill="both",
            padx=18,
            pady=15
        )

        tk.Label(
            inner,
            text=icon,
            bg=accent_bg,
            fg=accent,
            font=(
                FONT,
                16
            ),
            width=3
        ).pack(
            side="left"
        )

        text = tk.Frame(
            inner,
            bg=WHITE
        )

        text.pack(
            side="left",
            padx=12
        )

        tk.Label(
            text,
            text=title,
            bg=WHITE,
            fg=TEXT,
            font=(
                FONT,
                11,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            text,
            text=subtitle,
            bg=WHITE,
            fg=MUTED,
            font=(
                FONT,
                8
            )
        ).pack(
            anchor="w"
        )


    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        if messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        ):

            self.canvas.unbind_all(
                "<MouseWheel>"
            )

            self.logout_callback()


    # ========================================================
    # PATIENT MANAGEMENT
    # ========================================================

    def patient_management(self):

        self.clear()

        self.page_title(
            "👥 Patient Management",
            "Manage patient records and healthcare information"
        )

        items = [
            (
                "📋",
                "View Patients",
                "Browse all patient records.",
                self.view_patients,
                PRIMARY,
                PRIMARY_LIGHT
            ),

            (
                "🔎",
                "Search Patient",
                "Search patients by first or last name.",
                self.search_patient,
                BLUE,
                BLUE_LIGHT
            ),

            (
                "🏥",
                "View Clinics",
                "View registered healthcare clinics.",
                self.view_clinics,
                WARNING,
                WARNING_LIGHT
            ),

            (
                "👨‍⚕️",
                "View Providers",
                "View healthcare providers.",
                self.view_providers,
                SUCCESS,
                SUCCESS_LIGHT
            )
        ]

        if self.role == "ADMIN":

            items.append(
                (
                    "➕",
                    "Create Patient",
                    "Register a new patient.",
                    self.create_patient,
                    PRIMARY,
                    PRIMARY_LIGHT
                )
            )

        self.bento_grid(
            items,
            columns=2
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # CREATE PATIENT
    # ========================================================

    def create_patient(self):

        self.clear()

        self.page_title(
            "➕ Create Patient",
            "Register a new patient in PatientConnect"
        )

        card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=35,
            pady=15
        )

        form = tk.Frame(
            card,
            bg=WHITE
        )

        form.pack(
            padx=35,
            pady=30
        )

        fields = [
            "Clinic ID",
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Date of Birth"
        ]

        entries = {}

        for row, field in enumerate(fields):

            tk.Label(
                form,
                text=field,
                bg=WHITE,
                fg=TEXT_LIGHT,
                font=(
                    FONT,
                    9,
                    "bold"
                )
            ).grid(
                row=row,
                column=0,
                sticky="e",
                padx=15,
                pady=9
            )

            entry = ttk.Entry(
                form,
                width=38,
                style="Modern.TEntry"
            )

            entry.grid(
                row=row,
                column=1,
                padx=15,
                pady=9,
                ipady=4
            )

            entries[field] = entry

        # ----------------------------------------------------
        # Gender
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Gender",
            bg=WHITE,
            fg=TEXT_LIGHT,
            font=(
                FONT,
                9,
                "bold"
            )
        ).grid(
            row=6,
            column=0,
            sticky="e",
            padx=15,
            pady=9
        )

        gender = ttk.Combobox(
            form,
            values=[
                "M",
                "F",
                "Other",
                "Unknown"
            ],
            state="readonly",
            width=35,
            style="Modern.TCombobox"
        )

        gender.grid(
            row=6,
            column=1,
            padx=15,
            pady=9,
            ipady=3
        )

        gender.set(
            "Unknown"
        )

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        def save():

            conn = None

            cursor = None

            try:

                clinic_text = entries[
                    "Clinic ID"
                ].get().strip()

                first_name = entries[
                    "First Name"
                ].get().strip()

                last_name = entries[
                    "Last Name"
                ].get().strip()

                email = entries[
                    "Email"
                ].get().strip()

                phone = entries[
                    "Phone"
                ].get().strip()

                dob = entries[
                    "Date of Birth"
                ].get().strip()

                if not clinic_text:

                    messagebox.showwarning(
                        "Required",
                        "Clinic ID is required."
                    )

                    return

                if not first_name:

                    messagebox.showwarning(
                        "Required",
                        "First Name is required."
                    )

                    return

                if not last_name:

                    messagebox.showwarning(
                        "Required",
                        "Last Name is required."
                    )

                    return

                clinic_id = int(
                    clinic_text
                )

                conn = get_connection()

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO patients
                    (
                        clinic_id,
                        first_name,
                        last_name,
                        email,
                        phone,
                        date_of_birth,
                        gender
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        clinic_id,
                        first_name,
                        last_name,
                        email or None,
                        phone or None,
                        dob or None,
                        gender.get()
                    )
                )

                conn.commit()

                patient_id = cursor.lastrowid

                messagebox.showinfo(
                    "Success",
                    f"✅ Patient created successfully!\n\n"
                    f"Patient ID: {patient_id}"
                )

                for entry in entries.values():

                    entry.delete(
                        0,
                        "end"
                    )

                gender.set(
                    "Unknown"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Data",
                    "Clinic ID must be a number."
                )

            except Exception as e:

                if conn:

                    conn.rollback()

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:

                if cursor:

                    cursor.close()

                if conn:

                    conn.close()

        ttk.Button(
            form,
            text="✅  Create Patient",
            command=save,
            style="Success.TButton"
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            pady=20
        )

        self.back_button(
            self.patient_management
        )


    # ========================================================
    # VIEW PATIENTS
    # ========================================================

    def view_patients(self):

        self.clear()

        self.page_title(
            "📋 Patients",
            "All registered patient records"
        )

        columns = (
            "patient_id",
            "clinic_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "gender"
        )

        tree = self.create_table(
            columns
        )

        conn = None

        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    patient_id,
                    clinic_id,
                    first_name,
                    last_name,
                    email,
                    phone,
                    date_of_birth,
                    gender
                FROM patients
                ORDER BY patient_id DESC
                """
            )

            self.populate_tree(
                tree,
                cursor.fetchall()
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:

                cursor.close()

            if conn:

                conn.close()

        self.back_button(
            self.patient_management
        )


    # ========================================================
    # SEARCH PATIENT
    # ========================================================

    def search_patient(self):

        self.clear()

        self.page_title(
            "🔎 Search Patient",
            "Find patients by first or last name"
        )

        search_card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        search_card.pack(
            fill="x",
            padx=35,
            pady=15
        )

        form = tk.Frame(
            search_card,
            bg=WHITE
        )

        form.pack(
            fill="x",
            padx=20,
            pady=18
        )

        tk.Label(
            form,
            text="Patient name",
            bg=WHITE,
            fg=TEXT_LIGHT,
            font=(
                FONT,
                9,
                "bold"
            )
        ).pack(
            side="left",
            padx=8
        )

        search = ttk.Entry(
            form,
            width=35,
            style="Modern.TEntry"
        )

        search.pack(
            side="left",
            padx=8,
            ipady=3
        )

        columns = (
            "patient_id",
            "clinic_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "gender"
        )

        tree = self.create_table(
            columns
        )

        def search_patient():

            for item in tree.get_children():

                tree.delete(
                    item
                )

            conn = None

            cursor = None

            try:

                conn = get_connection()

                cursor = conn.cursor()

                value = search.get().strip()

                cursor.execute(
                    """
                    SELECT
                        patient_id,
                        clinic_id,
                        first_name,
                        last_name,
                        email,
                        phone,
                        date_of_birth,
                        gender
                    FROM patients
                    WHERE first_name LIKE %s
                       OR last_name LIKE %s
                    ORDER BY patient_id DESC
                    """,
                    (
                        f"%{value}%",
                        f"%{value}%"
                    )
                )

                self.populate_tree(
                    tree,
                    cursor.fetchall()
                )

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

            finally:

                if cursor:

                    cursor.close()

                if conn:

                    conn.close()

        ttk.Button(
            form,
            text="🔎 Search",
            command=search_patient,
            style="Primary.TButton"
        ).pack(
            side="left",
            padx=8
        )

        self.back_button(
            self.patient_management
        )


    # ========================================================
    # CLINICS
    # ========================================================

    def view_clinics(self):

        self.clear()

        self.page_title(
            "🏥 Clinics",
            "Registered healthcare clinics"
        )

        self.simple_query_table(
            "SELECT * FROM clinics"
        )

        self.back_button(
            self.patient_management
        )


    # ========================================================
    # PROVIDERS
    # ========================================================

    def view_providers(self):

        self.clear()

        self.page_title(
            "👨‍⚕️ Providers",
            "Registered healthcare providers"
        )

        self.simple_query_table(
            "SELECT * FROM providers"
        )

        self.back_button(
            self.patient_management
        )


    # ========================================================
    # APPOINTMENT MANAGEMENT
    # ========================================================

    def appointment_management(self):

        self.clear()

        self.page_title(
            "📅 Appointment Management",
            "Manage bookings, status and appointment reports"
        )

        items = [
            (
                "📋",
                "View Appointments",
                "Browse all appointments.",
                self.view_appointments,
                BLUE,
                BLUE_LIGHT
            ),

            (
                "🕘",
                "Appointment History",
                "Review patient appointment history.",
                self.patient_history,
                PRIMARY,
                PRIMARY_LIGHT
            ),

            (
                "👨‍⚕️",
                "Provider Count",
                "View appointments grouped by provider.",
                self.provider_count,
                SUCCESS,
                SUCCESS_LIGHT
            ),

            (
                "🏥",
                "Clinic Count",
                "View appointments grouped by clinic.",
                self.clinic_count,
                WARNING,
                WARNING_LIGHT
            ),

            (
                "📊",
                "Status Summary",
                "Review appointment status totals.",
                self.status_summary,
                PURPLE,
                PURPLE_LIGHT
            )
        ]

        if self.role in (
            "ADMIN",
            "DOCTOR"
        ):

            items.extend(
                [
                    (
                        "➕",
                        "Book Appointment",
                        "Create a new appointment.",
                        self.book_appointment,
                        SUCCESS,
                        SUCCESS_LIGHT
                    ),

                    (
                        "🔄",
                        "Update Status",
                        "Change an appointment status.",
                        self.update_status,
                        PRIMARY,
                        PRIMARY_LIGHT
                    )
                ]
            )

        self.bento_grid(
            items,
            columns=2
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # VIEW APPOINTMENTS
    # ========================================================

    def view_appointments(self):

        self.clear()

        self.page_title(
            "📋 Appointments",
            "All scheduled and historical appointments"
        )

        self.simple_query_table(
            """
            SELECT *
            FROM appointments
            ORDER BY appointment_id DESC
            """
        )

        self.back_button(
            self.appointment_management
        )


    # ========================================================
    # BOOK APPOINTMENT
    # ========================================================

    def book_appointment(self):

        self.clear()

        self.page_title(
            "➕ Book Appointment",
            "Create an appointment and send confirmation email"
        )

        card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=35,
            pady=15
        )

        frame = tk.Frame(
            card,
            bg=WHITE
        )

        frame.pack(
            padx=35,
            pady=30
        )

        labels = [
            "Patient ID",
            "Provider ID",
            "Appointment Date/Time"
        ]

        entries = []

        for row, label in enumerate(labels):

            tk.Label(
                frame,
                text=label,
                bg=WHITE,
                fg=TEXT_LIGHT,
                font=(
                    FONT,
                    9,
                    "bold"
                )
            ).grid(
                row=row,
                column=0,
                padx=12,
                pady=10,
                sticky="e"
            )

            entry = ttk.Entry(
                frame,
                width=38,
                style="Modern.TEntry"
            )

            entry.grid(
                row=row,
                column=1,
                padx=12,
                pady=10,
                ipady=4
            )

            entries.append(
                entry
            )

        def book():

            conn = None

            cursor = None

            try:

                conn = get_connection()

                cursor = conn.cursor()

                patient_id = int(
                    entries[0].get().strip()
                )

                provider_id = int(
                    entries[1].get().strip()
                )

                appointment_time = entries[
                    2
                ].get().strip()

                if not appointment_time:

                    messagebox.showwarning(
                        "Required",
                        "Appointment Date/Time is required."
                    )

                    return

                # ------------------------------------------------
                # EXISTING BACKEND LOGIC
                # ------------------------------------------------

                reason = "General consultation"

                result = cursor.callproc(
                    "sp_book_appointment",
                    [
                        patient_id,
                        provider_id,
                        appointment_time,
                        reason
                    ]
                )

                conn.commit()

                # ------------------------------------------------
                # LOOK UP PATIENT EMAIL
                # ------------------------------------------------

                lookup_cursor = conn.cursor(
                    dictionary=True
                )

                lookup_cursor.execute(
                    """
                    SELECT
                        first_name,
                        last_name,
                        email
                    FROM patients
                    WHERE patient_id = %s
                    """,
                    (
                        patient_id,
                    )
                )

                patient = lookup_cursor.fetchone()

                lookup_cursor.close()

                # ------------------------------------------------
                # SEND MAILTRAP
                # ------------------------------------------------

                email_sent = False

                if patient and patient.get(
                    "email"
                ):

                    full_name = (
                        f"{patient['first_name']} "
                        f"{patient['last_name']}"
                    )

                    email_sent = send_email(
                        to_email=patient[
                            "email"
                        ],

                        to_name=full_name,

                        subject=(
                            "Your PatientConnect "
                            "Appointment is Confirmed"
                        ),

                        text=(
                            f"Hi {patient['first_name']},\n\n"
                            f"Your appointment has been "
                            f"booked successfully.\n\n"
                            f"Appointment Date/Time: "
                            f"{appointment_time}\n"
                            f"Reason: {reason}\n\n"
                            f"Thanks,\n"
                            f"PatientConnect"
                        )
                    )

                # ------------------------------------------------
                # EMAIL STATUS
                # ------------------------------------------------

                if email_sent:

                    status_note = (
                        "\n\n📧 Confirmation email sent."
                    )

                else:

                    status_note = (
                        "\n\n⚠️ Appointment booked, "
                        "but no confirmation email was sent."
                    )

                messagebox.showinfo(
                    "Success",
                    f"✅ Appointment booked successfully.\n\n"
                    f"Patient ID: {patient_id}\n"
                    f"Provider ID: {provider_id}\n"
                    f"Date/Time: {appointment_time}\n"
                    f"Reason: {reason}"
                    f"{status_note}"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Data",
                    "Patient ID and Provider ID must be numbers."
                )

            except Exception as e:

                if conn:

                    conn.rollback()

                messagebox.showerror(
                    "Appointment Error",
                    str(e)
                )

            finally:

                if cursor:

                    cursor.close()

                if conn:

                    conn.close()

        ttk.Button(
            frame,
            text="✅  Book Appointment",
            command=book,
            style="Success.TButton"
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=20
        )

        self.back_button(
            self.appointment_management
        )


    # ========================================================
    # UPDATE STATUS
    # ========================================================

    def update_status(self):

        self.clear()

        self.page_title(
            "🔄 Update Appointment Status",
            "Change the status of an existing appointment"
        )

        card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=35,
            pady=15
        )

        frame = tk.Frame(
            card,
            bg=WHITE
        )

        frame.pack(
            padx=35,
            pady=30
        )

        tk.Label(
            frame,
            text="Appointment ID",
            bg=WHITE,
            fg=TEXT_LIGHT,
            font=(
                FONT,
                9,
                "bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=10
        )

        appointment_id = ttk.Entry(
            frame,
            width=38,
            style="Modern.TEntry"
        )

        appointment_id.grid(
            row=0,
            column=1,
            padx=12,
            pady=10,
            ipady=4
        )

        tk.Label(
            frame,
            text="Status",
            bg=WHITE,
            fg=TEXT_LIGHT,
            font=(
                FONT,
                9,
                "bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=12,
            pady=10
        )

        status = ttk.Combobox(
            frame,
            values=[
                "SCHEDULED",
                "CONFIRMED",
                "COMPLETED",
                "CANCELLED",
                "NO_SHOW",
                "RESCHEDULED"
            ],
            state="readonly",
            width=35,
            style="Modern.TCombobox"
        )

        status.grid(
            row=1,
            column=1,
            padx=12,
            pady=10,
            ipady=3
        )

        status.set(
            "SCHEDULED"
        )

        def update():

            conn = None

            cursor = None

            try:

                conn = get_connection()

                cursor = conn.cursor()

                cursor.callproc(
                    "sp_update_appointment_status",
                    [
                        int(
                            appointment_id.get()
                        ),
                        status.get()
                    ]
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "✅ Appointment status updated."
                )

            except Exception as e:

                if conn:

                    conn.rollback()

                messagebox.showerror(
                    "Update Error",
                    str(e)
                )

            finally:

                if cursor:

                    cursor.close()

                if conn:

                    conn.close()

        ttk.Button(
            frame,
            text="✅  Update Status",
            command=update,
            style="Success.TButton"
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=20
        )

        self.back_button(
            self.appointment_management
        )


    # ========================================================
    # PATIENT HISTORY
    # ========================================================

    def patient_history(self):

        self.clear()

        self.page_title(
            "🕘 Patient Appointment History",
            "Appointment records ordered by latest appointment"
        )

        self.simple_query_table(
            """
            SELECT *
            FROM appointments
            ORDER BY appointment_id DESC
            """
        )

        self.back_button(
            self.appointment_management
        )


    # ========================================================
    # REPORTS
    # ========================================================

    def reports(self):

        self.clear()

        self.page_title(
            "📊 Reports",
            "Healthcare analytics and stored procedure reports"
        )

        items = [
            (
                "🏥",
                "Clinic Appointment Count",
                "Appointments grouped by clinic.",
                self.clinic_report,
                WARNING,
                WARNING_LIGHT
            ),

            (
                "👨‍⚕️",
                "Provider Appointment Count",
                "Appointments grouped by provider.",
                self.provider_report,
                SUCCESS,
                SUCCESS_LIGHT
            ),

            (
                "📊",
                "Status Summary",
                "Appointment status distribution.",
                self.status_report,
                PRIMARY,
                PRIMARY_LIGHT
            ),

            (
                "💬",
                "Message Delivery",
                "Message delivery statistics.",
                self.message_report,
                BLUE,
                BLUE_LIGHT
            ),

            (
                "⚠️",
                "No-show Report",
                "Appointments marked as no-show.",
                self.no_show,
                DANGER,
                DANGER_LIGHT
            ),

            (
                "🔔",
                "Recall Candidates",
                "Patients requiring recall.",
                self.recall_candidates,
                PURPLE,
                PURPLE_LIGHT
            ),

            (
                "⏰",
                "Due Reminders",
                "Appointments requiring reminders.",
                self.due_reminders,
                WARNING,
                WARNING_LIGHT
            ),

            (
                "🕘",
                "Appointment Status History",
                "Historical status changes.",
                self.appointment_history,
                BLUE,
                BLUE_LIGHT
            )
        ]

        self.bento_grid(
            items,
            columns=2
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # REPORT HELPERS
    # ========================================================

    def clinic_report(self):

        self.procedure_table(
            "sp_clinic_appointment_count",
            [],
            self.reports
        )


    def clinic_count(self):

        self.procedure_table(
            "sp_clinic_appointment_count",
            [],
            self.appointment_management
        )


    def provider_report(self):

        self.clear()

        self.page_title(
            "👨‍⚕️ Provider Appointment Count",
            "Appointments grouped by provider"
        )

        self.simple_query_table(
            """
            SELECT
                provider_id,
                COUNT(*) AS appointment_count
            FROM appointments
            GROUP BY provider_id
            """
        )

        self.back_button(
            self.reports
        )


    def provider_count(self):

        self.provider_report()


    def status_report(self):

        self.clear()

        self.page_title(
            "📊 Appointment Status Summary",
            "Appointment totals grouped by status"
        )

        self.simple_query_table(
            """
            SELECT
                status,
                COUNT(*) AS total
            FROM appointments
            GROUP BY status
            """
        )

        self.back_button(
            self.reports
        )


    def status_summary(self):

        self.status_report()


    def message_report(self):

        self.clear()

        self.page_title(
            "💬 Message Delivery Summary",
            "Message totals grouped by delivery status"
        )

        self.simple_query_table(
            """
            SELECT
                status,
                COUNT(*) AS total
            FROM messages
            GROUP BY status
            """
        )

        self.back_button(
            self.reports
        )


    def message_summary(self):

        self.message_report()


    def no_show(self):

        self.clear()

        self.page_title(
            "⚠️ No-show Report",
            "Appointments marked as no-show by provider"
        )

        self.simple_query_table(
            """
            SELECT
                provider_id,
                COUNT(*) AS no_show_count
            FROM appointments
            WHERE status = 'NO_SHOW'
            GROUP BY provider_id
            """
        )

        self.back_button(
            self.reports
        )


    def recall_candidates(self):

        self.procedure_table(
            "sp_recall_candidates",
            [],
            self.reports
        )


    # ========================================================
    # DUE REMINDERS
    # ========================================================

    def due_reminders(self):

        self.clear()

        self.page_title(
            "⏰ Due Reminders",
            "Find appointments that require reminders"
        )

        control_card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        control_card.pack(
            fill="x",
            padx=35,
            pady=15
        )

        control = tk.Frame(
            control_card,
            bg=WHITE
        )

        control.pack(
            padx=20,
            pady=18
        )

        tk.Label(
            control,
            text="Hours ahead",
            bg=WHITE,
            fg=TEXT_LIGHT,
            font=(
                FONT,
                9,
                "bold"
            )
        ).pack(
            side="left",
            padx=8
        )

        hours = ttk.Entry(
            control,
            width=10,
            style="Modern.TEntry"
        )

        hours.insert(
            0,
            "48"
        )

        hours.pack(
            side="left",
            padx=8,
            ipady=3
        )

        tree = self.create_table(
            [
                "Result"
            ]
        )

        def run():

            conn = None

            cursor = None

            try:

                conn = get_connection()

                cursor = conn.cursor()

                result = cursor.callproc(
                    "sp_due_reminders",
                    [
                        int(
                            hours.get()
                        )
                    ]
                )

                for item in tree.get_children():

                    tree.delete(
                        item
                    )

                self.populate_tree(
                    tree,
                    [
                        (
                            value,
                        )
                        for value in result
                    ]
                )

            except Exception as e:

                messagebox.showerror(
                    "Reminder Error",
                    str(e)
                )

            finally:

                if cursor:

                    cursor.close()

                if conn:

                    conn.close()

        ttk.Button(
            control,
            text="▶  Run",
            command=run,
            style="Primary.TButton"
        ).pack(
            side="left",
            padx=8
        )

        self.back_button(
            self.reports
        )


    # ========================================================
    # APPOINTMENT HISTORY
    # ========================================================

    def appointment_history(self):

        self.clear()

        self.page_title(
            "🕘 Appointment Status History",
            "Historical appointment status changes"
        )

        self.simple_query_table(
            """
            SELECT *
            FROM appointment_status_history
            ORDER BY 1 DESC
            """
        )

        self.back_button(
            self.clinical_information
        )


    # ========================================================
    # MESSAGES
    # ========================================================

    def messages(self):

        self.clear()

        self.page_title(
            "💬 Messages",
            "PatientConnect communication records"
        )

        self.simple_query_table(
            "SELECT * FROM messages"
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # CLINICAL INFORMATION
    # ========================================================

    def clinical_information(self):

        self.clear()

        self.page_title(
            "🩺 Clinical Information",
            "Clinical conditions and patient history"
        )

        items = [
            (
                "🧬",
                "Conditions",
                "View available medical conditions.",
                self.conditions,
                DANGER,
                DANGER_LIGHT
            ),

            (
                "👤",
                "Patient Conditions",
                "View patient-condition relationships.",
                self.patient_conditions,
                PRIMARY,
                PRIMARY_LIGHT
            ),

            (
                "🔔",
                "Recall Candidates",
                "Find patients requiring recall.",
                self.recall_candidates,
                PURPLE,
                PURPLE_LIGHT
            ),

            (
                "🕘",
                "Appointment History",
                "Review appointment status history.",
                self.appointment_history,
                BLUE,
                BLUE_LIGHT
            )
        ]

        self.bento_grid(
            items,
            columns=2
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # CONDITIONS
    # ========================================================

    def conditions(self):

        self.clear()

        self.page_title(
            "🧬 Conditions",
            "Available medical conditions"
        )

        self.simple_query_table(
            "SELECT * FROM conditions"
        )

        self.back_button(
            self.clinical_information
        )


    # ========================================================
    # PATIENT CONDITIONS
    # ========================================================

    def patient_conditions(self):

        self.clear()

        self.page_title(
            "👤 Patient Conditions",
            "Patient-condition records"
        )

        self.simple_query_table(
            "SELECT * FROM patient_conditions"
        )

        self.back_button(
            self.clinical_information
        )


    # ========================================================
    # INSURANCE
    # ========================================================

    def insurance(self):

        self.clear()

        self.page_title(
            "💳 Patient Insurance",
            "Patient insurance records"
        )

        self.simple_query_table(
            "SELECT * FROM patient_insurance"
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # ELIGIBILITY
    # ========================================================

    def eligibility(self):

        self.clear()

        self.page_title(
            "✅ Insurance Eligibility",
            "Insurance eligibility records"
        )

        self.simple_query_table(
            "SELECT * FROM insurance_eligibility"
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # AUDIT LOGS
    # ========================================================

    def audit_logs(self):

        self.clear()

        self.page_title(
            "🔐 Audit Logs",
            "System activity and audit records"
        )

        self.simple_query_table(
            "SELECT * FROM audit_logs"
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # CLINIC INFORMATION
    # ========================================================

    def clinic_information(self):

        self.clear()

        self.page_title(
            "🏥 Clinic Information",
            "Clinics and healthcare providers"
        )

        items = [
            (
                "🏥",
                "View Clinics",
                "Browse registered clinics.",
                self.view_clinics,
                WARNING,
                WARNING_LIGHT
            ),

            (
                "👨‍⚕️",
                "View Providers",
                "Browse registered providers.",
                self.view_providers,
                SUCCESS,
                SUCCESS_LIGHT
            )
        ]

        self.bento_grid(
            items,
            columns=2
        )

        self.back_button(
            self.build
        )


    # ========================================================
    # EXPORT PATIENTS
    # ========================================================

    def export_patients(self):

        conn = None

        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM patients"
            )

            rows = cursor.fetchall()

            columns = [
                desc[0]
                for desc in cursor.description
            ]

            filename = (
                "patients_gui_export.csv"
            )

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow(
                    columns
                )

                writer.writerows(
                    rows
                )

            messagebox.showinfo(
                "Export Complete",
                f"✅ Patients exported successfully.\n\n"
                f"File: {filename}"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )

        finally:

            if cursor:

                cursor.close()

            if conn:

                conn.close()


    # ========================================================
    # CREATE TABLE
    # ========================================================

    def create_table(
        self,
        columns
    ):

        card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        frame = tk.Frame(
            card,
            bg=WHITE
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        y_scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview
        )

        x_scroll = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        y_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        x_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        frame.rowconfigure(
            0,
            weight=1
        )

        frame.columnconfigure(
            0,
            weight=1
        )

        for column in columns:

            tree.heading(
                column,
                text=column.replace(
                    "_",
                    " "
                ).title()
            )

            tree.column(
                column,
                width=150,
                minwidth=100
            )

        tree.tag_configure(
            "evenrow",
            background=WHITE
        )

        tree.tag_configure(
            "oddrow",
            background=BG
        )

        return tree


    # ========================================================
    # POPULATE TREE
    # ========================================================

    def populate_tree(
        self,
        tree,
        rows
    ):

        for index, row in enumerate(
            rows
        ):

            if index % 2 == 0:

                tag = "evenrow"

            else:

                tag = "oddrow"

            tree.insert(
                "",
                "end",
                values=row,
                tags=(
                    tag,
                )
            )


    # ========================================================
    # SIMPLE QUERY TABLE
    # ========================================================

    def simple_query_table(
        self,
        query
    ):

        conn = None

        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                query
            )

            rows = cursor.fetchall()

            columns = [
                desc[0]
                for desc in cursor.description
            ]

            tree = self.create_table(
                columns
            )

            self.populate_tree(
                tree,
                rows
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:

                cursor.close()

            if conn:

                conn.close()


    # ========================================================
    # STORED PROCEDURE TABLE
    # ========================================================

    def procedure_table(
        self,
        procedure,
        args,
        back_command=None
    ):

        self.clear()

        self.page_title(
            procedure,
            "Stored procedure result"
        )

        conn = None

        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            result = cursor.callproc(
                procedure,
                args
            )

            tree = self.create_table(
                [
                    "Result"
                ]
            )

            self.populate_tree(
                tree,
                [
                    (
                        value,
                    )
                    for value in result
                ]
            )

        except Exception as e:

            messagebox.showerror(
                "Procedure Error",
                str(e)
            )

        finally:

            if cursor:

                cursor.close()

            if conn:

                conn.close()

        if back_command is None:

            back_command = self.reports

        self.back_button(
            back_command
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    LoginWindow(
        root
    )

    root.mainloop()