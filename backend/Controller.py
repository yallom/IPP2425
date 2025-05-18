
import json
import json
import uuid
from Modell import Paciente, Medico

class GestorPacientes:
    def __init__(self, caminho_ficheiro='pacientes.json'):
        self.caminho_ficheiro = caminho_ficheiro
        self.pacientes = []
        self.carregar_de_ficheiro()

    def adicionar_paciente(self, paciente):
        if not paciente.id:
            paciente.id = str(uuid.uuid4())
        self.pacientes.append(paciente)

    def remover_paciente(self, id):
        self.pacientes = [p for p in self.pacientes if p.id != id]

    def editar_paciente(self, id, **kwargs):
        paciente = self.obter_paciente(id)
        if paciente:
            for key, value in kwargs.items():
                if hasattr(paciente, key):
                    setattr(paciente, key, value)
    
    def atualizar_paciente(self, id, novo_paciente):
        for i, paciente in enumerate(self.pacientes):
            if paciente.id == id:
                novo_paciente.id = id  # mantém o ID original
                novo_paciente.historico_consultas = paciente.historico_consultas
                novo_paciente.historico_vacinas = paciente.historico_vacinas
                self.pacientes[i] = novo_paciente
                return True
        return False

    def obter_paciente(self, id):
        for paciente in self.pacientes:
            if paciente.id == id:
                return paciente
        return None

    def listar_pacientes(self):
        return self.pacientes

    def guardar_em_ficheiro(self):
        dados = [p.to_dict() for p in self.pacientes]
        with open(self.caminho_ficheiro, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar_de_ficheiro(self):
        try:
            with open(self.caminho_ficheiro, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.pacientes = [Paciente.from_dict(d) for d in dados]
        except FileNotFoundError:
            self.pacientes = []

class GestorMedicos:
    def __init__(self, caminho_ficheiro='pacientes_com_morada.json'):
        self.caminho_ficheiro = caminho_ficheiro
        self.medico = []
        self.carregar_de_ficheiro()
    
    def adicionar_medico(self, medico):
        if not medico.id:
            medico.id = str(uuid.uuid4())
        self.medico.append(medico)

    def remover_medico(self, id):
        self.medico = [m for m in self.medico if m.id != id]

    def editar_medico(self, id, **kwargs):
        medico = self.obter_medico(id)
        if medico:
            for key, value in kwargs.items():
                if hasattr(medico, key):
                    setattr(medico, key, value)
    
    def atualizar_medico(self, id, novo_medico):
        for i, medico in enumerate(self.medico):
            if medico.id == id:
                novo_medico.id = id  # mantém o ID original
                novo_medico.historico_consultas = medico.historico_consultas
                novo_medico.historico_vacinas = medico.historico_vacinas
                self.medico[i] = novo_medico
                return True
        return False

    def obter_medico(self, id):
        for medico in self.medico:
            if medico.id == id:
                return medico
        return None

    def listar_medicos(self):
        return self.medico

    def guardar_em_ficheiro(self):
        dados = [m.to_dict() for m in self.medico]
        with open(self.caminho_ficheiro, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar_de_ficheiro(self):
        try:
            with open(self.caminho_ficheiro, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.medico = [Medico.from_dict(d) for d in dados]
        except FileNotFoundError:
            self.medico = []


