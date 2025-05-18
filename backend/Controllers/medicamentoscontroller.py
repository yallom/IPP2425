#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.medicamentoscontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from ..Models.medicamentos import Medicamento    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

def addMedicine(name, age1, age2, gravidez, risk1, risk2, expiry, type):    #Cria uma nova pessoa no sistema
    newname = name
    agerange = [age1, age2]
    riskrange = [risk1, risk2]
    pregnancy = gravidez
    validade = expiry

    X = Medicamento(newname, type, agerange, riskrange, pregnancy, validade)

    return X

def deleteMedicine(obj):    #Apaga uma pessoa da classe "Pessoa" atual
    return Medicamento.delete_instance(obj)

def search(id):    #Procura uma pessoa específica pelo seu ID
    return Medicamento.show_by_id(id)

def getAll():
    return Medicamento.instances

def read(list):
    try:
        for m in list:
            nome = m["nome"]
            tipo = m["tipo"]
            idade = m["idade"]
            eficacia = m["eficacia"]
            gravidez = m["gravidez"]
            validade = m["validade"]
            addMedicine(nome, idade[0], idade[1], tipo, gravidez, eficacia[0], eficacia[1], validade)
    except Exception as e:
        print(f"Erro ao ler medicamentos: {e}")

def write(obj):
    medicamento = {
        'id': obj.id,
        'nome': obj.nome,
        'tipo': obj.tipo,
        'idade': obj.idade,
        'eficacia': obj.eficacia,
        'gravidez': obj.gravidez,
        'validade': obj.validade
    }
    return medicamento
