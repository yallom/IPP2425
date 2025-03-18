import weakref
from campanhas import Campanha

class Fila:

    instances = weakref.WeakSet()

    def __init__(self,name,users,idcampaign):
        
        self.nome = name.strip()
        self.filaespera = users
        self.idcampanha = idcampaign

        Fila.instances.add(self)

    def printself(self):
        print(self.nome, self.filaespera, self.idcampanha)
        print(id(self))

    @classmethod
    def get_all_instances(cls):
        print (list(cls.instances))
    
    @classmethod
    def get_instance(cls, arg):
        print([obj.nome for obj in cls.instances if obj.idcampanha == arg])
