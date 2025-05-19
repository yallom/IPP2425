import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime, timedelta

from Models.consultas import Consulta

def addConsulta(id_paciente, data, hora, id_medico, tipo):
    X = Consulta(id_paciente, data, hora, id_medico, tipo)
    return X

def intervalo30(start,end):
    horarios = []
    inicio = datetime.strptime(start, "%H:%M")
    fim = datetime.strptime(end, "%H:%M")
    atual = inicio
    while atual < fim:
        horarios.append(atual.strftime("%H:%M"))
        atual += timedelta(minutes=30)
    return horarios

def search(id):
    return Consulta.search_by_id(id)

def delete(id):
    x = search(id)
    Consulta.delete_instance(x)
    return False

def cascadeDelete(id):
    consultas = Consulta.search_secondary(id)
    if consultas:
        for consulta in consultas:
            Consulta.delete_instance(consulta)
        return True
    else:
        return False


