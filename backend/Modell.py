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

class Medico:

    medicos = []

    def __init__(self, nome, especialidade, disponibilidade):
        self.id = f"M{len(Medico.medicos)+1:04d}"
        self.name = nome
        self.speciality = especialidade
        self.servico = disponibilidade
        Medico.medicos.append(self)

    def get_self(self):
        return(self.id, self.name, self.speciality, self.servico)
    
    def to_dict(self):
        return {
            "nome": self.name,
            "especialidade": self.speciality,
            "disponibilidade": self.servico 
        }
    
    def ler_ficheiro_medicos(self, filename):
        try:
            ficheiro = open(filename, 'r', encoding = 'utf-8')
            medicos = json.load(ficheiro)
            for m in medicos:
                nome = m['nome']
                especialidade = m['especialidade']
                disponibilidade = m['disponibilidade']
                Medico(nome,especialidade, disponibilidade)
        except:
            print("Erro ao ler o ficheiro!")
            
    
    def formatar_disponibilidade(matriz):
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        horarios = [h for h in range(8, 20, 2)]  # 8,10,12,14,16,18

        resultado = []

        for dia_idx, dia_lista in enumerate(matriz):
            blocos = []
            i = 0
            while i < len(dia_lista):
                if i >= len(horarios):
                    break  # evita índice inválido
                if dia_lista[i]:
                    inicio = horarios[i]
                    fim_idx = i
                    while fim_idx + 1 < len(dia_lista) and fim_idx + 1 < len(horarios) and dia_lista[fim_idx + 1]:
                        fim_idx += 1
                    fim = horarios[fim_idx] + 2
                    blocos.append(f"{inicio:02d}h-{fim:02d}h")
                    i = fim_idx + 1
                else:
                    i += 1
            if blocos:
                resultado.append(f"{dias_semana[dia_idx]} - {' '.join(blocos)}")

        return " | ".join(resultado)



    @staticmethod
    def lista_para_matriz(lista_blocos):
        horarios = [f"{h:02d}:00-{h+2:02d}:00" for h in range(8, 20, 2)]
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        matriz = [[False]*7 for _ in range(6)]
        for bloco in lista_blocos:
            try:
                dia, hora = bloco.split(' ', 1)
                i = horarios.index(hora)
                j = dias_semana.index(dia)
                matriz[i][j] = True
            except ValueError:
                pass
        return matriz



    def procurar_id(self, id):
        encontrado = False
        for medico in Medico.medicos:
            if medico.id == id:
                encontrado = True
                return medico.get_self()
            else:
                return "Médico não encontrado"
    
    @staticmethod
    def from_dict(dados):
        return Medico(
            dados["nome"],
            dados["especialidade"],
            dados.get("disponibilidade", [])
        )

class Consulta:

    consultas  = []

    def __init__(self, id_paciente, data, id_medico, tipo):
        self.id_consulta = f"P{len(Consulta.consultas)+1:04d}"
        self.id_paciente = id_paciente
        self.data = data
        self.id_medico = id_medico
        self.tipo = tipo
        Consulta.consultas.append(self)
    
    
 
