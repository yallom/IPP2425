import weakref

class Pessoa:

    instances = weakref.WeakSet()

    def __init__(self,name,age,sex,gravidez,risk):

        self.nome = name.strip()
        self.idade = int(age.strip())
        self.sexo = sex.strip()
        self.risco = int(risk.strip())
        if sex == "m":
            self.gravidez = False
        else:
            self.gravidez = gravidez
            
        Pessoa.instances.add(self)

    def printself(self):
        print(self.nome, self.idade, self.sexo, self.gravidez, self.risco)

    @classmethod
    def get_all_instances(cls):
        print (list(cls.instances))

q = Pessoa("João","18","m",True,"1")
q.printself()
Pessoa.get_all_instances()
del q
Pessoa.get_all_instances()