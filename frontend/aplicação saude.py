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

        self.configure(padding=20)

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

        # Título
        ttk.Label(self, text="Gestão de Campanhas de Saúde", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))

        # Filtros e Ações
        filtro_frame = ttk.Frame(self)
        filtro_frame.pack(fill="x", pady=10)

        ttk.Label(filtro_frame, text="Filtrar por:").pack(side="left")
        self.combo_filtro = ttk.Combobox(filtro_frame, values=["Todas", "Ativas", "Encerradas"], state="readonly")
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side="left", padx=5)
        self.combo_filtro.bind("<<ComboboxSelected>>", self.filtrar_campanhas)  # Adiciona evento para filtrar

        # Botão "Nova Campanha"
        ttk.Button(filtro_frame, text="+ Nova Campanha", command=self.abrir_janela_cadastro).pack(side="right")

        # Botão "Eliminar Campanha"
        ttk.Button(filtro_frame, text="Eliminar Campanha", command=self.eliminar_campanha).pack(side="right", padx=5)

        # Tabela de campanhas
        colunas = ("Nome", "Início", "Fim", "Grupo-Alvo", "Estado")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=10)
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=100, anchor="center")

        self.tabela.pack(fill="both", expand=True, pady=10)

        self.tabela.bind("<Double-1>", self.abrir_detalhes_campanha)  # Clique duplo para abrir detalhes

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
        janela.geometry("700x600")
        janela.transient(self)

        # Cria um canvas para permitir a rolagem
        canvas = tk.Canvas(janela)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adiciona a barra de rolagem
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a barra de rolagem
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno para os widgets
        frame_interno = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_interno, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_interno.bind("<Configure>", atualizar_scrollregion)

        ttk.Label(frame_interno, text="Cadastro de Campanha", font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Campos do formulário
        campos = [
            ("ID", "entry"),  # Novo campo para ID
            ("Nome", "entry"),
            ("Data Início", "date"),
            ("Data Fim", "date"),
            ("Grupo Risco", "combobox"),
            ("Grupo-Alvo", "combobox"),
            ("Grávidas", "combobox"),
            ("Sexo", "combobox"),
            ("Recurso", "combobox"),
            ("Item", "combobox"),
            ("Profissionais Atribuídos", "entry"),  # Novo campo
            ("Número de Participantes", "entry"),  # Novo campo
            ("Observações", "text")  # Novo campo
        ]
        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_interno)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=campo).pack(anchor="w")

            if tipo == "entry":
                entry = ttk.Entry(frame)
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="yyyy-mm-dd", width=12, background="darkblue",
                                  foreground="white", borderwidth=2)
            elif tipo == "combobox":
                if campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly")
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly")
                elif campo == "Grávidas":
                    entry = ttk.Combobox(frame, values=["Sim", "Não"], state="readonly")
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly")
                elif campo == "Recurso":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly")
                    entry.bind("<<ComboboxSelected>>", self.atualizar_itens)
                elif campo == "Item":
                    entry = ttk.Combobox(frame, values=[], state="readonly")
            elif tipo == "text":
                entry = tk.Text(frame, height=5, wrap="word")
            entry.pack(fill="x")
            self.entries[campo] = entry

        ttk.Button(frame_interno, text="Guardar", command=self.guardar_campanha).pack(pady=10)

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
        id_campanha = self.entries["ID"].get().strip()  # Novo campo
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
        if not all([id_campanha, nome, data_inicio, data_fim, grupo_risco, grupo_alvo, gravidas, sexo, recurso, item]):
            messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos!")
            return

        # Adiciona a nova campanha
        nova_campanha = {
            "ID": id_campanha,  # Novo campo
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
        self.entries["ID"].winfo_toplevel().destroy()

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
        janela.geometry("700x600")  # Define a largura inicial como 800
        janela.resizable(True, True)  # Permite redimensionamento

        # Cria um canvas para permitir a rolagem
        canvas = tk.Canvas(janela)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adiciona a barra de rolagem
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a barra de rolagem
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno para os widgets
        frame_interno = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_interno, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_interno.bind("<Configure>", atualizar_scrollregion)

        ttk.Label(frame_interno, text="Detalhes da Campanha", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Campos do formulário
        campos = [
            ("ID", "entry"),  # Adiciona o campo ID
            ("Nome", "entry"),
            ("Início", "date"),
            ("Fim", "date"),
            ("Grupo Risco", "combobox"),
            ("Grupo-Alvo", "combobox"),
            ("Grávidas", "combobox"),
            ("Sexo", "combobox"),
            ("Recurso", "combobox"),
            ("Item", "combobox"),
            ("Profissionais atribuídos", "entry"),
            ("Número de participantes", "entry"),
            ("Observações", "text")  # Campo de texto para observações
        ]
        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_interno)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=campo).pack(anchor="w")

            if tipo == "entry":
                entry = ttk.Entry(frame)
                entry.insert(0, campanha.get(campo, ""))  # Preenche com o valor atual ou vazio
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="yyyy-mm-dd", width=12, background="darkblue",
                                  foreground="white", borderwidth=2)
                if campo in campanha:
                    entry.set_date(campanha[campo])  # Preenche com o valor atual
            elif tipo == "combobox":
                if campo == "Grupo Risco":
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly")
                elif campo == "Grupo-Alvo":
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly")
                elif campo == "Grávidas":
                    entry = ttk.Combobox(frame, values=["Sim", "Não"], state="readonly")
                elif campo == "Sexo":
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly")
                elif campo == "Recurso":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly")
                    entry.bind("<<ComboboxSelected>>", self.atualizar_itens)
                elif campo == "Item":
                    entry = ttk.Combobox(frame, values=self.dataset.get(campanha.get("Recurso", ""), []), state="readonly")
                entry.set(campanha.get(campo, ""))  # Preenche com o valor atual ou vazio
            elif tipo == "text":
                entry = tk.Text(frame, height=5, wrap="word")
                entry.insert("1.0", campanha.get(campo, ""))  # Preenche com o valor atual ou vazio
            entry.pack(fill="x")
            self.entries[campo] = entry

        # Botões para salvar ou cancelar
        botoes_frame = ttk.Frame(frame_interno)
        botoes_frame.pack(fill="x", pady=10)
        ttk.Button(botoes_frame, text="Guardar", command=lambda: self.guardar_alteracoes_campanha(campanha, janela)).pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy).pack(side="right", padx=5)

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
        self.configure(padding=20)

        # Inicializa o atributo frames para evitar o AttributeError
        self.master.frames = getattr(self.master, "frames", {})

        # Título
        ttk.Label(self, text="Recursos", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))

        # Botões de ação
        botoes_frame = ttk.Frame(self)
        botoes_frame.pack(fill="x", pady=10)

        # Botão "Novo Medicamento/Vacina"
        ttk.Button(botoes_frame, text="➕ Novo Medicamento/Vacina", command=self.novo_medicamento).pack(side="left", padx=5)

        # Botão "Filtrar"
        ttk.Button(botoes_frame, text="🔍 Filtrar", command=self.filtrar_recursos).pack(side="left", padx=5)

        # Botão "Exportar"
        ttk.Button(botoes_frame, text="⬇️ Exportar", command=self.exportar_dados).pack(side="left", padx=5)

        # Frame para a tabela e scrollbars
        tabela_frame = ttk.Frame(self)
        tabela_frame.pack(fill="both", expand=True, pady=10)

        # Barra de rolagem horizontal
        scrollbar_horizontal = ttk.Scrollbar(tabela_frame, orient="horizontal")
        scrollbar_horizontal.pack(side="bottom", fill="x")

        # Tabela de recursos
        colunas = ("Tipo", "Nome", "Grupo-Alvo", "Grupo Risco", "Gravidez", "Data de Validade", "Quantidade em Stock", "Campanha")
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=15, xscrollcommand=scrollbar_horizontal.set)

        # Configura as barras de rolagem
        scrollbar_horizontal.config(command=self.tabela.xview)

        # Configura as colunas
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=120, anchor="center")

        self.tabela.pack(fill="both", expand=True, pady=10)

        # Dados iniciais (exemplo)
        self.dados = [
            {"Tipo": "Medicamento", "Nome": "Paracetamol", "Grupo-Alvo": "Adultos", "Grupo Risco": "Baixo",
             "Gravidez": "Sim", "Data de Validade": "2025-12-31", "Quantidade em Stock": 100, "Campanha": "Campanha de Vacinação Gripe"},
            {"Tipo": "Vacina", "Nome": "Vacina Gripe", "Grupo-Alvo": "Idosos", "Grupo Risco": "Médio",
             "Gravidez": "Não", "Data de Validade": "2025-10-15", "Quantidade em Stock": 50, "Campanha": "Campanha de Vacinação Gripe"}
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
                recurso["Tipo"], recurso["Nome"], recurso["Grupo-Alvo"], recurso["Grupo Risco"],
                recurso["Gravidez"], recurso["Data de Validade"], recurso["Quantidade em Stock"], recurso["Campanha"]
            ))

    def novo_medicamento(self):
        """Abre uma janela para adicionar um novo medicamento ou vacina."""
        janela = tk.Toplevel(self)
        janela.title("Novo Medicamento/Vacina")
        janela.geometry("700x500")  # Largura maior (800) e altura menor (500)
        janela.transient(self)

        # Título
        ttk.Label(janela, text="Novo Medicamento/Vacina", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Canvas para permitir rolagem
        canvas = tk.Canvas(janela)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configura o canvas para usar a scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno para os widgets
        frame_campos = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_campos, anchor="nw")

        # Atualiza o scrollregion sempre que o frame interno for redimensionado
        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_campos.bind("<Configure>", atualizar_scrollregion)

        # Obtém os nomes das campanhas do dataset da aba "Campanhas"
        def obter_campanhas_disponiveis():
            try:
                campanhas_frame = self.master.frames["Campanhas"]  # Acessa o frame da aba "Campanhas"
                return [campanha["Nome"] for campanha in campanhas_frame.campanhas]
            except (AttributeError, KeyError):
                return []  # Caso não consiga acessar as campanhas, retorna vazio

        campanhas_disponiveis = obter_campanhas_disponiveis()

        # Campos do formulário
        campos = [
            ("Campanha", "combobox"),  # Adiciona o campo para selecionar a campanha
            ("Tipo", "combobox"),
            ("Nome", "entry"),
            ("Descrição", "text"),
            ("Composição/Substância ativa", "entry"),
            ("Dose Recomendada", "entry"),
            ("Via de Administração", "combobox"),
            ("Grupo-Alvo", "combobox"),  # Substituído "Idade Permitida" por "Grupo-Alvo"
            ("Gravidez Permitida?", "checkbox"),
            ("Sexo", "combobox"),  # Novo campo
            ("Grupo Risco", "combobox"),  # Novo campo
            ("Efeitos Secundários Comuns", "entry"),
            ("Data de Validade", "date"),
            ("Lote", "entry"),
            ("Fabricante/Laboratório", "entry"),
            ("Quantidade em Stock", "entry"),
            ("Estado", "combobox")
        ]

        self.entries = {}

        for campo, tipo in campos:
            frame = ttk.Frame(frame_campos)
            frame.pack(fill="x", pady=5)

            ttk.Label(frame, text=campo).pack(anchor="w")

            if tipo == "entry":
                entry = ttk.Entry(frame)
            elif tipo == "combobox":
                if campo == "Campanha":
                    entry = ttk.Combobox(frame, values=campanhas_disponiveis, state="readonly")  # Usa os nomes das campanhas
                elif campo == "Tipo":
                    entry = ttk.Combobox(frame, values=["Medicamento", "Vacina"], state="readonly")
                elif campo == "Via de Administração":
                    entry = ttk.Combobox(frame, values=["Oral", "Injetável", "Nasal", "Tópico"], state="readonly")
                elif campo == "Grupo-Alvo":  # Adiciona as opções de grupo-alvo
                    entry = ttk.Combobox(frame, values=[
                        "Bebês (0-3 anos)",
                        "Crianças (4-12 anos)",
                        "Jovens (12-18 anos)",
                        "Adultos (18-65 anos)",
                        "Idosos (+65 anos)"
                    ], state="readonly")
                elif campo == "Sexo":  # Adiciona as opções de sexo
                    entry = ttk.Combobox(frame, values=["Masculino", "Feminino"], state="readonly")
                elif campo == "Grupo Risco":  # Adiciona as opções de grupo risco
                    entry = ttk.Combobox(frame, values=["Baixo", "Médio", "Alto"], state="readonly")
                elif campo == "Estado":
                    entry = ttk.Combobox(frame, values=["Disponível", "Fora de stock", "Expirado"], state="readonly")
            elif tipo == "checkbox":
                entry = tk.BooleanVar()
                ttk.Checkbutton(frame, variable=entry, text="Sim").pack(anchor="w")
                self.entries[campo] = entry
                continue
            elif tipo == "text":
                entry = tk.Text(frame, height=4, wrap="word")
            elif tipo == "date":
                entry = DateEntry(frame, date_pattern="dd/mm/yyyy", width=12, background="darkblue", foreground="white", borderwidth=2)

            entry.pack(fill="x")
            self.entries[campo] = entry

        # Botões de ação
        botoes_frame = ttk.Frame(frame_campos, padding=10)
        botoes_frame.pack(fill="x", pady=10)

        ttk.Button(botoes_frame, text="Guardar", command=self.guardar_medicamento).pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy).pack(side="right", padx=5)

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

        # Adiciona os dados à tabela
        novo_recurso = {
            "Tipo": dados.get("Tipo", ""),
            "Nome": dados.get("Nome", ""),
            "Grupo-Alvo": dados.get("Grupo-Alvo", ""),
            "Grupo Risco": dados.get("Grupo Risco", ""),
            "Gravidez": dados.get("Gravidez Permitida?", ""),
            "Data de Validade": dados.get("Data de Validade", ""),
            "Quantidade em Stock": dados.get("Quantidade em Stock", ""),
            "Campanha": dados.get("Campanha", "")
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
        janela.transient(self)
        janela.resizable(False, False)

        ttk.Label(janela, text="Filtrar Recursos", font=("Segoe UI", 16, "bold")).pack(pady=10)

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
            frame = ttk.Frame(janela)
            frame.pack(fill="x", padx=10, pady=5)

            ttk.Label(frame, text=campo).pack(anchor="w")
            combobox = ttk.Combobox(frame, values=["Todos"] + opcoes, state="readonly")
            combobox.current(0)  # Define "Todos" como padrão
            combobox.pack(fill="x")
            self.filtros_selecionados[campo] = combobox

        # Botões de ação
        botoes_frame = ttk.Frame(janela)
        botoes_frame.pack(fill="x", pady=10)

        ttk.Button(botoes_frame, text="Aplicar Filtro", command=lambda: self.aplicar_filtro(janela)).pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy).pack(side="right", padx=5)

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

class RelatoriosFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=20)

        # Título
        ttk.Label(self, text="Relatórios", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))

        # Combobox para selecionar o tipo de relatório
        self.combo_relatorios = ttk.Combobox(
            self,
            values=["Pacientes", "Consultas", "Recursos", "Campanhas"],
            state="readonly",
            font=("Segoe UI", 11)
        )
        self.combo_relatorios.set("Selecione um relatório")
        self.combo_relatorios.pack(pady=10)
        self.combo_relatorios.bind("<<ComboboxSelected>>", self.alternar_relatorio)

        # Frame para exibir o conteúdo do relatório
        self.conteudo_frame = ttk.Frame(self)
        self.conteudo_frame.pack(fill="both", expand=True, pady=10)

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
        # Limpa o frame de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

        # Frame para filtros (esquerda)
        filtros_frame = ttk.Frame(self.conteudo_frame, padding=10)
        filtros_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(filtros_frame, text="Relatório de Pacientes", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Filtros disponíveis
        filtros = [
            ("Grupo de Idade", ["Todas as Faixas", "Bebês (0-3 anos)", "Crianças (4-12 anos)", "Jovens (12-18 anos)", "Adultos (18-65 anos)", "Idosos (+65 anos)"]),
            ("Gênero", ["Ambos", "Masculino", "Feminino"]),
            ("Risco de Saúde", ["Todos", "Baixo", "Médio", "Alto"])
        ]

        self.filtros_selecionados = {}

        for campo, opcoes in filtros:
            frame = ttk.Frame(filtros_frame)
            frame.pack(fill="x", pady=5)

            ttk.Label(frame, text=campo).pack(anchor="w")
            combobox = ttk.Combobox(frame, values=opcoes, state="readonly")
            combobox.current(0)  # Define a primeira opção como padrão
            combobox.pack(fill="x")
            self.filtros_selecionados[campo] = combobox

        # Botão para gerar relatório
        ttk.Button(filtros_frame, text="Gerar Relatório", command=self.gerar_relatorio_pacientes).pack(pady=10)

        # Frame para o gráfico (direita)
        grafico_frame = ttk.Frame(self.conteudo_frame, padding=10)
        grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(grafico_frame, text="Pacientes por Risco de Saúde", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Dados fictícios para o gráfico
        categorias = ["Baixo", "Médio", "Alto"]
        valores = [200, 150, 50]

        # Criação do gráfico usando pyplot
        figura, ax = plt.subplots(figsize=(6, 4), dpi=100)
        bars = ax.bar(categorias, valores, color=["#74b9ff", "#55efc4", "#ff7675"], edgecolor="black", linewidth=1.2)

        # Personaliza o gráfico
        ax.set_ylabel("Número de Pacientes", fontsize=12, labelpad=10)
        ax.set_xlabel("Risco de Saúde", fontsize=12, labelpad=10)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Adiciona os valores acima das barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height + 5, f"{int(height)}", ha="center", va="bottom", fontsize=10)

        # Adiciona o gráfico ao frame
        canvas = FigureCanvasTkAgg(figura, grafico_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def gerar_relatorio_pacientes(self):
        """Abre uma nova janela com os dados do relatório de pacientes."""
        # Nova janela
        janela = tk.Toplevel(self)
        janela.title("Relatório de Pacientes")
        janela.geometry("800x600")
        janela.transient(self)

        # Tabela para exibir os dados
        colunas = ["Nome", "Idade", "Gênero", "Risco de Saúde"]
        tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=20)
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=150, anchor="center")
        tabela.pack(fill="both", expand=True, padx=10, pady=10)

        # Dados fictícios para a tabela
        dados = [
            ["João Silva", "35", "Masculino", "Baixo"],
            ["Maria Oliveira", "62", "Feminino", "Médio"],
            ["Carlos Santos", "45", "Masculino", "Alto"]
        ]

        # Insere os dados na tabela
        for linha in dados:
            tabela.insert("", "end", values=linha)

        # Botão para fechar a janela
        ttk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)

    def _mostrar_relatorio_consultas(self):
        """Exibe o layout do relatório de consultas."""
        ttk.Label(self.conteudo_frame, text="Relatório de Consultas", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Label(self.conteudo_frame, text="Conteúdo do relatório de campanhas...", font=("Segoe UI", 11)).pack()


    def _mostrar_relatorio_recursos(self):
        """Exibe o relatório de recursos."""
        ttk.Label(self.conteudo_frame, text="Relatório de Recursos", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Label(self.conteudo_frame, text="Conteúdo do relatório de recursos...", font=("Segoe UI", 11)).pack()

    def _mostrar_relatorio_campanhas(self):
        """Exibe o relatório de campanhas."""
        ttk.Label(self.conteudo_frame, text="Relatório de Campanhas", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Label(self.conteudo_frame, text="Conteúdo do relatório de campanhas...", font=("Segoe UI", 11)).pack()


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

