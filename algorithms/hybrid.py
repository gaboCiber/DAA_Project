from algorithms.kernelization import Kernelizador
from algorithms.brute_force import SolucionFuerzaBruta
from algorithms.greedy import SolucionGreedy
from algorithms.local_search import SolucionLocalSearch
from algorithms.genetic import SolucionGenetico

class SolucionHibrida:
    def __init__(self, freelancers, proyecto):
        self.freelancers = freelancers
        self.proyecto = proyecto
        self.log_estrategia = ""

    def resolver(self):
        """
        Resuelve el problema utilizando una estrategia híbrida:
        1. Preprocesamiento (Kernelization) para reducir el tamaño.
        2. Selección de algoritmo según el tamaño restante (m).
        """
        # 1. Kernelization
        kernel = Kernelizador(self.freelancers, self.proyecto)
        candidatos, esenciales = kernel.ejecutar()
        
        m = len(candidatos)
        original_m = len(self.freelancers)
        
        self.log_estrategia = f"Reducción: {original_m} -> {m} freelancers."
        
        equipo_optimo = []
        costo_optimo = float('inf')
        
        # 2. Selección de Estrategia
        if m <= 900:
            # Estrategia Exacta
            self.log_estrategia += " Usando Fuerza Bruta (Exacto)."
            fb = SolucionFuerzaBruta(candidatos, self.proyecto)
            # Usamos la versión con podas que es la más rápida exacta
            equipo_optimo, costo_optimo = fb.resolver_backtracking_con_podas_avanzadas()
            
        elif m <= 500:
            # Estrategia Metaheurística Ligera (Greedy + Local Search)
            self.log_estrategia += " Usando Greedy + Búsqueda Local."
            greedy = SolucionGreedy(candidatos, self.proyecto)
            # Generar solución inicial rápida (Ratio suele ser mejor)
            sol_inicial, _ = greedy.resolver_greedy_ratio()
            
            if sol_inicial:
                ls = SolucionLocalSearch(candidatos, self.proyecto)
                equipo_optimo, costo_optimo = ls.resolver_local_search(sol_inicial)
            else:
                equipo_optimo, costo_optimo = [], float('inf')
                
        else:
            # Estrategia Metaheurística Poblacional (Genético)
            self.log_estrategia += " Usando Algoritmo Genético."
            genetico = SolucionGenetico(candidatos, self.proyecto, pop_size=50, generations=100)
            equipo_optimo, costo_optimo = genetico.resolver_genetico()

        return equipo_optimo, costo_optimo, self.log_estrategia
