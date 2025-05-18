class Medico:

    instances = []

    def __init__(self, nome, especialidade, disponibilidade):
        
        self.nome = nome
        self.specialty = especialidade
        self.servico = disponibilidade
        self.id = f"Med{len(Medico.instances)+1:04d}"
        Medico.instances.append(self)

    def get_self(self):
        return(self.id, self.nome, self.servico, self.specialty)
    
    def edit_self(self,name,availabilities,specialty):

        self.nome = name
        self.servico = availabilities
        self.specialty = specialty

        return self.get_self()


    @classmethod
    def get_all_instances(cls):
        return ([obj[0] for obj in list(cls.instances)])

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
        return([obj[0].get_self() for obj in list(cls.instances)])
    
    @classmethod
    def show_by_id(cls, uuid):
        for item in cls.instances:
            if item.id == uuid:
                return item
        return f"Utilizador {uuid} não encontrado!"