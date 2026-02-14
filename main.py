import customtkinter as ctk
import sqlite3
import hashlib
import os
import json
import base64
import io
import random
import string
import shutil
import csv
import datetime
import tkinter as tk
import webbrowser
import threading
import ctypes 
from tkinter import font, colorchooser, filedialog
from PIL import Image, ImageDraw, ImageTk


from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


try:
    import requests
except ImportError:
    print("Biblioteca 'requests' não encontrada. Instale com: pip install requests")
    requests = None


C_BG_MAIN = ("#FFFFFF", "#191919")
C_BG_SIDEBAR = ("#F7F7F5", "#202020")
C_CARD = ("#FFFFFF", "#2B2B2B")
C_BORDER = ("#E0E0E0", "#333333")
C_TEXT_MAIN = ("#37352F", "#E6E6E6")
C_TEXT_DIM = ("#9B9A97", "#A0A0A0")
C_HOVER = ("#EFEFEF", "#353535")
C_ACCENT = ("#2383E2", "#0A84FF")
C_TOOLBAR = ("#F2F2F2", "#252525") 
C_DANGER = ("#EB5757", "#CF6679")


class IconAssets:
    @staticmethod
    def get_image(name, color=None):
        size = (24, 24)
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        fill = (255, 255, 255, 255)
        
        if color:
            fill = color

        try:
            if name == "trash":
                draw.rectangle([7, 8, 17, 20], outline=fill, width=2)
                draw.line([5, 6, 19, 6], fill=fill, width=2)
                draw.line([10, 4, 14, 4], fill=fill, width=2)
            elif name == "edit":
                draw.polygon([(14, 6), (18, 10), (9, 19), (5, 19), (5, 15)], outline=fill, width=2)
                draw.line([14, 6, 18, 10], fill=fill, width=2)
            elif name == "restore":
                draw.arc([6, 6, 18, 18], 0, 270, fill=fill, width=2)
                draw.polygon([(18, 6), (14, 10), (18, 14)], fill=fill)
            elif name == "external":
                draw.rectangle([5, 11, 13, 19], outline=fill, width=2)
                draw.line([13, 11, 19, 5], fill=fill, width=2)
                draw.line([19, 5, 19, 10], fill=fill, width=2)
                draw.line([19, 5, 14, 5], fill=fill, width=2)
            elif name == "lock":
                draw.rectangle([6, 10, 18, 20], outline=fill, width=2)
                draw.arc([8, 4, 16, 12], 180, 0, fill=fill, width=2)
            elif name == "home":
                draw.polygon([(12, 2), (4, 9), (20, 9)], outline=fill, fill=None)
                draw.rectangle([6, 9, 18, 20], outline=fill, width=2)
            elif name == "plus":
                draw.line([12, 5, 12, 19], fill=fill, width=2)
                draw.line([5, 12, 19, 12], fill=fill, width=2)
            elif name == "search":
                draw.ellipse([5, 5, 15, 15], outline=fill, width=2)
                draw.line([14, 14, 19, 19], fill=fill, width=2)
            elif name == "settings":
                draw.ellipse([5, 5, 19, 19], outline=fill, width=2)
                draw.ellipse([10, 10, 14, 14], fill=fill)
            elif name == "folder":
                draw.line([4, 6, 10, 6], fill=fill, width=2)
                draw.line([10, 6, 12, 8], fill=fill, width=2)
                draw.rectangle([4, 8, 20, 18], outline=fill, width=2)
            elif name == "check":
                draw.ellipse([2, 2, 22, 22], outline=fill, width=2)
                draw.line([7, 12, 10, 15], fill=fill, width=2)
                draw.line([10, 15, 17, 8], fill=fill, width=2)
            elif name == "chevron_right":
                draw.line([10, 8, 15, 12], fill=fill, width=2)
                draw.line([15, 12, 10, 16], fill=fill, width=2)
            elif name == "chevron_down":
                draw.line([8, 10, 12, 15], fill=fill, width=2)
                draw.line([12, 15, 16, 10], fill=fill, width=2)
            elif name == "eye":
                draw.ellipse([4, 7, 20, 17], outline=fill, width=2)
                draw.ellipse([10, 10, 14, 14], fill=fill)
            elif name == "eye_off":
                draw.ellipse([4, 7, 20, 17], outline=fill, width=2)
                draw.line([5, 5, 19, 19], fill=fill, width=2)
            elif name == "details":
                draw.rectangle([6, 4, 18, 20], outline=fill, width=2)
                draw.line([9, 8, 15, 8], fill=fill, width=2)
                draw.line([9, 12, 15, 12], fill=fill, width=2)
                draw.line([9, 16, 13, 16], fill=fill, width=2)
            elif name == "copy":
                draw.rectangle([8, 8, 18, 20], outline=fill, width=2)
                draw.line([6, 16, 6, 6], fill=fill, width=2)
                draw.line([6, 6, 14, 6], fill=fill, width=2)
            else:
                draw.text((8, 4), "?", fill=fill)

            if color:
                return img

            alpha = img.split()[3]
            icon_white = Image.new("RGBA", size, (255, 255, 255, 255))
            icon_white.putalpha(alpha)
            icon_dark = Image.new("RGBA", size, (55, 53, 47, 255))
            icon_dark.putalpha(alpha)
            
            return ctk.CTkImage(light_image=icon_dark, dark_image=icon_white, size=(18, 18))
        except Exception as e:
            return None


class ModernPopups:
    @staticmethod
    def _create_base_dialog(parent, title, height=180, width=360):
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#2B2B2B" if is_dark else "#FFFFFF"
        
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry(f"{width}x{height}")
        dialog.overrideredirect(True) 
        dialog.attributes("-topmost", True)
        
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
            dialog.geometry(f"+{x}+{y}")
        except: pass

        main_frame = ctk.CTkFrame(dialog, fg_color=bg_color, corner_radius=12, 
                                  border_width=1, border_color="#333333" if is_dark else "#E0E0E0")
        main_frame.pack(fill="both", expand=True)
        return dialog, main_frame, is_dark

    @staticmethod
    def show_confirm(parent, title, message, command_yes, danger=True):
        dialog, main_frame, is_dark = ModernPopups._create_base_dialog(parent, title, 180)
        text_color = "#E6E6E6" if is_dark else "#37352F"

        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))
        ctk.CTkLabel(header, text="⚠️", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 16, "bold"), text_color=text_color).pack(side="left")

        ctk.CTkLabel(main_frame, text=message, font=("Segoe UI", 13), 
                     text_color="#A0A0A0" if is_dark else "#666666", wraplength=320, justify="left").pack(fill="x", padx=25, pady=(0, 20))

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        def on_confirm():
            dialog.grab_release()
            dialog.destroy()
            parent.focus_force()
            parent.update()
            command_yes()

        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="transparent", border_width=1, 
                      border_color="#404040" if is_dark else "#D1D1D1", text_color=text_color, 
                      hover_color="#353535" if is_dark else "#F0F0F0", width=100, height=32, corner_radius=6,
                      command=dialog.destroy).pack(side="right", padx=(5, 0))

        btn_color = "#EB5757" if danger else C_ACCENT
        btn_hover = "#C0392B" if danger else "#1068BF"
        btn_text = "Confirmar" if not danger else "Excluir"

        ctk.CTkButton(btn_frame, text=btn_text, fg_color=btn_color, hover_color=btn_hover, text_color="white",
                      width=100, height=32, corner_radius=6, command=on_confirm).pack(side="right")

        dialog.transient(parent)
        dialog.grab_set()
        parent.wait_window(dialog)

    @staticmethod
    def show_input(parent, title, placeholder, callback, initial_value=""):
        dialog, main_frame, is_dark = ModernPopups._create_base_dialog(parent, title, 200)
        text_color = "#E6E6E6" if is_dark else "#37352F"

        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(header, text="📂", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 16, "bold"), text_color=text_color).pack(side="left")

        entry = ctk.CTkEntry(main_frame, placeholder_text=placeholder, height=35,
                             fg_color="#202020" if is_dark else "#F7F7F5",
                             border_color="#404040" if is_dark else "#E0E0E0",
                             text_color=text_color)
        entry.pack(fill="x", padx=25, pady=(0, 20))
        if initial_value: entry.insert(0, initial_value)
        entry.focus()

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        def on_confirm(event=None):
            text = entry.get().strip()
            if text:
                dialog.grab_release()
                dialog.destroy()
                parent.focus_force()
                parent.update()
                callback(text)
            else:
                entry.configure(placeholder_text="Digite um nome válido!", border_color="#EB5757")

        entry.bind("<Return>", on_confirm)

        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="transparent", border_width=1, 
                      border_color="#404040" if is_dark else "#D1D1D1", text_color=text_color, 
                      hover_color="#353535" if is_dark else "#F0F0F0", width=100, height=32, corner_radius=6,
                      command=dialog.destroy).pack(side="right", padx=(5, 0))

        ctk.CTkButton(btn_frame, text="Confirmar", fg_color=C_ACCENT, hover_color="#1068BF", text_color="white",
                      width=100, height=32, corner_radius=6, command=on_confirm).pack(side="right")

        dialog.transient(parent)
        dialog.grab_set()
        parent.wait_window(dialog)
    
    @staticmethod
    def show_create_type(parent, callback):
        dialog, main_frame, is_dark = ModernPopups._create_base_dialog(parent, "Novo Tipo Personalizado", 280)
        text_color = "#E6E6E6" if is_dark else "#37352F"

        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(header, text="✨", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text="Criar Novo Tipo", font=("Segoe UI", 16, "bold"), text_color=text_color).pack(side="left")

        entry_name = ctk.CTkEntry(main_frame, placeholder_text="Nome (ex: Banco de Dados)", height=35,
                                  fg_color="#202020" if is_dark else "#F7F7F5", text_color=text_color)
        entry_name.pack(fill="x", padx=25, pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Campos (separados por vírgula):", font=("Segoe UI", 11), text_color="#999").pack(anchor="w", padx=25)
        entry_fields = ctk.CTkEntry(main_frame, placeholder_text="Ex: Host, Porta, Usuário, Senha", height=35,
                                    fg_color="#202020" if is_dark else "#F7F7F5", text_color=text_color)
        entry_fields.pack(fill="x", padx=25, pady=(0, 20))

        def on_confirm():
            name = entry_name.get().strip()
            fields = entry_fields.get().strip()
            if name and fields:
                dialog.grab_release()
                dialog.destroy()
                parent.focus_force()
                callback(name, fields)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(btn_frame, text="Criar", fg_color=C_ACCENT, width=100, height=32, command=on_confirm).pack(side="right")
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="transparent", border_width=1, text_color=text_color, width=100, height=32, command=dialog.destroy).pack(side="right", padx=5)

        dialog.transient(parent)
        dialog.grab_set()
        parent.wait_window(dialog)

    @staticmethod
    def show_details(parent, title, data_dict, copy_callback):
        dialog, main_frame, is_dark = ModernPopups._create_base_dialog(parent, "Detalhes", 450, 500)
        text_color = "#E6E6E6" if is_dark else "#37352F"

        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(header, text="📄", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 18, "bold"), text_color=text_color).pack(side="left")

        scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        for key, value in data_dict.items():
            if key == "title": continue 
            
            row = ctk.CTkFrame(scroll, fg_color=C_BG_SIDEBAR if is_dark else "#F9F9F9", corner_radius=6)
            row.pack(fill="x", pady=5, padx=5)
            
            key_clean = key.replace("_", " ").upper()
            ctk.CTkLabel(row, text=key_clean, font=("Segoe UI", 10, "bold"), text_color="#999").pack(anchor="w", padx=10, pady=(5,0))
            
            val_frame = ctk.CTkFrame(row, fg_color="transparent")
            val_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))
            
            display_text = str(value)
            is_long_text = False

            if isinstance(value, str) and value.strip().startswith('['):
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], list):
                        display_text = "".join([item[1] for item in parsed if item[0] == "text"])
                        is_long_text = True
                except:
                    pass
            
            if "\n" in display_text or len(display_text) > 60:
                is_long_text = True

            if is_long_text:
                txt_widget = ctk.CTkTextbox(val_frame, height=120, fg_color="transparent", 
                                          text_color=text_color, wrap="word", font=("Segoe UI", 12))
                txt_widget.insert("0.0", display_text)
                txt_widget.configure(state="disabled")
                txt_widget.pack(side="left", fill="both", expand=True)
            else:
                ent = ctk.CTkEntry(val_frame, fg_color="transparent", border_width=0, text_color=text_color)
                ent.insert(0, display_text)
                ent.configure(state="readonly")
                ent.pack(side="left", fill="x", expand=True)
            
            btn_copy = ctk.CTkButton(val_frame, text="", image=IconAssets.get_image("copy"), width=25, height=25,
                                     fg_color="transparent", hover_color=C_HOVER,
                                     command=lambda v=display_text: copy_callback(v))
            btn_copy.pack(side="right", anchor="ne" if is_long_text else "center")

        ctk.CTkButton(main_frame, text="Fechar", fg_color=C_ACCENT, width=100, command=dialog.destroy).pack(pady=15)

        dialog.transient(parent)
        dialog.grab_set()
        parent.wait_window(dialog)

    @staticmethod
    def show_notify(parent, message="Sucesso!"):
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#2B2B2B" if is_dark else "#FFFFFF"
        text_color = "#E6E6E6" if is_dark else "#37352F"

        dialog = ctk.CTkToplevel(parent)
        dialog.overrideredirect(True)
        dialog.attributes("-topmost", True)
        width = 240
        height = 50
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
            y = parent.winfo_y() + (parent.winfo_height() - 100) 
            dialog.geometry(f"{width}x{height}+{x}+{y}")
        except: dialog.geometry(f"{width}x{height}")

        frame = ctk.CTkFrame(dialog, fg_color=bg_color, corner_radius=25, border_width=1, border_color="#27AE60")
        frame.pack(fill="both", expand=True)
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        try:
            ctk.CTkLabel(content, text="", image=IconAssets.get_image("check")).pack(side="left", padx=(0, 10))
        except: pass
        ctk.CTkLabel(content, text=message, font=("Segoe UI", 13, "bold"), text_color=text_color).pack(side="left")
        dialog.after(1500, dialog.destroy)

