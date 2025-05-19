class Consulta:

    instances = []

    def __init__(self, id_paciente, data, hora, id_medico, tipo):
        self.id = f"A{int(Consulta.instances[-1].id[1:5])+1:04d}" if len(Consulta.instances) > 0 else "A0001"
        self.id_paciente = id_paciente
        self.data = data
        self.hora = hora
        self.id_medico = id_medico
        self.tipo = tipo
        Consulta.instances.append(self)

    def get_self(self):
        return (self.id, self.id_paciente, self.data, self.hora, self.id_medico, self.tipo)
    
    def __str__(self):
        return f"Consulta {self.id}: {self.data} {self.hora} | Médico: {self.id_medico} | Paciente: {self.id_paciente}"
            
    @classmethod        
    def search_by_id(cls, id_consulta):
        for consulta in cls.instances:
            if consulta.id == id_consulta:
                return consulta
        return "Consulta não encontrada"
    
    @classmethod
    def search_secondary(cls, id):
        consultas = []
        for consulta in cls.instances:
            if consulta.id_medico == id or consulta.id_paciente == id:
                consultas.append(consulta)
        print (f"Consultas encontradas: {len(consultas)}")
        return consultas
    
    @classmethod
    def delete_instance(cls,obj):
        if obj in cls.instances:
            print("Consulta encontrada") 
            try:
                print("A iniciar desmarcação da consulta")
                cls.instances.remove(obj)
                print("Consulta desmarcada")
                del obj
                print("Consulta desmarcada com sucesso")
            except:
                return f"Erro ao desmarcar consulta {obj.id}"
        else:
            return f"Consulta não encontrada"