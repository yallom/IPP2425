import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
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
from backend.Controllers import pessoascontroller as PC
from backend.Controllers import medicamentoscontroller as MC
from backend.Controllers import campanhascontroller as CC
from backend.Controllers import medicoscontroller as DC


def Read_File (filename):
    with open(filename, 'r', encoding='utf-8') as ficheiro:
        fullfile = json.load(ficheiro)        
        pacientlist = fullfile.get('Pacientes',{})
        medicationlist = fullfile.get('Medicamentos',{})
        vaccinelist = fullfile.get('Vacinas',{})
        Doctorlist = fullfile.get('Médicos',{})
        campaignlist = fullfile.get('Campanhas',{})
        consultationlist = fullfile.get('Consultas',{})
        Queuelist = fullfile.get('Filas',{})
        if pacientlist:
            PC.read(pacientlist)
        if medicationlist:
            MC.read(medicationlist)
        if vaccinelist:
            MC.read(vaccinelist)
        if Doctorlist:
            DC.read(Doctorlist)

    return

#Read_File("pacientes.json")
#Read_File("medicos.json")
#print(PC.getAll())
#print(DC.getAll())

def Save_File (filepath):
    with open(filepath, 'w', encoding='utf-8') as ficheiro:
        data = {
            'Pacientes': [PC.write(p) for p in PC.getAll()],
            'Medicamentos': [MC.write(m) for m in MC.getAll() if m.tipo == "Medicamento"],
            'Vacinas': [MC.write(v) for v in MC.getAll() if v.tipo == "Vacina"],
            'Médicos': [DC.write(d) for d in DC.getAll()]
        }
        json.dump(data, ficheiro, ensure_ascii=False, indent=4)
    return

#Save_File("novoficheiro.json")






