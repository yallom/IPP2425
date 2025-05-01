import weakref
from campanhas import Campanha

class Fila: #Classe de filas para uma campanha, implementada como uma queue
    
    instances = []

    def __init__(self,name,users,idcampaign):
        
        self.nome = name.strip()
        self.filaespera = users
        self.idcampanha = idcampaign
        self.users = []
        self.id = f"Q{len(Fila.instances) + 1:04d}"

        Fila.instances.append(self)

    def get_self(self):
        return(self.nome, self.filaespera, self.idcampanha, self.id)

    @classmethod
    def get_all_instances(cls):
        return (list(cls.instances))
    
    @classmethod
    def get_instance(cls, arg):
        return([obj for obj in cls.instances if obj.idcampanha == arg])
    
    @classmethod
    def delete_instance(cls,id):
        for obj in cls.instances:
            if obj.id == id:
                cls.instances.remove(obj)
                del obj
                return("Feito")
            return("done")

    def addUser(self,obj):
        try:
            self.users.add(obj)
            return("Utilizador adicionado com sucesso!")
        except:
            return f"Erro ao adicionar Utilizador a fila {self.nome}!"

    def checkUser(pacient, ID):
        if pacient.id == ID:
            return True
        else:
            return False
    
    def findUser(self, ID):
        for user in self.users:
            if self.checkUser(user,ID):
                return user
            else:
                return False
        
    def delUser(self,ID):
        try:
            x = self.finduser(ID)
            if x != False:
                self.users.remove(x)
                return f"Utilizador {x.id} removido com sucesso!"
            else:
                return f"Utilizador {x.id} não encontrado!"
        except:
            return f"Erro ao apagar Utilizador {ID.nome} de lista {self.nome}"


    