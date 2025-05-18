import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.pacientes import Paciente

def addPacient(name: str, age: str, sex: str, gravidez: bool, doenca: str, tipo_sanguineo: str, morada):     #Cria uma nova Pessoa no sistema
    X = Paciente(name,age,sex,tipo_sanguineo,morada,doenca,gravidez)
    return X

def delete(id):    #Apaga uma pessoa da classe "Pessoa" atual
    obj = search(id)
    print(f"Apagar {obj.nome} com ID {obj.id}")
    return Paciente.delete_instance(id)

#def searchPerson(obj):    #Meio inútil, mantém-se por agora
    return Paciente.get_instance(obj)

def search(id):    #Procura uma pessoa específica pelo seu ID
    return Paciente.show_by_id(id)


def edit(id, name, age, sex, tipo_sanguineo, location, doenca, gravidez):    #Edita a informação de uma pessoa na classe "Pessoa" atual
    ageint = int(age.strip()) if age is str else int(age)
    newname = name.strip()
    newsex = sex.strip()
    newlocation = location.strip()
    newdoenca = doenca.strip() if doenca is str else doenca
    newtipo = tipo_sanguineo.strip()
    obj = search(id)

    return Paciente.edit_self(obj, newname, ageint, newsex, newtipo, newlocation, newdoenca, gravidez)

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
