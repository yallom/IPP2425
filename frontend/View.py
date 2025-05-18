import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from tkcalendar import Calendar
import datetime
import json
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