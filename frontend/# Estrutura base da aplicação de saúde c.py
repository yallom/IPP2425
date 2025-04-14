# Sistema de Gestão de Saúde Comunitária com UI Inspirada em Grandes Apps de Saúde
# Interface gráfica com design moderno estilo MyChart / Doctolib / NHS App

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import datetime

# Dados simulados
utilizadores = {"admin": "admin123", "medico1": "med123", "paciente1": "pac123"}
utilizador_atual = None

pacientes = {}
consultas = []
campanhas = {}
medicamentos = {"Paracetamol": 100, "Vacina COVID": 50}
modo_escuro = False

# Tema cores
cores = {
    "light": {"bg": "#FAFAFA", "fg": "#000000", "header": "#1976D2", "btn": "#1976D2", "btn_fg": "white"},
    "dark": {"bg": "#121212", "fg": "#ffffff", "header": "#333333", "btn": "#BB86FC", "btn_fg": "black"},
}

# Função para alternar modo escuro

def alternar_modo():
    global modo_escuro
    modo_escuro = not modo_escuro
    root.destroy()
    iniciar_app(utilizador_atual)

# Autenticação

def autenticar():
    def verificar():
        user = entry_user.get()
        pw = entry_pass.get()
        if user in utilizadores and utilizadores[user] == pw:
            login.destroy()
            iniciar_app(user)
        else:
            messagebox.showerror("Erro", "Credenciais inválidas")

    login = tk.Tk()
    login.title("Login - Saúde Comunitária")
    login.geometry("400x600")  # Dimensão ajustada para um design compacto
    login.configure(bg="#FAFAFA")  # Fundo branco

    # Cabeçalho com design moderno e ícone
    header_frame = tk.Frame(login, bg="#1976D2", height=150)  # Fundo azul
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="🩺 Saúde Comunitária", font=("Helvetica", 24, "bold"),
             bg="#1976D2", fg="white").pack(expand=True, pady=20)

    # Caixa principal que contém todos os elementos
    main_frame = tk.Frame(login, bg="white", bd=2, relief="groove", highlightbackground="#1976D2", highlightthickness=2)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=350)  # Ajustado para acomodar os elementos

    # Campo "Utilizador"
    tk.Label(main_frame, text="Utilizador", font=("Helvetica", 12, "bold"),
             bg="white", fg="#1976D2").grid(row=0, column=0, sticky='w', pady=10, padx=10)
    entry_user = tk.Entry(main_frame, width=25, font=("Helvetica", 12), relief="flat", bd=2, highlightbackground="#1976D2",
                          highlightthickness=1)
    entry_user.grid(row=0, column=1, pady=10, padx=10)

    # Campo "Palavra-passe"
    tk.Label(main_frame, text="Palavra-passe", font=("Helvetica", 12, "bold"),
             bg="white", fg="#1976D2").grid(row=1, column=0, sticky='w', pady=10, padx=10)
    entry_pass = tk.Entry(main_frame, show="*", width=25, font=("Helvetica", 12), relief="flat", bd=2,
                          highlightbackground="#1976D2", highlightthickness=1)
    entry_pass.grid(row=1, column=1, pady=10, padx=10)

    # Botão de login estilizado
    btn_login = tk.Button(main_frame, text="Entrar", command=verificar,
                          bg="#1976D2", fg="white", font=("Helvetica", 14, "bold"),
                          width=20, height=2, relief="flat", bd=0, activebackground="#145A86", activeforeground="white")
    btn_login.grid(row=2, column=0, columnspan=2, pady=20)

    # Rodapé com informações
    footer = tk.Label(login, text="© Saúde Comunitária 2025", font=("Helvetica", 10),
                      bg="#FAFAFA", fg="#1976D2")
    footer.pack(side="bottom", pady=10)

    login.mainloop()

# Funções auxiliares

def gerar_id_paciente(nome):
    return f"{len(pacientes)+1:03d}_{nome.split()[0]}"

