import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
from tkcalendar import DateEntry  
import csv
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import numpy as np
from matplotlib import pyplot as plt  # Importação correta para usar pyplot

# Fade-in effect
def fade_in(window):
    alpha = 0.0
    while alpha < 1.0:
        alpha += 0.02
        time.sleep(0.01)
        window.attributes("-alpha", alpha)

# Efeito de hover no botão
def on_enter(e):
    btn_login.configure(style="Hover.TButton")

def on_leave(e):
    btn_login.configure(style="TButton")

# Animação simples de pulsar o ícone
def pulse_icon():
    scale = 1.0
    grow = True
    while True:
        time.sleep(0.05)
        if grow:
            scale += 0.01
        else:
            scale -= 0.01

        if scale >= 1.05:
            grow = False
        elif scale <= 0.95:
            grow = True

        try:
            new_size = int(80 * scale)
            resized = icon_img.resize((new_size, new_size))
            icon_tk = ImageTk.PhotoImage(resized)
            icon_label.configure(image=icon_tk)
            icon_label.image = icon_tk
        except:
            break  # Para evitar erro ao fechar janela

# Função de login
def login():
    username = entry_user.get()
    password = entry_pass.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        root.destroy()
    else:
        messagebox.showerror("Erro", "Utilizador ou senha incorretos.")

# Janela principal (Login)
root = ThemedTk(theme="arc")  # Tema moderno
root.title("Saúde Comunitária")
root.geometry("420x600")
root.configure(bg="#f5f5f5")  # Fundo neutro claro
root.attributes("-alpha", 0.0)  # Começa invisível

# Fade-in
threading.Thread(target=fade_in, args=(root,), daemon=True).start()

# Cabeçalho
header = tk.Frame(root, bg="#2c3e50", height=50)  # Fundo cinza escuro para o cabeçalho
header.pack(fill=tk.X, side=tk.TOP)
title = tk.Label(header, text="Saúde Comunitária", font=("Orbitron", 18, "bold"), bg="#2c3e50", fg="white")
title.pack(pady=10)

# Ícone com animação
try:
    icon_img = Image.open("hospital.png")  # Substitua pelo nome da imagem do hospital
    icon_img = icon_img.resize((120, 120), Image.ANTIALIAS)  # Ajuste o tamanho do ícone para 120x120
    icon_tk = ImageTk.PhotoImage(icon_img)
    icon_label = tk.Label(root, image=icon_tk, bg="#f5f5f5")  # Fundo neutro claro
    icon_label.image = icon_tk
    icon_label.pack(pady=20)  # Espaçamento ao redor do ícone
    threading.Thread(target=pulse_icon, daemon=True).start()
except:
    icon_label = tk.Label(root, text="🏥", font=("Segoe UI", 48), bg="#f5f5f5")  # Emoji como fallback
    icon_label.pack(pady=20)

# Frame do formulário
form_frame = ttk.Frame(root, padding=20)
form_frame.pack(pady=30)

