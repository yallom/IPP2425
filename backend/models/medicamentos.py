import weakref

class Medicamento: #uma classe de medicamentos referentes a um grupo etário ou de risco

    instances = weakref.WeakSet()

    def __init__(self,name,age_min,age_max,efficiency_min,efficiency_max,gravidas):

        self.nome = name.strip()
        self.idade = [int(age_min.strip()), int(age_max.strip())]
        self.eficacia = [int(efficiency_min.strip()), int(efficiency_max.strip())]
        self.gravidez = int(gravidas.strip())
        
        Medicamento.instances.add(self)

    def printself(self):
        print(self.nome, self.idade, self.eficacia, self.gravidez)

    @classmethod
    def get_all_instances(cls):
        print (list(cls.instances))

q = Medicamento("Minoxidil","18", "20","1", "3","1")
q.printself()
Medicamento.get_all_instances()
del q
Medicamento.get_all_instances()