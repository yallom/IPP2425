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
from datetime import datetime
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

MC.addMedicine("Paracetamol", "Bebés", "Sim", "Baixo", "2025-12-31", "Medicamento")
MC.addMedicine("Vacina da Gripe", "Adultos", "Não", "Médio", "2025-12-31", "Vacina")
MC.addMedicine("Vacina da Gravidez", "Adultos", "Apenas", "Médio", "2025-12-31", "Vacina")

Read_File("pacientes.json")
Read_File("medicos.json")
Read_File("novoficheiro.json")
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

#Save_File("fdsbora.json")

x1 = MC.search("M0001")
CC.addCampaign("Vacina da Gripe", "2025-12-01", "2025-12-31", x1.gravidez, x1.idade, x1.eficacia, "M0001", 100)



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
            #elif cat== "Consultas":
                #self.gerente_consultas = Consultas(self.tabs)
                #self.tabs.add(self.gerente_consultas.get_frame(), text=f"{emoji}  {cat}")
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

class Interface_Medicos:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.especialidades = [
            "Cardiologia", "Ginecologia", "Neurologia", "Oftalmologia",
            "Pediatria", "Pneumonologia", "Psiquiatria"]
        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):
        titulo = tk.Label(self.frame, text="Gestão de Médicos", font=("Segoe UI", 16, "bold"), fg="#2c3e50", bg="#f5f5f5")
        titulo.pack(pady=10)

        topo = tk.Frame(self.frame, bg="#f5f5f5")
        topo.pack(fill="x", pady=10, padx=20)

        ttk.Label(topo, text="Filtrar especialidades:", background="#f5f5f5").pack(side=tk.LEFT)
        self.filtro_esp = ttk.Combobox(topo, values=["Todas"] + self.especialidades, state="readonly", width=18)
        self.filtro_esp.set("Todas")
        self.filtro_esp.pack(side=tk.LEFT, padx=5)
        self.filtro_esp.bind("<<ComboboxSelected>>", lambda e: self.aplicar_filtros())

        tk.Label(topo, text="Pesquisar nome:", bg="#f5f5f5").pack(side=tk.LEFT, padx=(20, 2))
        self.entry_pesquisa = tk.Entry(topo, width=20)
        self.entry_pesquisa.pack(side=tk.LEFT)
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.aplicar_filtros())

        botoes_medicos = tk.Frame(topo, bg="#f5f5f5")
        botoes_medicos.pack(side=tk.RIGHT)

        btn_adicionar = tk.Button(botoes_medicos, text="+ Adicionar Médico", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.formulario_adicao_medico)
        btn_adicionar.pack(side=tk.LEFT, padx=5)

        btn_editar = tk.Button(botoes_medicos, text="Editar Médico", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.editar_medico)
        btn_editar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(botoes_medicos, text="Eliminar Médico", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.eliminar_medico)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        style = ttk.Style()
        style.configure("Treeview.Heading", background="#2c3e50", foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

        frame_tabela = tk.Frame(self.frame, bg="#f5f5f5")
        frame_tabela.pack(fill="both", expand=True, padx=20)

        scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_tabela, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")

        colunas = ("id", "nome", "especialidade")
        self.tabela = ttk.Treeview(
            frame_tabela, columns=colunas, show="headings", height=12,
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tabela.yview)
        scroll_x.config(command=self.tabela.xview)

        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("especialidade", text="Especialidade")
        
        self.tabela.column("id", anchor=tk.CENTER, width=120, stretch = True)
        self.tabela.column("nome", anchor=tk.CENTER, width=120, stretch = True)
        self.tabela.column("especialidade", anchor=tk.CENTER, width=120, stretch = True)
        self.tabela.pack(fill="both", expand=True)

    def formulario_adicao_medico(self):
        janela_adicao = tk.Toplevel()
        janela_adicao.title("Adicionar Médico")
        janela_adicao.geometry("400x300")
        self.disponibilidade_selecionada = []

        def adicionar_medico():
            nome = entry_nome.get()
            especialidade = combo_esp.get()
            disponibilidade = self.disponibilidade_selecionada
            if nome and especialidade and disponibilidade:
                DC.addMedico(nome, especialidade, disponibilidade)
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!")
                janela_adicao.destroy()
            else:
                tk.Label(janela_adicao, text="Preencha todos os campos!").pack(pady=4)

        tk.Label(janela_adicao, text="Nome:").pack(pady=4)
        entry_nome = tk.Entry(janela_adicao, width=30)
        entry_nome.pack(pady=4)

        tk.Label(janela_adicao, text="Especialidade:").pack(pady=4)
        combo_esp = ttk.Combobox(janela_adicao, values=self.especialidades, state="readonly")
        combo_esp.pack(pady=4)

        btn_disp = tk.Button(janela_adicao, text="Selecionar Disponibilidade",
                             command=lambda: selecionar_disponibilidade(atualizar_disponibilidade))
        btn_disp.pack(pady=4)

        def selecionar_disponibilidade(callback):
            janela_disponibilidade = tk.Toplevel()
            janela_disponibilidade.title("Selecionar Disponibilidade")
            janela_disponibilidade.geometry("400x300")

            dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            horarios = [f"{h:02d}-{h+2:02d}:00" for h in range(8, 20, 2)]

            check_vars = [[tk.BooleanVar() for _ in horarios] for _ in dias]

            for i, dia in enumerate(dias):
                tk.Label(janela_disponibilidade, text=dia, font=("Segoe UI", 10, "bold")).grid(row=0, column=i+1, padx=5, pady=5)

            for j, hora in enumerate(horarios):
                tk.Label(janela_disponibilidade, text=hora).grid(row=j+1, column=0, padx=5, pady=5)
                for i, dia in enumerate(dias):
                    var = check_vars[i][j]
                    chk = tk.Checkbutton(janela_disponibilidade, variable=var)
                    chk.grid(row=j+1, column=i+1)
                    print(check_vars)

            def salvar():
                disponibilidade = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
                for i, dia in enumerate(dias):
                    for j, hora in enumerate(horarios):
                        if check_vars[i][j].get():
                            disponibilidade[i][j] = 1
                callback(disponibilidade)
                janela_disponibilidade.destroy()

            tk.Button(janela_disponibilidade, text="Confirmar", command=salvar).grid(row=len(horarios)+1, column=0, columnspan=len(dias)+1, pady=10)

        def atualizar_disponibilidade(lista):
            self.disponibilidade_selecionada = lista

        tk.Button(janela_adicao, text="Adicionar Médico", command=adicionar_medico).pack(pady=10)

    def editar_medico(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um médico para editar.")
            return

        valores = self.tabela.item(selecionado, "values")
        if not valores:
            return

        medico = DC.search(valores[0])
        if not medico:
            messagebox.showerror("Erro", "Médico não encontrado.")
            return

        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar Médico")
        janela_edicao.geometry("400x350")

        tk.Label(janela_edicao, text="Nome:").pack(pady=4)
        entry_nome = tk.Entry(janela_edicao, width=30)
        entry_nome.insert(0, valores[1])
        entry_nome.pack(pady=4)

        tk.Label(janela_edicao, text="Especialidade:").pack(pady=4)
        entry_esp = ttk.Combobox(janela_edicao, values=self.especialidades, state="readonly")
        entry_esp.set(valores[2])
        entry_esp.pack(pady=4)

        # Disponibilidade grid selection
        tk.Label(janela_edicao, text="Disponibilidade:").pack(pady=4)
        disponibilidade_selecionada = [row[:] for row in medico.servico] if hasattr(medico, "servico") else []

        def selecionar_disponibilidade():
            dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            horarios = [f"{h:02d}-{h+2:02d}:00" for h in range(8, 20, 2)]
            janela_disp = tk.Toplevel(janela_edicao)
            janela_disp.title("Editar Disponibilidade")
            janela_disp.geometry("400x300")

            check_vars = [[tk.BooleanVar(value=(disponibilidade_selecionada[i][j] if disponibilidade_selecionada and i < len(disponibilidade_selecionada) and j < len(disponibilidade_selecionada[i]) else 0))
                           for j in range(len(horarios))] for i in range(len(dias))]

            for i, dia in enumerate(dias):
                tk.Label(janela_disp, text=dia, font=("Segoe UI", 10, "bold")).grid(row=0, column=i+1, padx=5, pady=5)
            for j, hora in enumerate(horarios):
                tk.Label(janela_disp, text=hora).grid(row=j+1, column=0, padx=5, pady=5)
                for i, dia in enumerate(dias):
                    chk = tk.Checkbutton(janela_disp, variable=check_vars[i][j])
                    chk.grid(row=j+1, column=i+1)

            def salvar():
                for i in range(len(dias)):
                    for j in range(len(horarios)):
                        disponibilidade_selecionada[i][j] = 1 if check_vars[i][j].get() else 0
                janela_disp.destroy()

            tk.Button(janela_disp, text="Confirmar", command=salvar).grid(row=len(horarios)+1, column=0, columnspan=len(dias)+1, pady=10)

        # Inicializa a disponibilidade se necessário
        if not disponibilidade_selecionada or not isinstance(disponibilidade_selecionada[0], list):
            disponibilidade_selecionada = [[0 for _ in range(6)] for _ in range(7)]

        label_disp = tk.Label(janela_edicao, text="")
        label_disp.pack(pady=2)

        btn_disp = tk.Button(janela_edicao, text="Editar Disponibilidade", command=selecionar_disponibilidade)
        btn_disp.pack(pady=4)

        def salvar():
            nome = entry_nome.get()
            esp = entry_esp.get()
            disp = disponibilidade_selecionada
            if nome and esp and disp:
                DC.edit(medico, nome, disp, esp)
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!")
                janela_edicao.destroy()
            else:
                tk.Label(janela_edicao, text="Preencha todos os campos!").pack(pady=4)

        tk.Button(janela_edicao, text="Salvar Alterações", command=salvar).pack(pady=10)

    def eliminar_medico(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um médico para eliminar.")
            return

        valores = self.tabela.item(selecionado, "values")
        if not valores:
            return

        medico = DC.search(valores[0])
        if not medico:
            messagebox.showerror("Erro", "Médico não encontrado.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"Tem certeza que deseja eliminar o médico '{valores[1]}'?")
        if confirmar:
            DC.delete(medico)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Médico eliminado com sucesso!")

    def atualizar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for medico in DC.getAll():
            self.tabela.insert("", tk.END, values=(medico.id, medico.nome, medico.specialty, medico.servico))

    def aplicar_filtros(self):
        filtro_nome = self.entry_pesquisa.get().lower()
        filtro_esp = self.filtro_esp.get()
        dados_filtrados = []
        for medico in DC.getAll():
            nome_match = filtro_nome in medico.nome.lower()
            esp_match = filtro_esp == "Todas" or medico.specialty == filtro_esp
            if nome_match and esp_match:
                dados_filtrados.append(medico)
        self.tabela.delete(*self.tabela.get_children())
        for medico in dados_filtrados:
            self.tabela.insert("", tk.END, values=(medico.id, medico.nome, medico.specialty, medico.servico))

    def get_frame(self):
        return self.frame
class Interface_Paciente:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.risco = ["Muito Elevado","Elevado", "Médio", "Baixo"]
        self.sangue = ["A+","A-", "B+", "B-", "AB+","AB-", "O+","O-"]
        self.doencas = ["Diabetes", "Asma", "Hipertensão", "Outras"]

        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):

        # Título
        titulo = tk.Label(self.frame, text="Gestão de Pacientes", font=("Segoe UI", 16, "bold"),fg="#2c3e50", bg = "#f5f5f5")
        titulo.pack(pady=10)

        topo = tk.Frame(self.frame, bg="#f5f5f5")
        topo.pack(fill="x", pady=10, padx=20)

        # Filtro por risco
        ttk.Label(topo, text="Filtrar risco:", background="#f5f5f5").pack(side=tk.LEFT)
        self.filtro_esp = ttk.Combobox(topo, values=["Todas"] + self.risco, state="readonly", width=18)
        self.filtro_esp.set("Todas")
        self.filtro_esp.pack(side=tk.LEFT, padx=5)
        self.filtro_esp.bind("<<ComboboxSelected>>", lambda e: self.aplicar_filtros())

        # Barra de pesquisa
        tk.Label(topo, text="Pesquisar nome:", bg="#f5f5f5").pack(side=tk.LEFT, padx=(20, 2))
        self.entry_pesquisa = tk.Entry(topo, width=20)
        self.entry_pesquisa.pack(side=tk.LEFT)
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.aplicar_filtros())

        # Botões (à direita)
        botoes_pacientes = tk.Frame(topo, bg="#f5f5f5")
        botoes_pacientes.pack(side=tk.RIGHT)

        btn_adicionar_paciente = tk.Button(botoes_pacientes, text="+ Adicionar Paciente", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.abrir_formulario_adicao)
        btn_adicionar_paciente.pack(side=tk.LEFT, padx=5)

        btn_editar_paciente = tk.Button(botoes_pacientes, text="Editar Paciente", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.editar_paciente)
        btn_editar_paciente.pack(side=tk.LEFT, padx=5)

        btn_editar_paciente = tk.Button(botoes_pacientes, text="Remover", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.remover_paciente)
        btn_editar_paciente.pack(side=tk.LEFT, padx=5)
        

        # Tabela

        # Frame para conter a tabela e as scrollbars
        frame_tabela = tk.Frame(self.frame, bg="#f5f5f5")
        frame_tabela.pack(fill="both", expand=True, padx=20)
        

        # Scrollbars
        scroll_x = ttk.Scrollbar(frame_tabela, orient="horizontal")
        scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical")
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")

        style = ttk.Style()
        style.configure("Treeview.Heading", background="#2c3e50", foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

        colunas = ("id","nome", "idade", "morada", "sexo", "gravidez", "sangue", "doença", "risco")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        self.tabela.bind("<Double-1>", self.ver_paciente)
        # Conectar scrollbars à tabela
        scroll_x.config(command=self.tabela.xview)
        scroll_y.config(command=self.tabela.yview)

        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("idade", text="Idade")
        self.tabela.heading("morada", text="Localidade")
        self.tabela.heading("sexo", text="Sexo")
        self.tabela.heading("gravidez", text="Gravidez")
        self.tabela.heading("sangue", text= "Tipo de Sangue")
        self.tabela.heading("doença", text="Doença Crónica")
        self.tabela.heading("risco", text="Nível de Risco")

        for col in colunas:
            self.tabela.column(col, anchor=tk.CENTER, width=150)

        self.tabela.pack(fill="both", expand=True)

    def atualizar_tabela(self, currentdata=None):
        if currentdata is None:
            data = PC.getAll()
        else:
            data = currentdata
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for paciente in data:
            self.tabela.insert("", tk.END, values=(
                paciente.id, paciente.nome, paciente.idade, paciente.morada, paciente.sexo,
                paciente.gravidez, paciente.sangue, paciente.doenca, paciente.risco
            ))

    def abrir_formulario_adicao(self):
        janela_pacientes = tk.Toplevel()
        janela_pacientes.title("Adicionar Paciente")
        janela_pacientes.geometry("400x600")

        def adicionar_paciente():
            nome = entry_nome.get()
            idade = entry_idade.get()
            morada = entry_concelho.get()
            sexo = sexo_var.get()
            gravida = var_gravidez.get()
            sangue = opcoes_sangue.get()
            doencas_escolhidas = [lista_doencas.get(i) for i in lista_doencas.curselection()] if doenca_var.get() else []

            # Validação dos campos obrigatórios
            if nome and idade and morada and sexo and sangue:
                try:
                    idade_int = int(idade)
                except ValueError:
                    messagebox.showerror("Erro", "A idade deve ser um número inteiro.")
                    return

                # Adiciona o paciente usando o controller
                PC.addPacient(nome, idade_int, sexo, gravida, doencas_escolhidas, sangue, morada)
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")
                janela_pacientes.destroy()
            else:
                messagebox.showerror("Erro", "É preciso preencher todos os campos obrigatórios.")

        # Formulário
        tk.Label(janela_pacientes, text="Nome:").pack(pady=4)
        entry_nome = tk.Entry(janela_pacientes, width=30)
        entry_nome.pack(pady=4)

        tk.Label(janela_pacientes, text="Idade:").pack(pady=4)
        entry_idade = tk.Entry(janela_pacientes, width=30)
        entry_idade.pack(pady=4)

        tk.Label(janela_pacientes, text="Morada:").pack(pady=4)
        entry_concelho = tk.Entry(janela_pacientes, width=30)
        entry_concelho.pack(pady=4)

        def toggle_gravidez():
            if sexo_var.get() == "F":
                checkbox_gravidez.config(state="normal")
            else:
                var_gravidez.set(False)
                checkbox_gravidez.config(state="disabled")

        tk.Label(janela_pacientes, text="Sexo:").pack(pady=4)
        sexo_var = tk.StringVar(value=" ")
        frame_sexo = tk.Frame(janela_pacientes)
        frame_sexo.pack(pady=4)
        tk.Radiobutton(frame_sexo, text="Feminino", variable=sexo_var, value="F", command = toggle_gravidez).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_sexo, text="Masculino", variable=sexo_var, value="M", command = toggle_gravidez).pack(side=tk.LEFT, padx=10)

        var_gravidez = tk.BooleanVar()
        checkbox_gravidez = tk.Checkbutton(janela_pacientes, text="Gravidez:", variable=var_gravidez, state="disabled")
        checkbox_gravidez.pack(pady=5)

        tk.Label(janela_pacientes, text="Tipo Sanguíneo:").pack(pady=5)
        opcoes_sangue = ttk.Combobox(janela_pacientes, values=self.sangue, state="readonly")
        opcoes_sangue.pack(pady=4)

        
        tk.Label(janela_pacientes, text="Doenças Crónicas:").pack(pady=5)
        frame_doenca = tk.Frame(janela_pacientes)
        frame_doenca.pack(pady=4)

        lista_doencas = tk.Listbox(frame_doenca, selectmode="multiple", height=5, exportselection=False)
        for doenca in self.doencas:
            lista_doencas.insert(tk.END, doenca)
        lista_doencas.config(state="disabled")
        lista_doencas.pack()

        def toggle_doenca():
            if doenca_var.get():
                lista_doencas.config(state="normal")
            else:
                lista_doencas.config(state="disabled")
                lista_doencas.selection_clear(0, tk.END)

        doenca_var = tk.BooleanVar()
        tk.Checkbutton(janela_pacientes, text="Tem Doenças Crónicas?", variable=doenca_var, command=toggle_doenca).pack(pady=5)


        tk.Button(janela_pacientes, text="Adicionar Paciente", command=adicionar_paciente).pack(pady=10)
   
    def ver_paciente(self, event=None):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um paciente para editar.")
            return

        valores = self.tabela.item(selecionado, "values")
        if not valores:
            return

        ID = valores[0]
        paciente = PC.search(ID)

        janela_ver_pacientes = tk.Toplevel()
        janela_ver_pacientes.title("Visualizar Paciente")
        janela_ver_pacientes.geometry("900x500")

        # Frame principal horizontal
        main_frame = tk.Frame(janela_ver_pacientes)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame da esquerda (dados principais)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Frame da direita (históricos)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # --- Dados principais ---
        tk.Label(left_frame, text="Nome:").pack(anchor="w", pady=4)
        entry_nome = tk.Entry(left_frame, width=50, state="normal")
        entry_nome.insert(0, valores[1])
        entry_nome.pack(anchor="w", pady=4)
        entry_nome.config(state="readonly")

        tk.Label(left_frame, text="Idade:").pack(anchor="w", pady=4)
        entry_idade = tk.Entry(left_frame, width=50)
        entry_idade.insert(0, str(valores[2]))
        entry_idade.pack(anchor="w", pady=4)
        entry_idade.config(state="readonly")

        tk.Label(left_frame, text="Morada:").pack(anchor="w", pady=4)
        entry_concelho = tk.Entry(left_frame, width=50)
        entry_concelho.insert(0, valores[3])
        entry_concelho.pack(anchor="w", pady=4)
        entry_concelho.config(state="readonly")

        tk.Label(left_frame, text="Sexo:").pack(anchor="w", pady=4)
        entry_sexo = tk.Entry(left_frame, width=50)
        entry_sexo.insert(0, valores[4])
        entry_sexo.pack(anchor="w", pady=4)
        entry_sexo.config(state="readonly")

        tk.Label(left_frame, text="Gravidez:").pack(anchor="w", pady=4)
        entry_gravidez = tk.Entry(left_frame, width=50)
        entry_gravidez.insert(0, valores[5])
        entry_gravidez.pack(anchor="w", pady=4)
        entry_gravidez.config(state="readonly")

        tk.Label(left_frame, text="Tipo Sanguíneo:").pack(anchor="w", pady=4)
        entry_sangue = tk.Entry(left_frame, width=50)
        entry_sangue.insert(0, valores[6])
        entry_sangue.pack(anchor="w", pady=4)
        entry_sangue.config(state="readonly")

        tk.Label(left_frame, text="Doenças Crónicas:").pack(anchor="w", pady=4)
        entry_doenca = tk.Entry(left_frame, width=50)
        entry_doenca.insert(0, valores[7])
        entry_doenca.pack(anchor="w", pady=4)
        entry_doenca.config(state="readonly")

        def history_consultas():
            text = ""
            for i in paciente.historico_consultas:
                text += f'Consulta de {i["tipo"]} em {i["data"]} com o médico {i["médico"]}.\n'
            return text
        
        def history_vacinas():
            text = ""
            for i in paciente.historico_vacinas:
                text += f'Vacina {i["nome"]} administrada em {i["data"]}.\n'
            return text
        # --- Históricos (lado direito) ---
        tk.Label(right_frame, text="Histórico de Consultas:").pack(anchor="nw", pady=4)
        text_consultas = tk.Text(right_frame, width=45, height=8)
        text_consultas.insert("1.0", history_consultas())
        text_consultas.pack(anchor="nw", pady=4, fill="x")
        text_consultas.config(state="disabled")

        tk.Label(right_frame, text="Histórico de Vacinas:").pack(anchor="nw", pady=4)
        text_vacinas = tk.Text(right_frame, width=45, height=8)
        text_vacinas.insert("1.0", history_vacinas())
        text_vacinas.pack(anchor="nw", pady=4, fill="x")
        text_vacinas.config(state="disabled")


    def editar_paciente(self, event=None):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um paciente para editar.")
            return

        valores = self.tabela.item(selecionado, "values")
        if not valores:
            return

        

        janela_editar_pacientes = tk.Toplevel()
        janela_editar_pacientes.title("Editar Paciente")
        janela_editar_pacientes.geometry("400x600")

        tk.Label(janela_editar_pacientes, text="Nome:").pack(pady=4)
        entry_nome = tk.Entry(janela_editar_pacientes, width=30)
        entry_nome.insert(0, valores[1])
        entry_nome.pack(pady=4)

        tk.Label(janela_editar_pacientes, text="Idade:").pack(pady=4)
        entry_idade = tk.Entry(janela_editar_pacientes, width=30)
        entry_idade.insert(0, str(valores[2]))
        entry_idade.pack(pady=4)

        tk.Label(janela_editar_pacientes, text="Morada:").pack(pady=4)
        entry_concelho = tk.Entry(janela_editar_pacientes, width=30)
        entry_concelho.insert(0, valores[3])
        entry_concelho.pack(pady=4)

        # Variáveis que precisam ser definidas antes do toggle
        sexo_var = tk.StringVar()
        var_gravidez = tk.BooleanVar(value=(valores[5] == "Sim"))

        def toggle_gravidez():
            if sexo_var.get() == "F":
                checkbox_gravidez.config(state="normal")
            else:
                checkbox_gravidez.config(state="disabled")
                var_gravidez.set(False)

        tk.Label(janela_editar_pacientes, text="Sexo:").pack(pady=4)
        frame_sexo = tk.Frame(janela_editar_pacientes)
        frame_sexo.pack(pady=4)
        tk.Radiobutton(frame_sexo, text="Feminino", variable=sexo_var, value="F", command=toggle_gravidez).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_sexo, text="Masculino", variable=sexo_var, value="M", command=toggle_gravidez).pack(side=tk.LEFT, padx=10)
        sexo_var.set(valores[4])

        checkbox_gravidez = tk.Checkbutton(janela_editar_pacientes, text="Gravidez:", variable=var_gravidez)
        checkbox_gravidez.pack(pady=5)
        toggle_gravidez()  # Atualiza visibilidade da checkbox com base no sexo

        tk.Label(janela_editar_pacientes, text="Tipo sanguíneo:").pack(pady=5)
        combo_sangue = ttk.Combobox(janela_editar_pacientes, values=self.sangue, state="readonly")
        combo_sangue.set(valores[6])
        combo_sangue.pack(pady=4)

        # Doenças Crónicas
        doenca_var = tk.BooleanVar(value=(valores[7] != "Nenhuma"))
        tk.Checkbutton(
            janela_editar_pacientes,
            text="Tem Doença Crónica",
            variable=doenca_var,
            command=lambda: listbox_doencas.config(state="normal" if doenca_var.get() else "disabled")
        ).pack(pady=5)

        listbox_doencas = tk.Listbox(janela_editar_pacientes, selectmode="multiple", exportselection=False, height=6)
        for doenca in self.doencas:
            listbox_doencas.insert(tk.END, doenca)
        listbox_doencas.pack(pady=4)

        # Pré-selecionar doenças existentes
        doencas_atuais = valores[7].split(", ") if valores[7] != "Nenhuma" else []
        for i, d in enumerate(self.doencas):
            if d in doencas_atuais:
                listbox_doencas.selection_set(i)

        if not doenca_var.get():
            listbox_doencas.config(state="disabled")

        def salvar_edicao():
            nome = entry_nome.get()
            idade = entry_idade.get()
            concelho = entry_concelho.get()
            sexo = sexo_var.get()
            gravida = "Sim" if var_gravidez.get() else "Não"
            sangue = combo_sangue.get()
            doencas = []
            if doenca_var.get():
                selecionados = listbox_doencas.curselection()
                doencas = [self.doencas[i] for i in selecionados]
            doenca = ", ".join(doencas) if doencas else None

            if nome and idade and concelho and sexo and sangue:
                try:
                    idade = int(idade)
                except ValueError:
                    messagebox.showerror("Erro", "A idade deve ser um número inteiro.")
                    return

                PC.edit(valores[0], nome, idade, sexo, sangue, concelho, doenca, gravida)
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
                janela_editar_pacientes.destroy()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")

        tk.Button(janela_editar_pacientes, text="Guardar Alterações", command=salvar_edicao).pack(pady=10)




    def remover_paciente(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente da tabela.")
            return

        paciente_id = self.tabela.item(selecionado)["values"][0]
        print (paciente_id)
        confirmar = messagebox.askyesno("Confirmar", f"Tem a certeza que quer remover o paciente com ID {paciente_id}?")
        if confirmar:
            PC.delete(paciente_id)
            self.atualizar_tabela()

    

    def aplicar_filtros(self):
        filtro_nome = self.entry_pesquisa.get().lower()
        filtro_esp = self.filtro_esp.get()
        print(filtro_esp)

        dados_filtrados = []
        for paciente in PC.getAll():
            nome = paciente.nome.lower()

            nome_match = filtro_nome in nome
            risco_match = filtro_esp == "Todas" or filtro_esp == paciente.risco
            

            if nome_match and risco_match:
                dados_filtrados.append(paciente)

        print(f"Filtrados: {len(dados_filtrados)} pacientes")
        self.atualizar_tabela(dados_filtrados)


    def get_frame(self):
        return self.frame  # ou self.main_frame, dependendo do nom

class CampanhasFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(padding=20, style="Custom.TFrame")  # Define o estilo do frame
        self.availableitems = MC.getAll()
        self.currentitems = []
        self.expiry_date= None

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
        self.campanhas = CC.getAll()

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
        ttk.Button(filtro_frame, text="Importar Dados", command=self.importar_dados, style="Blue.TButton").pack(side="right", padx=5)
        
        # Tabela de campanhas
        colunas = ("ID", "Nome", "Início", "Fim", "Grupo-Alvo", "Grupo Etário", "Gravidez", "Inscrições Atuais", "Inscrições-Alvo", "Estado")
        
        # Frame para a tabela e scrollbar
        tabela_frame = ttk.Frame(self)
        tabela_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(tabela_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10, style="Custom.Treeview", yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tabela.yview)
        #self.tabela.bind("<Double-1>", self.ver_fila_campanha)
        
        for col in colunas:
            self.tabela.heading(col, text=col, anchor="center")
            self.tabela.column(col, width=100, anchor="center")

        self.tabela.pack(fill="both", expand=True)

        self.tabela.bind("<Double-1>", self.abrir_detalhes_campanha)

        # Preenche a tabela com os dados iniciais
        self.atualizar_tabela(self.campanhas)

    def datechecker(self, datas):
        """Verifica se a data atual está dentro do intervalo de datas da campanha."""
        today = datetime.today().date()
        compare_date1 = datetime.strptime(datas[0], "%Y-%m-%d").date()
        compare_date2 = datetime.strptime(datas[1], "%Y-%m-%d").date()
        if compare_date1 <= today:
            if compare_date2 >= today:
                return "Ativa"
            else:
                return "Encerrada"
        else:
            return "Agendada"

    def atualizar_tabela(self, campanhas):
        """Atualiza a tabela com os dados fornecidos."""
        # Limpa a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Insere os novos dados
        for campanha in CC.getAll():
            self.tabela.insert('', 'end', values=(
                campanha.id, campanha.nome, campanha.datas[0], campanha.datas[1], campanha.gruporisco, campanha.grupoidade, campanha.gravidas, len(campanha.pacientes), campanha.maximo, self.datechecker(campanha.datas)
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

    def importar_dados(self):
        """Abre um diálogo para importar dados de um arquivo CSV."""
        filepath = filedialog.askopenfilename(filetypes=[("json files", "*.json")])
        if not filepath:
            return

        Read_File(filepath)

        self.atualizar_tabela(self.campanhas)

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
            ("Recurso", "combobox"),
            ("Item", "combobox"),
            ("Data Início", "date"),
            ("Data Fim", "date"),
            ("Grupo Risco", "combobox"),
            ("Grupo-Alvo", "combobox"),
            ("Grávidas", "combobox"),
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
                                foreground="white", borderwidth=2, style="Custom.TCombobox", maxdate=self.expiry_date)
                entry.pack(fill="x", expand=True)
            elif tipo == "combobox":
                if campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=[], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[], state="readonly", style="Custom.TCombobox")
                elif campo == "Grávidas":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox")
                elif campo == "Recurso":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox")
                    entry.bind("<<ComboboxSelected>>", self.atualizar_itens)
                elif campo == "Item":
                    entry = ttk.Combobox(frame, values=[], state="readonly", style="Custom.TCombobox")
                    entry.bind("<<ComboboxSelected>>", self.on_item_select)
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
        itens = []
        for i in self.availableitems:
            if i.tipo == recurso:
                itens.append(i) # Obtém os itens do dataset
        self.entries["Item"]["values"] = [i.nome for i in itens]
        self.currentitems = itens  
        if itens:
            self.entries["Item"].current(0)  # Define o primeiro item como padrão
            self.on_item_select()  # Atualiza os campos com o primeiro item

    def datelimit(self, event=None):
        """Atualiza a data limite com base no item selecionado."""
        item = self.entries["Item"].get()
        for i in MC.getAll():
            if i.nome == item:
                self.expiry_date = datetime.strptime(i.validade, "%Y-%m-%d").date()
                print(self.expiry_date)
                self.entries["Data Início"].configure(maxdate=self.expiry_date)
                self.entries["Data Fim"].configure(maxdate=self.expiry_date)
                break

    def atualizar_campos(self, event=None):
        """Atualiza as opções de grávidas com base no sexo selecionado."""
        item = self.entries["Item"].get()
        for i in MC.getAll():
            if i.nome == item:
                self.medicamento = i
                print("Sucesso")
                self.entries["Grávidas"]["values"] = i.gravidez
                self.entries["Grupo Risco"]["values"] = i.eficacia
                self.entries["Grupo-Alvo"]["values"] = i.idade
                self.entries["Grávidas"].current(0)
                self.entries["Grupo Risco"].current(0)
                self.entries["Grupo-Alvo"].current(0)

    def on_item_select(self, event=None):
        self.atualizar_campos()
        self.datelimit()

    def guardar_campanha(self):
        """Guarda os dados da nova campanha e atualiza a tabela."""
        # Obtém os valores dos campos
        nome = self.entries["Nome"].get().strip()
        data_inicio = self.entries["Data Início"].get().strip()
        data_fim = self.entries["Data Fim"].get().strip()
        grupo_risco = self.entries["Grupo Risco"].get().strip()
        grupo_alvo = self.entries["Grupo-Alvo"].get().strip()
        gravidas = self.entries["Grávidas"].get().strip()
        recurso = self.entries["Recurso"].get().strip()
        item = self.entries["Item"].get().strip()
        participantes = self.entries["Número de Participantes"].get().strip()  # Novo campo
        

        # Validação: verifica se todos os campos obrigatórios estão preenchidos
        if not all([nome, data_inicio, data_fim, grupo_risco, grupo_alvo, gravidas, recurso, item]):
            messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos!")
            return

        # Adiciona a nova campanha
        CC.addCampaign(nome, data_inicio, data_fim, gravidas, grupo_alvo, grupo_risco, self.medicamento.id, participantes)
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
                        "Bebés (0-3 anos)",
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

    def fdsprint(self):
        print("Olá")

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
            CC.delete(valores[0])

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
        ttk.Button(botoes_frame, text="Filtrar", command=self.filtrar_recursos, style="App.TButton").pack(side="right", padx=5)
        ttk.Button(botoes_frame, text="+ Adicionar Recurso", command=self.novo_medicamento, style="App.TButton").pack(side="right", padx=5)        
        #ttk.Button(botoes_frame, text="Exportar", command=self.exportar_dados, style="App.TButton").pack(side="left", padx=5)
        #ttk.Button(botoes_frame, text="Importar", command=self.importar_dados, style="App.TButton").pack(side="left", padx=5)

        # Frame para a tabela e scrollbars
        tabela_frame = ttk.Frame(self)
        tabela_frame.pack(fill="both", expand=True, pady=10)

        # Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(tabela_frame, orient="vertical")
        scrollbar_vertical.pack(side="right", fill="y")

        # Tabela de recursos

        colunas = ("ID", "Tipo", "Nome", "Grupo-Alvo", "Grupo Risco", "Gravidez", "Data de Validade")
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=15, style="Custom.Treeview", yscrollcommand=scrollbar_vertical.set)
        
        # Configura a scrollbar para controlar a tabela
        scrollbar_vertical.configure(command=self.tabela.yview)

        
        # Ajusta o tamanho das colunas
        self.tabela.column("ID", width=80, anchor="center")
        self.tabela.column("Tipo", width=100, anchor="center")
        self.tabela.column("Nome", width=150, anchor="center")
        self.tabela.column("Grupo-Alvo", width=150, anchor="center")
        self.tabela.column("Grupo Risco", width=100, anchor="center")
        self.tabela.column("Gravidez", width=100, anchor="center")
        self.tabela.column("Data de Validade", width=120, anchor="center")

        
        # Configura os cabeçalhos
        for col in colunas:
            self.tabela.heading(col, text=col, anchor="center")
            
        # Empacota a tabela
        self.tabela.pack(fill="both", expand=True)

        # Adiciona o evento de clique na tabela
        #self.tabela.bind("<Double-1>", self.abrir_detalhes_recurso)

        # Barra de rolagem horizontal
        scrollbar_horizontal = ttk.Scrollbar(tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        self.tabela.configure(xscrollcommand=scrollbar_horizontal.set)

        # Dados iniciais (exemplo)
        #self.dados = MC.getAll()

        # Preenche a tabela com os dados iniciais
        self.atualizar_tabela()

    def atualizar_tabela(self):
        """Atualiza a tabela com os dados fornecidos."""
        # Limpa a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Insere os novos dados
        for recurso in MC.getAll():
            self.tabela.insert('', 'end', values=(
                recurso.id, 
                recurso.nome,
                recurso.idade,
                recurso.eficacia,
                recurso.gravidez,
                recurso.validade,
                

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
                        "Bebés",
                        "Crianças",
                        "Jovens",
                        "Adultos",
                        "Idosos"
                    ], state="readonly", style="Custom.TCombobox", width=50)
                elif campo == "Gravidez":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox", width=50)
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
        newname = dados.get("Nome", "")
        newtype = dados.get("Tipo", "")
        newage = dados.get("Grupo-Alvo", "")
        if newage == "Bebés":
            age1 = 0
            age2 = 3
        elif newage == "Crianças":
            age1 = 4
            age2 = 12
        elif newage == "Jovens":
            age1 = 13
            age2 = 18
        elif newage == "Adultos":
            age1 = 19
            age2 = 65
        elif newage == "Idosos":
            age1 = 66
            age2 = 999
        newrisk = dados.get("Grupo Risco", "")
        newpreg = dados.get("Gravidez", "")
        newvalid = dados.get("Data de Validade", "")
        MC.addMedicine(newname,newage,newpreg,newrisk,newvalid,newtype)  # Adiciona aos dados existentes
        self.atualizar_tabela()  # Atualiza a tabela com os novos dados

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
                "Bebés (0-3 anos)", "Crianças (4-12 anos)", "Jovens (12-18 anos)",
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

    def importar_dados(self):
        """Abre um diálogo para importar dados de um arquivo CSV."""
        filepath = filedialog.askopenfilename(filetypes=[("json files", "*.json")])
        if not filepath:
            return

        Read_File(filepath)
        self.dados = MC.getAll()
        self.atualizar_tabela(self.dados)
        

    def exportar_dados(self):
        """Exporta todos os dados (tabela e outros) para um arquivo TXT."""
        # Abre uma janela para selecionar o local e o nome do arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            title="Salvar arquivo como"
        )

        if not file_path:
            return  # Se o usuário cancelar, não faz nada

        try:
            Save_File(file_path)
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

    """def abrir_detalhes_recurso(self, event):
        #Abre uma janela com os detalhes do recurso selecionado.
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
            "Tipo": valores[1],
            "Nome": valores[2],
            "Grupo-Alvo": valores[3],
            "Grupo Risco": valores[4],
            "Gravidez": valores[5],
            "Data de Validade": data_validade,
        }

        ID = valores[0]
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
                        "Bebés",
                        "Crianças",
                        "Jovens",
                        "Adultos",
                        "Idosos"
                    ], state="readonly", style="Custom.TCombobox")
                elif campo == "Gravidez":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox")
                elif campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Elevado", "Muito Elevado"], state="readonly", style="Custom.TCombobox")
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

        ttk.Button(botoes_frame, text="Guardar", command=lambda: self.guardar_alteracoes_recurso(ID, recurso, janela), style="App.TButton").pack(side="left", padx=10)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy, style="App.TButton").pack(side="right", padx=10)
"""
    """def guardar_alteracoes_recurso(self, ID, recurso, janela):
        #Guarda as alterações feitas no recurso.
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
        MC.edit
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
        self.atualizar_tabela()

        messagebox.showinfo("Sucesso", "Alterações guardadas com sucesso!")
        janela.destroy()
"""
    def atualizar_tabela(self):
        """Atualiza a tabela com os dados fornecidos."""
        # Limpa a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Insere os novos dados
        for recurso in MC.getAll():
            self.tabela.insert('', 'end', values=(
                recurso.id,
                recurso.tipo,
                recurso.nome,
                recurso.idade,
                recurso.eficacia,
                recurso.gravidez,
                recurso.validade,
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

        self.root.state("zoomed")

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
            if cat == "Médicos":
                interface = Interface_Medicos(self.tabs)
                frame = interface.get_frame()
                self.frames[cat] = interface
                self.tabs.add(frame, text=f"{emoji}  {cat}")
            elif cat == "Relatórios":
                frame = RelatoriosFrame(self.tabs)
                self.frames[cat] = frame
                self.tabs.add(frame, text=f"{emoji}  {cat}")
            elif cat == "Campanhas":
                frame = CampanhasFrame(self.tabs)
                self.frames[cat] = frame
                self.tabs.add(frame, text=f"{emoji}  {cat}")
            elif cat == "Pacientes":
                interface = Interface_Paciente(self.tabs)
                frame = interface.get_frame()
                self.frames[cat] = interface
                self.tabs.add(frame, text=f"{emoji}  {cat}")
            elif cat == "Recursos":
                frame = RecursosFrame(self.tabs)
                self.frames[cat] = frame
                self.tabs.add(frame, text=f"{emoji}  {cat}")
            else:
                frame = ttk.Frame(self.tabs)
                frame.configure(style="TFrame", padding=10)
                self.frames[cat] = frame
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