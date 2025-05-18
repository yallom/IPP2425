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

MC.addMedicine("Paracetamol", 1, 20, 0, 1, 2, "10-05-2026", "Medicamento")
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

#Save_File("fdsbora.json")

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

        colunas = ("id", "nome", "especialidade", "disponibilidade")
        self.tabela = ttk.Treeview(
            frame_tabela, columns=colunas, show="headings", height=12,
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tabela.yview)
        scroll_x.config(command=self.tabela.xview)

        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("especialidade", text="Especialidade")
        self.tabela.heading("disponibilidade", text="Disponibilidade")
        
        self.tabela.column("id", anchor=tk.CENTER, width=120, stretch = False)
        self.tabela.column("nome", anchor=tk.CENTER, width=120, stretch = False)
        self.tabela.column("especialidade", anchor=tk.CENTER, width=120, stretch = False)
        self.tabela.column("disponibilidade", anchor=tk.CENTER, stretch=True)
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
        janela_edicao.geometry("400x300")

        tk.Label(janela_edicao, text="Nome:").pack(pady=4)
        entry_nome = tk.Entry(janela_edicao, width=30)
        entry_nome.insert(0, valores[1])
        entry_nome.pack(pady=4)

        tk.Label(janela_edicao, text="Especialidade:").pack(pady=4)
        entry_esp = ttk.Combobox(janela_edicao, values=self.especialidades, state="readonly")
        entry_esp.set(valores[2])
        entry_esp.pack(pady=4)

        tk.Label(janela_edicao, text="Disponibilidade:").pack(pady=4)
        entry_disp = tk.Entry(janela_edicao, width=30)
        entry_disp.insert(0, valores[3])
        entry_disp.pack(pady=4)

        def salvar():
            nome = entry_nome.get()
            esp = entry_esp.get()
            disp = entry_disp.get()
            if nome and esp and disp:
                DC.edit(medico, nome, esp, disp)
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
   
    def editar_paciente(self):
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
        ttk.Button(filtro_frame, text="Importar Dados", command=self.importar_dados, style="Blue.TButton").pack(side="right", padx=5)
        
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
            ("Profissionais Atribuídos", "entry"),
            ("Número de Participantes", "entry"),
            ("Observações", "text"),
            ("Estado", "combobox"),
            
            # Planejamento e Execução
            ("Tipo de Campanha", "combobox"),
            ("Objetivo Principal", "combobox"),
            ("Metas Quantitativas", "entry"),
            ("Metas Qualitativas", "combobox"),
            ("Fase da Campanha", "combobox"),
            ("Responsável Principal", "entry"),
            ("Plano de Ação", "combobox"),
            ("Estratégia de Implementação", "combobox"),
            
            # Gestão de Riscos
            ("Probabilidade de Ocorrência", "combobox"),
            ("Impacto Potencial", "combobox"),
            ("Nível de Risco", "combobox"),
            ("Medidas Preventivas", "combobox"),
            ("Responsável por Riscos", "entry"),
            ("Frequência de Monitoramento de Riscos", "combobox")
        ]

        self.entries = {}

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
                elif campo == "Grávidas":
                    entry = ttk.Combobox(frame, values=["Sim", "Não", "Apenas"], state="readonly", style="Custom.TCombobox")
                elif campo == "Recurso":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly", style="Custom.TCombobox")
                    entry.bind("<<ComboboxSelected>>", self.atualizar_itens)
                elif campo == "Item":
                    entry = ttk.Combobox(frame, values=[], state="readonly", style="Custom.TCombobox")
                elif campo == "Estado":
                    entry = ttk.Combobox(frame, values=["Ativa", "Encerrada"], state="readonly", style="Custom.TCombobox")
                elif campo == "Tipo de Campanha":
                    entry = ttk.Combobox(frame, values=["Preventiva", "Curativa", "Educativa", "Rastreio", "Vacinação"], state="readonly", style="Custom.TCombobox")
                elif campo == "Objetivo Principal":
                    entry = ttk.Combobox(frame, values=["Prevenção", "Tratamento", "Educação", "Rastreio", "Vacinação"], state="readonly", style="Custom.TCombobox")
                elif campo == "Metas Qualitativas":
                    entry = ttk.Combobox(frame, values=["Alta", "Média", "Baixa"], state="readonly", style="Custom.TCombobox")
                elif campo == "Fase da Campanha":
                    entry = ttk.Combobox(frame, values=["Planejamento", "Execução", "Monitoramento", "Avaliação", "Conclusão"], state="readonly", style="Custom.TCombobox")
                elif campo == "Plano de Ação":
                    entry = ttk.Combobox(frame, values=["Estratégico", "Tático", "Operacional"], state="readonly", style="Custom.TCombobox")
                elif campo == "Estratégia de Implementação":
                    entry = ttk.Combobox(frame, values=["Centralizada", "Descentralizada", "Mista"], state="readonly", style="Custom.TCombobox")
                elif campo == "Probabilidade de Ocorrência":
                    entry = ttk.Combobox(frame, values=["Baixa", "Média", "Alta"], state="readonly", style="Custom.TCombobox")
                elif campo == "Impacto Potencial":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox")
                elif campo == "Nível de Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly", style="Custom.TCombobox")
                elif campo == "Medidas Preventivas":
                    entry = ttk.Combobox(frame, values=["Treinamento", "Protocolos", "Equipamentos", "Monitoramento", "Comunicação"], state="readonly", style="Custom.TCombobox")
                elif campo == "Frequência de Monitoramento de Riscos":
                    entry = ttk.Combobox(frame, values=["Diário", "Semanal", "Quinzenal", "Mensal", "Trimestral"], state="readonly", style="Custom.TCombobox")
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
        ttk.Button(botoes_frame, text="Importar", command=self.importar_dados, style="App.TButton").pack(side="left", padx=5)

        # Frame para a tabela e scrollbars
        tabela_frame = ttk.Frame(self)
        tabela_frame.pack(fill="both", expand=True, pady=10)

        # Tabela de recursos
        colunas = ("Tipo", "Nome", "Grupo-Alvo", "Grupo Risco", "Gravidez", "Data de Validade", "ID")
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=15, style="Custom.Treeview")
        
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
            
        # Empacota a tabela antes da barra de rolagem horizontal
        self.tabela.pack(fill="both", expand=True)

        # Adiciona o evento de clique na tabela
        self.tabela.bind("<Double-1>", self.abrir_detalhes_recurso)

        # Barra de rolagem horizontal
        scrollbar_horizontal = ttk.Scrollbar(tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        self.tabela.configure(xscrollcommand=scrollbar_horizontal.set)

        # Dados iniciais (exemplo)
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
        #self.combo_relatorios.bind("<<ComboboxSelected>>", self.alternar_relatorio)

        # Botão para gerar relatório
        ttk.Button(filtros_frame, text="Gerar Relatório", command=self.gerar_relatorio, style="Blue.TButton").pack(side="right", padx=5)

        # Frame para o conteúdo do relatório
        self.conteudo_frame = ttk.Frame(self, style="Custom.TFrame")
        self.conteudo_frame.pack(fill="both", expand=True, pady=10)

        # Inicializa com o relatório de pacientes
        self._mostrar_relatorio_pacientes()

    def _mostrar_relatorio_pacientes(self):
        """Exibe o layout do relatório de pacientes com visualizações modernas."""
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

        # Frame para os gráficos (direita)
        graficos_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        graficos_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Dados fictícios para os gráficos
        categorias = ["Baixo", "Médio", "Alto"]
        valores = [200, 150, 50]
        generos = ["Masculino", "Feminino"]
        valores_genero = [180, 220]
        faixas_etarias = ["0-3", "4-12", "13-18", "19-65", "65+"]
        valores_idade = [50, 80, 70, 120, 80]

        # Criação dos gráficos usando subplots
        figura = plt.figure(figsize=(12, 8), dpi=100)
        gs = figura.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Gráfico 1: Distribuição por Risco (Barras horizontais)
        ax1 = figura.add_subplot(gs[0, 0])
        cores = ['#2ecc71', '#f1c40f', '#e74c3c']
        bars = ax1.barh(categorias, valores, color=cores, height=0.6)
        ax1.set_title('Distribuição por Risco de Saúde', pad=20, fontsize=12, color='#2c3e50')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        ax1.grid(axis='x', linestyle='--', alpha=0.3)
        for bar in bars:
            width = bar.get_width()
            ax1.text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}',
                    ha='left', va='center', fontsize=10, color='#2c3e50')

        # Gráfico 2: Distribuição por Gênero (Pizza)
        ax2 = figura.add_subplot(gs[0, 1])
        ax2.pie(valores_genero, labels=generos, autopct='%1.1f%%', colors=['#3498db', '#e84393'],
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax2.set_title('Distribuição por Gênero', pad=20, fontsize=12, color='#2c3e50')

        # Gráfico 3: Distribuição por Faixa Etária (Área)
        ax3 = figura.add_subplot(gs[1, :])
        ax3.fill_between(faixas_etarias, valores_idade, alpha=0.3, color='#3498db')
        ax3.plot(faixas_etarias, valores_idade, marker='o', color='#2980b9', linewidth=2)
        ax3.set_title('Distribuição por Faixa Etária', pad=20, fontsize=12, color='#2c3e50')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(axis='y', linestyle='--', alpha=0.3)
        for i, valor in enumerate(valores_idade):
            ax3.text(i, valor + 5, f'{int(valor)}', ha='center', va='bottom',
                    fontsize=10, color='#2c3e50')

        # Ajusta o layout
        plt.tight_layout()

        # Adiciona os gráficos ao frame
        canvas = FigureCanvasTkAgg(figura, graficos_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def _mostrar_relatorio_consultas(self):
        """Exibe o layout do relatório de consultas com visualizações modernas."""
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

        # Frame para os gráficos (direita)
        graficos_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        graficos_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Dados fictícios para os gráficos
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        consultas_geral = [120, 150, 180, 160, 200, 190]
        consultas_especializada = [80, 100, 120, 110, 140, 130]
        consultas_emergencia = [40, 50, 60, 55, 70, 65]
        tipos_consulta = ["Geral", "Especializada", "Emergência"]
        total_consultas = [1000, 700, 340]

        # Criação dos gráficos usando subplots
        figura = plt.figure(figsize=(12, 8), dpi=100)
        gs = figura.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Gráfico 1: Evolução Mensal (Linha com área)
        ax1 = figura.add_subplot(gs[0, :])
        ax1.fill_between(meses, consultas_geral, alpha=0.2, color='#3498db', label='Geral')
        ax1.fill_between(meses, consultas_especializada, alpha=0.2, color='#2ecc71', label='Especializada')
        ax1.fill_between(meses, consultas_emergencia, alpha=0.2, color='#e74c3c', label='Emergência')
        ax1.plot(meses, consultas_geral, marker='o', color='#2980b9', linewidth=2)
        ax1.plot(meses, consultas_especializada, marker='o', color='#27ae60', linewidth=2)
        ax1.plot(meses, consultas_emergencia, marker='o', color='#c0392b', linewidth=2)
        ax1.set_title('Evolução Mensal de Consultas', pad=20, fontsize=12, color='#2c3e50')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='y', linestyle='--', alpha=0.3)
        ax1.legend()

        # Gráfico 2: Distribuição por Tipo (Barras empilhadas)
        ax2 = figura.add_subplot(gs[1, 0])
        cores = ['#3498db', '#2ecc71', '#e74c3c']
        bars = ax2.bar(tipos_consulta, total_consultas, color=cores)
        ax2.set_title('Total de Consultas por Tipo', pad=20, fontsize=12, color='#2c3e50')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.grid(axis='y', linestyle='--', alpha=0.3)
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, color='#2c3e50')

        # Gráfico 3: Distribuição Percentual (Pizza)
        ax3 = figura.add_subplot(gs[1, 1])
        total = sum(total_consultas)
        porcentagens = [x/total*100 for x in total_consultas]
        ax3.pie(porcentagens, labels=tipos_consulta, autopct='%1.1f%%', colors=cores,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax3.set_title('Distribuição Percentual', pad=20, fontsize=12, color='#2c3e50')

        # Ajusta o layout
        plt.tight_layout()

        # Adiciona os gráficos ao frame
        canvas = FigureCanvasTkAgg(figura, graficos_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def _mostrar_relatorio_recursos(self):
        """Exibe o layout do relatório de recursos com visualizações modernas."""
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

        # Frame para os gráficos (direita)
        graficos_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        graficos_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Dados fictícios para os gráficos
        estados = ["Disponível", "Fora de stock", "Expirado"]
        quantidades = [150, 30, 20]
        tipos = ["Medicamento", "Vacina"]
        quantidades_tipo = [120, 80]
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        consumo_medicamentos = [100, 120, 90, 110, 130, 115]
        consumo_vacinas = [60, 70, 80, 75, 85, 90]

        # Criação dos gráficos usando subplots
        figura = plt.figure(figsize=(12, 8), dpi=100)
        gs = figura.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Gráfico 1: Distribuição por Estado (Barras horizontais)
        ax1 = figura.add_subplot(gs[0, 0])
        cores = ['#2ecc71', '#f1c40f', '#e74c3c']
        bars = ax1.barh(estados, quantidades, color=cores, height=0.6)
        ax1.set_title('Distribuição por Estado', pad=20, fontsize=12, color='#2c3e50')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        ax1.grid(axis='x', linestyle='--', alpha=0.3)
        for bar in bars:
            width = bar.get_width()
            ax1.text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}',
                    ha='left', va='center', fontsize=10, color='#2c3e50')

        # Gráfico 2: Distribuição por Tipo (Pizza)
        ax2 = figura.add_subplot(gs[0, 1])
        ax2.pie(quantidades_tipo, labels=tipos, autopct='%1.1f%%', colors=['#3498db', '#e84393'],
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax2.set_title('Distribuição por Tipo', pad=20, fontsize=12, color='#2c3e50')

        # Gráfico 3: Consumo Mensal (Área)
        ax3 = figura.add_subplot(gs[1, :])
        ax3.fill_between(meses, consumo_medicamentos, alpha=0.2, color='#3498db', label='Medicamentos')
        ax3.fill_between(meses, consumo_vacinas, alpha=0.2, color='#e84393', label='Vacinas')
        ax3.plot(meses, consumo_medicamentos, marker='o', color='#2980b9', linewidth=2)
        ax3.plot(meses, consumo_vacinas, marker='o', color='#c0392b', linewidth=2)
        ax3.set_title('Consumo Mensal', pad=20, fontsize=12, color='#2c3e50')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(axis='y', linestyle='--', alpha=0.3)
        ax3.legend()

        # Ajusta o layout
        plt.tight_layout()

        # Adiciona os gráficos ao frame
        canvas = FigureCanvasTkAgg(figura, graficos_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def _mostrar_relatorio_campanhas(self):
        """Exibe o layout do relatório de campanhas com visualizações modernas."""
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

        # Frame para os gráficos (direita)
        graficos_frame = ttk.Frame(self.conteudo_frame, style="Custom.TFrame", padding=10)
        graficos_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Dados fictícios para os gráficos
        estados = ["Ativa", "Encerrada"]
        quantidades = [5, 3]
        grupos_alvo = ["Bebês", "Crianças", "Jovens", "Adultos", "Idosos"]
        participantes = [100, 150, 120, 200, 180]
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        campanhas_ativas = [2, 3, 4, 4, 5, 5]
        campanhas_encerradas = [1, 1, 2, 2, 2, 3]

        # Criação dos gráficos usando subplots
        figura = plt.figure(figsize=(12, 8), dpi=100)
        gs = figura.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Gráfico 1: Estado das Campanhas (Barras horizontais)
        ax1 = figura.add_subplot(gs[0, 0])
        cores = ['#2ecc71', '#e74c3c']
        bars = ax1.barh(estados, quantidades, color=cores, height=0.6)
        ax1.set_title('Estado das Campanhas', pad=20, fontsize=12, color='#2c3e50')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        ax1.grid(axis='x', linestyle='--', alpha=0.3)
        for bar in bars:
            width = bar.get_width()
            ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{int(width)}',
                    ha='left', va='center', fontsize=10, color='#2c3e50')

        # Gráfico 2: Participantes por Grupo-Alvo (Barras)
        ax2 = figura.add_subplot(gs[0, 1])
        bars = ax2.bar(grupos_alvo, participantes, color='#3498db')
        ax2.set_title('Participantes por Grupo-Alvo', pad=20, fontsize=12, color='#2c3e50')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.grid(axis='y', linestyle='--', alpha=0.3)
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, color='#2c3e50')

        # Gráfico 3: Evolução Mensal (Área)
        ax3 = figura.add_subplot(gs[1, :])
        ax3.fill_between(meses, campanhas_ativas, alpha=0.2, color='#2ecc71', label='Ativas')
        ax3.fill_between(meses, campanhas_encerradas, alpha=0.2, color='#e74c3c', label='Encerradas')
        ax3.plot(meses, campanhas_ativas, marker='o', color='#27ae60', linewidth=2)
        ax3.plot(meses, campanhas_encerradas, marker='o', color='#c0392b', linewidth=2)
        ax3.set_title('Evolução Mensal das Campanhas', pad=20, fontsize=12, color='#2c3e50')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(axis='y', linestyle='--', alpha=0.3)
        ax3.legend()

        # Ajusta o layout
        plt.tight_layout()

        # Adiciona os gráficos ao frame
        canvas = FigureCanvasTkAgg(figura, graficos_frame)
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