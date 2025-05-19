from .medicamentos import Medicamento

class Campanha: #Classe para campanhas de vacinação, referentes a um medicamento específico

    instances = []

    def __init__(self,name,dates,ages,efficiency,gravidas,idmedicine,maxpeople):
        
        self.nome = name
        self.datas = dates
        self.grupoidade = ages
        self.gruporisco = efficiency
        self.gravidas = gravidas
        self.idmedicamento = idmedicine
        self.id = f"C{int(Campanha.instances[-1].id[1:5])+1:04d}" if len(Campanha.instances) > 0 else "C0001"
        self.maximo = maxpeople
        self.pacientes = []

        Campanha.instances.append(self)

    def get_self(self):
        return(self.nome, self.datas, self.grupoidade, self.gruporisco, self.gravidas, self.idmedicamento, self.id)

    @classmethod
    def get_all_instances(cls):
        return (list(cls.instances))
    
    @classmethod
    def get_instance(cls, id):
        return([obj for obj in cls.instances if obj.id == id])
    
    @classmethod
    def show_by_id(cls, uuid):
        for item in cls.get_all_instances():
            if item.id == uuid:
                return item
        return f"Medicamento {uuid} não encontrado!"
    
    @classmethod
    def delete_instance(cls,id):
        obj = cls.show_by_id(id)
        if obj in cls.instances:
            try:
                cls.instances.remove(obj)
                del obj
                return "Campanha apagada com sucesso"
            except:
                return f"Erro ao apagar Campanha {obj.nome}"
        else:
            return f"Campanha {obj.nome} não encontrada"
        
    def add_patient(self, patient):
        self.pacientes.append(patient)
        return f"Paciente {patient.nome} adicionado ao medicamento {self.nome} com sucesso!"