def guardar_dados_em_ficheiro(id_nome):
    id_pac = next((k for k, v in pacientes.items() if v['nome'] == id_nome), None)
    if id_pac:
        nome = pacientes[id_pac]['nome']
        path = f"{id_pac}_{nome.replace(' ', '_')}.txt"
        with open(path, 'w') as f:
            for k, v in pacientes[id_pac].items():
                f.write(f"{k}: {v}\n")
        messagebox.showinfo("Sucesso", f"Dados guardados em {path}")
    else:
        messagebox.showerror("Erro", "Paciente não encontrado")

def carregar_dados_de_ficheiro():
    ficheiro = simpledialog.askstring("Ficheiro", "Nome do ficheiro:")
    if ficheiro and os.path.exists(ficheiro):
        with open(ficheiro, 'r') as f:
            dados = f.readlines()
        paciente = {}
        for linha in dados:
            chave, valor = linha.strip().split(': ', 1)
            paciente[chave] = valor
        pacientes[paciente['id']] = paciente
        messagebox.showinfo("Sucesso", "Dados carregados com sucesso")
    else:
        messagebox.showerror("Erro", "Ficheiro não encontrado")

# APP PRINCIPAL

def iniciar_app(user):
    global utilizador_atual, root
    utilizador_atual = user

    tema = 'dark' if modo_escuro else 'light'
    cor = cores[tema]

    root = tk.Tk()
    root.title("Dashboard - Saúde Comunitária")
    root.geometry("1000x700")
    root.configure(bg=cor['bg'])

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background=cor['bg'], borderwidth=0)
    style.configure("TFrame", background=cor['bg'])
    style.configure("TButton", font=("Helvetica", 11), background=cor['btn'], foreground=cor['btn_fg'])
    style.configure("TLabel", background=cor['bg'], foreground=cor['fg'], font=("Helvetica", 11))

    header = tk.Label(root, text=f"Bem-vindo, {utilizador_atual}", font=("Helvetica", 14, "bold"), 
                      bg=cor['header'], fg=cor['fg'])
    header.pack(fill="x", pady=5)

    ttk.Button(root, text="Alternar Modo", command=alternar_modo).pack(pady=5)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=20, pady=10)

    # PÁGINA PACIENTES
    frame_pacientes = ttk.Frame(notebook)
    notebook.add(frame_pacientes, text="👥 Pacientes")

    entry_nome = tk.Entry(frame_pacientes, width=40, font=("Helvetica", 12))
    entry_nome.pack(pady=10)

    listbox_pacientes = tk.Listbox(frame_pacientes, width=60, height=10, font=("Helvetica", 11))
    listbox_pacientes.pack(pady=10)

    def adicionar_paciente():
        nome = entry_nome.get()
        if nome:
            idp = gerar_id_paciente(nome)
            pacientes[idp] = {"id": idp, "nome": nome, "historial": [], "consultas": []}
            listbox_pacientes.insert(tk.END, f"{idp} - {nome}")
            entry_nome.delete(0, tk.END)

    def ver_paciente():
        sel = listbox_pacientes.curselection()
        if sel:
            valor = listbox_pacientes.get(sel)
            idp = valor.split(' ')[0]
            pac = pacientes[idp]
            messagebox.showinfo("Dados do Paciente", f"ID: {idp}\nNome: {pac['nome']}\nConsultas: {len(pac['consultas'])}")

    ttk.Button(frame_pacientes, text="➕ Adicionar", command=adicionar_paciente).pack()
    ttk.Button(frame_pacientes, text="🔍 Ver Dados", command=ver_paciente).pack()
    ttk.Button(frame_pacientes, text="💾 Guardar", command=lambda: guardar_dados_em_ficheiro(entry_nome.get())).pack()
    ttk.Button(frame_pacientes, text="📂 Carregar", command=carregar_dados_de_ficheiro).pack()

    # CONSULTAS
    frame_consultas = ttk.Frame(notebook)
    notebook.add(frame_consultas, text="📋 Consultas")

    text_consultas = tk.Text(frame_consultas, height=15, width=90, font=("Courier New", 10))
    text_consultas.pack(pady=10)

    def registar_consulta():
        nome = simpledialog.askstring("Paciente", "Nome do paciente:")
        medico = simpledialog.askstring("Médico", "Nome do médico:")
        if nome and medico:
            idp = [k for k, v in pacientes.items() if v['nome'] == nome]
            if idp:
                consulta = f"Consulta com {medico} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                pacientes[idp[0]]['consultas'].append(consulta)
                consultas.append(consulta)
                text_consultas.insert(tk.END, f"{consulta}\n")

    ttk.Button(frame_consultas, text="➕ Nova Consulta", command=registar_consulta).pack(pady=5)

    # RELATÓRIOS
    frame_relatorios = ttk.Frame(notebook)
    notebook.add(frame_relatorios, text="📊 Relatórios")

    canvas_frame = ttk.Frame(frame_relatorios)
    canvas_frame.pack(fill="both", expand=True)

    def gerar_relatorio(frame):
        for widget in frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        faixas = ['0-18', '19-35', '36-60', '60+']
        vacinados = [20, 40, 60, 30]  # valores fictícios
        ax.bar(faixas, vacinados, color="#03DAC6")
        ax.set_title("Vacinas por Faixa Etária")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    ttk.Button(frame_relatorios, text="📈 Gerar Relatório", command=lambda: gerar_relatorio(canvas_frame)).pack(pady=10)

    # INVENTÁRIO
    frame_inventario = ttk.Frame(notebook)
    notebook.add(frame_inventario, text="💊 Inventário")

    listbox_meds = tk.Listbox(frame_inventario, width=50, font=("Helvetica", 11))
    listbox_meds.pack(pady=10)

    def atualizar_inventario():
        listbox_meds.delete(0, tk.END)
        for k, v in medicamentos.items():
            listbox_meds.insert(tk.END, f"{k}: {v} unidades")

    ttk.Button(frame_inventario, text="🔄 Atualizar", command=atualizar_inventario).pack()
    atualizar_inventario()

    # CONFIGURAÇÕES
    frame_configuracoes = ttk.Frame(notebook)
    notebook.add(frame_configuracoes, text="⚙️ Configurações")

    def alterar_senha():
        nova_senha = simpledialog.askstring("Alterar Senha", "Digite a nova senha:")
        if nova_senha:
            utilizadores[utilizador_atual] = nova_senha
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")

    ttk.Button(frame_configuracoes, text="🔒 Alterar Senha", command=alterar_senha).pack(pady=10)

    # OUTRAS CONFIGURAÇÕES
    ttk.Label(frame_configuracoes, text="Outras configurações podem ser adicionadas aqui.", font=("Helvetica", 12)).pack(pady=10)

    # PERFIL DO UTILIZADOR
    frame_perfil = ttk.Frame(notebook)
    notebook.add(frame_perfil, text="👤 Perfil")

    ttk.Label(frame_perfil, text=f"Nome de Utilizador: {utilizador_atual}", font=("Helvetica", 14)).pack(pady=10)
    ttk.Label(frame_perfil, text="Funções disponíveis:", font=("Helvetica", 12, "bold")).pack(pady=5)

    def logout():
        root.destroy()
        autenticar()

    ttk.Button(frame_perfil, text="🔄 Logout", command=logout).pack(pady=10)

    ttk.Label(frame_perfil, text="Mais informações sobre o utilizador podem ser exibidas aqui.", font=("Helvetica", 12)).pack(pady=10)

    footer = tk.Label(root, text=f"Utilizador: {utilizador_atual} | Projeto IPP 2025", font=("Helvetica", 10), 
                      bg=cor['header'], fg=cor['fg'])
    footer.pack(side="bottom", fill="x", pady=5)

    root.mainloop()

# Iniciar aplicação
autenticar()
