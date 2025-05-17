import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.cappmanhascontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from ..Models.campanhas import Campanha    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

def addCampaign(name:str, date1:str, date2:str, gravidez:int, age1:str, age2:str, risk1:str, risk2:str, id):    #Cria uma nova pessoa no sistema
    newname = name.strip()
    daterange = [int(date1.strip()), int(date2.strip())]
    agerange = [int(age1.strip()), int(age2.strip())]
    riskrange = [int(risk1.strip()), int(risk2.strip())]
    pregnancy = gravidez
    medicine = id

    X = Campanha(newname, daterange, agerange, riskrange, pregnancy, medicine)

    return X

def deleteCampaign(obj):    #Apaga uma pessoa da classe "Pessoa" atual
    return Campanha.delete_instance(obj)

#def searchCampaign(obj):    #Meio inútil, mantém-se por agora
    return Campanha.get_instance(obj)

def getCampaign(id):    #Procura uma pessoa específica pelo seu ID
    return Campanha.show_by_id(id)
