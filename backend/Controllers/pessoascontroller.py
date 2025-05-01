#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.pessoascontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from ..Models.pacientes import Paciente    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

def addPacient(name: str, age: str, sex: str, gravidez: bool, risk: str, doenca: str, tipo_sanguineo: str):     #Cria uma nova Pessoa no sistema
    ageint = int(age.strip())
    newname = name.strip()
    newsex = sex.strip()
    newrisk = int(risk.strip())
    newdoenca = doenca.strip()
    newtipo = tipo_sanguineo.strip()

    X = Paciente(newname, ageint, newsex, gravidez, newrisk, newdoenca, newtipo)
    return X

def deletePacient(obj):    #Apaga uma pessoa da classe "Pessoa" atual
    return Paciente.delete_instance(obj)

#def searchPerson(obj):    #Meio inútil, mantém-se por agora
    return Paciente.get_instance(obj)

def getPacient(id):    #Procura uma pessoa específica pelo seu ID
    return Paciente.show_by_id(id)


def editPacient(obj, name, age, sex, gravidez, risk, doenca, tipo_sanguineo):    #Edita a informação de uma pessoa na classe "Pessoa" atual
    ageint = int(age.strip())
    newname = name.strip()
    newsex = sex.strip()
    newrisk = int(risk.strip())
    newdoenca = doenca.strip()
    newtipo = tipo_sanguineo.strip()

    return obj.edit_self(newname, ageint, newsex, gravidez, newrisk, newdoenca, newtipo)

def getAllPacients():
    return Paciente.get_all_instances()


#TESTES DE FUNCIONALIDADES

"""
x = addPerson("João", "17", "m", True, "1")
print("OBJ: ", x)
print("ID: ", id(x))

addPerson("Maria", "21", "f", True, "2")
addPerson("António", "45", "m", True, "0")

y = Paciente.get_all_instances()
z = Paciente.show_all()

print(y)
print(z)


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

z = Paciente.get_all_instances()
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
