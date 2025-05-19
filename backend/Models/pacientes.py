class Paciente:

    instances = []

    def __init__(self,name,age,sex,grupo_sanguineo,morada,doenca,pregnancy):
        self.id = f"P{int(Paciente.instances[-1].id[1:5])+1:04d}" if len(Paciente.instances) > 0 else "P0001"
        self.nome = name
        self.idade = age
        self.sexo = sex
        self.sangue = grupo_sanguineo
        self.morada = morada
        self.doenca = doenca
        self.gravidez = False
        if self.sexo != "m":
            self.gravidez = pregnancy
        self.risco = self.risco_paciente()
        self.historico_consultas = []
        self.historico_vacinas = []
        Paciente.instances.append(self)

    def risco_paciente(self):
        if self.idade < 45:
            risco = "Baixo"
            if self.doenca:
                risco = "Médio"
        elif self.idade < 65:
            risco = "Médio"
            if self.gravidez or self.doenca:
                risco = "Elevado"
        else:
            risco = "Elevado"
            if self.doenca:
                risco = "Muito Elevado" 
        return risco

    def get_self(self):
        return(self.id, self.nome, self.idade, self.sexo, self.sangue, self.morada, self.gravidez, self.risco, self.historico_consultas, self.historico_vacinas, self.doenca)

    def edit_self(self,name,age,sex,grupo_sanguineo,morada,doenca,pregnancy):
        self.nome = name
        self.idade = age
        self.sexo = sex
        self.sangue = grupo_sanguineo
        self.morada = morada
        self.doenca = doenca
        self.gravidez = False
        if self.sexo != "m":
            self.gravidez = pregnancy
        self.risco = self.risco_paciente()  
        self.historico_consultas = []
        self.historico_vacinas = []
        return self.get_self()
        
    def add_history(self, consulta = None, vacina = None):
        if consulta:
            self.historico_consultas.append(consulta)
        if vacina:
            self.historico_vacinas.append(vacina)
        return self.get_self()

    @classmethod
    def get_all_instances(cls):
        return ([obj for obj in list(cls.instances)])

    #@classmethod
    #def get_instance(cls,arg):    #Meio inútil, mantém-se por agora
        return([tuple[0].get_self() for tuple in cls.instances if tuple == arg])

    @classmethod
    def delete_instance(cls,uuid):
        obj = cls.show_by_id(uuid)
        try:
            print("A iniciar remoção do utilizador")
            cls.instances.remove(obj)
            print("Utilizador removido de instances")
            del obj
            return "Utilizador apagado com sucesso"
        except:
            return f"Erro ao apagar utilizador P{uuid}"
        
    @classmethod
    def show_all(cls):
        return([obj.get_self() for obj in list(cls.instances)])
    
    @classmethod
    def show_by_id(cls, uuid):
        for obj in cls.instances:
            if obj.id == uuid:
                return obj
        return f"Utilizador {uuid} não encontrado!"

