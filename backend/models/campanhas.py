import weakref
from medicamentos import Medicamento

class Campanha: #Classe para campanhas de vacinação, referentes a um medicamento específico

    instances = []

    def __init__(self,name,dates,ages,efficiency,gravidas,idmedicine):
        
        self.nome = name
        self.datas = dates
        self.grupoidade = ages
        self.gruporisco = efficiency
        self.gravidas = gravidas
        self.idmedicamento = idmedicine
        self.id = f"C{len(Campanha.instances) + 1:04d}"

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
    def search_id(cls, id):
        return([obj for obj in cls.instances if obj.idmedicamento == id])