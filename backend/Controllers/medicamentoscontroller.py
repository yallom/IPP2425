#ESTE FICHEIRO NÃO DÁ PARA CORRER NORMALMENTE POR SER PARTE DE UM PACKAGE, SE FOR PRECISO TESTAR TEM DE CORRER "python -m backend.Controllers.medicamentoscontroller" NO TERMINAL, COM A PASTA IPP2425 ABERTA

from ..Models.medicamentos import Medicamento    #Import da classe "Pessoa", torna este ficheiro executável apenas como um package

def addMedicine(name, age, gravidez, risk, expiry, type):    #Cria uma nova pessoa no sistema
    newname = name
    agerange = age
    riskrange = risk
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

def read(lista):
    try:
        for m in lista:
            nome = m.get("nome")
            idade = m.get("idade")
            gravidez = m.get("gravidez")
            risco = m.get("risco")
            validade = m.get("validade")
            tipo = m.get("tipo")
            addMedicine(nome, idade, gravidez, risco, validade, tipo)
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
