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


from Controller import GestorPacientes, GestorMedicos
from Modell import Paciente, Medico





class Interface_Paciente:
    
    def __init__(self, parent):
        self.lista_pacientes = []
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.risco = ["Muito Elevado","Elevado", "Médio", "Baixo"]
        self.sangue = ["A+","A-", "B+", "B-", "AB+","AB-", "O+","O-"]
        self.doencas = ["Diabetes", "Asma", "Hipertensão", "Outras"]
        
        #self.root = root
        self.gestor = GestorPacientes()
        self.gestor.carregar_de_ficheiro()

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

        colunas = ("id","nome", "idade", "morada", "sexo", "gravidez", "sangue", "doença", "risco","histórico")
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
        self.tabela.heading("histórico", text="Histórico")

        for col in colunas:
            self.tabela.column(col, anchor=tk.CENTER, width=150)

        self.tabela.pack(fill="both", expand=True)

    def atualizar_tabela(self):
        self.tabela.delete(*self.tabela.get_children())
        for paciente in self.gestor.listar_pacientes():
            self.tabela.insert("", tk.END, values=(paciente.id, paciente.nome, paciente.idade, paciente.morada, paciente.sexo, paciente.gravidez, paciente.sangue, paciente.doença, paciente.risco, paciente.historico_consultas))

    def abrir_formulario_adicao(self):
        janela_pacientes = tk.Toplevel()
        janela_pacientes.title("Adicionar Paciente")
        janela_pacientes.geometry("400x600")

        def adicionar_paciente():
            nome = entry_nome.get()
            idade = int(entry_idade.get())
            morada = entry_concelho.get()
            sexo = sexo_var.get()
            gravida = "Sim" if var_gravidez.get() else "Não"
            sangue = opcoes_sangue.get()
            doencas_escolhidas = [lista_doencas.get(i) for i in lista_doencas.curselection()] if doenca_var.get() else []

            if nome and idade and morada and sexo and sangue:
                novo_paciente = Paciente(nome, idade, sexo, sangue, morada, doencas_escolhidas, gravida)
                risco = novo_paciente.risco_paciente()
                self.gestor.adicionar_paciente(novo_paciente)
                self.gestor.guardar_em_ficheiro()
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")
                janela_pacientes.destroy()
            else:
                label_name = tk.Label(janela_pacientes, text="É preciso preencher todos os campos.")
                label_name.pack(pady=4)

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
        entry_idade.insert(0, valores[2])
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
            doenca = ", ".join(doencas) if doencas else "Nenhuma"

            if nome and idade and concelho and sexo and sangue:
                try:
                    idade = int(idade)
                except ValueError:
                    messagebox.showerror("Erro", "A idade deve ser um número inteiro.")
                    return

                paciente_atualizado = Paciente(nome, idade, sexo, sangue, concelho, doenca, gravida)
                risco = paciente_atualizado.risco_paciente()
                id_paciente = valores[0]
                self.gestor.atualizar_paciente(id_paciente, paciente_atualizado)
                self.gestor.guardar_em_ficheiro()
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
        confirmar = messagebox.askyesno("Confirmar", f"Tem a certeza que quer remover o paciente com ID {paciente_id}?")
        if confirmar:
            self.gestor.remover_paciente(paciente_id)
            self.gestor.guardar_em_ficheiro()
            self.atualizar_tabela()
            self.limpar_campos()

    

    def aplicar_filtros(self):
        filtro_nome = self.entry_pesquisa.get().lower()
        filtro_esp = self.filtro_esp.get().lower()

        dados_filtrados = []
        for paciente in self.lista_pacientes:
            nome = paciente[1].lower()
            especialidade = paciente[4].lower()

            nome_match = filtro_nome in nome
            risco_match = filtro_esp == "todas" or especialidade == filtro_esp

            if nome_match and risco_match:
                dados_filtrados.append(paciente)

        print(f"Filtrados: {len(dados_filtrados)} pacientes")
        self.atualizar_tabela(dados_filtrados)


    def get_frame(self):
        return self.frame  # ou self.main_frame, dependendo do nom
    

