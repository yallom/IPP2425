import weakref

class Medicamento: #uma classe de medicamentos referentes a um grupo etário ou de risco

    instances = []

    def __init__(self,name,agerange,riskrange,gravidas,expiry):

        self.nome = name
        self.idade = agerange
        self.eficacia = riskrange
        self.gravidez = gravidas
        self.validade = expiry
        self.id = f"M{len(Medicamento.instances) + 1:04d}"
        
        Medicamento.instances.append(self)

    def get_self(self):
        return(self.nome, self.idade, self.eficacia, self.gravidez, self.validade, self.id)

    @classmethod
    def get_all_instances(cls):
        return ([obj for obj in list(cls.instances)])
    
    @classmethod
    def delete_instance(cls,obj):
        if (obj,id(obj)) in cls.instances:
            #print("Utilizador encontrado") 
            try:
                #print("A iniciar remoção do utilizador")
                cls.instances.remove((obj, id(obj)))
                #print("Utilizador removido de instances")
                del obj
                return "UMedicamento apagado com sucesso"
            except:
                return f"Erro ao apagar Medicamento {obj.nome}"
        else:
            return f"Medicamento {obj} não encontrado"
        
    @classmethod
    def show_by_id(cls, uuid):
        for item in cls.get_all_instances():
            if item.id == uuid:
                return item
        return f"Medicamento {uuid} não encontrado!"

q = Medicamento("Minoxidil","18", "20","1", "3","1", "10-11-12")
q.get_self()
Medicamento.get_all_instances()
del q
Medicamento.get_all_instances()