class SolucionGreedy:
    def __init__(self, freelancers, proyecto):
        self.freelancers = freelancers
        self.proyecto = proyecto
    
    def resolver_greedy_ratio(self):
        """Algoritmo greedy seleccionando por mejor ratio (nuevas_habilidades / costo)"""
        habilidades_cubiertas = set()
        equipo = []
        costo_total = 0
        
        # Hacer una copia para no modificar la original
        freelancers_disponibles = self.freelancers.copy()
        habilidades_requeridas = set(self.proyecto.requisitos.keys())
        
        while habilidades_cubiertas != habilidades_requeridas:
            mejor_ratio = -1
            mejor_freelancer = None
            mejores_nuevas_habilidades = set()
            
            for freelancer in freelancers_disponibles:
                # Calcular habilidades nuevas que cubre
                nuevas = set()
                for habilidad in habilidades_requeridas - habilidades_cubiertas:
                    if freelancer.tiene_habilidad(habilidad, self.proyecto.requisitos[habilidad]):
                        nuevas.add(habilidad)
                
                if nuevas:  # Solo considerar si aporta algo
                    ratio = len(nuevas) / freelancer.costo
                    if ratio > mejor_ratio:
                        mejor_ratio = ratio
                        mejor_freelancer = freelancer
                        mejores_nuevas_habilidades = nuevas
            
            if mejor_freelancer is None:
                # No se puede cubrir todas las habilidades
                return [], float('inf')
            
            # Añadir al equipo
            equipo.append(mejor_freelancer)
            costo_total += mejor_freelancer.costo
            habilidades_cubiertas.update(mejores_nuevas_habilidades)
            freelancers_disponibles.remove(mejor_freelancer)
        
        # Eliminar freelancers redundantes
        equipo = self.eliminar_redundantes(equipo)
        costo_total = sum(f.costo for f in equipo)
        
        return equipo, costo_total
    
    def resolver_greedy_costo_efectivo(self):
        """Algoritmo greedy seleccionando por menor costo por habilidad nueva"""
        habilidades_cubiertas = set()
        equipo = []
        costo_total = 0
        freelancers_disponibles = self.freelancers.copy()
        habilidades_requeridas = set(self.proyecto.requisitos.keys())
        
        while habilidades_cubiertas != habilidades_requeridas:
            mejor_costo_efectivo = float('inf')
            mejor_freelancer = None
            mejores_nuevas_habilidades = set()
            
            for freelancer in freelancers_disponibles:
                nuevas = set()
                for habilidad in habilidades_requeridas - habilidades_cubiertas:
                    if freelancer.tiene_habilidad(habilidad, self.proyecto.requisitos[habilidad]):
                        nuevas.add(habilidad)
                
                if nuevas:
                    costo_efectivo = freelancer.costo / len(nuevas)
                    if costo_efectivo < mejor_costo_efectivo:
                        mejor_costo_efectivo = costo_efectivo
                        mejor_freelancer = freelancer
                        mejores_nuevas_habilidades = nuevas
            
            if mejor_freelancer is None:
                return [], float('inf')
            
            equipo.append(mejor_freelancer)
            costo_total += mejor_freelancer.costo
            habilidades_cubiertas.update(mejores_nuevas_habilidades)
            freelancers_disponibles.remove(mejor_freelancer)
        
        equipo = self.eliminar_redundantes(equipo)
        costo_total = sum(f.costo for f in equipo)
        
        return equipo, costo_total
    
    def eliminar_redundantes(self, equipo):
        """Elimina freelancers redundantes del equipo"""
        if not equipo:
            return equipo
        
        # Ordenar por costo descendente (eliminar los más caros primero)
        equipo_ordenado = sorted(equipo, key=lambda f: f.costo, reverse=True)
        equipo_final = equipo_ordenado.copy()
        
        for freelancer in equipo_ordenado:
            # Verificar si podemos remover este freelancer
            equipo_sin_f = [f for f in equipo_final if f != freelancer]
            
            if self.cubre_todos_requisitos(equipo_sin_f):
                equipo_final = equipo_sin_f
        
        return equipo_final
    
    def cubre_todos_requisitos(self, equipo):
        """Misma función que en fuerza bruta"""
        for habilidad, nivel_min in self.proyecto.requisitos.items():
            cubierto = False
            for freelancer in equipo:
                if freelancer.tiene_habilidad(habilidad, nivel_min):
                    cubierto = True
                    break
            if not cubierto:
                return False
        return True