#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.medicamentoscontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from ..Models.medicamentos import Medicamento    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

def addMedicine(name:str, age1:str, age2:str, sex:str, gravidez:int, risk1:str, risk2:str, expiry:str):    #Cria uma nova pessoa no sistema
    newname = name.strip()
    agerange = [int(age1.strip()), int(age2.strip())]
    riskrange = [int(risk1.strip()), int(risk2.strip())]
    pregnancy = gravidez
    validade = expiry.strip()

    X = Medicamento(newname, agerange, riskrange, pregnancy, validade)

    return X

def deleteMedicine(obj):    #Apaga uma pessoa da classe "Pessoa" atual
    return Medicamento.delete_instance(obj)

#def searchMedicine(obj):    #Meio inútil, mantém-se por agora
    return Medicamento.get_instance(obj)

def getMedicine(id):    #Procura uma pessoa específica pelo seu ID
    return Medicamento.show_by_id(id)
