import weakref
from campanhas import Campanha

class Fila:

    instances = weakref.WeakSet()

    def __init__(self,name,users,idcampaign):
        
        self.nome = name.strip()
        self.filaespera = users
        self.idcampanha = idcampaign
        self.users = weakref.WeakSet()

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
    
    @classmethod
    def delete_instance(cls,obj):
        if obj in cls.instances:
            cls.instances.remove(obj)
            del obj
            print("Feito")
        print("done")

    def addUser(self,obj):
        try:
            self.users.add(obj)
            print("Utilizador adicionado com sucesso!")
        except:
            return f"Erro ao adicionar Utilizador a fila {self.nome}!"

    def checkUser(self,obj):
        if obj in list(self.users):
            return True
        else:
            return False
    
    def findUser(self, obj):
        if self.checkUser(obj):
            return obj
        else:
            return False
        
    def delUser(self,obj):
        try:
            if self.checkUser(obj):
                self.users.remove(obj)
                del obj
                return "Utilizador removido com sucesso!"
            else:
                return "Utilizador não encontrado!"
        except:
            return f"Erro ao apagar Utilizador {obj.nome} de lista {self.nome}"


    