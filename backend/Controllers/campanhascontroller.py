import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.cappmanhascontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from ..Models.campanhas import Campanha    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

def addCampaign(name:str, date1:str, date2:str, gravidez:int, age, risk, id, maxpeople):    #Cria uma nova pessoa no sistema
    newname = name.strip()
    daterange = [date1,date2]
    agerange = age
    riskrange = risk
    pregnancy = gravidez
    medicine = id

    X = Campanha(newname, daterange, agerange, riskrange, pregnancy, medicine, maxpeople)

    return X

def deleteCampaign(obj):    #Apaga uma pessoa da classe "Pessoa" atual
    return Campanha.delete_instance(obj)

#def searchCampaign(obj):    #Meio inútil, mantém-se por agora
    return Campanha.get_instance(obj)

def getCampaign(id):    #Procura uma pessoa específica pelo seu ID
    return Campanha.show_by_id(id)

def getAll():
    return Campanha.get_all_instances()
