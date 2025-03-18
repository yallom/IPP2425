import PySimpleGUI as sg

# Lista global para armazenar os pacientes
pacientes = {}

def janela_adicionar_paciente(nome_paciente):
    """Abre uma janela para adicionar os detalhes do paciente."""
    layout_adicionar = [
        [sg.Text("Adicionar Paciente", font=("Helvetica", 20), text_color='white')],
        [sg.Text("Nome:"), sg.Text(nome_paciente, key='-NOME-', font=("Helvetica", 14))],
        [sg.Text("ID:"), sg.InputText(key='-ID-')],
        [sg.Text("Idade:"), sg.InputText(key='-IDADE-')],
        [sg.Text("Sexo:"), sg.Combo(["Masculino", "Feminino"], key='-SEXO-', readonly=True)],
        [sg.Text("Gravidez:"), sg.Combo(["Sim", "Não", "Não se aplica"], key='-GRAVIDEZ-', readonly=True)],
        [sg.Text("Risco de Doença:"), sg.Combo(["Baixo", "Médio", "Alto"], key='-RISCO-', readonly=True)],
        [sg.Button("Salvar", key='-SALVAR-'), sg.Button("Cancelar", key='-CANCELAR-')]
    ]

    window_adicionar = sg.Window("Adicionar Paciente", layout_adicionar, font=("Helvetica", 14))

    while True:
        event, values = window_adicionar.read()
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            break
        elif event == '-SALVAR-':
            if all(values[key].strip() for key in ['-ID-', '-IDADE-']) and values['-SEXO-'] and values['-GRAVIDEZ-'] and values['-RISCO-']:
                pacientes[nome_paciente] = {
                    "ID": values['-ID-'],
                    "Idade": values['-IDADE-'],
                    "Sexo": values['-SEXO-'],
                    "Gravidez": values['-GRAVIDEZ-'],
                    "Risco de Doença": values['-RISCO-']
                }
                sg.popup("Paciente adicionado com sucesso!", title="Sucesso")
                break
            else:
                sg.popup("Preencha todos os campos!", title="Erro")

    window_adicionar.close()

def janela_visualizar_paciente(nome_paciente):
    """Abre uma janela para visualizar e editar um paciente."""
    if nome_paciente not in pacientes:
        sg.popup("Paciente não encontrado!", title="Erro")
        return
    
    dados = pacientes[nome_paciente]
    edit_mode = False

    layout_visualizar = [
        [sg.Text(f"Detalhes de {nome_paciente}", font=("Helvetica", 20), text_color='white')],
        [sg.Text("ID:"), sg.InputText(dados["ID"], key='-ID-', disabled=True)],
        [sg.Text("Idade:"), sg.InputText(dados["Idade"], key='-IDADE-', disabled=True)],
        [sg.Text("Sexo:"), sg.Combo(["Masculino", "Feminino"], default_value=dados["Sexo"], key='-SEXO-', readonly=True, disabled=True)],
        [sg.Text("Gravidez:"), sg.Combo(["Sim", "Não", "Não se aplica"], default_value=dados["Gravidez"], key='-GRAVIDEZ-', readonly=True, disabled=True)],
        [sg.Text("Risco de Doença:"), sg.Combo(["Baixo", "Médio", "Alto"], default_value=dados["Risco de Doença"], key='-RISCO-', readonly=True, disabled=True)],
        [sg.Button("Editar", key='-EDITAR-', size=(10, 1)), sg.Button("Salvar", key='-SALVAR-', visible=False), sg.Button("Fechar", key='-FECHAR-', size=(10, 1))]
    ]

    window_visualizar = sg.Window("Detalhes do Paciente", layout_visualizar, font=("Helvetica", 14))

    while True:
        event, values = window_visualizar.read()

        if event in (sg.WIN_CLOSED, '-FECHAR-'):
            break
        elif event == '-EDITAR-':
            edit_mode = True
            for key in ['-ID-', '-IDADE-', '-SEXO-', '-GRAVIDEZ-', '-RISCO-']:
                window_visualizar[key].update(disabled=False)
            window_visualizar['-SALVAR-'].update(visible=True)
            window_visualizar['-EDITAR-'].update(visible=False)
        elif event == '-SALVAR-' and edit_mode:
            pacientes[nome_paciente] = {
                "ID": values['-ID-'],
                "Idade": values['-IDADE-'],
                "Sexo": values['-SEXO-'],
                "Gravidez": values['-GRAVIDEZ-'],
                "Risco de Doença": values['-RISCO-']
            }
            sg.popup("Dados atualizados com sucesso!", title="Sucesso")
            break

    window_visualizar.close()

