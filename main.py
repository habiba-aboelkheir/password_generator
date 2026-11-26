from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk

from qr_logic import create_qr_image, save_qr_image


class ModernDarkQRApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SnapQR • QR Code Generator")
        self.root.geometry("440x610")
        self.root.resizable(False, False)

        # لوحة ألوان داكنة شبابية متناسقة
        self.bg_main = "#090d16"
        self.bg_card = "#111827"
        self.bg_input = "#0b1120"
        self.border_color = "#1e293b"
        self.text_primary = "#f8fafc"
        self.text_muted = "#94a3b8"
        self.accent = "#6366f1"
        self.accent_hover = "#4f46e5"
        self.success = "#10b981"

        self.current_pil_img = None
        self.tk_img = None

        self.root.configure(bg=self.bg_main, padx=20, pady=20)

        card = tk.Frame(
            root,
            bg=self.bg_card,
            highlightbackground=self.border_color,
            highlightthickness=1,
            padx=20,
            pady=20,
        )
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="INSTANT & CLEAN",
            bg=self.bg_card,
            fg="#818cf8",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")

        tk.Label(
            card,
            text="QR Code Generator",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(2, 2))

        tk.Label(
            card,
            text="حوّل أي رابط أو نص إلى QR Code واحفظه كصورة PNG",
            bg=self.bg_card,
            fg=self.text_muted,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(0, 14))

        # حقل إدخال النص أو الرابط
        tk.Label(
            card,
            text="الرابط أو النص",
            bg=self.bg_card,
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(0, 6))

        input_box = tk.Frame(
            card,
            bg=self.bg_input,
            highlightbackground=self.border_color,
            highlightthickness=1,
            padx=8,
            pady=6,
        )
        input_box.pack(fill="x")

        self.data_var = tk.StringVar(value="https://github.com")
        self.data_entry = tk.Entry(
            input_box,
            textvariable=self.data_var,
            bg=self.bg_input,
            fg=self.text_primary,
            insertbackground="#38bdf8",
            relief="flat",
            bd=0,
            font=("Consolas", 10),
        )
        self.data_entry.pack(fill="x", ipady=4)
        self.data_entry.bind("<Return>", lambda e: self.generate_qr())

        # اختيار ستايل الألوان للـ QR
        style_row = tk.Frame(card, bg=self.bg_card)
        style_row.pack(fill="x", pady=(12, 12))

        tk.Label(
            style_row,
            text="لون الكود:",
            bg=self.bg_card,
            fg=self.text_muted,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

        self.theme_var = tk.StringVar(value="cyan")
        themes = [
            ("سماوي داكن", "cyan"),
            ("بنفسجي نيون", "indigo"),
            ("كلاسيك أبيض/أسود", "classic"),
        ]
        for title, key in themes:
            tk.Radiobutton(
                style_row,
                text=title,
                variable=self.theme_var,
                value=key,
                command=self.generate_qr,
                bg=self.bg_card,
                fg=self.text_primary,
                selectcolor=self.bg_input,
                activebackground=self.bg_card,
                activeforeground=self.text_primary,
                font=("Segoe UI", 8, "bold"),
                highlightthickness=0,
                bd=0,
                cursor="hand2",
            ).pack(side="left", padx=(10, 0))

        # صندوق معاينة الـ QR Code
        preview_frame = tk.Frame(
            card,
            bg=self.bg_input,
            highlightbackground=self.border_color,
            highlightthickness=1,
            height=220,
        )
        preview_frame.pack(fill="x", pady=(2, 8))
        preview_frame.pack_propagate(False)

        self.preview_label = tk.Label(
            preview_frame,
            text="سيظهر الكود هنا",
            bg=self.bg_input,
            fg=self.text_muted,
            font=("Segoe UI", 10),
        )
        self.preview_label.pack(expand=True)

        # رسالة الحالة أو الخطأ
        self.status_label = tk.Label(
            card,
            text="",
            bg=self.bg_card,
            fg=self.success,
            font=("Segoe UI", 9, "bold"),
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

        # أزرار التوليد والحفظ
        btns_row = tk.Frame(card, bg=self.bg_card)
        btns_row.pack(fill="x")

        self.gen_btn = tk.Button(
            btns_row,
            text="Generate QR",
            command=self.generate_qr,
            bg=self.accent,
            fg="#ffffff",
            activebackground=self.accent_hover,
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10,
        )
        self.gen_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.save_btn = tk.Button(
            btns_row,
            text="Save PNG",
            command=self.save_qr,
            bg="#1e293b",
            fg=self.text_primary,
            activebackground="#334155",
            activeforeground=self.text_primary,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10,
            padx=16,
        )
        self.save_btn.pack(side="right")

        self.gen_btn.bind("<Enter>", lambda e: self.gen_btn.config(bg=self.accent_hover))
        self.gen_btn.bind("<Leave>", lambda e: self.gen_btn.config(bg=self.accent))

        self.generate_qr()

    def _get_palette(self):
        choice = self.theme_var.get()
        if choice == "indigo":
            return "#a5b4fc", "#090d16"
        if choice == "classic":
            return "#090d16", "#f8fafc"
        return "#38bdf8", "#0b1120"

    def generate_qr(self):
        fill_color, back_color = self._get_palette()
        try:
            pil_img = create_qr_image(
                data=self.data_var.get(),
                fill_color=fill_color,
                back_color=back_color,
                box_size=8,
                border=2,
            )
            self.current_pil_img = pil_img
            resized = pil_img.resize((190, 190))
            self.tk_img = ImageTk.PhotoImage(resized)
            self.preview_label.config(image=self.tk_img, text="")
            self.status_label.config(text="تم توليد الـ QR Code بنجاح", fg=self.success)
        except ValueError as err:
            self.current_pil_img = None
            self.preview_label.config(image="", text="أدخل نصًا أو رابطًا صالحًا")
            self.status_label.config(text=str(err), fg="#f87171")

    def save_qr(self):
        if not self.current_pil_img:
            self.status_label.config(text="لا يوجد QR Code لحفظه بعد.", fg="#f87171")
            return

        default_name = f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
        )
        if not file_path:
            return

        saved_path = save_qr_image(self.current_pil_img, file_path)
        self.status_label.config(text=f"تم الحفظ: {Path(saved_path).name}", fg=self.success)


if __name__ == "__main__":
    root = tk.Tk()
    ModernDarkQRApp(root)
    root.mainloop()