class NotionVaultV8(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x800")
        self.overrideredirect(True)
        self.configure(fg_color=C_BG_MAIN)
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("dark-blue")

        app_name = "SafeVault"
        if os.name == 'nt': 
            self.app_data_dir = os.path.join(os.environ['APPDATA'], app_name)
        else: 
            self.app_data_dir = os.path.join(os.path.expanduser("~"), ".local", "share", app_name)

        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)

        self.db_file = os.path.join(self.app_data_dir, "vault_v6.db")
        self.security_file = os.path.join(self.app_data_dir, "security.dat")
        
        self.expanded_folders = set()
        self.editing_id = None 
        
        self.init_db()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Title Bar ---
        self.title_bar = ctk.CTkFrame(self, height=35, corner_radius=0, fg_color=C_BG_SIDEBAR)
        self.title_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.lbl_icon = ctk.CTkLabel(self.title_bar, text="", image=IconAssets.get_image("lock"))
        self.lbl_icon.pack(side="left", padx=(15, 5))
        self.lbl_app = ctk.CTkLabel(self.title_bar, text="SafeVault / Workspace", text_color=C_TEXT_DIM, font=("Segoe UI", 12))
        self.lbl_app.pack(side="left")
        
        # --- ESTADO INICIAL DE TELA CHEIA ---
        self.is_fullscreen = False
        self.last_geometry = "1200x800"

        # Botão Fechar
        self.btn_close = ctk.CTkButton(self.title_bar, text="✕", width=35, height=35, fg_color="transparent", hover_color=C_BORDER, text_color=C_TEXT_DIM, command=self.close_app)
        self.btn_close.pack(side="right")
        
        # Botão Maximizar / Restaurar (NOVO)
        self.btn_max = ctk.CTkButton(self.title_bar, text="□", width=35, height=35, fg_color="transparent", hover_color=C_BORDER, text_color=C_TEXT_DIM, command=self.toggle_fullscreen)
        self.btn_max.pack(side="right")

        # Botão Minimizar
        self.btn_min = ctk.CTkButton(self.title_bar, text="—", width=35, height=35, fg_color="transparent", hover_color=C_BORDER, text_color=C_TEXT_DIM, command=self.minimize_app)
        self.btn_min.pack(side="right")

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        # --- Sidebar (Largura Aumentada e Redimensionável) ---
        self.sidebar_width = 280 
        self.sidebar = ctk.CTkFrame(self, width=self.sidebar_width, corner_radius=0, fg_color=C_BG_SIDEBAR)
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.profile_frame.pack(fill="x", padx=10, pady=(20, 10))
        self.avatar = ctk.CTkLabel(self.profile_frame, text="E", width=25, height=25, fg_color="#E0AA98", text_color="black", corner_radius=5)
        self.avatar.pack(side="left", padx=(5, 10))
        ctk.CTkLabel(self.profile_frame, text="Espaço de Trabalho", font=("Segoe UI", 14, "bold"), text_color=C_TEXT_MAIN).pack(side="left")

        ctk.CTkLabel(self.sidebar, text="FAVORITOS", font=("Segoe UI", 11), text_color=C_TEXT_DIM, anchor="w").pack(fill="x", padx=18, pady=(10, 5))
        
        self.create_menu_btn("Buscar", "search", lambda: self.switch_page("search"))
        self.create_menu_btn("Página Inicial", "home", lambda: self.switch_page("home"))
        self.create_menu_btn("Adicionar Novo", "plus", lambda: self.switch_page("add"))

        folder_header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        folder_header.pack(fill="x", padx=18, pady=(20, 5))
        ctk.CTkLabel(folder_header, text="PASTAS", font=("Segoe UI", 11), text_color=C_TEXT_DIM).pack(side="left")
        btn_add_folder = ctk.CTkButton(folder_header, text="+", width=20, height=20, fg_color="transparent", hover_color=C_HOVER, text_color=C_TEXT_DIM, command=lambda: self.popup_add_folder(None))
        btn_add_folder.pack(side="right")

        # Campo de Pesquisa de Pasta
        self.entry_folder_search = ctk.CTkEntry(self.sidebar, placeholder_text="Filtrar pastas...", height=28, 
                                                font=("Segoe UI", 12), fg_color="transparent", border_color=C_BORDER, border_width=1)
        self.entry_folder_search.pack(fill="x", padx=15, pady=(0, 5))
        self.entry_folder_search.bind("<KeyRelease>", lambda e: self.load_folders_sidebar())

        self.folder_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.folder_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkFrame(self.sidebar, height=1, fg_color=C_BORDER).pack(fill="x")
        
        # --- MENU ATUALIZADO ---
        self.create_menu_btn("  Configurações", "settings", lambda: self.switch_page("settings"), parent=self.sidebar)
        self.create_menu_btn("  Bloquear", "lock", self.lock_app, parent=self.sidebar)

        # Barra de Redimensionamento
        self.resizer_bar = ctk.CTkFrame(self.sidebar, width=5, cursor="sb_h_double_arrow", fg_color="transparent")
        self.resizer_bar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")
        self.resizer_bar.bind("<Button-1>", self.start_resize_sidebar)
        self.resizer_bar.bind("<B1-Motion>", self.do_resize_sidebar)
        self.resizer_bar.bind("<Enter>", lambda e: self.resizer_bar.configure(fg_color=C_ACCENT))
        self.resizer_bar.bind("<Leave>", lambda e: self.resizer_bar.configure(fg_color="transparent"))

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=C_BG_MAIN)
        self.content.grid(row=1, column=1, sticky="nsew", padx=40, pady=20)

        # Resize grip for main window
        self.sizegrip = ctk.CTkLabel(self, text="◢", text_color=C_TEXT_DIM, font=("Arial", 16), cursor="sizing")
        self.sizegrip.place(relx=1.0, rely=1.0, anchor="se", x=-2, y=-2)
        self.sizegrip.bind("<B1-Motion>", self.resize_window)

        if not os.path.exists(self.security_file): self.show_register()
        else: self.show_login()

        # Configurar ícone na barra de tarefas (Windows)
        self.after(200, self.setup_taskbar)

    def setup_taskbar(self):
        try:
            # Gera um ícone azul (cadeado)
            icon_img = IconAssets.get_image("lock", color=(35, 131, 226, 255))
            if icon_img:
                photo_icon = ImageTk.PhotoImage(icon_img)
                self.iconphoto(False, photo_icon)
        except: pass

        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            if hwnd == 0: hwnd = self.winfo_id()
            
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20) # GWL_EXSTYLE
            style = style & ~0x00000080 # Remove WS_EX_TOOLWINDOW
            style = style | 0x00040000  # Adiciona WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
            
            self.withdraw()
            self.after(10, self.deiconify)
        except: pass

    # --- CORREÇÃO DO MINIMIZAR ---
    def minimize_app(self):
        self.withdraw() # Esconde a janela
        self.overrideredirect(False) # Devolve o controle para o Windows
        self.iconify() # Minimiza de verdade
        self.bind("<Map>", self.on_restore) # Fica ouvindo quando ela voltar

    def on_restore(self, event):
        # Quando a janela for restaurada (mapeada na tela de novo)
        if self.state() == 'normal':
            self.overrideredirect(True) # Tira as bordas do Windows
            self.setup_taskbar() # Garante que o ícone continue na barra
            self.unbind("<Map>") # Para de ouvir o evento

    # --- Funções de Redimensionamento do Menu ---
    def start_resize_sidebar(self, event):
        pass

    def do_resize_sidebar(self, event):
        # Calcula largura baseada em coordenada absoluta para evitar "snap back"
        new_width = event.x_root - self.winfo_rootx()
        if 150 < new_width < 800:
            self.sidebar_width = new_width
            self.sidebar.configure(width=self.sidebar_width)
    
    def toggle_folder_state(self, folder_id):
        if folder_id in self.expanded_folders: 
            self.expanded_folders.remove(folder_id)
        else: 
            self.expanded_folders.add(folder_id)
        self.load_folders_sidebar()

    def load_folders_sidebar(self):
        for w in self.folder_scroll.winfo_children(): w.destroy()
        
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT id, name, parent_id FROM folders WHERE is_deleted=0 ORDER BY name")
        all_folders = c.fetchall()
        conn.close()

        search_query = self.entry_folder_search.get().lower().strip()

        bg_color = C_BG_SIDEBAR[1] if ctk.get_appearance_mode() == "Dark" else C_BG_SIDEBAR[0]
        fg_color = "#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#000000"
        self.context_menu = tk.Menu(self, tearoff=0, bg=bg_color, fg=fg_color)
        
        # --- MENU DE CONTEXTO ATUALIZADO (Renomear e Excluir) ---
        self.context_menu.add_command(label="✏️ Renomear Pasta", command=lambda: self.rename_folder(self.selected_folder_id))
        self.context_menu.add_command(label="❌ Excluir Pasta", command=lambda: self.delete_folder(self.selected_folder_id))

        def show_context(event, f_id, f_name):
            self.selected_folder_id = f_id
            self.selected_folder_name = f_name # Salva o nome para usar no popup
            try: self.context_menu.tk_popup(event.x_root, event.y_root)
            finally: self.context_menu.grab_release()

        def create_folder_row(f_id, f_name, level=0, has_children=False, is_expanded=False):
            row_frame = ctk.CTkFrame(self.folder_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=1)
            indent_padding = level * 16

            display_name = f_name
            max_chars = 22 - (level * 2)
            if len(display_name) > max_chars:
                display_name = display_name[:max_chars] + "..."

            if has_children and not search_query:
                icon_name = "chevron_down" if is_expanded else "chevron_right"
                btn_toggle = ctk.CTkButton(row_frame, text="", image=IconAssets.get_image(icon_name), width=20, height=28,
                                           fg_color="transparent", hover_color=C_HOVER, command=lambda i=f_id: self.toggle_folder_state(i))
                btn_toggle.pack(side="left", padx=(indent_padding, 0))
            else:
                ctk.CTkLabel(row_frame, text="", width=20).pack(side="left", padx=(indent_padding, 0))

            btn_add_sub = ctk.CTkButton(row_frame, text="+", width=25, height=25, fg_color="transparent", hover_color=C_HOVER,
                                        text_color=C_TEXT_DIM, font=("Segoe UI", 14), command=lambda i=f_id: self.popup_add_folder(i))
            btn_add_sub.pack(side="right", padx=(0, 5))

            btn = ctk.CTkButton(row_frame, text=f" {display_name}", image=IconAssets.get_image("folder"), compound="left",
                                anchor="w", fg_color="transparent", hover_color=C_HOVER, text_color=C_TEXT_DIM, height=28, font=("Segoe UI", 13),
                                command=lambda i=f_id, n=f_name: self.filter_by_folder(i, n))
            btn.pack(side="left", fill="x", expand=True, padx=2)
            
            # Atualizado para passar o nome também
            btn.bind("<Button-3>", lambda event, i=f_id, n=f_name: show_context(event, i, n))

        if search_query:
            count = 0
            for f_id, f_name, f_parent in all_folders:
                if search_query in f_name.lower():
                    create_folder_row(f_id, f_name, level=0, has_children=False)
                    count += 1
            if count == 0:
                ctk.CTkLabel(self.folder_scroll, text="Nenhuma pasta encontrada", text_color=C_TEXT_DIM, font=("Segoe UI", 12)).pack(pady=10)
        else:
            def draw_tree(parent_id, level):
                current_level_folders = [f for f in all_folders if (f[2] == parent_id if parent_id is not None else f[2] is None)]
                for f_id, f_name, f_parent in current_level_folders:
                    has_children = any(f[2] == f_id for f in all_folders)
                    is_expanded = f_id in self.expanded_folders
                    create_folder_row(f_id, f_name, level, has_children, is_expanded)
                    if has_children and is_expanded:
                        draw_tree(f_id, level + 1)
            draw_tree(None, 0)

    def popup_add_folder(self, parent_id=None):
        title = "Nova Subpasta" if parent_id else "Nova Pasta Raiz"
        def save_folder(name):
            conn = sqlite3.connect(self.db_file)
            conn.execute("INSERT INTO folders (name, parent_id, is_deleted) VALUES (?, ?, 0)", (name, parent_id))
            conn.commit(); conn.close()
            if parent_id is not None: self.expanded_folders.add(parent_id)
            self.load_folders_sidebar()
            
        ModernPopups.show_input(parent=self, title=title, placeholder="Nome da pasta...", callback=save_folder)

    # --- NOVA FUNÇÃO DE RENOMEAR ---
    def rename_folder(self, folder_id):
        current_name = getattr(self, 'selected_folder_name', "")
        
        def save_rename(new_name):
            if not new_name or new_name == current_name: return
            conn = sqlite3.connect(self.db_file)
            conn.execute("UPDATE folders SET name=? WHERE id=?", (new_name, folder_id))
            conn.commit()
            conn.close()
            self.load_folders_sidebar()
            ModernPopups.show_notify(self, "Pasta renomeada!")

        ModernPopups.show_input(self, "Renomear Pasta", "Novo nome...", save_rename, initial_value=current_name)

    def delete_folder(self, folder_id):
        
        def confirm_action():
            conn = sqlite3.connect(self.db_file)
            
            conn.execute("UPDATE folders SET is_deleted=1 WHERE id=?", (folder_id,))
            
            conn.execute("UPDATE folders SET is_deleted=1 WHERE parent_id=?", (folder_id,)) 
            
            conn.execute("UPDATE entries SET is_deleted=1 WHERE folder_id=?", (folder_id,))
            conn.commit(); conn.close()
            self.load_folders_sidebar()
            self.switch_page("home")
            ModernPopups.show_notify(self, "Pasta movida para lixeira")
        ModernPopups.show_confirm(parent=self, title="Excluir Pasta", message="A pasta e seus itens serão movidos para a lixeira.", command_yes=confirm_action)

    def filter_by_folder(self, folder_id, folder_name):
        self.clear_content()
        self.render_search(folder_name=f"📂 {folder_name}", folder_id=folder_id)

    def create_menu_btn(self, text, icon_name, command, parent=None):
        target = parent if parent else self.sidebar
        btn = ctk.CTkButton(target, text=f"  {text}", image=IconAssets.get_image(icon_name), compound="left",
                            anchor="w", fg_color="transparent", text_color=C_TEXT_MAIN, hover_color=C_HOVER, 
                            font=("Segoe UI", 13), height=32, corner_radius=5, command=command)
        btn.pack(fill="x", padx=10, pady=1)

    
    def get_key_from_password(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def show_register(self):
        self.clear_content()
        self.sidebar.grid_forget()
        self.content.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
        
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(frame, text="Configurar SafeVault", font=("Segoe UI", 20, "bold"), text_color=C_TEXT_MAIN).pack(pady=10)
        ctk.CTkLabel(frame, text="Crie uma senha mestra forte. Se perdê-la, seus dados serão irrecuperáveis.", font=("Segoe UI", 12), text_color=C_TEXT_DIM).pack(pady=5)
        self.entry_master = ctk.CTkEntry(frame, placeholder_text="Senha Mestra", show="*", width=280, height=40, fg_color=C_BG_SIDEBAR, border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN)
        self.entry_master.pack(pady=15)
        ctk.CTkButton(frame, text="Criar Workspace", command=self.register_master, fg_color=C_ACCENT, width=280, height=40).pack()

    def register_master(self):
        pwd = self.entry_master.get()
        if len(pwd) < 6: 
            ModernPopups.show_notify(self, "Senha muito curta! Mínimo 6 chars.")
            return

        salt = os.urandom(16)
        self.key = self.get_key_from_password(pwd, salt)
        self.cipher = Fernet(self.key)
        
        
        with open(self.security_file, "wb") as f:
            f.write(salt) 
            token = self.cipher.encrypt(b"VALIDACAO")
            f.write(token)

        self.is_logged_in = True
        
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.content.grid(row=1, column=1, columnspan=1, sticky="nsew", padx=40, pady=20)
        
        self.switch_page("home")
        self.load_folders_sidebar()

    def show_login(self):
        self.clear_content()
        self.sidebar.grid_forget()
        self.content.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
        
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(frame, text="", image=IconAssets.get_image("lock")).pack(pady=10)
        ctk.CTkLabel(frame, text="Bem-vindo de volta", font=("Segoe UI", 20, "bold"), text_color=C_TEXT_MAIN).pack(pady=5)
        self.entry_login = ctk.CTkEntry(frame, placeholder_text="Senha Mestra", show="*", width=280, height=40, fg_color=C_BG_SIDEBAR, border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN)
        self.entry_login.pack(pady=15)
        self.entry_login.bind("<Return>", lambda e: self.check_login())
        ctk.CTkButton(frame, text="Entrar", command=self.check_login, fg_color=C_ACCENT, width=280, height=40).pack()

    def check_login(self):
        pwd = self.entry_login.get()
        if not os.path.exists(self.security_file): return

        with open(self.security_file, "rb") as f:
            salt = f.read(16)
            token_validacao = f.read()

        try:
            temp_key = self.get_key_from_password(pwd, salt)
            temp_cipher = Fernet(temp_key)
            check = temp_cipher.decrypt(token_validacao)
            
            if check == b"VALIDACAO":
                self.key = temp_key
                self.cipher = temp_cipher
                self.is_logged_in = True
                
                self.sidebar.grid(row=1, column=0, sticky="nsew")
                self.content.grid(row=1, column=1, columnspan=1, sticky="nsew", padx=40, pady=20)
                
                self.switch_page("home")
                self.load_folders_sidebar()
        except:
            self.entry_login.delete(0, 'end') 
            self.entry_login.configure(placeholder_text="Senha Incorreta!") 
            ModernPopups.show_notify(self, "Senha Incorreta! Tente novamente.") 

    def lock_app(self):
        self.is_logged_in = False
        self.key = None
        self.cipher = None
        self.show_login()

    
    def switch_page(self, page):
        if not getattr(self, 'is_logged_in', False): return
        self.clear_content()
        if page == "home": self.render_home()
        elif page == "search": self.render_search()
        elif page == "add": self.render_add()
        elif page == "trash": self.render_trash()
        elif page == "settings": self.render_settings()

    def render_settings(self):
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="⚙️", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text="Configurações", font=("Segoe UI", 28, "bold"), text_color=C_TEXT_MAIN).pack(side="left")

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # --- SEÇÃO PERFIL E SEGURANÇA ---
        ctk.CTkLabel(scroll, text="PERFIL & SEGURANÇA", font=("Segoe UI", 12, "bold"), text_color=C_TEXT_DIM).pack(anchor="w", pady=(10, 5))
        sec_frame = ctk.CTkFrame(scroll, fg_color=C_CARD, corner_radius=8)
        sec_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(sec_frame, text="Alterar Senha Mestra", font=("Segoe UI", 14, "bold"), text_color=C_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(sec_frame, text="Isso irá re-criptografar todo o seu banco de dados com a nova senha.", font=("Segoe UI", 12), text_color=C_TEXT_DIM).pack(anchor="w", padx=20, pady=(0, 10))
        
        self.old_pwd_entry = ctk.CTkEntry(sec_frame, placeholder_text="Senha Atual", show="*", width=250, fg_color=C_BG_SIDEBAR)
        self.old_pwd_entry.pack(anchor="w", padx=20, pady=5)
        self.new_pwd_entry = ctk.CTkEntry(sec_frame, placeholder_text="Nova Senha", show="*", width=250, fg_color=C_BG_SIDEBAR)
        self.new_pwd_entry.pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkButton(sec_frame, text="Atualizar Senha", fg_color=C_ACCENT, width=150, command=self.change_master_password).pack(anchor="w", padx=20, pady=(10, 20))

        # --- SEÇÃO APARÊNCIA ---
        ctk.CTkLabel(scroll, text="APARÊNCIA", font=("Segoe UI", 12, "bold"), text_color=C_TEXT_DIM).pack(anchor="w", pady=(5, 5))
        app_frame = ctk.CTkFrame(scroll, fg_color=C_CARD, corner_radius=8)
        app_frame.pack(fill="x", pady=(0, 20))
        
        theme_row = ctk.CTkFrame(app_frame, fg_color="transparent")
        theme_row.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(theme_row, text="Tema do Aplicativo", font=("Segoe UI", 14), text_color=C_TEXT_MAIN).pack(side="left")
        ctk.CTkButton(theme_row, text="Alternar Claro/Escuro", fg_color=C_BG_SIDEBAR, text_color=C_TEXT_MAIN, border_width=1, border_color=C_BORDER, hover_color=C_HOVER, command=self.toggle_theme).pack(side="right")

        # --- SEÇÃO GERENCIAR TIPOS ---
        ctk.CTkLabel(scroll, text="GERENCIAMENTO DE TIPOS", font=("Segoe UI", 12, "bold"), text_color=C_TEXT_DIM).pack(anchor="w", pady=(5, 5))
        type_frame = ctk.CTkFrame(scroll, fg_color=C_CARD, corner_radius=8)
        type_frame.pack(fill="x", pady=(0, 20))

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT name FROM custom_types")
        custom_types = c.fetchall()
        conn.close()

        if not custom_types:
            ctk.CTkLabel(type_frame, text="Nenhum tipo personalizado criado.", text_color=C_TEXT_DIM).pack(pady=15)
        else:
            for (t_name,) in custom_types:
                row = ctk.CTkFrame(type_frame, fg_color="transparent")
                row.pack(fill="x", padx=20, pady=5)
                ctk.CTkLabel(row, text=f"• {t_name}", font=("Segoe UI", 13), text_color=C_TEXT_MAIN).pack(side="left")
                ctk.CTkButton(row, text="Excluir", fg_color="transparent", text_color="#EB5757", hover_color=C_HOVER, width=60, height=25,
                              command=lambda n=t_name: self.delete_custom_type_from_settings(n)).pack(side="right")

        ctk.CTkButton(type_frame, text="+ Criar Novo Tipo", fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN, 
                      command=lambda: ModernPopups.show_create_type(self, self.create_type_callback)).pack(pady=15)

        # --- SEÇÃO DADOS E LIXEIRA ---
        ctk.CTkLabel(scroll, text="DADOS E ARMAZENAMENTO", font=("Segoe UI", 12, "bold"), text_color=C_TEXT_DIM).pack(anchor="w", pady=(5, 5))
        data_frame = ctk.CTkFrame(scroll, fg_color=C_CARD, corner_radius=8)
        data_frame.pack(fill="x", pady=(0, 20))

        # Botões de Backup
        btn_row = ctk.CTkFrame(data_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkButton(btn_row, text="Fazer Backup (.db)", fg_color="#27AE60", hover_color="#219150", width=140, command=self.do_backup).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="Restaurar Backup", fg_color="#E67E22", hover_color="#D35400", width=140, command=self.do_import).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="Exportar CSV", fg_color=C_ACCENT, width=140, command=self.do_export).pack(side="left")

        # Divisor
        ctk.CTkFrame(data_frame, height=1, fg_color=C_BORDER).pack(fill="x", padx=20, pady=5)

        # Lixeira
        trash_row = ctk.CTkFrame(data_frame, fg_color="transparent")
        trash_row.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(trash_row, text="Itens Excluídos", font=("Segoe UI", 14), text_color=C_TEXT_MAIN).pack(side="left")
        ctk.CTkButton(trash_row, text="Acessar Lixeira", fg_color=C_BG_SIDEBAR, text_color=C_TEXT_MAIN, border_width=1, border_color=C_BORDER, hover_color=C_HOVER,
                      command=lambda: self.switch_page("trash")).pack(side="right")

    def create_type_callback(self, name, fields):
        conn = sqlite3.connect(self.db_file)
        try:
            conn.execute("INSERT INTO custom_types (name, fields) VALUES (?, ?)", (name, fields))
            conn.commit()
            ModernPopups.show_notify(self, f"Tipo '{name}' criado!")
            self.render_settings() # Recarrega a página de settings
        except sqlite3.IntegrityError:
            ModernPopups.show_notify(self, "Esse nome já existe!")
        finally:
            conn.close()

    def delete_custom_type_from_settings(self, type_name):
        def confirm():
            conn = sqlite3.connect(self.db_file)
            conn.execute("DELETE FROM custom_types WHERE name=?", (type_name,))
            conn.commit()
            conn.close()
            ModernPopups.show_notify(self, "Tipo excluído!")
            self.render_settings()
        ModernPopups.show_confirm(self, "Excluir Tipo", f"Tem certeza que deseja excluir '{type_name}'?", confirm)

    def change_master_password(self):
        old_pwd = self.old_pwd_entry.get()
        new_pwd = self.new_pwd_entry.get()

        if len(new_pwd) < 6:
            ModernPopups.show_notify(self, "Nova senha muito curta (mín 6)!")
            return

        # Verifica senha antiga tentando derivar a chave e decriptar o token
        with open(self.security_file, "rb") as f:
            salt = f.read(16)
            token = f.read()
        
        try:
            old_key = self.get_key_from_password(old_pwd, salt)
            old_cipher = Fernet(old_key)
            if old_cipher.decrypt(token) != b"VALIDACAO":
                raise Exception("Senha errada")
        except:
            ModernPopups.show_notify(self, "Senha atual incorreta!")
            return

        # Se chegou aqui, a senha antiga está certa. Vamos re-criptografar TUDO.
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT id, data_blob FROM entries")
            rows = c.fetchall()

            decrypted_data = []
            for r_id, blob in rows:
                try:
                    txt = old_cipher.decrypt(blob.encode()).decode()
                    decrypted_data.append((r_id, txt))
                except: pass # Se falhar algum, infelizmente perde-se o dado
            
            # Gerar nova chave
            new_salt = os.urandom(16)
            new_key = self.get_key_from_password(new_pwd, new_salt)
            new_cipher = Fernet(new_key)

            # Atualizar banco
            for r_id, txt in decrypted_data:
                new_blob = new_cipher.encrypt(txt.encode()).decode()
                c.execute("UPDATE entries SET data_blob=? WHERE id=?", (new_blob, r_id))
            
            conn.commit()
            conn.close()

            # Atualizar arquivo de segurança
            with open(self.security_file, "wb") as f:
                f.write(new_salt)
                f.write(new_cipher.encrypt(b"VALIDACAO"))

            # Atualizar sessão atual
            self.key = new_key
            self.cipher = new_cipher
            
            self.old_pwd_entry.delete(0, 'end')
            self.new_pwd_entry.delete(0, 'end')
            ModernPopups.show_notify(self, "Senha alterada com sucesso!")

        except Exception as e:
            ModernPopups.show_notify(self, f"Erro crítico: {e}")

    # --- Funções de Backup movidas para métodos da classe ---
    def do_backup(self):
        try:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            default_name = f"backup_vault_{ts}.db"
            filename = filedialog.asksaveasfilename(initialfile=default_name, defaultextension=".db", filetypes=[("Banco de Dados", "*.db")])
            if not filename: return
            shutil.copy(self.db_file, filename)
            ModernPopups.show_notify(self, "Backup salvo com sucesso!")
        except Exception as e: ModernPopups.show_notify(self, f"Erro: {e}")

    def do_import(self):
        def confirm_import():
            filename = filedialog.askopenfilename(filetypes=[("Banco de Dados", "*.db")])
            if not filename: return
            try:
                shutil.copy(filename, self.db_file)
                dir_backup = os.path.dirname(filename)
                sec_backup = os.path.join(dir_backup, "security.dat")
                if os.path.exists(sec_backup): shutil.copy(sec_backup, self.security_file)
                ModernPopups.show_notify(self, "Restaurado! Reinicie o App.")
                self.after(2000, self.destroy)
            except Exception as e: ModernPopups.show_notify(self, f"Erro: {e}")
        ModernPopups.show_confirm(self, "Importar Backup", "Isso substituirá todos os dados atuais!", confirm_import, danger=True)

    def do_export(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
            if not filename: return
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT type, title, subtitle, data_blob FROM entries WHERE is_deleted=0")
            rows = c.fetchall()
            conn.close()
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Tipo', 'Título', 'Subtítulo', 'Dados JSON'])
                for r in rows:
                    try:
                        decrypted = self.decrypt(r[3])
                        writer.writerow([r[0], r[1], r[2], decrypted])
                    except: pass
            ModernPopups.show_notify(self, "Exportado com sucesso!")
        except: ModernPopups.show_notify(self, "Erro ao exportar")

    def render_home(self):
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="⚡", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text="Painel de Ferramentas", font=("Segoe UI", 28, "bold"), text_color=C_TEXT_MAIN).pack(side="left")

        main_scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        main_scroll.pack(fill="both", expand=True)

        card_gen = ctk.CTkFrame(main_scroll, fg_color=C_CARD, corner_radius=10)
        card_gen.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(card_gen, text="🎲 Gerador Rápido", font=("Segoe UI", 16, "bold"), text_color=C_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        
        gen_row = ctk.CTkFrame(card_gen, fg_color="transparent")
        gen_row.pack(fill="x", padx=20, pady=(0, 15))
        
        self.dash_pwd_entry = ctk.CTkEntry(gen_row, placeholder_text="Sua senha aparecerá aqui...", height=40, 
                                           font=("Consolas", 14), fg_color=C_BG_SIDEBAR, border_color=C_BORDER)
        self.dash_pwd_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(gen_row, text="Gerar", width=80, height=40, fg_color=C_ACCENT, 
                      command=lambda: self.generate_dashboard_pwd()).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(gen_row, text="Copiar", width=80, height=40, fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN,
                      command=lambda: self.copy_to_clipboard(self.dash_pwd_entry.get())).pack(side="left")

        card_check = ctk.CTkFrame(main_scroll, fg_color=C_CARD, corner_radius=10)
        card_check.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(card_check, text="🛡️ Teste de Força", font=("Segoe UI", 16, "bold"), text_color=C_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(card_check, text="Digite uma senha para ver quão segura ela é (não será salva).", font=("Segoe UI", 12), text_color=C_TEXT_DIM).pack(anchor="w", padx=20, pady=(0, 10))

        self.check_entry = ctk.CTkEntry(card_check, placeholder_text="Digite para testar...", show="*", height=40, fg_color=C_BG_SIDEBAR, border_color=C_BORDER)
        self.check_entry.pack(fill="x", padx=20)
        
        self.strength_bar = ctk.CTkProgressBar(card_check, height=10)
        self.strength_bar.set(0)
        self.strength_bar.pack(fill="x", padx=20, pady=(10, 5))
        
        self.lbl_strength_msg = ctk.CTkLabel(card_check, text="Aguardando...", font=("Segoe UI", 12, "bold"), text_color=C_TEXT_DIM)
        self.lbl_strength_msg.pack(anchor="w", padx=20, pady=(0, 15))
        
        self.check_entry.bind("<KeyRelease>", self.update_strength_meter)

        stats_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)

        btn_new = ctk.CTkButton(stats_frame, text="\n➕\n\nNovo Item", font=("Segoe UI", 14, "bold"), 
                                fg_color=C_CARD, hover_color=C_HOVER, text_color=C_TEXT_MAIN, corner_radius=10,
                                height=120, command=lambda: self.switch_page("add"))
        btn_new.pack(side="left", fill="both", expand=True, padx=5)

        recent_frame = ctk.CTkFrame(stats_frame, fg_color=C_CARD, corner_radius=10, height=120)
        recent_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(recent_frame, text="🕒 Recentes", font=("Segoe UI", 13, "bold"), text_color=C_TEXT_DIM).pack(anchor="nw", padx=15, pady=10)
        
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # --- ATUALIZADO: JOIN PARA PEGAR O ID DA PASTA E O NOME DA PASTA ---
        c.execute("""
            SELECT e.title, e.type, e.folder_id, f.name 
            FROM entries e 
            LEFT JOIN folders f ON e.folder_id = f.id 
            WHERE e.is_deleted=0 
            ORDER BY e.id DESC LIMIT 3
        """)
        recents = c.fetchall()
        conn.close()

        if not recents:
            ctk.CTkLabel(recent_frame, text="Nenhum item ainda.", text_color=C_TEXT_DIM).pack(pady=20)
        else:
            for title, type_, f_id, f_name in recents:
                
                # Tratamento caso a pasta tenha sido excluída fisicamente ou seja nula
                if not f_name: f_name = "Sem Pasta"

                r_row = ctk.CTkFrame(recent_frame, fg_color="transparent", cursor="hand2")
                r_row.pack(fill="x", padx=15, pady=2)
                
                # --- EVENTO DE CLIQUE ---
                def on_click(event, fid=f_id, fname=f_name):
                    self.filter_by_folder(fid, fname)
                
                r_row.bind("<Button-1>", on_click)
                
                lbl_dot = ctk.CTkLabel(r_row, text="•", text_color=C_ACCENT)
                lbl_dot.pack(side="left", padx=(0, 5))
                lbl_dot.bind("<Button-1>", on_click)

                lbl_title = ctk.CTkLabel(r_row, text=title[:20], font=("Segoe UI", 12), text_color=C_TEXT_MAIN)
                lbl_title.pack(side="left")
                lbl_title.bind("<Button-1>", on_click)

                lbl_type = ctk.CTkLabel(r_row, text=type_, font=("Segoe UI", 10), text_color=C_TEXT_DIM)
                lbl_type.pack(side="right")
                lbl_type.bind("<Button-1>", on_click)

    def get_folder_path(self, folder_id):
        path = []
        current_id = folder_id
        if current_id is not None:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            while current_id is not None:
                c.execute("SELECT id, name, parent_id FROM folders WHERE id=?", (current_id,))
                res = c.fetchone()
                if res:
                    path.append({"id": res[0], "name": res[1]})
                    current_id = res[2]
                else: break
            conn.close()
        path.append({"id": None, "name": "Todas as Pastas"})
        path.reverse()
        return path

    def render_search(self, folder_name="Todas as Pastas", folder_id=None):
        self.clear_content()

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="🔍", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        
        breadcrumb_frame = ctk.CTkFrame(header, fg_color="transparent")
        breadcrumb_frame.pack(side="left", fill="x")

        path_list = self.get_folder_path(folder_id)
        for idx, item in enumerate(path_list):
            is_last = (idx == len(path_list) - 1)
            if idx > 0: ctk.CTkLabel(breadcrumb_frame, text="›", font=("Segoe UI", 18), text_color=C_TEXT_DIM).pack(side="left", padx=5)
            if is_last:
                ctk.CTkLabel(breadcrumb_frame, text=item["name"], font=("Segoe UI", 24, "bold"), text_color=C_TEXT_MAIN).pack(side="left")
            else:
                btn = ctk.CTkButton(breadcrumb_frame, text=item["name"], font=("Segoe UI", 18), 
                                    fg_color="transparent", hover_color=C_HOVER, text_color=C_TEXT_DIM,
                                    width=0, height=30,
                                    command=lambda i=item["id"], n=item["name"]: self.filter_by_folder(i, n))
                btn.pack(side="left")

        search_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        entry_search = ctk.CTkEntry(search_frame, placeholder_text="Buscar em todos os itens...", 
                                    height=40, fg_color=C_BG_SIDEBAR, border_color=C_BORDER, text_color=C_TEXT_MAIN)
        entry_search.pack(fill="x")
        
        self.scroll_area = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True)

        entry_search.bind("<KeyRelease>", lambda event: self.load_items(entry_search.get(), folder_filter=folder_id))
        self.load_items(folder_filter=folder_id)

    def render_trash(self):
        self.clear_content()
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="🗑️", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text="Lixeira", font=("Segoe UI", 28, "bold"), text_color=C_TEXT_MAIN).pack(side="left")
        
        self.scroll_area = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True)

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT id, type, title, subtitle, data_blob FROM entries WHERE is_deleted=1 ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        if not rows:
            ctk.CTkLabel(self.scroll_area, text="Lixeira vazia.", text_color=C_TEXT_DIM).pack(pady=20)

        for r_id, r_type, r_title, r_sub, r_blob in rows:
            row = ctk.CTkFrame(self.scroll_area, fg_color=C_CARD, corner_radius=0, height=40)
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=f" {r_title}", font=("Segoe UI", 13, "bold"), text_color=C_TEXT_MAIN, width=200, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=r_type, font=("Segoe UI", 10), text_color=C_TEXT_DIM).pack(side="left", padx=10)
            
            
            ctk.CTkButton(row, text="", image=IconAssets.get_image("trash"), width=30, height=25, 
                          fg_color="transparent", hover_color="#EB5757", 
                          command=lambda i=r_id: self.permanent_delete(i)).pack(side="right", padx=5)
            
            ctk.CTkButton(row, text="", image=IconAssets.get_image("restore"), width=30, height=25, 
                          fg_color="transparent", hover_color=C_ACCENT, 
                          command=lambda i=r_id: self.restore_item(i)).pack(side="right", padx=5)

    
    def generate_dashboard_pwd(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = ''.join(random.choice(chars) for _ in range(20))
        self.dash_pwd_entry.delete(0, 'end')
        self.dash_pwd_entry.insert(0, pwd)

    def update_strength_meter(self, event):
        pwd = self.check_entry.get()
        length = len(pwd)
        score = 0
        if length == 0:
            self.strength_bar.set(0)
            self.lbl_strength_msg.configure(text="Aguardando...", text_color=C_TEXT_DIM)
            self.strength_bar.configure(progress_color=C_TEXT_DIM[0])
            return
        if length >= 8: score += 0.2
        if length >= 12: score += 0.2
        if any(c.isdigit() for c in pwd): score += 0.2
        if any(c.isupper() for c in pwd): score += 0.2
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd): score += 0.2
        self.strength_bar.set(score)
        if score < 0.4:
            self.lbl_strength_msg.configure(text="Fraca 😟", text_color="#EB5757")
            self.strength_bar.configure(progress_color="#EB5757")
        elif score < 0.8:
            self.lbl_strength_msg.configure(text="Média 😐", text_color="#F2C94C")
            self.strength_bar.configure(progress_color="#F2C94C")
        else:
            self.lbl_strength_msg.configure(text="Forte 🚀", text_color="#27AE60")
            self.strength_bar.configure(progress_color="#27AE60")
            
    def load_items(self, query="", folder_filter=None):
        if not hasattr(self, 'scroll_area') or not self.scroll_area.winfo_exists(): return
        for w in self.scroll_area.winfo_children(): w.destroy()
        
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        
        if folder_filter is not None:
            c.execute("SELECT id, name FROM folders WHERE parent_id = ? AND is_deleted=0 ORDER BY name", (folder_filter,))
            subfolders = c.fetchall()
            if subfolders:
                for s_id, s_name in subfolders:
                    if query.lower() in s_name.lower(): self.draw_folder_row(s_id, s_name)

        
        sql = "SELECT id, type, title, subtitle, data_blob FROM entries WHERE is_deleted=0"
        params = []
        if folder_filter:
            sql += " AND folder_id = ?"
            params.append(folder_filter)
        sql += " ORDER BY id DESC"
        c.execute(sql, params)
        rows = c.fetchall()
        conn.close()

        for row in rows:
            r_id, r_type, r_title, r_sub, r_blob = row
            if query.lower() in r_title.lower() or query.lower() in r_sub.lower():
                self.draw_row(r_id, r_type, r_title, r_sub, r_blob)

    def load_favicon_async(self, url, label_widget):
        def _fetch():
            if not requests: return
            try:
                domain = url.split("//")[-1].split("/")[0]
                api_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
                response = requests.get(api_url, timeout=2)
                if response.status_code == 200:
                    img_data = io.BytesIO(response.content)
                    pil_img = Image.open(img_data)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(20, 20))
                    label_widget.configure(image=ctk_img, text="", fg_color="transparent", width=20)
            except: pass
        threading.Thread(target=_fetch, daemon=True).start()

    def draw_folder_row(self, folder_id, name):
        row = ctk.CTkFrame(self.scroll_area, fg_color=C_CARD, corner_radius=6, height=45)
        row.pack(fill="x", pady=2, padx=2)
        icon_folder = IconAssets.get_image("folder")
        ctk.CTkLabel(row, text="", image=icon_folder, width=30).pack(side="left", padx=(10, 5))
        ctk.CTkLabel(row, text=name, font=("Segoe UI", 14, "bold"), text_color=C_TEXT_MAIN).pack(side="left", padx=5)
        ctk.CTkLabel(row, text="›", font=("Segoe UI", 18), text_color=C_TEXT_DIM).pack(side="right", padx=15)
        def on_click(e): self.filter_by_folder(folder_id, name)
        row.bind("<Button-1>", on_click)
        for child in row.winfo_children(): child.bind("<Button-1>", on_click)

    def draw_row(self, item_id, item_type, title, subtitle, blob):
        row = ctk.CTkFrame(self.scroll_area, fg_color=C_CARD, corner_radius=0, height=40)
        row.pack(fill="x", pady=1)
        
        ctk.CTkLabel(row, text=f" {title}", font=("Segoe UI", 13, "bold"), text_color=C_TEXT_MAIN, width=200, anchor="w").pack(side="left", padx=10)
        
        badge_color = {"Login": "#E3E2E0", "Cartão": "#D3E5EF", "Nota": "#FDECC8", "Link": "#F7F6F3"}
        badge_txt = {"Login": "#32302C", "Cartão": "#183347", "Nota": "#442A1E", "Link": "#37352F"}
        if ctk.get_appearance_mode() == "Dark":
             badge_color = {"Login": "#373737", "Cartão": "#1D282E", "Nota": "#392E1E", "Link": "#252525"}
             badge_txt = {"Login": "#E0E0E0", "Cartão": "#85C2E0", "Nota": "#E6C697", "Link": "#9B9A97"}
        b_bg = badge_color.get(item_type, "#D4E6F1")
        b_fg = badge_txt.get(item_type, "#154360")

        tf = ctk.CTkFrame(row, fg_color=b_bg, corner_radius=4, height=20, width=80)
        tf.pack(side="left", padx=5)
        tf.pack_propagate(False)
        lbl_badge = ctk.CTkLabel(tf, text=item_type[:10], font=("Segoe UI", 10), text_color=b_fg)
        lbl_badge.place(relx=0.5, rely=0.5, anchor="center")

        if item_type == "Link":
            try:
                data = json.loads(self.decrypt(blob))
                url = data.get("url", "")
                if url: self.load_favicon_async(url, lbl_badge)
            except: pass

        ctk.CTkLabel(row, text=subtitle[:30], font=("Segoe UI", 12), text_color=C_TEXT_DIM, anchor="w").pack(side="left", padx=10, fill="x", expand=True)

        ctk.CTkButton(row, text="", image=IconAssets.get_image("trash"), width=30, height=25, 
                      fg_color="transparent", hover_color="#EB5757", command=lambda: self.soft_delete_item(item_id)).pack(side="right", padx=5)

        
        ctk.CTkButton(row, text="", image=IconAssets.get_image("edit"), width=30, height=25, 
                      fg_color="transparent", hover_color=C_HOVER, command=lambda: self.edit_item(item_id, item_type, blob)).pack(side="right", padx=5)

        if item_type == "Link":
            ctk.CTkButton(row, text="", image=IconAssets.get_image("external"), width=30, height=25,
                          fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_DIM,
                          command=lambda: self.open_link(blob)).pack(side="right", padx=5)

        ctk.CTkButton(row, text="", image=IconAssets.get_image("details"), width=30, height=25,
                      fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_DIM,
                      command=lambda: self.view_details(blob)).pack(side="right", padx=5)

        ctk.CTkButton(row, text="Copiar", width=50, height=25, 
                      fg_color="transparent", border_width=1, border_color=C_BORDER, 
                      text_color=C_TEXT_DIM, font=("Segoe UI", 11),
                      command=lambda: self.action_item(item_type, blob)).pack(side="right", padx=5)

    def view_details(self, blob):
        try:
            data = json.loads(self.decrypt(blob))
            title = data.get("title", "Detalhes")
            def copy_text(val): self.copy_to_clipboard(val)
            ModernPopups.show_details(self, title, data, copy_text)
        except Exception as e: ModernPopups.show_notify(self, "Erro ao abrir detalhes")

    
    def edit_item(self, item_id, item_type, blob):
        try:
            data = json.loads(self.decrypt(blob))
            
            
            self.switch_page("add")
            self.editing_id = item_id 
            
            
            self.combo_type.set(item_type)
            self.update_form_fields(item_type)
            
            
            for key, widget in self.inputs.items():
                if key in data:
                    val = data[key]
                    if isinstance(widget, ctk.CTkTextbox):
                        self.deserialize_richtext(widget, val)
                    else:
                        widget.delete(0, 'end')
                        widget.insert(0, val)
                        
            ModernPopups.show_notify(self, "Modo de Edição Ativado")
            
        except Exception as e:
            print(e)
            ModernPopups.show_notify(self, "Erro ao carregar dados")

    def render_add(self):
        
        if not hasattr(self, 'editing_id'): self.editing_id = None
        
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        title_txt = "Editar Item" if self.editing_id else "Novo Item"
        icon = "edit" if self.editing_id else "plus"
        
        ctk.CTkLabel(header, text="", image=IconAssets.get_image(icon)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(header, text=title_txt, font=("Segoe UI", 28, "bold"), text_color=C_TEXT_MAIN).pack(side="left")

        ctk.CTkLabel(self.content, text="SALVAR EM", font=("Segoe UI", 10, "bold"), text_color=C_TEXT_DIM).pack(anchor="w")
        
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT id, name, parent_id FROM folders WHERE is_deleted=0")
        raw_folders = c.fetchall()
        c.execute("SELECT name FROM custom_types")
        custom_types = [r[0] for r in c.fetchall()]
        conn.close()

        folder_dict = {f[0]: f for f in raw_folders}
        self.folder_map = {} 
        display_list = []
        for f_id, f_name, f_parent in raw_folders:
            path = f_name
            curr_parent = f_parent
            while curr_parent is not None and curr_parent in folder_dict:
                parent_data = folder_dict[curr_parent]
                path = parent_data[1] + " / " + path
                curr_parent = parent_data[2]
            self.folder_map[path] = f_id
            display_list.append(path)

        display_list.sort()
        
        # --- VERIFICA SE EXISTEM PASTAS ---
        self.combo_folder = ctk.CTkComboBox(self.content, values=display_list, width=300, 
                                            fg_color=C_BG_SIDEBAR, border_color=C_BORDER, 
                                            text_color=C_TEXT_MAIN)
        
        if not display_list:
            self.combo_folder.set("Nenhuma pasta criada!")
            self.combo_folder.configure(state="disabled")
        else:
            self.combo_folder.configure(state="readonly")
            if not self.editing_id:
                self.combo_folder.set(display_list[0])

        self.combo_folder.pack(anchor="w", pady=(5, 15))

        ctk.CTkLabel(self.content, text="TIPO", font=("Segoe UI", 10, "bold"), text_color=C_TEXT_DIM).pack(anchor="w")
        
        type_row = ctk.CTkFrame(self.content, fg_color="transparent")
        type_row.pack(anchor="w", pady=(5, 20))

        all_types = ["Login", "Cartão", "Nota", "Link"] + custom_types
        self.combo_type = ctk.CTkComboBox(type_row, values=all_types, command=self.update_form_fields, state="readonly", width=200, fg_color=C_BG_SIDEBAR, border_color=C_BORDER, text_color=C_TEXT_MAIN)
        self.combo_type.set("Login")
        self.combo_type.pack(side="left")

        # Botão de Excluir Tipo (NOVO)
        btn_del_type = ctk.CTkButton(type_row, text="-", width=30, height=28, fg_color=C_BG_SIDEBAR, text_color=C_TEXT_MAIN, 
                                     border_width=1, border_color=C_BORDER, hover_color=C_HOVER,
                                     command=self.delete_custom_type)
        btn_del_type.pack(side="left", padx=5)

        if not self.editing_id:
            btn_add_type = ctk.CTkButton(type_row, text="+", width=30, height=28, fg_color=C_BG_SIDEBAR, text_color=C_TEXT_MAIN, 
                                         border_width=1, border_color=C_BORDER, hover_color=C_HOVER,
                                         command=self.create_new_type)
            btn_add_type.pack(side="left", padx=5)

        self.form_frame = ctk.CTkScrollableFrame(self.content, fg_color="transparent") 
        self.form_frame.pack(fill="both", expand=True)
        
        
        if not self.editing_id:
            self.update_form_fields("Login")

    def delete_custom_type(self):
        current = self.combo_type.get()
        defaults = ["Login", "Cartão", "Nota", "Link"]
        
        if current in defaults:
            ModernPopups.show_notify(self, "Não é possível excluir tipos padrão!")
            return

        def confirm():
            conn = sqlite3.connect(self.db_file)
            conn.execute("DELETE FROM custom_types WHERE name=?", (current,))
            conn.commit()
            conn.close()
            ModernPopups.show_notify(self, f"Tipo '{current}' excluído!")
            self.switch_page("add") 

        ModernPopups.show_confirm(self, "Excluir Tipo", f"Deseja excluir o tipo '{current}'?", confirm)

    def create_new_type(self):
        def save_new_type(name, fields_str):
            conn = sqlite3.connect(self.db_file)
            try:
                conn.execute("INSERT INTO custom_types (name, fields) VALUES (?, ?)", (name, fields_str))
                conn.commit()
                ModernPopups.show_notify(self, f"Tipo '{name}' criado!")
                self.switch_page("add") 
            except sqlite3.IntegrityError:
                ModernPopups.show_notify(self, "Esse nome já existe!")
            finally:
                conn.close()
        ModernPopups.show_create_type(self, save_new_type)

    
    def generate_password(self):
        if "password" not in self.inputs: return
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = ''.join(random.choice(chars) for _ in range(16))
        self.inputs["password"].delete(0, 'end')
        self.inputs["password"].insert(0, pwd)

    def create_floating_menu(self):
        self.floating_menu = ctk.CTkFrame(self, height=40, corner_radius=10, 
                                          fg_color=C_CARD, border_width=1, border_color=C_BORDER)
        ctk.CTkButton(self.floating_menu, text="𝐁", width=35, height=30, fg_color="transparent", 
                      hover_color=C_HOVER, text_color=C_TEXT_MAIN, font=("Segoe UI", 14, "bold"),
                      command=lambda: self.toggle_style("bold")).pack(side="left", padx=2, pady=2)
        ctk.CTkButton(self.floating_menu, text="𝐼", width=35, height=30, fg_color="transparent", 
                      hover_color=C_HOVER, text_color=C_TEXT_MAIN, font=("Segoe UI", 14, "italic"),
                      command=lambda: self.toggle_style("italic")).pack(side="left", padx=2, pady=2)
        ctk.CTkButton(self.floating_menu, text="U̲", width=35, height=30, fg_color="transparent", 
                      hover_color=C_HOVER, text_color=C_TEXT_MAIN, font=("Segoe UI", 14),
                      command=lambda: self.toggle_style("underline")).pack(side="left", padx=2, pady=2)
        ctk.CTkFrame(self.floating_menu, width=1, height=20, fg_color="#AAAAAA").pack(side="left", padx=5)
        ctk.CTkButton(self.floating_menu, text="A", width=35, height=30, fg_color="transparent", 
                      hover_color=C_HOVER, text_color="#EB5757", font=("Segoe UI", 14, "bold"),
                      command=self.choose_color).pack(side="left", padx=2, pady=2)

    def check_text_selection(self, event=None):
        if "note" not in self.inputs: return
        textbox = self.inputs["note"]._textbox
        try:
            if not textbox.tag_ranges("sel"):
                self.hide_floating_menu(); return
            bbox = textbox.bbox("sel.first")
            if not bbox: self.hide_floating_menu(); return
            abs_x = textbox.winfo_rootx() + bbox[0]
            abs_y = textbox.winfo_rooty() + bbox[1]
            win_x = abs_x - self.winfo_rootx()
            win_y = abs_y - self.winfo_rooty()
            menu_width = 180 
            pos_x = win_x - (menu_width // 4) 
            pos_y = win_y - 55 
            if pos_x < 10: pos_x = 10
            if pos_y < 10: pos_y = win_y + 30 
            self.floating_menu.place(x=pos_x, y=pos_y)
            self.floating_menu.lift() 
        except: self.hide_floating_menu()

    def hide_floating_menu(self, event=None):
        if hasattr(self, 'floating_menu'): self.floating_menu.place_forget()

    def update_form_fields(self, choice):
        for w in self.form_frame.winfo_children(): w.destroy()
        self.inputs = {}
        self.create_input("Título", "title")

        def toggle_password(entry, btn):
            if entry.cget("show") == "*":
                entry.configure(show="")
                btn.configure(image=IconAssets.get_image("eye_off"))
            else:
                entry.configure(show="*")
                btn.configure(image=IconAssets.get_image("eye"))

        if choice == "Login":
            self.create_input("Email / Usuário", "username")
            pwd_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            pwd_container.pack(fill="x", pady=5)
            ctk.CTkLabel(pwd_container, text="SENHA", font=("Segoe UI", 10, "bold"), text_color=C_TEXT_DIM).pack(anchor="w")
            
            pwd_row = ctk.CTkFrame(pwd_container, fg_color="transparent")
            pwd_row.pack(fill="x")
            
            entry_pwd = ctk.CTkEntry(pwd_row, height=35, fg_color=C_BG_SIDEBAR, border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN, show="*")
            entry_pwd.pack(side="left", fill="x", expand=True, pady=(2, 5))
            entry_pwd.bind("<Button-1>", lambda event: entry_pwd.focus_set())
            self.inputs["password"] = entry_pwd
            
            btn_eye = ctk.CTkButton(pwd_row, text="", width=40, height=35, fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN,
                                    image=IconAssets.get_image("eye"))
            btn_eye.configure(command=lambda e=entry_pwd, b=btn_eye: toggle_password(e, b))
            btn_eye.pack(side="left", padx=(5,0), pady=(2, 5))

            btn_gen = ctk.CTkButton(pwd_row, text="🎲", width=40, height=35, fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN,
                                    command=self.generate_password)
            btn_gen.pack(side="left", padx=(5,0), pady=(2, 5))
            
            self.create_input("Site URL", "url")

        elif choice == "Cartão":
            self.create_input("Número", "card_number")
            col = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            col.pack(fill="x")
            self.create_input("Validade", "expiry", parent=col, side="left")
            self.create_input("CVV", "cvv", parent=col, side="left")
        
        elif choice == "Nota":
            toolbar = ctk.CTkFrame(self.form_frame, fg_color=C_BG_SIDEBAR, height=40, corner_radius=8)
            toolbar.pack(fill="x", pady=(10, 5))
            font_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
            font_frame.pack(side="left", padx=5)
            self.font_var = ctk.StringVar(value="Segoe UI")
            ctk.CTkComboBox(font_frame, values=["Segoe UI", "Arial", "Calibri", "Courier New"], width=110, height=28, 
                            variable=self.font_var, command=self.change_font_family, font=("Segoe UI", 12), border_color=C_BORDER).pack(side="left", padx=2)
            self.size_var = ctk.StringVar(value="12")
            ctk.CTkComboBox(font_frame, values=["10", "11", "12", "14", "18", "24"], width=60, height=28, 
                            variable=self.size_var, command=self.change_font_size, font=("Segoe UI", 12), border_color=C_BORDER).pack(side="left", padx=2)
            ctk.CTkLabel(toolbar, text="|", text_color=C_BORDER[1]).pack(side="left", padx=5)
            style_configs = [("𝐁", "bold"), ("𝐼", "italic"), ("U̲", "underline")]
            for text, mode in style_configs:
                ctk.CTkButton(toolbar, text=text, width=30, height=30, fg_color="transparent", hover_color=C_HOVER,
                              text_color=C_TEXT_MAIN, font=("Times New Roman", 14, "bold"), command=lambda m=mode: self.toggle_style(m)).pack(side="left", padx=1)
            ctk.CTkLabel(toolbar, text="|", text_color=C_BORDER[1]).pack(side="left", padx=5)
            align_configs = [("⫷", "left"), ("≡", "center"), ("⫸", "right")]
            for text, align in align_configs:
                ctk.CTkButton(toolbar, text=text, width=30, height=30, fg_color="transparent", hover_color=C_HOVER,
                              text_color=C_TEXT_MAIN, font=("Segoe UI", 14), command=lambda a=align: self.align_text(a)).pack(side="left", padx=1)
            
            ctk.CTkLabel(toolbar, text="|", text_color=C_BORDER[1]).pack(side="left", padx=5)
            
            self.block_var = ctk.StringVar(value="＋ Adicionar...")
            tools = ["H1 Título 1", "H2 Título 2", "H3 Título 3", "☐ Tarefa", "• Lista", " Código", "❝ Citação", "― Divisor"]
            
            combo_tools = ctk.CTkComboBox(toolbar, values=tools, width=130, height=28, 
                                          variable=self.block_var, command=self.insert_block,
                                          font=("Segoe UI", 12), border_color=C_BORDER, state="readonly")
            combo_tools.pack(side="left", padx=5)

            editor_container = ctk.CTkFrame(self.form_frame, fg_color=C_CARD, corner_radius=0, border_width=1, border_color=C_BORDER)
            editor_container.pack(fill="both", expand=True, pady=0)
            self.inputs["note"] = ctk.CTkTextbox(editor_container, height=400, fg_color="transparent", 
                                                 text_color=C_TEXT_MAIN, border_width=0, font=("Segoe UI", 12), wrap="word")
            self.inputs["note"].pack(fill="both", expand=True, padx=20, pady=20)
            
            self.setup_tags()
            self.create_floating_menu()
            
            tk_text = self.inputs["note"]._textbox
            tk_text.bind("<ButtonRelease-1>", self.check_text_selection)
            tk_text.bind("<KeyRelease>", self.check_text_selection)
            tk_text.bind("<Button-1>", self.handle_text_click) 
            tk_text.bind("<KeyPress>", self.hide_floating_menu)

        elif choice == "Link":
            self.create_input("Link", "url")
        
        else:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT fields FROM custom_types WHERE name=?", (choice,))
            row = c.fetchone()
            conn.close()
            
            if row:
                fields_str = row[0]
                field_list = [f.strip() for f in fields_str.split(',') if f.strip()]
                
                for field in field_list:
                    key = field.lower().replace(" ", "_")
                    
                    if "senha" in key or "password" in key or "pass" in key:
                         pwd_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
                         pwd_container.pack(fill="x", pady=5)
                         ctk.CTkLabel(pwd_container, text=field.upper(), font=("Segoe UI", 10, "bold"), text_color=C_TEXT_DIM).pack(anchor="w")
                         
                         pwd_row = ctk.CTkFrame(pwd_container, fg_color="transparent")
                         pwd_row.pack(fill="x")
                         
                         entry_pwd = ctk.CTkEntry(pwd_row, height=35, fg_color=C_BG_SIDEBAR, border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN, show="*")
                         entry_pwd.pack(side="left", fill="x", expand=True, pady=(2, 5))
                         entry_pwd.bind("<Button-1>", lambda event: entry_pwd.focus_set())
                         self.inputs[key] = entry_pwd
                         
                         btn_eye = ctk.CTkButton(pwd_row, text="", width=40, height=35, fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN,
                                                 image=IconAssets.get_image("eye"))
                         btn_eye.configure(command=lambda e=entry_pwd, b=btn_eye: toggle_password(e, b))
                         btn_eye.pack(side="left", padx=(5,0), pady=(2, 5))

                         btn_gen = ctk.CTkButton(pwd_row, text="🎲", width=40, height=35, fg_color="transparent", border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN,
                                                command=lambda k=key: self.generate_custom_password(k))
                         btn_gen.pack(side="left", padx=(5,0), pady=(2, 5))
                    else:
                        self.create_input(field, key)

        btn_txt = "Salvar Alterações" if self.editing_id else "Salvar Novo Item"
        ctk.CTkButton(self.form_frame, text=btn_txt, command=self.save_item, fg_color=C_ACCENT, height=40, width=150, corner_radius=20).pack(anchor="w", pady=30)

    def generate_custom_password(self, key):
        if key not in self.inputs: return
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = ''.join(random.choice(chars) for _ in range(16))
        self.inputs[key].delete(0, 'end')
        self.inputs[key].insert(0, pwd)

    

    def setup_tags(self):
        if "note" not in self.inputs: return
        txt = self.inputs["note"]._textbox
        txt.tag_configure("left", justify='left')
        txt.tag_configure("center", justify='center')
        txt.tag_configure("right", justify='right')
        txt.tag_configure("underline", underline=True)
        txt.tag_configure("h1", font=("Segoe UI", 24, "bold"), spacing3=10)
        txt.tag_configure("h2", font=("Segoe UI", 18, "bold"), spacing3=5)
        txt.tag_configure("h3", font=("Segoe UI", 14, "bold"))
        is_dark = ctk.get_appearance_mode() == "Dark"
        code_bg = "#2B2B2B" if is_dark else "#F0F0F0"
        code_fg = "#E0E0E0" if is_dark else "#DA1E28"
        txt.tag_configure("code", font=("Consolas", 11), background=code_bg, foreground=code_fg, lmargin1=10, lmargin2=10)
        txt.tag_configure("quote", font=("Segoe UI", 12, "italic"), lmargin1=20, lmargin2=20, foreground="#888888")
        txt.tag_configure("checked", foreground="#888888", overstrike=True)

    def change_font_family(self, family): self._apply_font_style()
    def change_font_size(self, size): self._apply_font_style()

    def _apply_font_style(self):
        if "note" not in self.inputs: return
        txt = self.inputs["note"]._textbox
        try:
            if not txt.tag_ranges("sel"): return
            family = self.font_var.get()
            size = int(self.size_var.get())
            tag_name = f"font_{family}_{size}".replace(" ", "")
            txt.tag_configure(tag_name, font=(family, size))
            txt.tag_add(tag_name, "sel.first", "sel.last")
        except Exception: pass

    def toggle_style(self, style):
        if "note" not in self.inputs: return
        txt = self.inputs["note"]._textbox
        try:
            if not txt.tag_ranges("sel"): return
            start, end = "sel.first", "sel.last"
            if style == "underline":
                current_tags = txt.tag_names(start)
                if "underline" in current_tags: txt.tag_remove("underline", start, end)
                else: txt.tag_add("underline", start, end)
            else:
                family = self.font_var.get()
                size = int(self.size_var.get())
                tag_name = f"{style}_{family}_{size}".replace(" ", "")
                font_config = (family, size, style)
                txt.tag_configure(tag_name, font=font_config)
                current_tags = txt.tag_names(start)
                if tag_name in current_tags: txt.tag_remove(tag_name, start, end)
                else: txt.tag_add(tag_name, start, end)
        except Exception: pass

    def align_text(self, align):
        if "note" not in self.inputs: return
        txt = self.inputs["note"]._textbox
        try:
            if not txt.tag_ranges("sel"): return
            for a in ["left", "center", "right"]: txt.tag_remove(a, "sel.first", "sel.last")
            txt.tag_add(align, "sel.first", "sel.last")
        except Exception: pass

    def choose_color(self):
        if "note" not in self.inputs: return
        txt = self.inputs["note"]._textbox
        try:
            if not txt.tag_ranges("sel"): return
            color = colorchooser.askcolor(title="Escolher Cor do Texto")[1]
            if color:
                tag_name = f"color_{color}"
                txt.tag_configure(tag_name, foreground=color)
                txt.tag_add(tag_name, "sel.first", "sel.last")
                self.hide_floating_menu()
        except Exception: pass

    def insert_block(self, choice):
        if "note" not in self.inputs: return
        txt = self.inputs["note"]._textbox
        self.block_var.set("＋ Adicionar...") 
        try:
            current_idx = txt.index("insert")
            line_start = f"{current_idx.split('.')[0]}.0"
            line_end = f"{current_idx.split('.')[0]}.end"
            if "H1" in choice:
                txt.tag_add("h1", line_start, line_end)
                txt.tag_remove("h2", line_start, line_end)
                txt.tag_remove("h3", line_start, line_end)
            elif "H2" in choice:
                txt.tag_add("h2", line_start, line_end)
                txt.tag_remove("h1", line_start, line_end)
            elif "H3" in choice:
                txt.tag_add("h3", line_start, line_end)
            elif "Tarefa" in choice: txt.insert(line_start, "☐  ")
            elif "Lista" in choice: txt.insert(line_start, "•  ")
            elif "Código" in choice:
                if txt.tag_ranges("sel"): txt.tag_add("code", "sel.first", "sel.last")
                else: txt.tag_add("code", line_start, line_end)
            elif "Citação" in choice: txt.tag_add("quote", line_start, line_end)
            elif "Divisor" in choice: txt.insert(current_idx, "\n" + ("―" * 40) + "\n")
            self.inputs["note"].focus_set()
        except Exception as e: print(f"Erro: {e}")

    def handle_text_click(self, event):
        self.hide_floating_menu()
        self.inputs["note"].focus_set() 
        txt = self.inputs["note"]._textbox
        try:
            index = txt.index(f"@{event.x},{event.y}")
            char = txt.get(index, f"{index}+1c")
            if char == "☐":
                txt.delete(index, f"{index}+1c")
                txt.insert(index, "☑")
                line_start = f"{index.split('.')[0]}.0"
                line_end = f"{index.split('.')[0]}.end"
                txt.tag_add("checked", line_start, line_end)
                return "break"
            elif char == "☑":
                txt.delete(index, f"{index}+1c")
                txt.insert(index, "☐")
                line_start = f"{index.split('.')[0]}.0"
                line_end = f"{index.split('.')[0]}.end"
                txt.tag_remove("checked", line_start, line_end)
                return "break"
        except Exception: pass

    
    def serialize_richtext(self, textbox):
        txt = textbox._textbox
        dump = txt.dump("1.0", "end-1c", tag=True, text=True)
        return json.dumps(dump)
    def deserialize_richtext(self, textbox, json_dump):
        try:
            data = json.loads(json_dump)
            txt = textbox._textbox
            txt.delete("1.0", "end")
            for item in data:
                key, value, index = item
                if key == "text": txt.insert(index, value)
                elif key == "tagon":
                    txt.tag_add(value, index)
                    if value.startswith("color_"):
                        color = value.split("_")[1]
                        txt.tag_config(value, foreground=color)
        except: textbox.insert("1.0", json_dump)

    
    def create_input(self, label, key, show=None, parent=None, side="top"):
        target = parent if parent else self.form_frame
        container = ctk.CTkFrame(target, fg_color="transparent")
        if side == "left": container.pack(side="left", expand=True, fill="x", padx=(0, 10))
        else: container.pack(fill="x", pady=5)
        ctk.CTkLabel(container, text=label.upper(), font=("Segoe UI", 10, "bold"), text_color=C_TEXT_DIM).pack(anchor="w")
        entry = ctk.CTkEntry(container, height=35, fg_color=C_BG_SIDEBAR, border_width=1, border_color=C_BORDER, text_color=C_TEXT_MAIN, show=show)
        entry.pack(fill="x", pady=(2, 5))
        entry.bind("<Button-1>", lambda event: entry.focus_set())
        self.inputs[key] = entry

    def save_item(self):
        item_type = self.combo_type.get()
        folder_selection = self.combo_folder.get()
        
        # --- VERIFICAÇÃO DE PASTA OBRIGATÓRIA ---
        if not folder_selection or folder_selection == "Nenhuma pasta criada!":
            ModernPopups.show_notify(self, "Selecione ou crie uma pasta!")
            return

        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox): 
                data[key] = self.serialize_richtext(widget)
            else: data[key] = widget.get().strip()
        if not data.get("title"): return

        folder_id = self.folder_map.get(folder_selection)

        subtitle = ""
        if item_type == "Login": subtitle = data.get("username", "")
        elif item_type == "Cartão": subtitle = f"Final {data.get('card_number', '')[-4:]}"
        elif item_type == "Link": subtitle = data.get("url", "")
        elif item_type == "Nota": subtitle = "Nota de texto"
        else:
            keys = list(data.keys())
            if "title" in keys: keys.remove("title")
            if keys: subtitle = f"{data[keys[0]]}"

        json_data = json.dumps(data)
        encrypted_blob = self.encrypt(json_data)

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        if self.editing_id:
            
            c.execute("UPDATE entries SET type=?, title=?, subtitle=?, data_blob=?, folder_id=? WHERE id=?",
                      (item_type, data["title"], subtitle, encrypted_blob, folder_id, self.editing_id))
            self.editing_id = None 
            ModernPopups.show_notify(self, "Item Atualizado!")
        else:
            
            c.execute("INSERT INTO entries (type, title, subtitle, data_blob, folder_id, is_deleted) VALUES (?, ?, ?, ?, ?, 0)", 
                      (item_type, data["title"], subtitle, encrypted_blob, folder_id))
            ModernPopups.show_notify(self, "Item Criado!")
            
        conn.commit()
        conn.close()
        self.switch_page("search")

    def action_item(self, i_type, blob):
        try:
            data = json.loads(self.decrypt(blob))
            text_to_copy = ""
            if i_type == "Link": text_to_copy = data.get("url", "")
            elif i_type == "Login": text_to_copy = data.get("password", "")
            elif i_type == "Cartão": text_to_copy = data.get("cvv", "")
            elif i_type == "Nota":
                try:
                    dump = json.loads(data.get("note", ""))
                    text_to_copy = "".join([x[1] for x in dump if x[0] == "text"])
                except: text_to_copy = data.get("note", "")
            else:
                text_to_copy = f"--- {data.get('title', 'Item')} ---\n"
                for k, v in data.items():
                    if k == "title": continue
                    clean_key = k.replace("_", " ").upper()
                    text_to_copy += f"{clean_key}: {v}\n"
            self.copy_to_clipboard(text_to_copy)
        except: pass

    def open_link(self, blob):
        try:
            data = json.loads(self.decrypt(blob))
            url = data.get("url", "")
            if url: webbrowser.open(url)
        except: pass

    def soft_delete_item(self, item_id):
        
        def confirm_action():
            conn = sqlite3.connect(self.db_file)
            conn.execute("UPDATE entries SET is_deleted=1 WHERE id=?", (item_id,))
            conn.commit(); conn.close()
            self.load_items()
            ModernPopups.show_notify(self, "Item movido para lixeira")
        ModernPopups.show_confirm(parent=self, title="Excluir Item", message="O item será movido para a lixeira.", command_yes=confirm_action)

    def restore_item(self, item_id):
        conn = sqlite3.connect(self.db_file)
        conn.execute("UPDATE entries SET is_deleted=0 WHERE id=?", (item_id,))
        conn.commit(); conn.close()
        self.render_trash()
        ModernPopups.show_notify(self, "Item restaurado!")

    def permanent_delete(self, item_id):
        def confirm_action():
            conn = sqlite3.connect(self.db_file)
            conn.execute("DELETE FROM entries WHERE id=?", (item_id,))
            conn.commit(); conn.close()
            self.render_trash()
            ModernPopups.show_notify(self, "Item apagado para sempre")
        ModernPopups.show_confirm(parent=self, title="Exclusão Permanente", message="Essa ação não pode ser desfeita.", command_yes=confirm_action, danger=True)

    
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")
    def start_move(self, event): self.x_offset = event.x; self.y_offset = event.y
    
    def do_move(self, event): 
        # Impede mover a janela se estiver em tela cheia
        if getattr(self, 'is_fullscreen', False):
            return
        x = self.winfo_pointerx() - self.x_offset
        y = self.winfo_pointery() - self.y_offset
        self.geometry(f"+{x}+{y}")
        
    def resize_window(self, event):
        # Impede redimensionar se estiver em tela cheia
        if getattr(self, 'is_fullscreen', False):
            return
        new_width = self.winfo_width() + (event.x_root - self.winfo_rootx() - self.winfo_width())
        new_height = self.winfo_height() + (event.y_root - self.winfo_rooty() - self.winfo_height())
        if new_width > 400 and new_height > 300: self.geometry(f"{new_width}x{new_height}")

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            # Salva geometria anterior
            self.last_geometry = self.geometry()
            self.is_fullscreen = True
            
            # Maximiza (Muda para ícone de restaurar)
            self.btn_max.configure(text="❐")
            
            # Define o tamanho para o tamanho da tela
            w = self.winfo_screenwidth()
            h = self.winfo_screenheight()
            self.geometry(f"{w}x{h}+0+0")
        else:
            # Restaura (Muda para ícone de quadrado)
            self.is_fullscreen = False
            self.btn_max.configure(text="□")
            self.geometry(self.last_geometry)

    def close_app(self): self.destroy()
    def clear_content(self): 
        for w in self.content.winfo_children(): w.destroy()
        
        if hasattr(self, 'editing_id') and self.editing_id: self.editing_id = None

    def encrypt(self, text): return self.cipher.encrypt(text.encode()).decode()
    def decrypt(self, text): return self.cipher.decrypt(text.encode()).decode()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        
        conn.execute('''CREATE TABLE IF NOT EXISTS folders (id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER, is_deleted INTEGER DEFAULT 0)''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, type TEXT, title TEXT, subtitle TEXT, data_blob TEXT, folder_id INTEGER, is_deleted INTEGER DEFAULT 0)''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS custom_types (name TEXT PRIMARY KEY, fields TEXT)''')
        
        
        try: conn.execute("ALTER TABLE entries ADD COLUMN is_deleted INTEGER DEFAULT 0")
        except: pass
        try: conn.execute("ALTER TABLE folders ADD COLUMN is_deleted INTEGER DEFAULT 0")
        except: pass
        
        conn.commit()
        conn.close()

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        ModernPopups.show_notify(self, "Copiado para área de transferência!")

if __name__ == "__main__":
    app = NotionVaultV8()
    app.mainloop()