class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Saúde Comunitária")
        self.root.geometry("1000x600")
        self.root.configure(bg="#eaf0f1")
        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#eaf0f1", height=50)
        header.pack(fill=tk.X, side=tk.TOP)
        title = tk.Label(header, text="Bem-vindo, admin", font=("Segoe UI", 16, "bold"), bg="#eaf0f1", fg="#2f4f4f")
        title.pack(pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#eaf0f1", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11), padding=[10, 5], background="#dfe6e9")
        style.map("TNotebook.Tab",
                  background=[("selected", "#b2bec3")],
                  foreground=[("selected", "#2d3436")])

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both", padx=20, pady=10)

        categorias = [
            ("Médicos", "🩺"),
            ("Pacientes", "👤"),
            ("Consultas", "📅"),
            ("Campanhas", "📢"),
            ("Recursos", "💉"),
            ("Relatórios", "📊")
        ]
        ##Atenção criar classes paciente e medicos e consulta 
        for cat, emoji in categorias:
            if cat == "Pacientes":
                self.gerente_pacientes = Interface_Paciente(self.tabs)
                self.tabs.add(self.gerente_pacientes.get_frame(), text=f"{emoji}  {cat}")
            elif cat == "Médicos": 
                self.gerente_medicos = Interface_Medicos(self.tabs)
                self.tabs.add(self.gerente_medicos.get_frame(), text= f"{emoji}  {cat}" )
            elif cat== "Consultas":
                self.gerente_consultas = Consultas(self.tabs)
                self.tabs.add(self.gerente_consultas.get_frame(), text=f"{emoji}  {cat}")
            else:
                frame = ttk.Frame(self.tabs)
                self.tabs.add(frame, text=f"{emoji}  {cat}")

        footer = tk.Frame(self.root, bg="#eaf0f1", height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        user_info = tk.Label(footer, text="Utilizador: admin | Projeto IPP 2025", bg="#eaf0f1", fg="#2f4f4f", font=("Segoe UI", 9))
        user_info.pack(pady=5)

    



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
            {"Nome": "Campanha de Vacinação Gripe 2025", "Início": "2025-04-01", "Fim": "2025-04-15", "Grupo-Alvo": "Idosos", "Estado": "Ativa", "Número de Participantes": 150},
            {"Nome": "Rastreio Diabetes", "Início": "2025-01-10", "Fim": "2025-02-10", "Grupo-Alvo": "Adultos", "Estado": "Encerrada", "Número de Participantes": 85},
            {"Nome": "Vacinação Infantil", "Início": "2025-03-01", "Fim": "2025-03-30", "Grupo-Alvo": "Bebês (0-3 anos)", "Estado": "Ativa", "Número de Participantes": 220},
            {"Nome": "Saúde Mental Jovens", "Início": "2025-02-15", "Fim": "2025-03-15", "Grupo-Alvo": "Jovens (12-18 anos)", "Estado": "Ativa", "Número de Participantes": 120},
            {"Nome": "Prevenção Cardíaca", "Início": "2024-11-01", "Fim": "2024-12-31", "Grupo-Alvo": "Adultos", "Estado": "Encerrada", "Número de Participantes": 300},
            {"Nome": "Campanha de Higiene Oral", "Início": "2025-05-01", "Fim": "2025-05-31", "Grupo-Alvo": "Crianças (4-12 anos)", "Estado": "Ativa", "Número de Participantes": 180},
            {"Nome": "Rastreio Visual", "Início": "2024-10-01", "Fim": "2024-10-31", "Grupo-Alvo": "Idosos", "Estado": "Encerrada", "Número de Participantes": 95},
            {"Nome": "Vacinação COVID-19", "Início": "2025-01-01", "Fim": "2025-01-31", "Grupo-Alvo": "Adultos", "Estado": "Encerrada", "Número de Participantes": 450},
            {"Nome": "Saúde da Mulher", "Início": "2025-06-01", "Fim": "2025-06-30", "Grupo-Alvo": "Adultos", "Estado": "Ativa", "Número de Participantes": 280},
            {"Nome": "Nutrição Infantil", "Início": "2025-02-01", "Fim": "2025-02-28", "Grupo-Alvo": "Crianças (4-12 anos)", "Estado": "Encerrada", "Número de Participantes": 110},
            {"Nome": "Prevenção de Acidentes", "Início": "2025-07-01", "Fim": "2025-07-31", "Grupo-Alvo": "Jovens (12-18 anos)", "Estado": "Ativa", "Número de Participantes": 70},
            {"Nome": "Saúde Bucal", "Início": "2024-12-01", "Fim": "2024-12-31", "Grupo-Alvo": "Crianças (4-12 anos)", "Estado": "Encerrada", "Número de Participantes": 160},
            {"Nome": "Rastreio de Pressão", "Início": "2025-03-15", "Fim": "2025-04-15", "Grupo-Alvo": "Idosos", "Estado": "Ativa", "Número de Participantes": 135},
            {"Nome": "Saúde Mental Adultos", "Início": "2025-05-15", "Fim": "2025-06-15", "Grupo-Alvo": "Adultos", "Estado": "Ativa", "Número de Participantes": 200},
            {"Nome": "Vacinação Hepatite B", "Início": "2024-09-01", "Fim": "2024-09-30", "Grupo-Alvo": "Adultos", "Estado": "Encerrada", "Número de Participantes": 350},
            {"Nome": "Desenvolvimento Infantil", "Início": "2025-04-15", "Fim": "2025-05-15", "Grupo-Alvo": "Bebês (0-3 anos)", "Estado": "Ativa", "Número de Participantes": 190},
            {"Nome": "Saúde do Adolescente", "Início": "2025-06-15", "Fim": "2025-07-15", "Grupo-Alvo": "Jovens (12-18 anos)", "Estado": "Ativa", "Número de Participantes": 105},
            {"Nome": "Prevenção de Quedas", "Início": "2024-11-15", "Fim": "2024-12-15", "Grupo-Alvo": "Idosos", "Estado": "Encerrada", "Número de Participantes": 75},
            {"Nome": "Saúde Ocupacional", "Início": "2025-01-15", "Fim": "2025-02-15", "Grupo-Alvo": "Adultos", "Estado": "Encerrada", "Número de Participantes": 260},
            {"Nome": "Alimentação Saudável", "Início": "2025-08-01", "Fim": "2025-08-31", "Grupo-Alvo": "Crianças (4-12 anos)", "Estado": "Ativa", "Número de Participantes": 140}
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
        
        # Frame para a tabela e scrollbar
        tabela_frame = ttk.Frame(self)
        tabela_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(tabela_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10, style="Custom.Treeview", yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tabela.yview)
        
        for col in colunas:
            self.tabela.heading(col, text=col, anchor="center")
            self.tabela.column(col, width=100, anchor="center")

        self.tabela.pack(fill="both", expand=True)

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
        """Abre uma janela para cadastrar uma nova campanha."""
        janela = tk.Toplevel(self)
        janela.title("Nova Campanha")
        janela.geometry("700x500")
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
        frame_interno = ttk.Frame(canvas, style="Custom.TFrame", padding=20)
        canvas.create_window((0, 0), window=frame_interno, anchor="nw", width=canvas.winfo_width())

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Atualiza a largura do frame interno quando a janela é redimensionada
            canvas.itemconfig(canvas.find_withtag("all")[0], width=canvas.winfo_width())

        frame_interno.bind("<Configure>", atualizar_scrollregion)
        canvas.bind("<Configure>", atualizar_scrollregion)

        # Define estilos para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")
        style.configure("Custom.TLabel", font=("Segoe UI", 11), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Custom.TEntry", padding=5, font=("Segoe UI", 11))
        style.configure("Custom.TCombobox", padding=5, font=("Segoe UI", 11))

        # Título com estilo maior e destacado
        ttk.Label(frame_interno, text="Informações da Campanha", style="Custom.TLabel", font=("Segoe UI", 14, "bold")).pack(pady=20)

        # Separador para os campos principais
        ttk.Label(frame_interno, text="Informações Básicas", style="Custom.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=10)

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
            ("Número de Participantes", "entry")
        ]

        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_interno, style="Custom.TFrame")
            frame.pack(fill="x", padx=20, pady=8)
            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)

            if tipo == "entry":
                entry = ttk.Entry(frame, style="Custom.TEntry")
                entry.pack(fill="x", expand=True)
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="yyyy-mm-dd", width=12, background="#2c3e50",
                                foreground="white", borderwidth=2, style="Custom.TCombobox")
                entry.pack(fill="x", expand=True)
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
                    entry = ttk.Combobox(frame, values=[], state="readonly", style="Custom.TCombobox")
                elif campo == "Estado":
                    entry = ttk.Combobox(frame, values=["Ativa", "Encerrada"], state="readonly", style="Custom.TCombobox")
                entry.pack(fill="x", expand=True)
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

    def atualizar_gravidas(self, event=None):
        """Atualiza as opções de grávidas com base no sexo selecionado."""
        sexo = self.entries["Sexo"].get()
        if sexo == "Masculino":
            self.entries["Grávidas"].set("Não")
            self.entries["Grávidas"]["state"] = "disabled"
        else:
            self.entries["Grávidas"]["state"] = "readonly"
            self.entries["Grávidas"].set("Sim")

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
        participantes = self.entries["Número de Participantes"].get().strip()  # Novo campo
        

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
           
            "Número de Participantes": participantes,  # Novo campo
           
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
        canvas.create_window((0, 0), window=frame_principal, anchor="nw", width=canvas.winfo_width())

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Atualiza a largura do frame principal quando a janela é redimensionada
            canvas.itemconfig(canvas.find_withtag("all")[0], width=canvas.winfo_width())

        frame_principal.bind("<Configure>", atualizar_scrollregion)
        canvas.bind("<Configure>", atualizar_scrollregion)

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
            ("Número de Participantes", "entry")
        ]

        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_principal, style="Custom.TFrame")
            frame.pack(fill="x", padx=20, pady=8)
            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)

            if tipo == "entry":
                entry = ttk.Entry(frame, style="Custom.TEntry")
                entry.pack(fill="x", expand=True)
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="yyyy-mm-dd", width=12, background="#2c3e50",
                                foreground="white", borderwidth=2, style="Custom.TCombobox")
                entry.pack(fill="x", expand=True)
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
                    entry = ttk.Combobox(frame, values=[], state="readonly", style="Custom.TCombobox")
                elif campo == "Estado":
                    entry = ttk.Combobox(frame, values=["Ativa", "Encerrada"], state="readonly", style="Custom.TCombobox")
                entry.pack(fill="x", expand=True)
            elif tipo == "text":
                entry = tk.Text(frame, height=5, wrap="word", bg="white", font=("Segoe UI", 11), relief="solid", borderwidth=1)

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

        # Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(tabela_frame, orient="vertical")
        scrollbar_vertical.pack(side="right", fill="y")

        # Tabela de recursos

        colunas = ("Tipo", "Nome", "Grupo-Alvo", "Grupo Risco", "Gravidez", "Data de Validade")
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=15, style="Custom.Treeview", yscrollcommand=scrollbar_vertical.set)
        
        # Configura a scrollbar para controlar a tabela
        scrollbar_vertical.configure(command=self.tabela.yview)

        
        # Ajusta o tamanho das colunas
        self.tabela.column("Tipo", width=100, anchor="center")
        self.tabela.column("Nome", width=150, anchor="center")
        self.tabela.column("Grupo-Alvo", width=150, anchor="center")
        self.tabela.column("Grupo Risco", width=100, anchor="center")
        self.tabela.column("Gravidez", width=100, anchor="center")
        self.tabela.column("Data de Validade", width=120, anchor="center")
        self.tabela.column("ID", width=80, anchor="center")

        
        # Configura os cabeçalhos
        for col in colunas:
            self.tabela.heading(col, text=col, anchor="center")
            
        # Empacota a tabela
        self.tabela.pack(fill="both", expand=True)

        # Adiciona o evento de clique na tabela
        self.tabela.bind("<Double-1>", self.abrir_detalhes_recurso)

        # Barra de rolagem horizontal
        scrollbar_horizontal = ttk.Scrollbar(tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        self.tabela.configure(xscrollcommand=scrollbar_horizontal.set)

        # Dados iniciais (exemplo)
        MC.addMedicine("Med1","10","12","m",0,"1","2","2024-11-23")
        self.dados = MC.getAll()

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

                recurso.nome,
                f"{recurso.idade[0]}-{recurso.idade[1]}",
                f"{recurso.eficacia[0]}-{recurso.eficacia[1]}",
                recurso.gravidez,
                recurso.validade,
                recurso.id

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
            ("Tipo", "combobox"),
            ("Nome", "entry"),
            ("Grupo-Alvo", "combobox"),
            ("Gravidez", "combobox"),
            ("Sexo", "combobox"),
            ("Grupo Risco", "combobox"),
            ("Data de Validade", "date")
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
                entry = ttk.Entry(frame, style="Custom.TEntry", width=50)
                entry.pack(fill="x", expand=True)
            elif tipo == "combobox":
                if campo == "Tipo":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox", width=50)
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly", style="Custom.TCombobox", width=50)
                elif campo == "Gravidez":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox", width=50)
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly", style="Custom.TCombobox", width=50)
                elif campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox", width=50)
                entry.pack(fill="x", expand=True)
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
            "Gravidez": dados.get("Gravidez", ""),
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
            
         
            "Sexo": ""
        
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
        canvas.create_window((0, 0), window=frame_principal, anchor="nw", width=canvas.winfo_width())

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Atualiza a largura do frame principal quando a janela é redimensionada
            canvas.itemconfig(canvas.find_withtag("all")[0], width=canvas.winfo_width())

        frame_principal.bind("<Configure>", atualizar_scrollregion)
        canvas.bind("<Configure>", atualizar_scrollregion)

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
            ("Grupo-Alvo", "combobox"),
            ("Gravidez", "combobox"),
            ("Sexo", "combobox"),
            ("Grupo Risco", "combobox"),
            ("Data de Validade", "date")
        ]

        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_principal, style="Custom.TFrame")
            frame.pack(fill="x", padx=20, pady=8)
            ttk.Label(frame, text=campo, style="Custom.TLabel").pack(anchor="w", pady=2)

            valor = recurso.get(campo, "")

            if tipo == "entry":
                entry = ttk.Entry(frame, style="Custom.TEntry")
                entry.insert(0, valor)
            elif tipo == "combobox":
                if campo == "Tipo":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly", style="Custom.TCombobox")
                elif campo == "Gravidez":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox")
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox")
                elif campo == "Estado":
                    entry = ttk.Combobox(frame, values=["Disponível", "Fora de stock", "Expirado"], state="readonly", style="Custom.TCombobox")
                entry.set(valor)
                entry.pack(fill="x", expand=True)
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

                "Medicamento",
                recurso.nome,
                f"{recurso.idade[0]}-{recurso.idade[1]}",
                f"{recurso.eficacia[0]}-{recurso.eficacia[1]}",
                recurso.gravidez,
                recurso.validade,
                recurso.id

            ))

class RelatoriosFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=20, style="Custom.TFrame")

        # Define o estilo personalizado para os widgets
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f5f5f5")
        style.configure("Custom.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f5f5", foreground="#2c3e50")
        style.configure("Custom.TButton", font=("Segoe UI", 11), padding=6)
        style.configure("App.TButton", background="#2c3e50", foreground="white", font=("Segoe UI", 11), padding=6)
        style.map("App.TButton",
                 background=[("active", "#1a252f")],
                  foreground=[("active", "white")])
        style.configure("Custom.TCombobox", font=("Segoe UI", 11), padding=5)
        style.configure("DateEntry", font=("Segoe UI", 11), padding=5) # Style for DateEntry

        # Título com estilo personalizado
        ttk.Label(self, text="Relatórios", style="Custom.TLabel").pack(pady=(0, 10))


        # Frame para a seleção do relatório e filtros de data
        controles_frame = ttk.Frame(self, style="Custom.TFrame")
        controles_frame.pack(fill="x", pady=10)

        # Frame para a seleção do tipo de relatório (esquerda)
        tipo_relatorio_frame = ttk.Frame(controles_frame, style="Custom.TFrame")
        tipo_relatorio_frame.pack(side="left")

        ttk.Label(tipo_relatorio_frame, text="Tipo de Relatório:", 
                 font=("Segoe UI", 11),
                 foreground="#2c3e50",
                 background="#f5f5f5").pack(side="left", padx=(0, 5))

        self.combo_relatorios = ttk.Combobox(tipo_relatorio_frame, 
                                           values=["Campanhas", "Consultas"],
                                           state="readonly",
                                           style="Custom.TCombobox",
                                           width=15)
        self.combo_relatorios.pack(side="left")
        self.combo_relatorios.bind("<<ComboboxSelected>>", self.mostrar_relatorio_selecionado)

        # Frame para os filtros de data (centro)
        data_filtro_frame = ttk.Frame(controles_frame, style="Custom.TFrame")
        data_filtro_frame.pack(side="left", padx=30)

        ttk.Label(data_filtro_frame, text="Período:", 
                 font=("Segoe UI", 11),
                 foreground="#2c3e50",
                 background="#f5f5f5").pack(side="left", padx=(0, 5))

        self.date_inicio = DateEntry(data_filtro_frame, date_pattern="dd/mm/yyyy", 
                                     width=10, background="#2c3e50", foreground="white", 
                                     borderwidth=2, style="DateEntry")
        self.date_inicio.pack(side="left", padx=5)

        ttk.Label(data_filtro_frame, text="a", 
                 font=("Segoe UI", 11),
                 foreground="#2c3e50",
                 background="#f5f5f5").pack(side="left")

        self.date_fim = DateEntry(data_filtro_frame, date_pattern="dd/mm/yyyy", 
                                  width=10, background="#2c3e50", foreground="white", 
                                  borderwidth=2, style="DateEntry")
        self.date_fim.pack(side="left", padx=5)

        # Botão Gerar Relatório (direita)
        ttk.Button(controles_frame, text="Gerar Relatório", 
                  command=self.atualizar_relatorio_selecionado,
                  style="App.TButton").pack(side="right")

        # Frame para o conteúdo do relatório (tabela e gráficos)

        self.conteudo_frame = ttk.Frame(self, style="Custom.TFrame")
        self.conteudo_frame.pack(fill="both", expand=True, pady=10)

        # Frame para os botões de exportação (inferior)
        export_botoes_frame = ttk.Frame(self, style="Custom.TFrame")
        export_botoes_frame.pack(fill="x", pady=10)

    def atualizar_relatorio_selecionado(self):
        """Atualiza o relatório com base no tipo selecionado e nas datas."""
        relatorio = self.combo_relatorios.get()
        
        # Obtém as datas selecionadas
        data_inicio = self.date_inicio.get_date()
        data_fim = self.date_fim.get_date()

        if relatorio == "Campanhas":
            self.atualizar_relatorio_campanhas()
        elif relatorio == "Consultas":
            # Obtém os dados das consultas
            try:
                consultas_frame = self.master.frames["Consultas"]
                todas_consultas = consultas_frame.consultas
            except (AttributeError, KeyError):
                messagebox.showerror("Erro", "Não foi possível acessar os dados das consultas.")
                return

            # Filtra as consultas pelo período selecionado
            consultas_filtradas = []
            for consulta in todas_consultas:
                try:
                    data_consulta = datetime.strptime(consulta["Data"], "%Y-%m-%d").date()
                    if data_inicio <= data_consulta <= data_fim:
                        consultas_filtradas.append(consulta)
                except ValueError:
                    continue

            # Atualiza a visualização com as consultas filtradas
            self.mostrar_relatorio_consultas(consultas_filtradas)

    def atualizar_relatorio_campanhas(self):
        """Atualiza o relatório de campanhas com base nas datas selecionadas."""
        # Obtém as datas selecionadas
        data_inicio = self.date_inicio.get_date()
        data_fim = self.date_fim.get_date()

        # Obtém os dados das campanhas
        try:
            campanhas_frame = self.master.frames["Campanhas"]
            todas_campanhas = campanhas_frame.campanhas
        except (AttributeError, KeyError):
            messagebox.showerror("Erro", "Não foi possível acessar os dados das campanhas.")
            return

        # Filtra as campanhas pelo período selecionado
        campanhas_filtradas = []
        for campanha in todas_campanhas:
            try:
                data_inicio_camp = datetime.strptime(campanha["Início"], "%Y-%m-%d").date()
                data_fim_camp = datetime.strptime(campanha["Fim"], "%Y-%m-%d").date()
                
                # Verifica se a campanha está dentro do período selecionado
                if data_inicio <= data_fim_camp and data_fim >= data_inicio_camp:
                    campanhas_filtradas.append(campanha)
            except ValueError:
                continue

        # Atualiza a visualização com as campanhas filtradas
        self.mostrar_relatorio_campanhas(campanhas_filtradas)

    def mostrar_relatorio_campanhas(self, campanhas=None):
        """Exibe o relatório de campanhas com tabela e visualizações (gráficos)."""
        # Limpa o frame de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

        # Se não foram fornecidas campanhas, obtém todas
        if campanhas is None:
            try:
                campanhas_frame = self.master.frames["Campanhas"]
                campanhas = campanhas_frame.campanhas
            except (AttributeError, KeyError):
                messagebox.showerror("Erro", "Não foi possível acessar os dados das campanhas.")
                return

        # Frame principal para a tabela e visualizações lado a lado
        main_viz_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame")
        main_viz_frame.pack(fill="both", expand=True)

        # Frame para a tabela (esquerda)
        tabela_frame = ttk.Frame(main_viz_frame, style="Custom.TFrame")
        tabela_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Título da Tabela
        ttk.Label(tabela_frame, text="Lista de Campanhas", 
                 font=("Segoe UI", 12, "bold"),
                 foreground="#2c3e50",
                 background="#f5f5f5").pack(pady=(0, 5))

        # Tabela de campanhas
        colunas = ("Nome", "Início", "Fim", "Grupo-Alvo", "Estado")
        
        # Frame para a tabela e scrollbar
        tabela_scroll_frame = ttk.Frame(tabela_frame) 
        tabela_scroll_frame.pack(fill="both", expand=True)
        
        # Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(tabela_scroll_frame, orient="vertical")
        scrollbar_vertical.pack(side="right", fill="y")
        
        self.tabela_relatorios = ttk.Treeview(tabela_scroll_frame, columns=colunas, show="headings", height=10, style="Custom.Treeview", yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.configure(command=self.tabela_relatorios.yview)
        
        for col in colunas:
            self.tabela_relatorios.heading(col, text=col, anchor="center")
            self.tabela_relatorios.column(col, width=100, anchor="center")

        self.tabela_relatorios.pack(side="left", fill="both", expand=True) 

        # Preenche a tabela com os dados
        for campanha in campanhas:
            self.tabela_relatorios.insert('', 'end', values=(
                campanha["Nome"], campanha["Início"], campanha["Fim"], campanha["Grupo-Alvo"], campanha["Estado"]
            ))

        # Frame para as visualizações (direita)
        viz_frame = ttk.Frame(main_viz_frame, style="Custom.TFrame")
        viz_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # --- Implementação dos Gráficos ---

        # Gráfico 1: Estado das Campanhas (Pizza)
        campanhas_ativas = sum(1 for c in campanhas if c["Estado"] == "Ativa")
        campanhas_encerradas = sum(1 for c in campanhas if c["Estado"] == "Encerrada")
        estado_labels = ['Ativas', 'Encerradas']
        estado_sizes = [campanhas_ativas, campanhas_encerradas]
        estado_colors = ['#27ae60', '#c0392b'] # Verde e Vermelho do tema

        fig1 = Figure(figsize=(6, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.pie(estado_sizes, labels=estado_labels, autopct='%1.1f%%', colors=estado_colors,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax1.set_title('Estado das Campanhas', fontsize=12, color='#2c3e50')
        
        canvas1 = FigureCanvasTkAgg(fig1, viz_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="x", pady=(0, 10))

        # --- Gráfico 2: Número de Participantes por Campanha (Barras) ---
        try:
            # Ordena as campanhas por número de participantes
            campanhas_ordenadas = sorted(campanhas, key=lambda x: float(x.get("Número de Participantes", 0)), reverse=True)
            nomes_ordenados = [c["Nome"] for c in campanhas_ordenadas]
            valores_ordenados = [float(c.get("Número de Participantes", 0)) for c in campanhas_ordenadas]
            
            fig2 = Figure(figsize=(6, 4), dpi=100)
            ax2 = fig2.add_subplot(111)
            
            # Cria as barras com cores diferentes baseadas no valor
            bars = ax2.bar(nomes_ordenados, valores_ordenados, 
                          color=['#2ecc71' if v > 100 else '#f1c40f' if v > 50 else '#e74c3c' for v in valores_ordenados])
            
            ax2.set_title('Número de Participantes por Campanha', fontsize=12, color='#2c3e50')
            ax2.set_ylabel('Número de Participantes', fontsize=10, color='#2c3e50')
            ax2.tick_params(axis='x', rotation=45, labelsize=9)
            ax2.tick_params(axis='y', labelsize=9)
            
            # Adiciona os valores no topo das barras
            for bar in bars:
                yval = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2.0, yval,
                        int(yval) if yval.is_integer() else round(yval, 2),
                        va='bottom', ha='center', fontsize=9)
            
            # Adiciona uma grade para melhor visualização
            ax2.grid(True, linestyle='--', alpha=0.7)
            
            fig2.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, viz_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="x", pady=(10, 0))
            
        except Exception as e:
            print(f"Erro ao criar gráfico de barras: {e}")
            messagebox.showerror("Erro", f"Erro ao criar gráfico de barras: {e}")

    def mostrar_relatorio_selecionado(self, event=None):
        """Exibe o relatório selecionado no combobox."""
        relatorio = self.combo_relatorios.get()
        # Limpa o frame de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

        if relatorio == "Campanhas":
            self.mostrar_relatorio_campanhas()
        elif relatorio == "Consultas":
            self.mostrar_relatorio_consultas()

    def mostrar_relatorio_consultas(self):
        """Exibe o relatório de consultas com visualizações e estatísticas."""
        # Limpa o frame de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

        # Dados de exemplo para demonstração
        consultas = [
            {"Data": "2025-01-15", "Médico": "Dr. Silva", "Paciente": "Maria Santos", "Tipo": "Consulta Regular", "Duração": 30, "Estado": "Concluída"},
            {"Data": "2025-01-16", "Médico": "Dra. Oliveira", "Paciente": "João Pereira", "Tipo": "Urgência", "Duração": 45, "Estado": "Concluída"},
            {"Data": "2025-01-17", "Médico": "Dr. Santos", "Paciente": "Ana Costa", "Tipo": "Consulta Regular", "Duração": 30, "Estado": "Concluída"},
            {"Data": "2025-01-18", "Médico": "Dra. Oliveira", "Paciente": "Pedro Lima", "Tipo": "Acompanhamento", "Duração": 20, "Estado": "Concluída"},
            {"Data": "2025-01-19", "Médico": "Dr. Silva", "Paciente": "Carla Mendes", "Tipo": "Urgência", "Duração": 60, "Estado": "Concluída"},
            {"Data": "2025-01-20", "Médico": "Dr. Santos", "Paciente": "Ricardo Alves", "Tipo": "Consulta Regular", "Duração": 30, "Estado": "Agendada"},
            {"Data": "2025-01-21", "Médico": "Dra. Oliveira", "Paciente": "Sofia Martins", "Tipo": "Acompanhamento", "Duração": 20, "Estado": "Agendada"},
            {"Data": "2025-01-22", "Médico": "Dr. Silva", "Paciente": "Miguel Costa", "Tipo": "Consulta Regular", "Duração": 30, "Estado": "Agendada"}
        ]

        # Frame principal para estatísticas e gráficos
        main_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame para estatísticas rápidas
        stats_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        stats_frame.pack(fill="x", pady=(0, 20))

        # Estatísticas rápidas
        total_consultas = len(consultas)
        consultas_concluidas = sum(1 for c in consultas if c["Estado"] == "Concluída")
        consultas_agendadas = sum(1 for c in consultas if c["Estado"] == "Agendada")
        media_duracao = sum(c["Duração"] for c in consultas) / len(consultas)

        # Cards de estatísticas
        stats = [
            ("Total de Consultas", total_consultas, "#2c3e50"),  # Azul escuro do tema
            ("Consultas Concluídas", consultas_concluidas, "#34495e"),  # Azul mais claro
            ("Consultas Agendadas", consultas_agendadas, "#3498db"),  # Azul médio
            ("Duração Média", f"{media_duracao:.1f} min", "#2980b9")  # Azul mais escuro
        ]

        for i, (label, value, color) in enumerate(stats):
            card = ttk.Frame(stats_frame, style="Custom.TFrame")
            card.pack(side="left", expand=True, fill="x", padx=5)
            
            # Estilo moderno para os cards
            card.configure(style="Card.TFrame")
            style = ttk.Style()
            style.configure("Card.TFrame", background=color, relief="solid", borderwidth=1)
            
            # Ajusta a largura dos cards
            card.configure(width=150)  # Largura fixa para os cards
            
            ttk.Label(card, text=label, 
                     font=("Segoe UI", 10),
                     foreground="white",
                     background=color,
                     wraplength=140).pack(pady=(10, 5))
            
            ttk.Label(card, text=str(value),
                     font=("Segoe UI", 16, "bold"),
                     foreground="white",
                     background=color).pack(pady=(0, 10))

        # Frame para gráficos
        graphs_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        graphs_frame.pack(fill="both", expand=True)

        # Gráfico 1: Consultas por Médico (Barras) - Agora à esquerda e maior
        consultas_medico = {}
        for consulta in consultas:
            medico = consulta["Médico"]
            consultas_medico[medico] = consultas_medico.get(medico, 0) + 1

        fig1 = Figure(figsize=(8, 4), dpi=100)  # Aumentado o tamanho
        ax1 = fig1.add_subplot(111)
        
        # Ajusta a largura das barras
        bar_width = 0.35  # Barras mais finas
        x = range(len(consultas_medico))
        bars = ax1.bar(x, consultas_medico.values(), 
                      width=bar_width,
                      color=['#2c3e50', '#34495e', '#3498db'])  # Cores do tema
        
        # Configura os labels do eixo x
        ax1.set_xticks(x)
        ax1.set_xticklabels(consultas_medico.keys(), rotation=45)
        
        ax1.set_title('Consultas por Médico', fontsize=12, color='#2c3e50')
        ax1.set_ylabel('Número de Consultas', fontsize=10, color='#2c3e50')
        ax1.tick_params(axis='x', rotation=45, labelsize=9)
        ax1.tick_params(axis='y', labelsize=9)
        
        # Adiciona os valores no topo das barras
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9)
        
        ax1.grid(True, linestyle='--', alpha=0.7)
        fig1.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, graphs_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)

        # Gráfico 2: Distribuição por Tipo de Consulta (Pizza) - Agora à direita e maior
        tipos_consulta = {}
        for consulta in consultas:
            tipo = consulta["Tipo"]
            tipos_consulta[tipo] = tipos_consulta.get(tipo, 0) + 1

        fig2 = Figure(figsize=(5, 5), dpi=100)  # Aumentado o tamanho do gráfico de pizza
        ax2 = fig2.add_subplot(111)
        ax2.pie(tipos_consulta.values(), labels=tipos_consulta.keys(), autopct='%1.1f%%',
                colors=['#2c3e50', '#34495e', '#3498db'],  # Cores do tema
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax2.set_title('Distribuição por Tipo de Consulta', fontsize=12, color='#2c3e50')
        
        canvas2 = FigureCanvasTkAgg(fig2, graphs_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True, padx=5)

        # Frame para a tabela de consultas
        table_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        table_frame.pack(fill="both", expand=True, pady=20)

        # Título da tabela
        ttk.Label(table_frame, text="Detalhes das Consultas",
                 font=("Segoe UI", 12, "bold"),
                 foreground="#2c3e50",
                 background="#f5f5f5").pack(pady=(0, 10))

        # Tabela de consultas
        colunas = ("Data", "Médico", "Paciente", "Tipo", "Duração", "Estado")
        
        # Frame para a tabela e scrollbar
        table_scroll_frame = ttk.Frame(table_frame)
        table_scroll_frame.pack(fill="both", expand=True)
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(table_scroll_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        self.tabela_consultas = ttk.Treeview(table_scroll_frame, columns=colunas, show="headings",
                                           height=8, style="Custom.Treeview",
                                           yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tabela_consultas.yview)
        
        # Configura as colunas
        for col in colunas:
            self.tabela_consultas.heading(col, text=col, anchor="center")
            self.tabela_consultas.column(col, width=100, anchor="center")

        self.tabela_consultas.pack(side="left", fill="both", expand=True)

        # Preenche a tabela com os dados
        for consulta in consultas:
            self.tabela_consultas.insert('', 'end', values=(
                consulta["Data"],
                consulta["Médico"],
                consulta["Paciente"],
                consulta["Tipo"],
                f"{consulta['Duração']} min",
                consulta["Estado"]
            ))

        # Botões de ação
        action_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        action_frame.pack(fill="x", pady=10)

        # Configura o estilo dos botões
        style = ttk.Style()
        style.configure("App.TButton",
                       background="#2c3e50",
                       foreground="white",
                       font=("Segoe UI", 11),
                       padding=6,
                       width=15)  # Largura fixa para os botões
        style.map("App.TButton",
                 background=[("active", "#1a252f")],
                 foreground=[("active", "white")])

        ttk.Button(action_frame, text="Exportar Relatório",
                  command=self.exportar_relatorio_consultas,
                  style="App.TButton").pack(side="right", padx=5)

    def exportar_relatorio_consultas(self):
        """Exporta o relatório de consultas para um arquivo."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Salvar relatório como"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("Relatório de Consultas\n")
                file.write("=" * 50 + "\n\n")

                # Estatísticas gerais
                file.write("Estatísticas Gerais:\n")
                file.write("-" * 30 + "\n")
                total_consultas = len(self.tabela_consultas.get_children())
                consultas_concluidas = sum(1 for item in self.tabela_consultas.get_children()
                                         if self.tabela_consultas.item(item)["values"][5] == "Concluída")
                file.write(f"Total de Consultas: {total_consultas}\n")
                file.write(f"Consultas Concluídas: {consultas_concluidas}\n")
                file.write(f"Consultas Agendadas: {total_consultas - consultas_concluidas}\n\n")

                # Detalhes das consultas
                file.write("Detalhes das Consultas:\n")
                file.write("-" * 30 + "\n")
                for item in self.tabela_consultas.get_children():
                    values = self.tabela_consultas.item(item)["values"]
                    file.write(f"Data: {values[0]}\n")
                    file.write(f"Médico: {values[1]}\n")
                    file.write(f"Paciente: {values[2]}\n")
                    file.write(f"Tipo: {values[3]}\n")
                    file.write(f"Duração: {values[4]}\n")
                    file.write(f"Estado: {values[5]}\n")
                    file.write("-" * 30 + "\n")

            messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {e}")

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