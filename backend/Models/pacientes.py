import json
class Paciente:

    pacientes = []

    def __init__(self,name,age,sex,grupo_sanguineo,morada,doença_cronica,pregnancy):
        self.id = f"P{len(Paciente.pacientes)+1:04d}"
        self.nome = name
        self.idade = age
        self.sexo = sex
        self.sangue = grupo_sanguineo
        self.morada = morada
        self.doença = doença_cronica
        self.gravidez = False
        if self.sexo != "m":
            self.gravidez = pregnancy
        self.risco = self.risco_paciente()  
        self.historico_consultas = []
        self.historico_vacinas = []
        Paciente.pacientes.append(self)

    
    def risco_paciente(self):
        if self.idade < 45:
            risco = "Baixo"
            if self.doença:
                risco = "Médio"
        elif self.idade < 65:
            risco = "Médio"
            if self.gravidez or self.doença:
                risco = "Elevado"
        else:
            risco = "Elevado"
            if self.doença:
                risco = "Muito Elevado" 
        return risco
        
    def get_self(self):
        return(self.id, self.nome, self.idade, self.sexo, self.sangue,self.morada, self.gravidez, self.risco, self.historico_consultas, self.historico_vacinas)
    
    def to_dict(self):
        paciente = {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'sexo': self.sexo,  
            'grupo sanguíneo': self.sangue,
            'morada': self.morada,
            'doenças crónicas': self.doença,
            'gravidez': self.gravidez,
            'risco': self.risco,
            'histórico': {
                'consultas': self.historico_consultas,
                'vacinas': self.historico_vacinas
            }
        }
        return paciente

    
    def ler_ficheiro_pacientes(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as ficheiro:
                pacientes = json.load(ficheiro)
                for p in pacientes:
                    nome = p['nome']
                    idade = p['idade']
                    sexo = p['sexo']
                    grupo_sanguineo = p['grupo sanguíneo']
                    morada = p['morada']
                    doenca_cronica = p['doenças crónicas']
                    gravidez = p['gravidez']
                    
                    paciente = Paciente(nome, idade, sexo, grupo_sanguineo, morada, doenca_cronica, gravidez)
                    
                    # Preencher histórico se disponível
                    historico = p.get('histórico', {})
                    paciente.historico_consultas = historico.get('consultas', [])
                    paciente.historico_vacinas = historico.get('vacinas', [])
        except Exception as e:
            print(f"Erro ao ler o ficheiro: {e}")

    def procurar_id(self, id):
        for p in Paciente.pacientes:
            if p.id == id:
                return p
        return None
    
    @classmethod
    def from_dict(cls, data):
        # Cria o paciente usando os dados do dicionário
        p = cls(
            name=data['nome'],
            age=data['idade'],
            sex=data['sexo'],
            grupo_sanguineo=data['grupo sanguíneo'],
            morada=data['morada'],
            doença_cronica=data['doenças crónicas'],
            pregnancy=data.get('gravidez', False)
        )
        # Carregar histórico se houver
        historico = data.get('histórico', {})
        p.historico_consultas = historico.get('consultas', [])
        p.historico_vacinas = historico.get('vacinas', [])
        return p



