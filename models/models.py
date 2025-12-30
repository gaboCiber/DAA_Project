class Freelancer:
    def __init__(self, id, costo):
        self.id = id
        self.costo = costo
        self.habilidades = {}  # Dict: {habilidad: nivel}
    
    def agregar_habilidad(self, habilidad, nivel):
        self.habilidades[habilidad] = nivel
    
    def tiene_habilidad(self, habilidad, nivel_minimo):
        """Retorna True si tiene la habilidad con nivel suficiente"""
        return self.habilidades.get(habilidad, 0) >= nivel_minimo
    
    def __repr__(self):
        return f"F{self.id}(costo:{self.costo}, habs:{self.habilidades})"

class Proyecto:
    def __init__(self):
        self.requisitos = {}  # Dict: {habilidad: nivel_minimo}
    
    def agregar_requisito(self, habilidad, nivel_minimo):
        self.requisitos[habilidad] = nivel_minimo
    
    def __repr__(self):
        return f"Proyecto(requisitos:{self.requisitos})"