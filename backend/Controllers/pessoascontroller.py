import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.pacientes import Paciente

def addPacient(name: str, age: str, sex: str, gravidez: bool, doenca: str, tipo_sanguineo: str, morada):     #Cria uma nova Pessoa no sistema
    X = Paciente(name,age,sex,tipo_sanguineo,morada,doenca,gravidez)
    return X

def delete(obj):    #Apaga uma pessoa da classe "Pessoa" atual
    return Paciente.delete_instance(obj)

#def searchPerson(obj):    #Meio inútil, mantém-se por agora
    return Paciente.get_instance(obj)

def search(id):    #Procura uma pessoa específica pelo seu ID
    return Paciente.show_by_id(id)


def edit(obj, name, age, sex, gravidez, risk, doenca, tipo_sanguineo):    #Edita a informação de uma pessoa na classe "Pessoa" atual
    ageint = int(age.strip())
    newname = name.strip()
    newsex = sex.strip()
    newrisk = int(risk.strip())
    newdoenca = doenca.strip()
    newtipo = tipo_sanguineo.strip()

    return obj.edit_self(newname, ageint, newsex, gravidez, newrisk, newdoenca, newtipo)

def getAll():
    return Paciente.instances

def getAllPacients():
    return Paciente.show_all()

def write(obj):
    paciente = {
        'id': obj.id,
        'nome': obj.nome,
        'idade': obj.idade,
        'sexo': obj.sexo,  
        'grupo sanguíneo': obj.sangue,
        'morada': obj.morada,
        'doenças crónicas': obj.doenca,
        'gravidez': obj.gravidez,
        'risco': obj.risco,
        'histórico': {
            'consultas': obj.historico_consultas,
            'vacinas': obj.historico_vacinas
            }
        }
    return paciente

def read(list):
        try:
            for p in list:
                nome = p['nome']
                idade = p['idade']
                sexo = p['sexo']
                grupo_sanguineo = p['grupo sanguíneo']
                morada = p['morada']
                doenca_cronica = p['doenças crónicas']
                gravidez = p['gravidez']
                
                paciente = addPacient(nome, idade, sexo, gravidez, doenca_cronica, grupo_sanguineo, morada)
                
                # Preencher histórico se disponível
                historico = p.get('histórico', {})
                paciente.historico_consultas = historico.get('consultas', [])
                paciente.historico_vacinas = historico.get('vacinas', [])
        except Exception as e:
            print(f"Erro ao ler o ficheiro: {e}")