class Interface_Medicos:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.especialidades = [
            "Cardiologia", "Ginecologia", "Neurologia", "Oftalmologia",
            "Pediatria", "Pneumonologia", "Psiquiatria"]
        self.gestor = GestorMedicos()
        self.gestor.carregar_de_ficheiro()
        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):

        #Titulo
        titulo = tk.Label(self.frame, text="Gestão de Médicos", font=("Segoe UI", 16, "bold"), fg="#2c3e50", bg="#f5f5f5")
        titulo.pack(pady=10)

        topo = tk.Frame(self.frame, bg="#f5f5f5")
        topo.pack(fill="x", pady=10, padx=20)

        # Filtro por especialidade
        ttk.Label(topo, text="Filtrar especialidades:", background="#f5f5f5").pack(side=tk.LEFT)
        self.filtro_esp = ttk.Combobox(topo, values=["Todas"] + self.especialidades, state="readonly", width=18)
        self.filtro_esp.set("Todas")
        self.filtro_esp.pack(side=tk.LEFT, padx=5)
        self.filtro_esp.bind("<<ComboboxSelected>>", lambda e: self.aplicar_filtros())

        # Barra de pesquisa
        tk.Label(topo, text="Pesquisar nome:", bg="#f5f5f5").pack(side=tk.LEFT, padx=(20, 2))
        self.entry_pesquisa = tk.Entry(topo, width=20)
        self.entry_pesquisa.pack(side=tk.LEFT)
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.aplicar_filtros())

        # Botões (à direita)
        botoes_medicos = tk.Frame(topo, bg="#f5f5f5")
        botoes_medicos.pack(side=tk.RIGHT)

        btn_adicionar = tk.Button(botoes_medicos, text="+ Adicionar Médico", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.formulario_adicao_medico)
        btn_adicionar.pack(side=tk.LEFT, padx=5)

        btn_editar = tk.Button(botoes_medicos, text="Editar Médico", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.editar_medico)
        btn_editar.pack(side=tk.LEFT, padx=5)

        btn_editar = tk.Button(botoes_medicos, text="Eliminar Médico", bg="#2c3e50", fg="white", font=("Segoe UI", 10), width=20, command=self.eliminar_medico)
        btn_editar.pack(side=tk.LEFT, padx=5)  


        # Tabela
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#2c3e50", foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

        frame_tabela = tk.Frame(self.frame, bg="#f5f5f5")
        frame_tabela.pack(fill="both", expand=True, padx=20)

        # Scrollbar vertical
        scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        #Scrollbar horizontal
        scroll_x = ttk.Scrollbar(frame_tabela, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        colunas = ("id", "nome", "especialidade", "disponibilidade")

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            height=12,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tabela.yview)
        scroll_x.config(command=self.tabela.xview)
        

        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("especialidade", text="Especialidade")
        self.tabela.heading("disponibilidade", text="Disponibilidade")

        # Depois de criares a tabela e definir os cabeçalhos:

        self.tabela.column("id", width=50, anchor=tk.CENTER)  # diminui para 50 pixels
        self.tabela.column("nome", width=160, anchor=tk.CENTER)  # mantém como está
        self.tabela.column("especialidade", width=160, anchor=tk.CENTER)  # mantém como está
        self.tabela.column("disponibilidade", width=1000, anchor=tk.CENTER)  # aumenta para 300 pixels


        self.tabela.pack(fill="both", expand=True)
        

    def abrir_visualizador_disponibilidade(self, disponibilidade):
        janela_disp = tk.Toplevel()
        janela_disp.title("Disponibilidade do Médico")
        janela_disp.geometry("600x350")

        dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        horarios = [f"{h:02d}:00-{h+2:02d}:00" for h in range(8, 20, 2)]

        # Cabeçalhos
        for i, dia in enumerate(dias):
            tk.Label(janela_disp, text=dia, font=("Segoe UI", 10, "bold")).grid(row=0, column=i+1, padx=5, pady=5)

        for j, hora in enumerate(horarios):
            tk.Label(janela_disp, text=hora).grid(row=j+1, column=0, padx=5, pady=5)
            for i, dia in enumerate(dias):
                bloco = f"{dia} {hora}"
                var = tk.BooleanVar(value=(bloco in disponibilidade))
                chk = tk.Checkbutton(janela_disp, variable=var, state="disabled")
                chk.grid(row=j+1, column=i+1)


    def formulario_adicao_medico(self):
        janela_adicao = tk.Toplevel()
        janela_adicao.title("Adicionar Médico")
        janela_adicao.geometry("400x300")
        self.disponibilidade_selecionada = []

        # Função para atualizar a disponibilidade selecionada
        def atualizar_disponibilidade(lista):
            self.disponibilidade_selecionada = lista

        # Função para criar o novo médico
        def adicionar_medico(): 
            nome = entry_nome.get()
            especialidade = combo_esp.get()
            disponibilidade = self.disponibilidade_selecionada

            disponibilidade_flat = []
            for item in disponibilidade:
                if isinstance(item, list):
                    disponibilidade_flat.extend(item)
                else:
                    disponibilidade_flat.append(item)

            if nome and especialidade and disponibilidade:
                matriz = Medico.lista_para_matriz(disponibilidade_flat)
                novo_medico = Medico(nome, especialidade, matriz)
                self.gestor.adicionar_medico(novo_medico)
                self.gestor.guardar_em_ficheiro()
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!")
                janela_adicao.destroy()
            else:
                messagebox.showwarning("Campos incompletos", "Preencha todos os campos!")

        # Interface do formulário
        tk.Label(janela_adicao, text="Nome:").pack(pady=4)
        entry_nome = tk.Entry(janela_adicao, width=30)
        entry_nome.pack(pady=4)

        tk.Label(janela_adicao, text="Especialidade:").pack(pady=4)
        combo_esp = ttk.Combobox(janela_adicao, values=self.especialidades, state="readonly")
        combo_esp.pack(pady=4)

        btn_disp = tk.Button(
            janela_adicao,
            text="Selecionar Disponibilidade",
            command=lambda: self.selecionar_disponibilidade(atualizar_disponibilidade)
        )
        btn_disp.pack(pady=4)

        tk.Button(janela_adicao, text="Adicionar Médico", command=adicionar_medico).pack(pady=10)


    def selecionar_disponibilidade(self, callback, disponibilidade_inicial=None):
        janela_disponibilidade = tk.Toplevel()
        janela_disponibilidade.title("Selecionar Disponibilidade")
        janela_disponibilidade.geometry("500x350")

        dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        horarios = [f"{h:02d}:00-{h+2:02d}:00" for h in range(8, 20, 2)]  # 8:00 às 20:00 em blocos de 2h

        check_vars = {}

        # Cabeçalhos
        for i, dia in enumerate(dias):
            tk.Label(janela_disponibilidade, text=dia, font=("Segoe UI", 10, "bold")).grid(row=0, column=i+1, padx=5, pady=5)

        for j, hora in enumerate(horarios):
            tk.Label(janela_disponibilidade, text=hora).grid(row=j+1, column=0, padx=5, pady=5)
            for i, dia in enumerate(dias):
                var = tk.BooleanVar()
                chk = tk.Checkbutton(janela_disponibilidade, variable=var)
                chk.grid(row=j+1, column=i+1)
                check_vars[(dia, hora)] = var

        def carregar_disponibilidade_em_checkbuttons(check_vars, matriz):
            for i, hora in enumerate(horarios):
                for j, dia in enumerate(dias):
                    check_vars[(dia, hora)].set(matriz[i][j])

        # Se fornecida disponibilidade inicial (lista), converte e carrega
        if disponibilidade_inicial:
            disponibilidade_flat = []
            for item in disponibilidade_inicial:
                if isinstance(item, list):
                    disponibilidade_flat.extend(item)
                else:
                    disponibilidade_flat.append(item)
            matriz = Medico.lista_para_matriz(disponibilidade_flat)
            carregar_disponibilidade_em_checkbuttons(check_vars, matriz)

        # Botão confirmar seleção
        def salvar():
            disponibilidade = []
            for (dia, hora), var in check_vars.items():
                if var.get():
                    disponibilidade.append(f"{dia} {hora}")
            callback(disponibilidade)
            janela_disponibilidade.destroy()

        tk.Button(janela_disponibilidade, text="Confirmar", command=salvar).grid(
            row=len(horarios)+1, column=0, columnspan=len(dias)+1, pady=10
        )


    def editar_medico(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um médico para editar.")
            return

        valores = self.tabela.item(selecionado, "values")
        if not valores:
            return

        id_medico = valores[0]
        medico = self.gestor.obter_medico(id_medico)
        if not medico:
            messagebox.showerror("Erro", "Médico não encontrado.")
            return

        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar Médico")
        janela_edicao.geometry("400x350")

        tk.Label(janela_edicao, text="Nome:").pack(pady=4)
        entry_nome = tk.Entry(janela_edicao, width=30)
        entry_nome.insert(0, medico.name)
        entry_nome.pack(pady=4)

        tk.Label(janela_edicao, text="Especialidade:").pack(pady=4)
        combo_esp = ttk.Combobox(janela_edicao, values=self.especialidades, state="readonly")
        combo_esp.set(medico.speciality)
        combo_esp.pack(pady=4)

        tk.Label(janela_edicao, text="Disponibilidade:").pack(pady=4)

        # Se estiver armazenando matriz, converta para lista
        if isinstance(medico.servico, list) and all(isinstance(row, list) for row in medico.servico):
            lista_disp = Medico.lista_para_matriz(medico.servico)  # método que converte matriz -> lista de strings
        else:
            lista_disp = medico.servico  # já está no formato correto
        
        def atualizar_disp(nova_disp):
            medico.servico = nova_disp

        btn_disp = tk.Button(
            janela_edicao,
            text="Editar Disponibilidade",
            command=lambda: self.selecionar_disponibilidade(atualizar_disp, lista_disp)
        )
        btn_disp.pack(pady=4)

        def salvar():
            nome = entry_nome.get()
            esp = combo_esp.get()
            disp = medico.servico  # atualizada na seleção

            if nome and esp and disp:
                medico.name = nome
                medico.speciality = esp
                medico.servico = disp
                self.gestor.guardar_em_ficheiro()
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!")
                janela_edicao.destroy()
            else:
                messagebox.showwarning("Campos incompletos", "Preencha todos os campos!")

        tk.Button(janela_edicao, text="Salvar Alterações", command=salvar).pack(pady=10)


    def atualizar_tabela(self):
        self.tabela.delete(*self.tabela.get_children())
        for medico in self.gestor.listar_medicos():
            print(medico.servico)
            disponibilidade_legivel = Medico.formatar_disponibilidade(medico.servico)
            self.tabela.insert("", tk.END, values=(medico.id, medico.name, medico.speciality, disponibilidade_legivel))


    def eliminar_medico(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um médico para eliminar.")
            return

        valores = self.tabela.item(selecionado, "values")
        if not valores:
            return

        id_medico = valores[0]  # considerando que a coluna ID está no índice 0
        confirmado = messagebox.askyesno("Confirmar", f"Deseja eliminar o médico {valores[1]}?")
        if confirmado:
            self.gestor.remover_medico(id_medico)
            self.gestor.guardar_em_ficheiro()
            self.atualizar_tabela()

    def aplicar_filtros(self):
        filtro_nome = self.entry_pesquisa.get().lower()
        filtro_esp = self.filtro_esp.get()

        self.tabela.delete(*self.tabela.get_children())
        for medico in self.gestor.listar_medicos():
            nome_match = filtro_nome in medico.name.lower()
            esp_match = (filtro_esp == "Todas") or (medico.speciality == filtro_esp)
            if nome_match and esp_match:
                disponibilidade_legivel = Medico.formatar_disponibilidade(medico.servico)
                self.tabela.insert("", tk.END, values=(medico.id, medico.name, medico.speciality, disponibilidade_legivel))



    def get_frame(self):
        return self.frame
    
class Consultas:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f5f5f5")
        self.consultas = []  # Lista de consultas (paciente, medico, especialidade, data)
        self.criar_interface()

    def criar_interface(self):
        # Título
        titulo = tk.Label(self.frame, text="Gestão de Consultas",font=("Segoe UI", 16, "bold"), fg="#2c3e50", bg="#f5f5f5")
        titulo.pack(pady=10)

        conteudo = tk.Frame(self.frame, bg="#f5f5f5")
        conteudo.pack(fill="both", expand=True, padx=20)

        # ------------------ LADO ESQUERDO - TABELA + BOTÕES ------------------
        esquerda = tk.Frame(conteudo, bg="#f5f5f5")
        esquerda.pack(side="left", fill="both", expand=True)

        # Botões no topo da tabela
        botoes_frame = tk.Frame(esquerda, bg="#f5f5f5")
        botoes_frame.pack(pady=5)

        btn_nova_consulta = tk.Button(botoes_frame, text="+ Marcar Consulta", bg="#2c3e50", fg="white",font=("Segoe UI", 10), command=self.abrir_formulario_consulta)
        btn_nova_consulta.pack(side=tk.LEFT, padx=5)

        btn_editar_consulta = tk.Button(botoes_frame, text="Editar Consulta", bg="#2c3e50", fg="white",font=("Segoe UI", 10), command=self.editar_consulta)
        btn_editar_consulta.pack(side=tk.LEFT, padx=5)

        btn_eliminar_consulta = tk.Button(botoes_frame, text="Eliminar Consulta", bg="#c0392b", fg="white",font=("Segoe UI", 10), command=self.eliminar_consulta)
        btn_eliminar_consulta.pack(side=tk.LEFT, padx=5)

        # Estilo da Tabela
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#2c3e50", foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

        # Tabela de consultas
        colunas = ("paciente", "medico", "especialidade", "data")
        self.tabela = ttk.Treeview(esquerda, columns=colunas, show="headings", height=12)

        for col in colunas:
            self.tabela.heading(col, text=col.capitalize())
            self.tabela.column(col, anchor=tk.CENTER, width=130)

        self.tabela.pack(fill="both", expand=True, pady=5)

        # ------------------ LADO DIREITO - CALENDÁRIO + LISTA ------------------
        direita = tk.Frame(conteudo, bg="#f5f5f5")
        direita.pack(side="right", fill="both", expand=True, padx=(20, 0))

        frame_calendario = tk.Frame(direita, bg="#f5f5f5")
        frame_calendario.pack(fill="both", expand=True)

        self.calendario = Calendar(frame_calendario, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendario.pack(expand=True, pady=5)

        frame_lista = tk.Frame(direita, bg="#f5f5f5")
        frame_lista.pack(fill="both", expand=True)

        self.lista_eventos = tk.Listbox(frame_lista, font=("Segoe UI", 10))
        self.lista_eventos.pack(fill="both", expand=True, padx=10, pady=5)

        self.calendario.bind("<<CalendarSelected>>", self.atualizar_lista_eventos)

    def abrir_formulario_consulta(self):
        janela_novaconsulta = tk.Toplevel()
        janela_novaconsulta.title("Nova Consulta")
        janela_novaconsulta.geometry("400x350")

        tk.Label(janela_novaconsulta, text="Paciente:").pack(pady=4)
        entry_paciente = tk.Entry(janela_novaconsulta, width=30)
        entry_paciente.pack(pady=4)

        tk.Label(janela_novaconsulta, text="Médico:").pack(pady=4)
        entry_medico = tk.Entry(janela_novaconsulta, width=30)
        entry_medico.pack(pady=4)

        tk.Label(janela_novaconsulta, text="Especialidade:").pack(pady=4)
        entry_esp = tk.Entry(janela_novaconsulta, width=30)
        entry_esp.pack(pady=4)

        tk.Label(janela_novaconsulta, text="Data e Hora (AAAA-MM-DD HH:MM):").pack(pady=4)
        entry_data = tk.Entry(janela_novaconsulta, width=30)
        entry_data.pack(pady=4)

        def guardar():
            paciente = entry_paciente.get()
            medico = entry_medico.get()
            esp = entry_esp.get()
            data = entry_data.get()

            if not (paciente and medico and esp and data):
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
                return

            try:
                datetime.datetime.strptime(data, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido.")
                return

            self.consultas.append((paciente, medico, esp, data))
            self.tabela.insert("", tk.END, values=(paciente, medico, esp, data))
            self.atualizar_lista_eventos(None)
            janela_novaconsulta.destroy()

        tk.Button(janela_novaconsulta, text="Marcar", bg="#2c3e50", fg="white", command=guardar).pack(pady=10)

    def editar_consulta(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma consulta para editar.")
            return

        valores = self.tabela.item(selecionado, "values")
        if not valores:
            return

        idx = self.tabela.index(selecionado)

        janela_editarconsulta = tk.Toplevel()
        janela_editarconsulta.title("Editar Consulta")
        janela_editarconsulta.geometry("400x350")

        tk.Label(janela_editarconsulta, text="Paciente:").pack(pady=4)
        entry_paciente = tk.Entry(janela_editarconsulta, width=30)
        entry_paciente.insert(0, valores[0])
        entry_paciente.pack(pady=4)

        tk.Label(janela_editarconsulta, text="Médico:").pack(pady=4)
        entry_medico = tk.Entry(janela_editarconsulta, width=30)
        entry_medico.insert(0, valores[1])
        entry_medico.pack(pady=4)

        tk.Label(janela_editarconsulta, text="Especialidade:").pack(pady=4)
        entry_esp = tk.Entry(janela_editarconsulta, width=30)
        entry_esp.insert(0, valores[2])
        entry_esp.pack(pady=4)

        tk.Label(janela_editarconsulta, text="Data e Hora (AAAA-MM-DD HH:MM):").pack(pady=4)
        entry_data = tk.Entry(janela_editarconsulta, width=30)
        entry_data.insert(0, valores[3])
        entry_data.pack(pady=4)

        def guardar():
            paciente = entry_paciente.get()
            medico = entry_medico.get()
            esp = entry_esp.get()
            data = entry_data.get()

            if not (paciente and medico and esp and data):
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
                return

            try:
                datetime.datetime.strptime(data, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido.")
                return

            self.consultas[idx] = (paciente, medico, esp, data)
            self.tabela.item(selecionado, values=(paciente, medico, esp, data))
            self.atualizar_lista_eventos(None)
            janela_editarconsulta.destroy()

        tk.Button(janela_editarconsulta, text="Salvar Alterações", bg="#2c3e50", fg="white", command=guardar).pack(pady=10)

    def eliminar_consulta(self):
        selecionado = self.tabela.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma consulta para eliminar.")
            return

        resposta = messagebox.askyesno("Confirmar", "Tem a certeza que quer eliminar esta consulta?")
        if resposta:
            idx = self.tabela.index(selecionado)
            self.tabela.delete(selecionado)
            del self.consultas[idx]
            self.atualizar_lista_eventos(None)

    def atualizar_lista_eventos(self, event):
        data_selecionada = self.calendario.get_date()
        self.lista_eventos.delete(0, tk.END)

        for c in self.consultas:
            if c[3].startswith(data_selecionada):
                self.lista_eventos.insert(tk.END, f"{c[0]} - {c[1]} ({c[2]}) - {c[3][11:]}")

    def get_frame(self):
        return self.frame






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

    


if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = DashboardApp(root)
    root.mainloop()

# --- Interface Principal com Todas as Abas ---

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

        for cat, emoji in categorias:
            if cat == "Pacientes":
                self.gerente_pacientes = Interface_Paciente(self.tabs)
                self.tabs.add(self.gerente_pacientes.get_frame(), text=f"{emoji}  {cat}")
            elif cat == "Médicos": 
                self.gerente_medicos = Interface_Medicos(self.tabs)
                self.tabs.add(self.gerente_medicos.get_frame(), text=f"{emoji}  {cat}")
            elif cat == "Consultas":
                self.gerente_consultas = Consultas(self.tabs)
                self.tabs.add(self.gerente_consultas.get_frame(), text=f"{emoji}  {cat}")
            elif cat == "Campanhas":
                self.gerente_campanhas = CampanhasFrame(self.tabs)
                self.tabs.add(self.gerente_campanhas, text=f"{emoji}  {cat}")
            elif cat == "Recursos":
                self.gerente_recursos = RecursosFrame(self.tabs)
                self.tabs.add(self.gerente_recursos, text=f"{emoji}  {cat}")
            elif cat == "Relatórios":
                frame = ttk.Frame(self.tabs)
                ttk.Label(frame, text="Área de Relatórios (em desenvolvimento)", font=("Segoe UI", 14)).pack(padx=20, pady=20)
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
                recurso["Data de Validade"]
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
                recurso["Tipo"],
                recurso["Nome"],
                recurso["Grupo-Alvo"],
                recurso["Grupo Risco"],
                recurso["Gravidez"],
                recurso["Data de Validade"]
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
        ttk.Button(controles_frame, text="Gerar Relatório", style="App.TButton").pack(side="right")

        # Frame para o conteúdo do relatório (tabela e gráficos)
        self.conteudo_frame = ttk.Frame(self, style="Custom.TFrame")
        self.conteudo_frame.pack(fill="both", expand=True, pady=10)

        # Frame para os botões de exportação (inferior)
        export_botoes_frame = ttk.Frame(self, style="Custom.TFrame")
        export_botoes_frame.pack(fill="x", pady=10)

        

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

    def mostrar_relatorio_campanhas(self):
        """Exibe o relatório de campanhas com tabela e visualizações (gráficos)."""
        # Limpa o frame de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

        # Obtém os dados das campanhas
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

        fig1 = Figure(figsize=(3.5, 2.5), dpi=100) # Reduced height
        ax1 = fig1.add_subplot(111)
        ax1.pie(estado_sizes, labels=estado_labels, autopct='%1.1f%%', colors=estado_colors,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax1.set_title('Estado das Campanhas', fontsize=10, color='#2c3e50')
        
        canvas1 = FigureCanvasTkAgg(fig1, viz_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="x", pady=(0, 10))

        # --- Novo Gráfico: Número de Participantes por Campanha (Barras) ---
        campanhas_nomes = [c["Nome"] for c in campanhas]
        # Ensure "Número de Participantes" is treated as a number, default to 0 if not available or invalid
        participantes_valores = []
        for c in campanhas:
            try:
                # Get the value, default to 0 if not available
                part = c.get("Número de Participantes", 0)
                # Convert to float. This works for both int and float types.
                participantes_valores.append(float(part))
            except (ValueError, TypeError):
                # If conversion fails (e.g., value is not a number), default to 0.0
                participantes_valores.append(0.0) 

        fig2 = Figure(figsize=(4, 3.5), dpi=100) # Adjust size as needed
        ax2 = fig2.add_subplot(111)
        
        # Create bars
        bars = ax2.bar(campanhas_nomes, participantes_valores, color='#3498db') # Azul do tema
        
        ax2.set_title('Número de Participantes por Campanha', fontsize=10, color='#2c3e50')
        ax2.set_ylabel('Nº de Participantes', fontsize=8, color='#2c3e50')
        ax2.tick_params(axis='x', rotation=90, labelsize=7) # Rotate labels for better visibility
        ax2.tick_params(axis='y', labelsize=8)
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval) if yval.is_integer() else round(yval, 2), va='bottom', ha='center', fontsize=7) # Add text slightly above the bar

        fig2.tight_layout() # Adjust layout to prevent overlap

        canvas2 = FigureCanvasTkAgg(fig2, viz_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="x", pady=(10, 0))

    def mostrar_relatorio_consultas(self):
        """Exibe o relatório de consultas (a ser implementado)."""
        # Limpa o frame de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()
            
        # Mensagem temporária
        ttk.Label(self.conteudo_frame, 
                 text="Relatório de Consultas em desenvolvimento...",
                 style="Custom.TLabel").pack(pady=20)

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
            ("Médicos", "🩺"),
            ("Pacientes", "👤"),
            ("Consultas", "📅"),
            ("Campanhas", "📢"),
            ("Recursos", "💉"),
            ("Relatórios", "📊")
        ]

        for cat, emoji in categorias:
            if cat == "Pacientes":
                self.gerente_pacientes = Interface_Paciente(self.tabs)
                self.tabs.add(self.gerente_pacientes.get_frame(), text=f"{emoji}  {cat}")
            elif cat == "Médicos": 
                self.gerente_medicos = Interface_Medicos(self.tabs)
                self.tabs.add(self.gerente_medicos.get_frame(), text=f"{emoji}  {cat}")
            elif cat == "Consultas":
                self.gerente_consultas = Consultas(self.tabs)
                self.tabs.add(self.gerente_consultas.get_frame(), text=f"{emoji}  {cat}")
            elif cat == "Campanhas":
                self.gerente_campanhas = CampanhasFrame(self.tabs)
                self.tabs.add(self.gerente_campanhas, text=f"{emoji}  {cat}")
            elif cat == "Recursos":
                self.gerente_recursos = RecursosFrame(self.tabs)
                self.tabs.add(self.gerente_recursos, text=f"{emoji}  {cat}")
            elif cat == "Relatórios":
                frame = ttk.Frame(self.tabs)
                ttk.Label(frame, text="Área de Relatórios (em desenvolvimento)", font=("Segoe UI", 14)).pack(padx=20, pady=20)
                self.tabs.add(frame, text=f"{emoji}  {cat}")


        footer = tk.Frame(self.root, bg="#eaf0f1", height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        user_info = tk.Label(footer, text="Utilizador: admin | Projeto IPP 2025", bg="#eaf0f1", fg="#2f4f4f", font=("Segoe UI", 9))
        user_info.pack(pady=5)


if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    root.after(10, lambda: DashboardApp(root))
    root.mainloop()