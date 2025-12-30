import itertools
import time

class SolucionFuerzaBruta:
    def __init__(self, freelancers, proyecto):
        self.freelancers = freelancers
        self.proyecto = proyecto
        self.mejor_costo = float('inf')
        self.mejor_equipo = []
        self.nodos_explorados = 0
    
    def cubre_todos_requisitos(self, equipo):
        """Verifica si un equipo cubre todos los requisitos del proyecto"""
        for habilidad, nivel_min in self.proyecto.requisitos.items():
            cubierto = False
            for freelancer in equipo:
                if freelancer.tiene_habilidad(habilidad, nivel_min):
                    cubierto = True
                    break
            if not cubierto:
                return False
        return True
    
    def resolver_por_enumeration(self):
        """Algoritmo de fuerza bruta explorando todos los subconjuntos"""
        m = len(self.freelancers)
        self.mejor_costo = float('inf')
        self.mejor_equipo = []
        self.nodos_explorados = 0
        
        # Generar todos los subconjuntos (2^m posibilidades)
        for r in range(1, m + 1):  # Empezar desde 1 (equipo no vacío)
            for combo in itertools.combinations(self.freelancers, r):
                self.nodos_explorados += 1
                
                # Calcular costo actual
                costo_actual = sum(f.costo for f in combo)
                
                # Podado simple: si ya supera el mejor costo, no verificar
                if costo_actual >= self.mejor_costo:
                    continue
                
                # Verificar si cubre todos los requisitos
                if self.cubre_todos_requisitos(combo):
                    if costo_actual < self.mejor_costo:
                        self.mejor_costo = costo_actual
                        self.mejor_equipo = list(combo)
        
        return self.mejor_equipo, self.mejor_costo
    
    def resolver_backtracking(self):
        """Versión con backtracking más eficiente (con podas)"""
        m = len(self.freelancers)
        self.mejor_costo = float('inf')
        self.mejor_equipo = []
        self.nodos_explorados = 0
        
        freelancers_ordenados = sorted(self.freelancers, key=lambda f: f.costo)
        
        def backtrack(idx, equipo_actual, costo_actual):
            self.nodos_explorados += 1
            
            # Podado por costo
            if costo_actual >= self.mejor_costo:
                return
            
            # Si ya cubre todos los requisitos
            if self.cubre_todos_requisitos(equipo_actual):
                if costo_actual < self.mejor_costo:
                    self.mejor_costo = costo_actual
                    self.mejor_equipo = equipo_actual.copy()
                return
            
            # Si ya procesamos todos los freelancers
            if idx >= m:
                return
            
            # Opción 1: No tomar este freelancer
            backtrack(idx + 1, equipo_actual, costo_actual)
            
            # Opción 2: Tomar este freelancer
            nuevo_f = freelancers_ordenados[idx]
            backtrack(idx + 1, 
                     equipo_actual + [nuevo_f], 
                     costo_actual + nuevo_f.costo)
        
        backtrack(0, [], 0)
        return self.mejor_equipo, self.mejor_costo
    
    def resolver_backtracking_con_podas_avanzadas(self):
        """Backtracking con podas y manejo correcto de casos límite"""
        if not self.freelancers or not self.proyecto.requisitos:
            return [], 0 if self.proyecto.requisitos else float('inf')
        
        m = len(self.freelancers)
        self.mejor_costo = float('inf')
        self.mejor_equipo = []
        self.nodos_explorados = 0
        
        # Ordenar por costo (más baratos primero) y luego por cobertura
        freelancers_ordenados = sorted(
            self.freelancers, 
            key=lambda f: (f.costo, -sum(1 for h in self.proyecto.requisitos 
                                        if f.tiene_habilidad(h, self.proyecto.requisitos[h])))
        )
        
        # Precomputar habilidades cubiertas por cada freelancer
        habilidades_por_freelancer = []
        for f in freelancers_ordenados:
            cubiertas = set()
            for habilidad, nivel_min in self.proyecto.requisitos.items():
                if f.tiene_habilidad(habilidad, nivel_min):
                    cubiertas.add(habilidad)
            habilidades_por_freelancer.append(cubiertas)
        
        # Verificar si hay solución posible
        habilidades_cubribles = set()
        for cubiertas in habilidades_por_freelancer:
            habilidades_cubribles.update(cubiertas)
        
        if habilidades_cubribles != set(self.proyecto.requisitos.keys()):
            return [], float('inf')  # No hay solución
        
        def backtrack(idx, equipo_actual, costo_actual, habilidades_cubiertas):
            self.nodos_explorados += 1
            
            # Si ya cubrimos todo, actualizar solución
            if habilidades_cubiertas == set(self.proyecto.requisitos.keys()):
                if costo_actual < self.mejor_costo:
                    self.mejor_costo = costo_actual
                    self.mejor_equipo = equipo_actual.copy()
                return
            
            # Si procesamos todos los freelancers
            if idx >= m:
                return
            
            # Podado 1: Por costo
            if costo_actual >= self.mejor_costo:
                return
            
            # Podado 2: Estimación optimista del costo mínimo restante
            habilidades_faltantes = len(self.proyecto.requisitos) - len(habilidades_cubiertas)
            if habilidades_faltantes > 0:
                # Buscar el freelancer más barato entre los restantes que cubra al menos una habilidad
                costo_min_por_habilidad = float('inf')
                for i in range(idx, m):
                    f = freelancers_ordenados[i]
                    nuevas = habilidades_por_freelancer[i] - habilidades_cubiertas
                    if nuevas:
                        costo_por_habilidad = f.costo / len(nuevas)
                        costo_min_por_habilidad = min(costo_min_por_habilidad, costo_por_habilidad)
                
                if costo_min_por_habilidad == float('inf'):
                    return  # No hay freelancers que cubran habilidades faltantes
                
                estimacion_costo = costo_actual + (costo_min_por_habilidad * habilidades_faltantes)
                if estimacion_costo >= self.mejor_costo:
                    return
            
            f_actual = freelancers_ordenados[idx]
            habilidades_f = habilidades_por_freelancer[idx]
            
            # Opción 1: No tomar este freelancer
            backtrack(idx + 1, equipo_actual, costo_actual, habilidades_cubiertas)
            
            # Opción 2: Tomar este freelancer (solo si aporta)
            nuevas_habilidades = habilidades_f - habilidades_cubiertas
            if nuevas_habilidades:
                backtrack(idx + 1,
                        equipo_actual + [f_actual],
                        costo_actual + f_actual.costo,
                        habilidades_cubiertas.union(habilidades_f))
        
        backtrack(0, [], 0, set())
        
        # Si no encontró solución pero debería haberla
        if self.mejor_costo == float('inf') and habilidades_cubribles == set(self.proyecto.requisitos.keys()):
            # Forzar búsqueda exhaustiva para debugging
            print("ADVERTENCIA: Backtracking no encontró solución pero debería existir")
            return self.resolver_por_enumeration()
        
        return self.mejor_equipo, self.mejor_costo