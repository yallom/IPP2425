import weakref
from medicamentos import Medicamento

class Campanha: #Classe para campanhas de vacinação, referentes a um medicamento específico

    instances = weakref.WeakSet()

    def __init__(self,name,start_date,end_date,age_min,age_max,efficiency_min,efficiency_max,gravidas,idmedicine):
        
        self.nome = name.strip()
        self.datas = [start_date, end_date]
        self.grupoidade = [int(age_min), int(age_max)]
        self.gruporisco = [int(efficiency_min), int(efficiency_max)]
        self.gravidas = int(gravidas)
        self.idmedicamento = idmedicine

        Campanha.instances.add(self)

    def printself(self):
        print(self.nome, self.datas, self.grupoidade, self.gruporisco, self.gravidas, self.idmedicamento)
        print(id(self))

    @classmethod
    def get_all_instances(cls):
        print (list(cls.instances))
    
    @classmethod
    def get_instance(cls, arg):
        print([obj.nome for obj in cls.instances if obj.idmedicamento == arg])

prozac = Medicamento("Prozac", "10", "30", "0", "3", "1")
q = Campanha("Campanha 1", "2024-10-13", "2024-10-15", prozac.idade[0], prozac.idade[1], prozac.eficacia[0], prozac.eficacia[1], prozac.gravidez, id(prozac))
q.printself()
Campanha.get_all_instances()

Campanha.get_instance(id(prozac))