def janela_visualizar_todos():
    """Abre uma janela para visualizar todos os pacientes e suas características."""
    if not pacientes:
        sg.popup("Não há pacientes cadastrados!", title="Aviso")
        return

    layout_lista = [[sg.Text("Lista Completa de Pacientes", font=("Helvetica", 20), text_color='white')]]

    paciente_infos = []
    for nome, dados in pacientes.items():
        paciente_info = f"Nome: {nome} | ID: {dados['ID']} | Idade: {dados['Idade']} | Sexo: {dados['Sexo']} | Gravidez: {dados['Gravidez']} | Risco: {dados['Risco de Doença']}"
        paciente_infos.append([sg.Text(paciente_info)])

    col_pacientes = sg.Column(paciente_infos, size=(550, 400), scrollable=True, vertical_scroll_only=True)

    layout = [
        [sg.Frame("Pacientes", [[col_pacientes]])],
        [sg.Button("Fechar", key='-FECHAR-')]
    ]

    window_lista = sg.Window("Lista de Pacientes", layout, font=("Helvetica", 14), resizable=True, size=(600, 400))

    while True:
        event, _ = window_lista.read()
        if event in (sg.WIN_CLOSED, '-FECHAR-'):
            break

    window_lista.close()
 


def janela_gestao_pacientes():
    """Janela principal de Gestão de Pacientes."""
    layout_pacientes = [
        [sg.Text("Gestão de Pacientes", font=("Helvetica", 20), text_color='white', justification='center', expand_x=True)],
        [sg.Text("Nome do Paciente:", font=("Helvetica", 14), justification='center', expand_x=True)],
        [sg.InputText(key='-NOME-', size=(30, 1), justification='center')],
        [sg.Button("Adicionar Paciente", key='-ADICIONAR-', size=(20, 2), button_color=('white', '#007BFF'))],
        [sg.Text("Lista de Pacientes", font=("Helvetica", 14), justification='center', expand_x=True)],
        [sg.Listbox(values=list(pacientes.keys()), size=(30, 10), key='-LISTA-', enable_events=True)],
        [sg.Button("Visualizar Todos", key='-VISUALIZAR-', size=(20, 2), button_color=('white', '#007BFF'))]
    ]

    window_pacientes = sg.Window("Gestão de Pacientes", layout_pacientes, font=("Helvetica", 14), element_justification='center')

    while True:
        event, values = window_pacientes.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-ADICIONAR-':
            nome = values['-NOME-'].strip()
            if nome and nome not in pacientes:
                janela_adicionar_paciente(nome)
                window_pacientes['-LISTA-'].update(list(pacientes.keys()))
        elif event == '-LISTA-' and values['-LISTA-']:
            nome_selecionado = values['-LISTA-'][0]
            janela_visualizar_paciente(nome_selecionado)
        elif event == '-VISUALIZAR-':
            janela_visualizar_todos()

    window_pacientes.close()

# Janela principal
sg.theme('DarkBlue14')

layout = [
    [sg.Text("Gestão de Saúde Comunitária", font=("Helvetica", 20), text_color='white', justification='center', expand_x=True)],
    [sg.Text(" ", size=(1, 2))],  # Espaçamento entre o título e os botões
    [sg.Button("Gestão de Pacientes", key='-PACIENTES-', size=(20, 2), button_color=('white', '#007BFF'))],
    [sg.Button("Campanhas de Saúde", key='-CAMPANHAS-', size=(20, 2), button_color=('white', '#007BFF'))],
    [sg.Button("Relatórios", key='-RELATORIOS-', size=(20, 2), button_color=('white', '#007BFF'))]
]

window = sg.Window("Gestão de Saúde Comunitária", layout, font=("Helvetica", 14), element_justification='center')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == '-PACIENTES-':
        janela_gestao_pacientes()

window.close()



