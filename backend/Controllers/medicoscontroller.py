import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.medicos import Medico

def addMedico(nome: str, especialidade: str, disponibilidade: list):
    X = Medico(nome, especialidade, disponibilidade)
    return X

def delete(obj):
    print("Deletando médico:", obj.nome, obj.id)
    return Medico.delete_instance(obj)

def search(id):
    return Medico.show_by_id(id)

def edit(obj, nome, disponibilidade, especialidade):
    print(f"Nome: {nome}, Especialidade: {especialidade}, Disponibilidade: {disponibilidade}")
    return obj.edit_self(nome, disponibilidade, especialidade)

def getAll():
    return Medico.instances

def getAllMedicos():
    return [obj.get_self() for obj in Medico.instances]

def searchType(tipo):
    medicos = Medico.search_specialty(tipo)
    return medicos

def write(obj):
    medico = {
        'id': obj.id,
        'nome': obj.nome,
        'especialidade': obj.specialty,
        'disponibilidade': obj.servico
    }
    return medico

def read(lista):
    try:
        for m in lista:
            nome = m["nome"]
            especialidade = m["especialidade"]
            disponibilidade = m["disponibilidade"]
            addMedico(nome, especialidade, disponibilidade)
    except Exception as e:
        print(f"Erro ao ler médicos: {e}")