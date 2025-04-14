#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.pessoascontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from ..Models.pessoas import Pessoa    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

def addPerson(name:str, age:str, sex:str, gravidez:bool, risk:str):    #Cria uma nova pessoa no sistema
    ageint = int(age.strip())
    newname = name.strip()
    newsex = sex.strip()
    newrisk = int(risk.strip())

    X = Pessoa(newname, ageint, newsex, gravidez, newrisk)

    return X

def deletePerson(obj):    #Apaga uma pessoa da classe "Pessoa" atual
    return Pessoa.delete_instance(obj)

#def searchPerson(obj):    #Meio inútil, mantém-se por agora
    return Pessoa.get_instance(obj)

def getPerson(id):    #Procura uma pessoa específica pelo seu ID
    return Pessoa.show_by_id(id)

def editPerson(obj, name, age, sex, gravidez, risk):    #Edita a informação de uma pessoa na classe "Pessoa" atual
    ageint = int(age.strip())
    newname = name.strip()
    newsex = sex.strip()
    newrisk = int(risk.strip())
    return obj.edit_self(newname, ageint, newsex, gravidez, newrisk)



#TESTES DE FUNCIONALIDADES

"""
x = addPerson("João", "17", "m", True, "1")
print("OBJ: ", x)
print("ID: ", id(x))

addPerson("Maria", "21", "f", True, "2")
addPerson("António", "45", "m", True, "0")

y = Pessoa.get_all_instances()
lista = [id(i) for i in y]
lista.append(0)

print(lista)

for elem in lista:
    try:
        print("AQUI: ", getPerson(elem).get_self()[0])
    except:
        print(f"ERRO: Elemento {elem} não pode ser acessado")

print("Elemento editado:", editPerson(x, "João", "18", "m", True, "1")[0])

print(deletePerson(x))

z = Pessoa.get_all_instances()
lista1 = [id(i) for i in z]
lista1.append(0)

print(lista1)

for elem in lista1:
    try:
        print("AQUI: ", getPerson(elem).get_self()[0])
    except:
        print(f"ERRO: Elemento {elem} não pode ser acessado")


x = addPerson("João", "17", "m", True, "1")
print("OBJ: ", x)
print("ID: ", id(x))
print(getPerson(id(x)).get_self())
print(deletePerson(getPerson(id(x))))
"""