class Paciente:

    instances = []

    def __init__(self, name, age, sex, gravidez, risk, doenca="", tipo_sanguineo=""):
        self.nome = name
        self.idade = age
        self.sexo = sex
        self.risco = risk
        self.doenca = doenca
        self.sangue = tipo_sanguineo

        if sex == "m":
            self.gravidez = False
        else:
            self.gravidez = gravidez

        self.id = f"P{len(Paciente.instances) + 1 :04d}"
        Paciente.instances.append((self, id(self)))

    def get_self(self):
        return (self.nome, self.idade, self.sexo, self.gravidez, self.risco, self.doenca, self.sangue, self.id)

    def edit_self(self, name, age, sex, gravidez, risk, doenca, tipo_sanguineo):
        self.nome = name
        self.idade = age
        self.sexo = sex
        self.risco = risk
        self.doenca = doenca
        self.sangue = tipo_sanguineo

        if sex == "m":
            self.gravidez = False
        else:
            self.gravidez = gravidez

        return self.get_self()


    @classmethod
    def get_all_instances(cls):
        return ([obj for obj in list(cls.instances)])

    #@classmethod
    #def get_instance(cls,arg):    #Meio inútil, mantém-se por agora
        return([tuple[0].get_self() for tuple in cls.instances if tuple == arg])

    @classmethod
    def delete_instance(cls,obj):
        if (obj,id(obj)) in cls.instances:
            #print("Utilizador encontrado") 
            try:
                #print("A iniciar remoção do utilizador")
                cls.instances.remove((obj, id(obj)))
                #print("Utilizador removido de instances")
                del obj
                return "Utilizador apagado com sucesso"
            except:
                return f"Erro ao apagar utilizador {obj.nome}"
        else:
            return f"Utilizador {obj} não encontrado"
        
    @classmethod
    def show_all(cls):
        return([obj.get_self() for obj in list(cls.instances)])
    
    @classmethod
    def show_by_id(cls, uuid):
        for item in cls.get_all_instances():
            if item[1] == uuid:
                return item
        return f"Utilizador {uuid} não encontrado!"

