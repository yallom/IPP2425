import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.pessoascontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from Models.pacientes import Paciente    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

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

def getAllObjects():
    return Paciente.get_all_instances()

def getAllPacients():
    return Paciente.show_all()


#TESTES DE FUNCIONALIDADES

a = addPacient("João", "23", "m", False, "3", "poliomielite", "A+")
print(a)
b = getAllObjects()
print(b)
for i in b:
    print(i.get_self())
print(getAllPacients())