style = ttk.Style()
style.configure("TEntry", padding=5, font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("Hover.TButton", background="#c0dfd9", foreground="#000")

# Define o estilo personalizado para os botões com a mesma cor do fundo da aplicação
style.configure(
    "App.TButton",
    background="#2c3e50",  # Azul escuro (mesma cor do fundo da aplicação)
    foreground="white",    # Texto branco
    font=("Segoe UI", 11),
    padding=6
)
style.map(
    "App.TButton",
    background=[("active", "#1a252f")],  # Azul mais escuro ao passar o mouse
    foreground=[("active", "white")]
)

# Combobox com opções estilizadas e seta branca
style.configure(
    "Custom.TCombobox",
    font=("Segoe UI", 12),
    padding=5,
    foreground="white",
    background="#2c3e50",  # Azul do fundo
    arrowcolor="white"  # Seta branca
)
style.map(
    "Custom.TCombobox",
    fieldbackground=[("readonly", "#2c3e50")],  # Fundo azul para o campo
    foreground=[("readonly", "white")],         # Texto branco nas opções
    background=[("readonly", "#2c3e50")],       # Fundo azul para as opções
    arrowcolor=[("readonly", "white")]          # Seta branca no estado readonly
)

# Campos
lbl_user = ttk.Label(form_frame, text="Utilizador:", font=("Segoe UI", 11), background="#f5f5f5")
lbl_user.pack(anchor="w", pady=(0, 2))
entry_user = ttk.Entry(form_frame, style="TEntry", width=30)
entry_user.pack(pady=5)

lbl_pass = ttk.Label(form_frame, text="Password:", font=("Segoe UI", 11), background="#f5f5f5")
lbl_pass.pack(anchor="w", pady=(10, 2))
entry_pass = ttk.Entry(form_frame, show="*", style="TEntry", width=30)
entry_pass.pack(pady=5)

# Botão de login
btn_login = ttk.Button(root, text="Entrar", command=login)
btn_login.pack(pady=20)

btn_login.bind("<Enter>", on_enter)
btn_login.bind("<Leave>", on_leave)

# Rodapé
footer = tk.Frame(root, bg="#2c3e50", height=30)  # Fundo cinza escuro para o rodapé
footer.pack(fill=tk.X, side=tk.BOTTOM)
user_info = tk.Label(footer, text="Utilizador: admin | Projeto IPP 2025", bg="#2c3e50", fg="white", font=("Orbitron", 9))
user_info.pack(pady=5)

root.mainloop()

class CampanhasFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(padding=20, style="Custom.TFrame")  # Define o estilo do frame

        # Define o estilo personalizado para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")  # Fundo neutro claro
        style.configure("Custom.TButton", background="#f5f5f5", font=("Segoe UI", 11))
        style.configure("Custom.Treeview", background="#f5f5f5", fieldbackground="#f5f5f5", font=("Segoe UI", 10))
        style.configure("Custom.Treeview.Heading", background="#2c3e50", foreground="white", font=("Segoe UI", 11, "bold"))
        style.configure("Custom.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Blue.TButton", background="#2c3e50", foreground="white", font=("Segoe UI", 11), padding=6)
        style.map("Blue.TButton",
                  background=[("active", "#1a252f")],  # Azul mais escuro ao passar o mouse
                  foreground=[("active", "white")])
        style.configure("Large.TLabel", font=("Segoe UI", 18, "bold"), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Small.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Section.TLabel", font=("Segoe UI", 14, "bold"), background="#f5f5f5", foreground="#2c3e50")

        # Dataset de medicamentos e vacinas
        self.dataset = {
            "Medicamento": ["Paracetamol", "Ibuprofeno", "Amoxicilina", "Omeprazol"],
            "Vacina": ["Vacina Gripe", "Vacina COVID-19", "Vacina Hepatite B", "Vacina Tétano"]
        }

        # Lista para armazenar os dados das campanhas
        self.campanhas = [
            {"Nome": "Campanha de Vacinação Gripe", "Início": "2025-04-01", "Fim": "2025-04-15", "Grupo-Alvo": "Idosos", "Estado": "Ativa"},
            {"Nome": "Rastreio Diabetes", "Início": "2025-01-10", "Fim": "2025-02-10", "Grupo-Alvo": "Adultos", "Estado": "Encerrada"}
        ]

        # Título com estilo personalizado
        ttk.Label(self, text="Gestão de Campanhas de Saúde", style="Custom.TLabel").pack(pady=(0, 10))

        # Filtros e Ações
        filtro_frame = ttk.Frame(self, style="Custom.TFrame")
        filtro_frame.pack(fill="x", pady=10)

        # Label "Filtrar por" com cor azul
        ttk.Label(
            filtro_frame,
            text="Filtrar por:",
            font=("Segoe UI", 11),
            foreground="#2c3e50",  # Azul escuro
            background="#f5f5f5"   # Fundo neutro claro
        ).pack(side="left")

        # Combobox com o estilo atualizado
        self.combo_filtro = ttk.Combobox(
            filtro_frame,
            values=["Todas", "Ativas", "Encerradas"],
            state="readonly",
            style="Custom.TCombobox"
        )
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side="left", padx=5)
        self.combo_filtro.bind("<<ComboboxSelected>>", self.filtrar_campanhas)

        # Botões com estilo azul
        ttk.Button(filtro_frame, text="+ Nova Campanha", command=self.abrir_janela_cadastro, style="Blue.TButton").pack(side="right", padx=5)
        ttk.Button(filtro_frame, text="Eliminar Campanha", command=self.eliminar_campanha, style="Blue.TButton").pack(side="right", padx=5)
        

        # Tabela de campanhas
        colunas = ("Nome", "Início", "Fim", "Grupo-Alvo", "Estado")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=10, style="Custom.Treeview")
        for col in colunas:
            self.tabela.heading(col, text=col, anchor="center")
            self.tabela.column(col, width=100, anchor="center")

        self.tabela.pack(fill="both", expand=True, pady=10)

        self.tabela.bind("<Double-1>", self.abrir_detalhes_campanha)

        # Preenche a tabela com os dados iniciais
        self.atualizar_tabela(self.campanhas)

    def atualizar_tabela(self, campanhas):
        """Atualiza a tabela com os dados fornecidos."""
        # Limpa a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Insere os novos dados
        for campanha in campanhas:
            self.tabela.insert('', 'end', values=(
                campanha["Nome"], campanha["Início"], campanha["Fim"], campanha["Grupo-Alvo"], campanha["Estado"]
            ))

    def filtrar_campanhas(self, event=None):
        """Filtra as campanhas com base na seleção do filtro."""
        filtro = self.combo_filtro.get().strip().lower()  # Remove espaços e converte para minúsculas

        if (filtro == "todas"):
            campanhas_filtradas = self.campanhas
        else:
            campanhas_filtradas = []
            for c in self.campanhas:
                estado = c.get("Estado", "").strip().lower()

                # Lógica de correspondência para "Ativas" e "Encerradas"
                if (filtro == "ativas" and estado == "ativa"):
                    campanhas_filtradas.append(c)
                elif (filtro == "encerradas" and estado == "encerrada"):
                    campanhas_filtradas.append(c)

        # Atualiza a tabela com as campanhas filtradas
        self.atualizar_tabela(campanhas_filtradas)

    def abrir_janela_cadastro(self):
        janela = tk.Toplevel(self)
        janela.title("Nova Campanha")
        janela.geometry("750x700")
        janela.configure(bg="#f5f5f5")  # Fundo neutro claro
        janela.transient(self)

        # Cabeçalho da janela
        header = tk.Frame(janela, bg="#2c3e50", height=50)
        header.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(header, text="Nova Campanha", font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=10)

        # Canvas para permitir rolagem
        canvas = tk.Canvas(janela, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno para os widgets
        frame_interno = ttk.Frame(canvas, style="Custom.TFrame")
        canvas.create_window((0, 0), window=frame_interno, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_interno.bind("<Configure>", atualizar_scrollregion)

        # Define estilos para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")
        style.configure("Custom.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Custom.TEntry", padding=5, font=("Segoe UI", 11))
        style.configure("Custom.TCombobox", padding=5, font=("Segoe UI", 11))

        # Título com estilo maior e destacado
        ttk.Label(frame_interno, text="Cadastro de Campanha", style="Custom.TLabel", font=("Segoe UI", 14, "bold")).pack(pady=20)

        # Separador para os campos principais
        ttk.Label(frame_interno, text="Informações Básicas", style="Custom.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=10)

        # Campos do formulário com fonte menor e espaçamento ajustado
        campos = [
            ("Nome", "entry"),
            ("Data Início", "date"),
            ("Data Fim", "date"),
            ("Grupo Risco", "combobox"),
            ("Grupo-Alvo", "combobox"),
            ("Sexo", "combobox"),
            ("Grávidas", "combobox"),
            ("Recurso", "combobox"),
            ("Item", "combobox"),
            ("Profissionais Atribuídos", "entry"),
            ("Número de Participantes", "entry"),
            ("Observações", "text")
        ]

        self.entries = {}

        def atualizar_gravidas(event):
            sexo = self.entries["Sexo"].get()
            gravidas_combobox = self.entries["Grávidas"]
            
            if sexo == "Masculino":
                gravidas_combobox.set("Não")
                gravidas_combobox["state"] = "disabled"
            else:
                gravidas_combobox["state"] = "readonly"
                if sexo == "Feminino":
                    gravidas_combobox["values"] = ["Sim", "Não", "Apenas"]
                else:  # Ambos
                    gravidas_combobox["values"] = ["Sim", "Não"]

        for campo, tipo in campos:
            frame = ttk.Frame(frame_interno, style="Custom.TFrame")
            frame.pack(fill="x", padx=20, pady=8)
            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)

            if tipo == "entry":
                entry = ttk.Entry(frame, style="Custom.TEntry")
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="yyyy-mm-dd", width=12, background="#2c3e50",
                                foreground="white", borderwidth=2, style="Custom.TCombobox")
            elif tipo == "combobox":
                if campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly", style="Custom.TCombobox")
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino", "Ambos"], state="readonly", style="Custom.TCombobox")
                    entry.bind("<<ComboboxSelected>>", atualizar_gravidas)
                elif campo == "Grávidas":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox")
                elif campo == "Recurso":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox")
                    entry.bind("<<ComboboxSelected>>", self.atualizar_itens)
                elif campo == "Item":
                    entry = ttk.Combobox(frame, values=[], state="readonly", style="Custom.TCombobox")
            elif tipo == "text":
                entry = tk.Text(frame, height=5, wrap="word", bg="white", font=("Segoe UI", 11), relief="solid", borderwidth=1)

            entry.pack(fill="x")
            self.entries[campo] = entry

        # Botões com estilo azul e espaçamento ajustado
        botoes_frame = ttk.Frame(frame_interno, style="Custom.TFrame", padding=20)
        botoes_frame.pack(fill="x", pady=20)

        ttk.Button(botoes_frame, text="Guardar", command=self.guardar_campanha, style="App.TButton").pack(side="left", padx=10)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy, style="App.TButton").pack(side="right", padx=10)

    def atualizar_itens(self, event=None):
        """Atualiza os itens disponíveis com base no recurso selecionado."""
        recurso = self.entries["Recurso"].get()
        itens = self.dataset.get(recurso, [])  # Obtém os itens do dataset
        self.entries["Item"]["values"] = itens  # Atualiza os valores do combobox de itens
        if itens:
            self.entries["Item"].current(0)  # Define o primeiro item como padrão

    def guardar_campanha(self):
        """Guarda os dados da nova campanha e atualiza a tabela."""
        # Obtém os valores dos campos
        nome = self.entries["Nome"].get().strip()
        data_inicio = self.entries["Data Início"].get().strip()
        data_fim = self.entries["Data Fim"].get().strip()
        grupo_risco = self.entries["Grupo Risco"].get().strip()
        grupo_alvo = self.entries["Grupo-Alvo"].get().strip()
        gravidas = self.entries["Grávidas"].get().strip()
        sexo = self.entries["Sexo"].get().strip()
        recurso = self.entries["Recurso"].get().strip()
        item = self.entries["Item"].get().strip()
        profissionais = self.entries["Profissionais Atribuídos"].get().strip()  # Novo campo
        participantes = self.entries["Número de Participantes"].get().strip()  # Novo campo
        observacoes = self.entries["Observações"].get("1.0", "end").strip()  # Novo campo

        # Validação: verifica se todos os campos obrigatórios estão preenchidos
        if not all([nome, data_inicio, data_fim, grupo_risco, grupo_alvo, gravidas, sexo, recurso, item]):
            messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos!")
            return

        # Adiciona a nova campanha
        nova_campanha = {
            "Nome": nome,
            "Início": data_inicio,
            "Fim": data_fim,
            "Grupo-Alvo": grupo_alvo,
            "Estado": "Ativa",
            "Grupo Risco": grupo_risco,
            "Grávidas": gravidas,
            "Sexo": sexo,
            "Recurso": recurso,
            "Item": item,
            "Profissionais Atribuídos": profissionais,  # Novo campo
            "Número de Participantes": participantes,  # Novo campo
            "Observações": observacoes  # Novo campo
        }
        self.campanhas.append(nova_campanha)
        self.atualizar_tabela(self.campanhas)

        # Fecha a janela e exibe mensagem de sucesso
        messagebox.showinfo("Sucesso", "Dados guardados com sucesso!")
        self.entries["Nome"].winfo_toplevel().destroy()

    def abrir_detalhes_campanha(self, event):
        """Abre uma janela para visualizar e editar os detalhes da campanha selecionada."""
        # Obtém o item selecionado na tabela
        item_id = self.tabela.focus()
        if not item_id:
            messagebox.showerror("Erro", "Nenhuma campanha selecionada!")
            return

        valores = self.tabela.item(item_id, "values")
        if not valores:
            messagebox.showerror("Erro", "Nenhuma campanha selecionada!")
            return

        # Encontra a campanha correspondente na lista
        campanha = next((c for c in self.campanhas if c["Nome"] == valores[0]), None)
        if not campanha:
            messagebox.showerror("Erro", "Campanha não encontrada!")
            return

        # Cria a janela de detalhes
        janela = tk.Toplevel(self)
        janela.title("Detalhes da Campanha")
        janela.geometry("750x700")
        janela.configure(bg="#f5f5f5")  # Fundo neutro claro
        janela.transient(self)

        # Cabeçalho da janela
        header = tk.Frame(janela, bg="#2c3e50", height=50)
        header.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(header, text="Detalhes da Campanha", font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=10)

        # Canvas para permitir rolagem
        canvas = tk.Canvas(janela, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno para os widgets
        frame_principal = ttk.Frame(canvas, style="Custom.TFrame", padding=20)
        canvas.create_window((0, 0), window=frame_principal, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_principal.bind("<Configure>", atualizar_scrollregion)

        # Define estilos para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")
        style.configure("Custom.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Custom.TEntry", padding=5, font=("Segoe UI", 11))
        style.configure("Custom.TCombobox", padding=5, font=("Segoe UI", 11))

        # Título com estilo maior e destacado
        ttk.Label(frame_principal, text="Informações da Campanha", style="Custom.TLabel", font=("Segoe UI", 14, "bold")).pack(pady=20)

        # Separador para os campos principais
        ttk.Label(frame_principal, text="Informações Básicas", style="Custom.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=10)

        # Campos do formulário
        campos = [
            ("Nome", "entry"),
            ("Data Início", "date"),
            ("Data Fim", "date"),
            ("Grupo Risco", "combobox"),
            ("Grupo-Alvo", "combobox"),
            ("Sexo", "combobox"),
            ("Grávidas", "combobox"),
            ("Recurso", "combobox"),
            ("Item", "combobox"),
            ("Profissionais Atribuídos", "entry"),
            ("Número de Participantes", "entry"),
            ("Observações", "text")
        ]

        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_principal, style="Custom.TFrame")
            frame.pack(fill="x", padx=20, pady=8)
            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)

            if tipo == "entry":
                entry = ttk.Entry(frame, style="Custom.TEntry")
                entry.insert(0, campanha.get(campo, ""))
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="yyyy-mm-dd", width=12, background="#2c3e50",
                                foreground="white", borderwidth=2, style="Custom.TCombobox")
                if campo in campanha:
                    entry.set_date(campanha[campo])
            elif tipo == "combobox":
                if campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly", style="Custom.TCombobox")
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino", "Ambos"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grávidas":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox")
                elif campo == "Recurso":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox")
                    entry.bind("<<ComboboxSelected>>", self.atualizar_itens)
                elif campo == "Item":
                    entry = ttk.Combobox(frame, values=self.dataset.get(campanha.get("Recurso", ""), []), state="readonly", style="Custom.TCombobox")
                entry.set(campanha.get(campo, ""))
            elif tipo == "text":
                entry = tk.Text(frame, height=5, wrap="word", bg="white", font=("Segoe UI", 11), relief="solid", borderwidth=1)
                entry.insert("1.0", campanha.get(campo, ""))

            entry.pack(fill="x")
            self.entries[campo] = entry

        # Botões com estilo azul e espaçamento ajustado
        botoes_frame = ttk.Frame(frame_principal, style="Custom.TFrame", padding=20)
        botoes_frame.pack(fill="x", pady=20)

        ttk.Button(botoes_frame, text="Guardar", command=lambda: self.guardar_alteracoes_campanha(campanha, janela), style="App.TButton").pack(side="left", padx=10)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy, style="App.TButton").pack(side="right", padx=10)

    def guardar_alteracoes_campanha(self, campanha, janela):
        """Salva as alterações feitas na campanha."""
        for campo, entry in self.entries.items():
            if isinstance(entry, tk.Text):  # Para campos de texto
                campanha[campo] = entry.get("1.0", "end").strip()
            else:
                campanha[campo] = entry.get().strip()

        # Verifica o estado da campanha com base na data de fim
        data_fim = campanha.get("Fim")
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d")
                if data_fim_obj < datetime.now():
                    campanha["Estado"] = "Encerrada"
                else:
                    campanha["Estado"] = "Ativa"
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido para o campo 'Fim'.")
                return

        # Atualiza a tabela com os novos dados
        self.atualizar_tabela(self.campanhas)

        # Fecha a janela e exibe mensagem de sucesso
        messagebox.showinfo("Sucesso", "Alterações guardadas com sucesso!")
        janela.destroy()

    def eliminar_campanha(self):
        """Elimina a campanha selecionada na tabela."""
        # Obtém o item selecionado na tabela
        item_id = self.tabela.focus()
        if not item_id:
            messagebox.showerror("Erro", "Nenhuma campanha selecionada!")
            return

        # Obtém os valores da campanha selecionada
        valores = self.tabela.item(item_id, "values")
        if not valores:
            messagebox.showerror("Erro", "Nenhuma campanha selecionada!")
            return

        # Confirmação de exclusão
        resposta = messagebox.askyesno("Confirmar", f"Tem certeza de que deseja eliminar a campanha '{valores[0]}'?")
        if resposta:
            # Remove a campanha da lista
            self.campanhas = [c for c in self.campanhas if c["Nome"] != valores[0]]

            # Atualiza a tabela
            self.atualizar_tabela(self.campanhas)

            # Mensagem de sucesso
            messagebox.showinfo("Sucesso", "Campanha eliminada com sucesso!")

class RecursosFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=20, style="Custom.TFrame")  # Fundo neutro claro

        # Título com estilo personalizado
        ttk.Label(self, text="Gestão de Recursos", style="Custom.TLabel").pack(pady=(0, 10))

        # Filtros e Ações
        botoes_frame = ttk.Frame(self, style="Custom.TFrame")
        botoes_frame.pack(fill="x", pady=10)

        # Define o estilo personalizado para os botões com a mesma cor do fundo da aplicação
        style = ttk.Style()
        style.configure(
            "App.TButton",
            background="#2c3e50",  # Azul escuro (mesma cor do fundo da aplicação)
            foreground="white",    # Texto branco
            font=("Segoe UI", 11),
            padding=6
        )
        style.map(
            "App.TButton",
            background=[("active", "#1a252f")],  # Azul mais escuro ao passar o mouse
            foreground=[("active", "white")]
        )

        # Botões com o novo estilo
        ttk.Button(botoes_frame, text="+ Novo Recurso", command=self.novo_medicamento, style="App.TButton").pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="Filtrar", command=self.filtrar_recursos, style="App.TButton").pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="Exportar", command=self.exportar_dados, style="App.TButton").pack(side="left", padx=5)

        # Frame para a tabela e scrollbars
        tabela_frame = ttk.Frame(self)
        tabela_frame.pack(fill="both", expand=True, pady=10)

        # Tabela de recursos
        colunas = ("Tipo", "Nome", "Grupo-Alvo", "Grupo Risco", "Gravidez", "Data de Validade", "Quantidade em Stock", "Campanha", "Estado")
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=15, style="Custom.Treeview")
        
        # Ajusta o tamanho das colunas
        self.tabela.column("Tipo", width=100, anchor="center")
        self.tabela.column("Nome", width=150, anchor="center")
        self.tabela.column("Grupo-Alvo", width=150, anchor="center")
        self.tabela.column("Grupo Risco", width=100, anchor="center")
        self.tabela.column("Gravidez", width=100, anchor="center")
        self.tabela.column("Data de Validade", width=120, anchor="center")
        self.tabela.column("Quantidade em Stock", width=150, anchor="center")
        self.tabela.column("Campanha", width=200, anchor="center")
        self.tabela.column("Estado", width=100, anchor="center")
        
        # Configura os cabeçalhos
        for col in colunas:
            self.tabela.heading(col, text=col, anchor="center")
            
        # Empacota a tabela antes da barra de rolagem horizontal
        self.tabela.pack(fill="both", expand=True)

        # Adiciona o evento de clique na tabela
        self.tabela.bind("<Double-1>", self.abrir_detalhes_recurso)

        # Barra de rolagem horizontal
        scrollbar_horizontal = ttk.Scrollbar(tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        self.tabela.configure(xscrollcommand=scrollbar_horizontal.set)

        # Dados iniciais (exemplo)
        self.dados = [
            {"Tipo": "Medicamento", "Nome": "Paracetamol", "Grupo-Alvo": "Adultos", "Grupo Risco": "Baixo",
             "Gravidez": "Sim", "Data de Validade": "2025-12-31", "Quantidade em Stock": "100", "Campanha": "Campanha de Vacinação Gripe", "Estado": "Disponível"},
            {"Tipo": "Vacina", "Nome": "Vacina Gripe", "Grupo-Alvo": "Idosos", "Grupo Risco": "Médio",
             "Gravidez": "Não", "Data de Validade": "2025-10-15", "Quantidade em Stock": "50", "Campanha": "Campanha de Vacinação Gripe", "Estado": "Disponível"}
        ]

        # Preenche a tabela com os dados iniciais
        self.atualizar_tabela(self.dados)

    def atualizar_tabela(self, dados):
        """Atualiza a tabela com os dados fornecidos."""
        # Limpa a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Insere os novos dados
        for recurso in dados:
            self.tabela.insert('', 'end', values=(
                recurso["Tipo"],
                recurso["Nome"],
                recurso["Grupo-Alvo"],
                recurso["Grupo Risco"],
                recurso["Gravidez"],
                recurso["Data de Validade"],
                recurso["Quantidade em Stock"],
                recurso.get("Campanha", "Sem campanha"),
                recurso.get("Estado", "Fora de stock")
            ))

    def novo_medicamento(self):
        """Abre uma janela para adicionar um novo medicamento ou vacina."""
        janela = tk.Toplevel(self)
        janela.title("Novo Medicamento/Vacina")
        janela.geometry("700x500")
        janela.configure(bg="#f5f5f5")  # Fundo neutro claro
        janela.transient(self)

        # Cabeçalho da janela
        header = tk.Frame(janela, bg="#2c3e50", height=50)
        header.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(header, text="Novo Medicamento/Vacina", font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=10)

        # Canvas para permitir rolagem
        canvas = tk.Canvas(janela, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno para os widgets
        frame_campos = ttk.Frame(canvas, style="Custom.TFrame")
        canvas.create_window((0, 0), window=frame_campos, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_campos.bind("<Configure>", atualizar_scrollregion)

        # Obtém os nomes das campanhas do dataset da aba "Campanhas"
        def obter_campanhas_disponiveis():
            try:
                campanhas_frame = self.master.frames["Campanhas"]
                return [campanha["Nome"] for campanha in campanhas_frame.campanhas]
            except (AttributeError, KeyError):
                return []

        campanhas_disponiveis = obter_campanhas_disponiveis()

        # Campos do formulário
        campos = [
            ("Campanha", "combobox"),
            ("Tipo", "combobox"),
            ("Nome", "entry"),
            ("Descrição", "text"),
            ("Composição/Substância ativa", "entry"),
            ("Dose Recomendada", "entry"),
            ("Via de Administração", "combobox"),
            ("Grupo-Alvo", "combobox"),
            ("Gravidez Permitida?", "checkbox"),
            ("Sexo", "combobox"),
            ("Grupo Risco", "combobox"),
            ("Efeitos Secundários Comuns", "entry"),
            ("Data de Validade", "date"),
            ("Quantidade em Stock", "entry"),
            ("Estado", "combobox")
        ]

        self.entries = {}

        # Define estilos para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")
        style.configure("Custom.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Custom.TEntry", padding=5, font=("Segoe UI", 11))
        style.configure("Custom.TCombobox", padding=5, font=("Segoe UI", 11))

        for campo, tipo in campos:
            frame = ttk.Frame(frame_campos, style="Custom.TFrame")
            frame.pack(fill="x", pady=5, padx=20)

            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)

            if tipo == "entry":
                entry = ttk.Entry(frame, style="Custom.TEntry")
            elif tipo == "combobox":
                if campo == "Campanha":
                    entry = ttk.Combobox(frame, values=campanhas_disponiveis, state="readonly", style="Custom.TCombobox")
                elif campo == "Tipo":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox")
                elif campo == "Via de Administração":
                    entry = ttk.Combobox(frame, values=["Oral", "Injetável", "Nasal", "Tópico"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly", style="Custom.TCombobox")
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox")
                elif campo == "Estado":
                    entry = ttk.Combobox(frame, values=["Disponível", "Fora de stock", "Expirado"], state="readonly", style="Custom.TCombobox")
            elif tipo == "checkbox":
                entry = tk.BooleanVar()
                ttk.Checkbutton(frame, variable=entry, text="Sim", style="Custom.TCheckbutton").pack(anchor="w")
                self.entries[campo] = entry
                continue
            elif tipo == "text":
                entry = tk.Text(frame, height=4, wrap="word", font=("Segoe UI", 11), bg="white", relief="solid", borderwidth=1)
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="dd/mm/yyyy", width=12, background="#2c3e50",
                                foreground="white", borderwidth=2, style="Custom.TCombobox")

            entry.pack(fill="x")
            self.entries[campo] = entry

        # Botões de ação
        botoes_frame = ttk.Frame(frame_campos, style="Custom.TFrame", padding=20)
        botoes_frame.pack(fill="x", pady=10)

        ttk.Button(botoes_frame, text="Guardar", command=self.guardar_medicamento, style="App.TButton").pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy, style="App.TButton").pack(side="right", padx=5)

        # Atualiza o combobox de campanhas dinamicamente
        self.atualizar_campanhas_disponiveis()

    def atualizar_campanhas_disponiveis(self):
        """Atualiza as opções do combobox de campanhas."""
        try:
            campanhas_frame = self.master.frames["Campanhas"]
            campanhas_disponiveis = [campanha["Nome"] for campanha in campanhas_frame.campanhas]
            if hasattr(self, "campanha_combobox"):  # Verifica se o atributo existe
                self.campanha_combobox["values"] = campanhas_disponiveis
        except (AttributeError, KeyError):
            if hasattr(self, "campanha_combobox"):  # Verifica se o atributo existe
                self.campanha_combobox["values"] = []

    def guardar_medicamento(self):
        """Guarda os dados do novo medicamento ou vacina e atualiza a tabela."""
        dados = {}
        for campo, entry in self.entries.items():
            if isinstance(entry, tk.Text):
                dados[campo] = entry.get("1.0", "end").strip()
            elif isinstance(entry, tk.BooleanVar):
                dados[campo] = "Sim" if entry.get() else "Não"
            else:
                dados[campo] = entry.get().strip()

        # Validação básica
        if not dados["Nome"] or not dados["Tipo"]:
            messagebox.showerror("Erro", "Os campos 'Nome' e 'Tipo' são obrigatórios!")
            return

        # Define o estado com base na quantidade em stock
        try:
            quantidade = int(dados.get("Quantidade em Stock", "0"))
            estado = "Disponível" if quantidade > 1 else "Fora de stock"
        except ValueError:
            estado = "Fora de stock"

        # Adiciona os dados à tabela
        novo_recurso = {
            "Tipo": dados.get("Tipo", ""),
            "Nome": dados.get("Nome", ""),
            "Grupo-Alvo": dados.get("Grupo-Alvo", ""),
            "Grupo Risco": dados.get("Grupo Risco", ""),
            "Gravidez": dados.get("Gravidez Permitida?", ""),
            "Data de Validade": dados.get("Data de Validade", ""),
            "Quantidade em Stock": dados.get("Quantidade em Stock", "0"),
            "Campanha": dados.get("Campanha", ""),
            "Estado": estado
        }
        self.dados.append(novo_recurso)  # Adiciona aos dados existentes
        self.atualizar_tabela(self.dados)  # Atualiza a tabela com os novos dados

        # Fecha a janela e exibe mensagem de sucesso
        messagebox.showinfo("Sucesso", "Medicamento/Vacina guardado com sucesso!")
        self.entries["Nome"].winfo_toplevel().destroy()

    def filtrar_recursos(self):
        """Abre uma janela para filtrar os recursos."""
        janela = tk.Toplevel(self)
        janela.title("Filtrar Recursos")
        janela.geometry("400x400")
        janela.configure(bg="#f5f5f5")  # Fundo neutro claro
        janela.transient(self)
        janela.resizable(False, False)

        # Cabeçalho da janela
        header = tk.Frame(janela, bg="#2c3e50", height=50)
        header.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(header, text="Filtrar Recursos", font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=10)

        # Canvas para permitir rolagem
        canvas = tk.Canvas(janela, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame principal para os filtros
        frame_principal = ttk.Frame(canvas, style="Custom.TFrame", padding=20)
        canvas.create_window((0, 0), window=frame_principal, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_principal.bind("<Configure>", atualizar_scrollregion)

        # Define estilos para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")
        style.configure("Custom.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Custom.TCombobox", padding=5, font=("Segoe UI", 11))

        # Campos de filtro
        filtros = [
            ("Tipo", ["Medicamento", "Vacina"]),
            ("Grupo-Alvo", [
                "Bebês (0-3 anos)", "Crianças (4-12 anos)", "Jovens (12-18 anos)",
                "Adultos (18-65 anos)", "Idosos (+65 anos)"
            ]),
            ("Estado", ["Disponível", "Fora de stock", "Expirado"]),
            ("Campanha", [campanha["Nome"] for campanha in self.master.frames["Campanhas"].campanhas])
        ]

        self.filtros_selecionados = {}

        for campo, opcoes in filtros:
            frame = ttk.Frame(frame_principal, style="Custom.TFrame")
            frame.pack(fill="x", pady=10)

            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)
            combobox = ttk.Combobox(frame, values=["Todos"] + opcoes, state="readonly", style="Custom.TCombobox")
            combobox.current(0)  # Define "Todos" como padrão
            combobox.pack(fill="x")
            self.filtros_selecionados[campo] = combobox

        # Botões de ação
        botoes_frame = ttk.Frame(frame_principal, style="Custom.TFrame", padding=20)
        botoes_frame.pack(fill="x", pady=10)

        # Frame para os botões com layout horizontal
        botoes_inner_frame = ttk.Frame(botoes_frame, style="Custom.TFrame")
        botoes_inner_frame.pack(expand=True)

        ttk.Button(botoes_inner_frame, text="Aplicar", command=lambda: self.aplicar_filtro(janela), style="App.TButton").pack(side="left", padx=5)
        ttk.Button(botoes_inner_frame, text="Cancelar", command=janela.destroy, style="App.TButton").pack(side="left", padx=5)

    def aplicar_filtro(self, janela):
        """Aplica os filtros selecionados e atualiza a tabela."""
        filtros = {campo: combobox.get() for campo, combobox in self.filtros_selecionados.items()}

        # Filtra os dados com base nos critérios selecionados
        dados_filtrados = self.dados
        for campo, valor in filtros.items():
            if valor != "Todos":
                if campo == "Tipo":
                    dados_filtrados = [d for d in dados_filtrados if d["Tipo"] == valor]
                elif campo == "Grupo-Alvo":
                    dados_filtrados = [d for d in dados_filtrados if d["Grupo-Alvo"] == valor]
                elif campo == "Estado":
                    dados_filtrados = [d for d in dados_filtrados if d["Estado"] == valor]
                elif campo == "Campanha":
                    dados_filtrados = [d for d in dados_filtrados if d["Campanha"] == valor]

        # Atualiza a tabela com os dados filtrados
        self.atualizar_tabela(dados_filtrados)

        # Fecha a janela de filtro
        janela.destroy()

    def exportar_dados(self):
        """Exporta todos os dados (tabela e outros) para um arquivo TXT."""
        # Abre uma janela para selecionar o local e o nome do arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Salvar arquivo como"
        )

        if not file_path:
            return  # Se o usuário cancelar, não faz nada

        try:
            # Abre o arquivo para escrita
            with open(file_path, mode="w", encoding="utf-8") as file:
                # Escreve o cabeçalho
                file.write("Dados da Tabela de Recursos\n")
                file.write("=" * 50 + "\n")

                # Escreve os dados da tabela
                for recurso in self.dados:
                    file.write(f"Tipo: {recurso['Tipo']}\n")
                    file.write(f"Nome: {recurso['Nome']}\n")
                    file.write(f"Grupo-Alvo: {recurso['Grupo-Alvo']}\n")
                    file.write(f"Grupo Risco: {recurso['Grupo Risco']}\n")
                    file.write(f"Gravidez: {recurso['Gravidez']}\n")
                    file.write(f"Data de Validade: {recurso['Data de Validade']}\n")
                    file.write(f"Quantidade em Stock: {recurso['Quantidade em Stock']}\n")
                    file.write(f"Campanha: {recurso['Campanha']}\n")
                    file.write("-" * 50 + "\n")

                # Adiciona outros dados (se houver)
                file.write("\nOutros Dados\n")
                file.write("=" * 50 + "\n")
                file.write("Exemplo de outro dado 1\n")
                file.write("Exemplo de outro dado 2\n")

            # Exibe mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {file_path}!")
        except Exception as e:
            # Exibe mensagem de erro em caso de falha
            messagebox.showerror("Erro", f"Erro ao exportar os dados: {e}")

    def obter_campanhas_disponiveis(self):
        """Obtém a lista de campanhas disponíveis do frame de campanhas."""
        try:
            # Tenta obter o frame de campanhas através do notebook
            campanhas_frame = self.master.frames["Campanhas"]
            return [campanha["Nome"] for campanha in campanhas_frame.campanhas]
        except (AttributeError, KeyError):
            return []

    def abrir_detalhes_recurso(self, event):
        """Abre uma janela com os detalhes do recurso selecionado."""
        # Obtém o item selecionado na tabela
        item_id = self.tabela.focus()
        if not item_id:
            return

        # Obtém os valores da linha selecionada
        valores = self.tabela.item(item_id, "values")
        if not valores:
            return

        print("Valores da tabela:", valores)  # Debug

        # Converte a data do formato yyyy-mm-dd para dd/mm/yyyy
        data_validade = valores[5]
        if data_validade:
            try:
                from datetime import datetime
                data_obj = datetime.strptime(data_validade, "%Y-%m-%d")
                data_validade = data_obj.strftime("%d/%m/%Y")
            except ValueError:
                data_validade = ""

        # Cria um dicionário com os valores da tabela
        recurso = {
            "Tipo": valores[0],
            "Nome": valores[1],
            "Grupo-Alvo": valores[2],
            "Grupo Risco": valores[3],
            "Gravidez": valores[4],
            "Data de Validade": data_validade,
            "Quantidade em Stock": valores[6],
            "Campanha": valores[7] if len(valores) > 7 else "Sem campanha",
            "Descrição": "",
            "Composição/Substância ativa": "",
            "Dose Recomendada": "",
            "Via de Administração": "",
            "Sexo": "",
            "Efeitos Secundários Comuns": "",
            "Estado": "Disponível"
        }

        print("Recurso criado:", recurso)  # Debug

        # Cria a janela de detalhes
        janela = tk.Toplevel(self)
        janela.title("Detalhes do Recurso")
        janela.geometry("750x700")
        janela.configure(bg="#f5f5f5")
        janela.transient(self)

        # Cabeçalho da janela
        header = tk.Frame(janela, bg="#2c3e50", height=50)
        header.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(header, text="Detalhes do Recurso", font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=10)

        # Canvas para permitir rolagem
        canvas = tk.Canvas(janela, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno para os widgets
        frame_principal = ttk.Frame(canvas, style="Custom.TFrame", padding=20)
        canvas.create_window((0, 0), window=frame_principal, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_principal.bind("<Configure>", atualizar_scrollregion)

        # Define estilos para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")
        style.configure("Custom.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Custom.TEntry", padding=5, font=("Segoe UI", 11))
        style.configure("Custom.TCombobox", padding=5, font=("Segoe UI", 11))

        # Título com estilo maior e destacado
        ttk.Label(frame_principal, text="Informações do Recurso", style="Custom.TLabel", font=("Segoe UI", 14, "bold")).pack(pady=20)

        # Separador para os campos principais
        ttk.Label(frame_principal, text="Informações Básicas", style="Custom.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=10)

        # Obtém as campanhas disponíveis e adiciona "Sem campanha"
        campanhas_disponiveis = self.obter_campanhas_disponiveis()
        campanhas_disponiveis = ["Sem campanha"] + campanhas_disponiveis

        # Campos do formulário
        campos = [
            ("Tipo", "combobox"),
            ("Nome", "entry"),
            ("Descrição", "text"),
            ("Composição/Substância ativa", "entry"),
            ("Dose Recomendada", "entry"),
            ("Via de Administração", "combobox"),
            ("Grupo-Alvo", "combobox"),
            ("Gravidez Permitida?", "checkbox"),
            ("Sexo", "combobox"),
            ("Grupo Risco", "combobox"),
            ("Efeitos Secundários Comuns", "entry"),
            ("Data de Validade", "date"),
            ("Quantidade em Stock", "entry"),
            ("Estado", "combobox"),
            ("Campanha", "combobox")
        ]

        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_principal, style="Custom.TFrame")
            frame.pack(fill="x", padx=20, pady=8)
            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)

            valor = recurso.get(campo, "")
            if campo == "Gravidez Permitida?":
                valor = recurso.get("Gravidez", "")

            print(f"Campo: {campo}, Valor: {valor}")  # Debug

            if tipo == "entry":
                entry = ttk.Entry(frame, style="Custom.TEntry")
                entry.insert(0, valor)
            elif tipo == "combobox":
                if campo == "Campanha":
                    entry = ttk.Combobox(frame, values=campanhas_disponiveis, state="readonly", style="Custom.TCombobox")
                    entry.set(valor)
                elif campo == "Tipo":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox")
                    entry.set(valor)
                elif campo == "Via de Administração":
                    entry = ttk.Combobox(frame, values=["Oral", "Injetável", "Nasal", "Tópico"], state="readonly", style="Custom.TCombobox")
                    entry.set(valor)
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly", style="Custom.TCombobox")
                    entry.set(valor)
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly", style="Custom.TCombobox")
                    entry.set(valor)
                elif campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox")
                    entry.set(valor)
                elif campo == "Estado":
                    entry = ttk.Combobox(frame, values=["Disponível", "Fora de stock", "Expirado"], state="readonly", style="Custom.TCombobox")
                    entry.set(valor)
            elif tipo == "checkbox":
                entry = tk.BooleanVar()
                entry.set(valor == "Sim")
                ttk.Checkbutton(frame, variable=entry, text="Sim", style="Custom.TCheckbutton").pack(anchor="w")
                self.entries[campo] = entry
                continue
            elif tipo == "text":
                entry = tk.Text(frame, height=4, wrap="word", font=("Segoe UI", 11), bg="white", relief="solid", borderwidth=1)
                entry.insert("1.0", valor)
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="dd/mm/yyyy", width=12, background="#2c3e50",
                                foreground="white", borderwidth=2, style="Custom.TCombobox")
                if valor:
                    try:
                        entry.set_date(valor)
                    except ValueError:
                        pass  # Ignora erros de data inválida

            entry.pack(fill="x")
            self.entries[campo] = entry

        # Botões com estilo azul e espaçamento ajustado
        botoes_frame = ttk.Frame(frame_principal, style="Custom.TFrame", padding=20)
        botoes_frame.pack(fill="x", pady=20)

        ttk.Button(botoes_frame, text="Guardar", command=lambda: self.guardar_alteracoes_recurso(recurso, janela), style="App.TButton").pack(side="left", padx=10)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy, style="App.TButton").pack(side="right", padx=10)

    def guardar_alteracoes_recurso(self, recurso, janela):
        """Guarda as alterações feitas no recurso."""
        # Atualiza os valores do recurso com os novos dados
        for campo, entry in self.entries.items():
            if isinstance(entry, tk.Text):
                recurso[campo] = entry.get("1.0", "end").strip()
            elif isinstance(entry, tk.BooleanVar):
                recurso["Gravidez"] = "Sim" if entry.get() else "Não"
            else:
                valor = entry.get().strip()
                if campo == "Data de Validade":
                    try:
                        from datetime import datetime
                        data_obj = datetime.strptime(valor, "%d/%m/%Y")
                        valor = data_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        pass
                recurso[campo] = valor

        # Define o estado com base na quantidade em stock
        try:
            quantidade = int(recurso.get("Quantidade em Stock", "0"))
            recurso["Estado"] = "Disponível" if quantidade > 1 else "Fora de stock"
        except ValueError:
            recurso["Estado"] = "Fora de stock"

        # Atualiza o recurso na lista de dados
        for i, r in enumerate(self.dados):
            if r["Nome"] == recurso["Nome"]:
                self.dados[i] = recurso
                break

        # Atualiza a tabela
        self.atualizar_tabela(self.dados)

        messagebox.showinfo("Sucesso", "Alterações guardadas com sucesso!")
        janela.destroy()

    def atualizar_tabela(self, dados):
        """Atualiza a tabela com os dados fornecidos."""
        # Limpa a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Insere os novos dados
        for recurso in dados:
            self.tabela.insert('', 'end', values=(
                recurso["Tipo"],
                recurso["Nome"],
                recurso["Grupo-Alvo"],
                recurso["Grupo Risco"],
                recurso["Gravidez"],
                recurso["Data de Validade"],
                recurso["Quantidade em Stock"],
                recurso.get("Campanha", "Sem campanha"),
                recurso.get("Estado", "Fora de stock")
            ))

class RelatoriosFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=20, style="Custom.TFrame")  # Fundo neutro claro

        # Define o estilo personalizado para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")  # Fundo neutro claro
        style.configure("Custom.TButton", background="#f5f5f5", font=("Segoe UI", 11))
        style.configure("Custom.Treeview", background="#f5f5f5", fieldbackground="#f5f5f5", font=("Segoe UI", 10))
        style.configure("Custom.Treeview.Heading", background="#2c3e50", foreground="white", font=("Segoe UI", 11, "bold"))
        style.configure("Custom.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Blue.TButton", background="#2c3e50", foreground="white", font=("Segoe UI", 11), padding=6)
        style.map("Blue.TButton",
                  background=[("active", "#1a252f")],  # Azul mais escuro ao passar o mouse
                  foreground=[("active", "white")])
        style.configure("Large.TLabel", font=("Segoe UI", 18, "bold"), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Small.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Section.TLabel", font=("Segoe UI", 14, "bold"), background="#f5f5f5", foreground="#2c3e50")

        # Título com estilo personalizado
        ttk.Label(self, text="Relatórios", style="Custom.TLabel").pack(pady=(0, 10))

        # Frame para filtros e seleção de relatório
        filtros_frame = ttk.Frame(self, style="Custom.TFrame")
        filtros_frame.pack(fill="x", pady=10)

        # Label "Selecione o Relatório" com cor azul
        ttk.Label(
            filtros_frame,
            text="Selecione o Relatório:",
            font=("Segoe UI", 11),
            foreground="#2c3e50",  # Azul escuro
            background="#f5f5f5"   # Fundo neutro claro
        ).pack(side="left")

        # Combobox com o estilo atualizado
        self.combo_relatorios = ttk.Combobox(
            filtros_frame,
            values=["Pacientes", "Consultas", "Recursos", "Campanhas"],
            state="readonly",
            style="Custom.TCombobox"
        )
        self.combo_relatorios.current(0)
        self.combo_relatorios.pack(side="left", padx=5)
        self.combo_relatorios.bind("<<ComboboxSelected>>", self.alternar_relatorio)

        # Botão para gerar relatório
        ttk.Button(filtros_frame, text="Gerar Relatório", command=self.gerar_relatorio, style="Blue.TButton").pack(side="right", padx=5)

        # Frame para o conteúdo do relatório
        self.conteudo_frame = ttk.Frame(self, style="Custom.TFrame")
        self.conteudo_frame.pack(fill="both", expand=True, pady=10)

        # Inicializa com o relatório de pacientes
        self._mostrar_relatorio_pacientes()

    def alternar_relatorio(self, event):
        """Atualiza o conteúdo com base no relatório selecionado."""
        # Limpa o frame de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

        # Obtém o relatório selecionado
        relatorio = self.combo_relatorios.get()

        if relatorio == "Pacientes":
            self._mostrar_relatorio_pacientes()
        elif relatorio == "Consultas":
            self._mostrar_relatorio_consultas()
        elif relatorio == "Recursos":
            self._mostrar_relatorio_recursos()
        elif relatorio == "Campanhas":
            self._mostrar_relatorio_campanhas()

    def _mostrar_relatorio_pacientes(self):
        """Exibe o layout do relatório de pacientes."""
        # Frame para filtros (esquerda)
        filtros_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        filtros_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(filtros_frame, text="Filtros", style="Section.TLabel").pack(pady=10)

        # Filtros disponíveis
        filtros = [
            ("Grupo de Idade", ["Todas as Faixas", "Bebês (0-3 anos)", "Crianças (4-12 anos)", "Jovens (12-18 anos)", "Adultos (18-65 anos)", "Idosos (+65 anos)"]),
            ("Gênero", ["Ambos", "Masculino", "Feminino"]),
            ("Risco de Saúde", ["Todos", "Baixo", "Médio", "Alto"])
        ]

        self.filtros_selecionados = {}

        for campo, opcoes in filtros:
            frame = ttk.Frame(filtros_frame, style="Custom.TFrame")
            frame.pack(fill="x", pady=5)

            ttk.Label(frame, text=campo, style="Small.TLabel").pack(anchor="w")
            combobox = ttk.Combobox(frame, values=opcoes, state="readonly", style="Custom.TCombobox")
            combobox.current(0)
            combobox.pack(fill="x")
            self.filtros_selecionados[campo] = combobox

        # Frame para o gráfico (direita)
        grafico_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(grafico_frame, text="Pacientes por Risco de Saúde", style="Section.TLabel").pack(pady=10)

        # Dados fictícios para o gráfico
        categorias = ["Baixo", "Médio", "Alto"]
        valores = [200, 150, 50]

        # Criação do gráfico usando matplotlib com estilo moderno
        figura, ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        # Define cores modernas e consistentes
        cores = ['#3498db', '#2ecc71', '#e74c3c']
        
        # Cria o gráfico de barras com estilo moderno
        bars = ax.bar(categorias, valores, color=cores, width=0.6, edgecolor='none')
        
        # Remove as bordas do gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#bdc3c7')
        
        # Adiciona grade horizontal sutil
        ax.grid(axis='y', linestyle='--', alpha=0.3, color='#bdc3c7')
        
        # Remove os ticks do eixo y
        ax.tick_params(axis='y', which='both', left=False)
        
        # Adiciona os valores acima das barras com estilo moderno
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, color='#2c3e50')
        
        # Configura o título e labels
        ax.set_xlabel('Risco de Saúde', fontsize=12, color='#2c3e50', labelpad=10)
        ax.set_ylabel('Número de Pacientes', fontsize=12, color='#2c3e50', labelpad=10)
        
        # Ajusta o layout
        plt.tight_layout()

        # Adiciona o gráfico ao frame
        canvas = FigureCanvasTkAgg(figura, grafico_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def _mostrar_relatorio_consultas(self):
        """Exibe o layout do relatório de consultas."""
        # Frame para filtros (esquerda)
        filtros_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        filtros_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(filtros_frame, text="Filtros", style="Section.TLabel").pack(pady=10)

        # Filtros disponíveis
        filtros = [
            ("Período", ["Último mês", "Últimos 3 meses", "Último ano", "Personalizado"]),
            ("Tipo de Consulta", ["Todas", "Geral", "Especializada", "Emergência"]),
            ("Status", ["Todas", "Agendada", "Realizada", "Cancelada"])
        ]

        self.filtros_selecionados = {}

        for campo, opcoes in filtros:
            frame = ttk.Frame(filtros_frame, style="Custom.TFrame")
            frame.pack(fill="x", pady=5)

            ttk.Label(frame, text=campo, style="Small.TLabel").pack(anchor="w")
            combobox = ttk.Combobox(frame, values=opcoes, state="readonly", style="Custom.TCombobox")
            combobox.current(0)
            combobox.pack(fill="x")
            self.filtros_selecionados[campo] = combobox

        # Frame para o gráfico (direita)
        grafico_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(grafico_frame, text="Consultas por Mês", style="Section.TLabel").pack(pady=10)

        # Dados fictícios para o gráfico
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        consultas = [120, 150, 180, 160, 200, 190]

        # Criação do gráfico de linha com estilo moderno
        figura, ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        # Define cores e estilo moderno
        cor_principal = '#3498db'
        
        # Cria o gráfico de linha com estilo moderno
        ax.plot(meses, consultas, marker='o', color=cor_principal, linewidth=2.5,
                markersize=8, markerfacecolor='white', markeredgecolor=cor_principal,
                markeredgewidth=2)
        
        # Remove as bordas do gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#bdc3c7')
        
        # Adiciona grade horizontal sutil
        ax.grid(axis='y', linestyle='--', alpha=0.3, color='#bdc3c7')
        
        # Remove os ticks do eixo y
        ax.tick_params(axis='y', which='both', left=False)
        
        # Adiciona os valores acima dos pontos
        for i, valor in enumerate(consultas):
            ax.text(i, valor + 5, f'{valor}', ha='center', va='bottom',
                   fontsize=10, color='#2c3e50')
        
        # Configura o título e labels
        ax.set_xlabel('Mês', fontsize=12, color='#2c3e50', labelpad=10)
        ax.set_ylabel('Número de Consultas', fontsize=12, color='#2c3e50', labelpad=10)
        
        # Ajusta o layout
        plt.tight_layout()

        # Adiciona o gráfico ao frame
        canvas = FigureCanvasTkAgg(figura, grafico_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def _mostrar_relatorio_recursos(self):
        """Exibe o layout do relatório de recursos."""
        # Frame para filtros (esquerda)
        filtros_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        filtros_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(filtros_frame, text="Filtros", style="Section.TLabel").pack(pady=10)

        # Filtros disponíveis
        filtros = [
            ("Tipo", ["Todos", "Medicamento", "Vacina"]),
            ("Estado", ["Todos", "Disponível", "Fora de stock", "Expirado"]),
            ("Campanha", ["Todas", "Sem campanha", "Campanha de Vacinação Gripe"])
        ]

        self.filtros_selecionados = {}

        for campo, opcoes in filtros:
            frame = ttk.Frame(filtros_frame, style="Custom.TFrame")
            frame.pack(fill="x", pady=5)

            ttk.Label(frame, text=campo, style="Small.TLabel").pack(anchor="w")
            combobox = ttk.Combobox(frame, values=opcoes, state="readonly", style="Custom.TCombobox")
            combobox.current(0)
            combobox.pack(fill="x")
            self.filtros_selecionados[campo] = combobox

        # Frame para o gráfico (direita)
        grafico_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(grafico_frame, text="Recursos por Estado", style="Section.TLabel").pack(pady=10)

        # Dados fictícios para o gráfico
        estados = ["Disponível", "Fora de stock", "Expirado"]
        quantidades = [150, 30, 20]

        # Criação do gráfico de pizza com estilo moderno
        figura, ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        # Define cores modernas
        cores = ['#2ecc71', '#e74c3c', '#f1c40f']
        
        # Cria o gráfico de pizza com estilo moderno
        wedges, texts, autotexts = ax.pie(quantidades, labels=estados, colors=cores,
                                         autopct='%1.1f%%', startangle=90,
                                         wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
                                         textprops={'color': '#2c3e50', 'fontsize': 10})
        
        # Remove a borda do gráfico
        ax.axis('equal')
        
        # Adiciona título
        ax.set_title('Distribuição de Recursos', fontsize=14, color='#2c3e50', pad=20)
        
        # Ajusta o layout
        plt.tight_layout()

        # Adiciona o gráfico ao frame
        canvas = FigureCanvasTkAgg(figura, grafico_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def _mostrar_relatorio_campanhas(self):
        """Exibe o layout do relatório de campanhas."""
        # Frame para filtros (esquerda)
        filtros_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        filtros_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(filtros_frame, text="Filtros", style="Section.TLabel").pack(pady=10)

        # Filtros disponíveis
        filtros = [
            ("Estado", ["Todas", "Ativa", "Encerrada"]),
            ("Grupo-Alvo", ["Todos", "Bebês", "Crianças", "Jovens", "Adultos", "Idosos"]),
            ("Período", ["Todas", "Último mês", "Últimos 3 meses", "Último ano"])
        ]

        self.filtros_selecionados = {}

        for campo, opcoes in filtros:
            frame = ttk.Frame(filtros_frame, style="Custom.TFrame")
            frame.pack(fill="x", pady=5)

            ttk.Label(frame, text=campo, style="Small.TLabel").pack(anchor="w")
            combobox = ttk.Combobox(frame, values=opcoes, state="readonly", style="Custom.TCombobox")
            combobox.current(0)
            combobox.pack(fill="x")
            self.filtros_selecionados[campo] = combobox

        # Frame para o gráfico (direita)
        grafico_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(grafico_frame, text="Campanhas por Estado", style="Section.TLabel").pack(pady=10)

        # Dados fictícios para o gráfico
        estados = ["Ativa", "Encerrada"]
        quantidades = [5, 3]

        # Criação do gráfico de barras com estilo moderno
        figura, ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        # Define cores modernas
        cores = ['#2ecc71', '#e74c3c']
        
        # Cria o gráfico de barras com estilo moderno
        bars = ax.bar(estados, quantidades, color=cores, width=0.6, edgecolor='none')
        
        # Remove as bordas do gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#bdc3c7')
        
        # Adiciona grade horizontal sutil
        ax.grid(axis='y', linestyle='--', alpha=0.3, color='#bdc3c7')
        
        # Remove os ticks do eixo y
        ax.tick_params(axis='y', which='both', left=False)
        
        # Adiciona os valores acima das barras com estilo moderno
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, color='#2c3e50')
        
        # Configura o título e labels
        ax.set_xlabel('Estado', fontsize=12, color='#2c3e50', labelpad=10)
        ax.set_ylabel('Número de Campanhas', fontsize=12, color='#2c3e50', labelpad=10)
        
        # Ajusta o layout
        plt.tight_layout()

        # Adiciona o gráfico ao frame
        canvas = FigureCanvasTkAgg(figura, grafico_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def gerar_relatorio(self):
        """Gera e exporta um relatório detalhado no formato TXT."""
        relatorio = self.combo_relatorios.get()
        
        # Abre uma janela para selecionar o local de salvamento
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Salvar Relatório"
        )
        
        if not file_path:  # Se o usuário cancelar
            return
            
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                # Cabeçalho do relatório
                file.write("=" * 50 + "\n")
                file.write(f"RELATÓRIO DE {relatorio.upper()}\n")
                file.write("=" * 50 + "\n\n")
                
                # Data e hora da geração
                from datetime import datetime
                file.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                # Filtros aplicados
                file.write("Filtros Aplicados:\n")
                for campo, combobox in self.filtros_selecionados.items():
                    file.write(f"- {campo}: {combobox.get()}\n")
                file.write("\n")
                
                # Conteúdo específico do relatório
                if relatorio == "Pacientes":
                    file.write("Distribuição de Pacientes por Risco de Saúde:\n")
                    file.write("- Baixo: 200 pacientes\n")
                    file.write("- Médio: 150 pacientes\n")
                    file.write("- Alto: 50 pacientes\n\n")
                    file.write("Total de Pacientes: 400\n")
                    
                elif relatorio == "Consultas":
                    file.write("Consultas por Mês (Últimos 6 meses):\n")
                    file.write("- Janeiro: 120 consultas\n")
                    file.write("- Fevereiro: 150 consultas\n")
                    file.write("- Março: 180 consultas\n")
                    file.write("- Abril: 160 consultas\n")
                    file.write("- Maio: 200 consultas\n")
                    file.write("- Junho: 190 consultas\n\n")
                    file.write("Média Mensal: 166.7 consultas\n")
                    file.write("Total de Consultas: 1000\n")
                    
                elif relatorio == "Recursos":
                    file.write("Distribuição de Recursos por Estado:\n")
                    file.write("- Disponíveis: 150 (75.0%)\n")
                    file.write("- Fora de stock: 30 (15.0%)\n")
                    file.write("- Expirados: 20 (10.0%)\n\n")
                    file.write("Total de Recursos: 200\n")
                    
                elif relatorio == "Campanhas":
                    file.write("Distribuição de Campanhas por Estado:\n")
                    file.write("- Ativas: 5 (62.5%)\n")
                    file.write("- Encerradas: 3 (37.5%)\n\n")
                    file.write("Total de Campanhas: 8\n")
                
                # Rodapé
                file.write("\n" + "=" * 50 + "\n")
                file.write("Relatório gerado pelo Sistema de Gestão de Saúde\n")
                file.write("=" * 50 + "\n")
                
            messagebox.showinfo("Sucesso", f"Relatório de {relatorio} exportado com sucesso para:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar o relatório:\n{str(e)}")

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Saúde Comunitária")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f5f5f5")  # Fundo neutro claro

        self.selected_tab = None
        self.create_widgets()

    def create_widgets(self):
        # Cabeçalho
        header = tk.Frame(self.root, bg="#2c3e50", height=50)  # Fundo cinza escuro para o cabeçalho
        header.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(header, text="Dashboard - Saúde Comunitária", font=("Orbitron", 18, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=10)

        # Notebook com separadores personalizados
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#f5f5f5", borderwidth=0)  # Fundo neutro para o Notebook
        style.configure("TNotebook.Tab", font=("Orbitron", 11), padding=[10, 5], background="#bdc3c7", foreground="#2c3e50", borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", "#2c3e50")],
                  foreground=[("selected", "white")])

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both", padx=20, pady=10)

        categorias = [
            ("Médicos", "🩺"),       # Estetoscópio
            ("Pacientes", "👤"),     # Pessoa
            ("Consultas", "📅"),     # Calendário
            ("Campanhas", "📢"),     # Megafone
            ("Recursos", "💉"),      # Seringa (para medicamentos e vacinas)
            ("Relatórios", "📊")    # Gráfico
        ]

        self.frames = {}
        for cat, emoji in categorias:
            if cat == "Relatórios":
                frame = RelatoriosFrame(self.tabs)  # Usa o frame para relatórios
            elif cat == "Campanhas":
                frame = CampanhasFrame(self.tabs)  # Usa o frame para campanhas
            elif cat == "Recursos":
                frame = RecursosFrame(self.tabs)  # Usa o novo frame para recursos
            else:
                frame = ttk.Frame(self.tabs)
                frame.configure(style="TFrame", padding=10)  # Fundo neutro para os frames
            self.frames[cat] = frame

            # Adiciona o emoji ao texto da aba
            self.tabs.add(frame, text=f"{emoji}  {cat}")

        # Atribui o dicionário de frames ao atributo frames do Notebook
        self.tabs.frames = self.frames  # Corrige o acesso ao dicionário de frames

        # Rodapé
        footer = tk.Frame(self.root, bg="#2c3e50", height=30)  # Fundo cinza escuro para o rodapé
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        user_info = tk.Label(footer, text="Utilizador: admin | Projeto IPP 2025", bg="#2c3e50", fg="white", font=("Orbitron", 9))
        user_info.pack(pady=5)


if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    root.after(10, lambda: DashboardApp(root))
    root.mainloop()



