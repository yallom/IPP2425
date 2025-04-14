import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import math

class FuturisticLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Saúde Comunitária")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a192f")

        self.create_gui()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_gui(self):
        main_canvas = tk.Canvas(self.root, bg="#0a192f", highlightthickness=0)
        main_canvas.pack(expand=True, fill="both")

        self.create_hexagon_logo(main_canvas, 250, 150, 40, "#64ffda")

        title_font = Font(family="Arial", size=28, weight="bold")
        main_canvas.create_text(250, 230, text="SAÚDE COMUNITÁRIA", fill="#64ffda", font=title_font)

        form_frame = tk.Frame(self.root, bg="#172a45")
        form_frame.place(relx=0.5, rely=0.58, anchor="center", width=380, height=300)

        self.create_neon_border(form_frame)
        self.configure_styles()

        self.create_neon_label(form_frame, "Utilizador", 40, 10)
        self.username = ttk.Entry(form_frame, style="Futuristic.TEntry")
        self.username.place(x=40, y=30, width=300, height=40)

        self.create_neon_label(form_frame, "Password", 40, 90)
        self.password = ttk.Entry(form_frame, show="•", style="Futuristic.TEntry")
        self.password.place(x=40, y=110, width=300, height=40)

        self.login_btn = tk.Canvas(form_frame, bg="#172a45", highlightthickness=0,
                                   width=300, height=45)
        self.login_btn.place(x=40, y=200)
        self.draw_animated_button()
        self.login_btn.bind("<Button-1>", lambda e: self.attempt_login())
        self.login_btn.bind("<Enter>", self.on_enter)
        self.login_btn.bind("<Leave>", self.on_leave)

    def create_hexagon_logo(self, canvas, x, y, size, color):
        angle = 60
        coordinates = []
        for i in range(6):
            x_coord = x + size * math.cos(math.radians(angle * i + 30))
            y_coord = y + size * math.sin(math.radians(angle * i + 30))
            coordinates.extend([x_coord, y_coord])
        canvas.create_polygon(coordinates, fill=color, outline="#0a192f", width=3)
        canvas.create_text(x, y, text="⚕", font=("Arial", int(size*1.2)), fill="#0a192f", anchor="center")

    def create_neon_border(self, frame):
        border = tk.Frame(frame, bg="#64ffda")
        border.place(x=5, y=5, width=370, height=290)

    def create_neon_label(self, parent, text, x, y):
        label = tk.Label(parent, text=text, font=("Arial", 10, "bold"),
                         fg="white", bg="#172a45")  # Letras brancas, fundo igual ao frame
        label.place(x=x, y=y)

    def draw_animated_button(self, color="#233554"):
        self.login_btn.delete("all")
        self.login_btn.create_rectangle(0, 0, 300, 45, fill=color, outline="#64ffda", width=1)
        self.login_btn.create_text(150, 22, text="ACESSAR SISTEMA", fill="#64ffda",
                                   font=("Arial", 12, "bold"), anchor="center")

    def on_enter(self, event):
        self.draw_animated_button("#1f3a60")

    def on_leave(self, event):
        self.draw_animated_button("#233554")

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Futuristic.TEntry",
                        fieldbackground="#172a45",
                        foreground="white",
                        insertcolor="#64ffda",
                        bordercolor="#172a45",
                        lightcolor="#172a45",
                        darkcolor="#172a45",
                        padding=10,
                        relief="flat")
        style.map("Futuristic.TEntry",
                  bordercolor=[("focus", "#64ffda")],
                  lightcolor=[("focus", "#64ffda")])

    def attempt_login(self):
        username = self.username.get()
        password = self.password.get()

        if not username or not password:
            messagebox.showwarning("Dados Incompletos", "Preencha todos os campos de acesso!")
            return

        self.show_loading_animation()
        self.root.after(1500, lambda: self.check_credentials(username, password))

    def show_loading_animation(self):
        self.login_btn.delete("all")
        self.loading_circle = self.login_btn.create_oval(130, 15, 170, 55, outline="#64ffda", width=2)
        self.animate_loading(0)

    def animate_loading(self, angle):
        self.login_btn.delete(self.loading_circle)
        x = 150 + 20 * math.cos(math.radians(angle))
        y = 35 + 20 * math.sin(math.radians(angle))
        self.loading_circle = self.login_btn.create_oval(x-5, y-5, x+5, y+5, fill="#64ffda", outline="")
        self.root.after(30, lambda: self.animate_loading((angle + 15) % 360))

    def check_credentials(self, username, password):
        self.login_btn.delete("all")
        self.draw_animated_button()

        if username == "admin" and password == "admin":
            messagebox.showinfo("Acesso Concedido", "Bem-vindo à Plataforma de Saúde Integrada!")
            self.root.destroy()
        else:
            messagebox.showerror("Acesso Negado", "Credenciais inválidas ou usuário não autorizado!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticLogin(root)
    root.mainloop()
