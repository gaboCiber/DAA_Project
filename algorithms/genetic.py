import random
from models.models import Freelancer, Proyecto
from algorithms.local_search import SolucionLocalSearch

class SolucionGenetico:
    def __init__(self, freelancers, proyecto, pop_size=50, generations=100, mutation_rate=0.05):
        self.freelancers = freelancers
        self.proyecto = proyecto
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.local_search = SolucionLocalSearch(freelancers, proyecto)

    def resolver_genetico(self):
        """
        Ejecuta el algoritmo genético.
        Devuelve (mejor_equipo, mejor_costo)
        """
        # 1. Inicialización
        poblacion = self._inicializar_poblacion()
        mejor_global = None
        mejor_costo_global = float('inf')
        
        for gen in range(self.generations):
            nueva_poblacion = []
            
            # Elitismo: Mantener al mejor
            poblacion_ordenada = sorted(poblacion, key=lambda ind: self._calcular_costo(ind))
            
            mejor_actual = poblacion_ordenada[0]
            costo_actual = self._calcular_costo(mejor_actual)
            
            if costo_actual < mejor_costo_global:
                mejor_costo_global = costo_actual
                mejor_global = mejor_actual
            
            nueva_poblacion.append(mejor_actual)
            
            # 2. Selección y Cruce
            while len(nueva_poblacion) < self.pop_size:
                p1 = self._torneo(poblacion)
                p2 = self._torneo(poblacion)
                
                hijo = self._cruce_uniforme(p1, p2)
                
                # 3. Mutación
                if random.random() < 0.2: # Probabilidad de mutar el individuo
                    hijo = self._mutacion(hijo)
                
                # 4. Reparación y Optimización local ligera
                hijo_reparado = self._reparar(hijo)
                # Opcional: eliminar redundantes para mantener la población "sana"
                hijo_optimizado = self.local_search.eliminar_redundantes(hijo_reparado)
                
                nueva_poblacion.append(hijo_optimizado)
            
            poblacion = nueva_poblacion
            
            # Logging opcional
            if gen % 20 == 0:
                # print(f"Generación {gen}: Mejor costo = {mejor_costo_global}")
                pass
                
        return mejor_global, mejor_costo_global

    def _inicializar_poblacion(self):
        poblacion = []
        # Generar individuos aleatorios y repararlos
        for _ in range(self.pop_size):
            # Selección aleatoria de freelancers (prob 0.1 de incluir cada uno inicial)
            ind = [f for f in self.freelancers if random.random() < 0.1]
            ind_valido = self._reparar(ind)
            ind_opt = self.local_search.eliminar_redundantes(ind_valido)
            poblacion.append(ind_opt)
        return poblacion

    def _torneo(self, poblacion, k=3):
        participantes = random.sample(poblacion, k)
        return min(participantes, key=lambda ind: self._calcular_costo(ind))

    def _cruce_uniforme(self, p1, p2):
        # Unión de conjuntos (conservadora) o Intersección?
        # En set cover, la unión es segura para cobertura, la intersección reduce costo.
        # Uniforme sobre la presencia:
        hijo = []
        set_p1 = set(f.id for f in p1)
        set_p2 = set(f.id for f in p2)
        
        # Unir todos los candidatos presentes en alguno
        pool = {f.id: f for f in p1 + p2}.values()
        
        for f in pool:
            in_p1 = f.id in set_p1
            in_p2 = f.id in set_p2
            
            if in_p1 and in_p2:
                hijo.append(f)
            elif in_p1 or in_p2:
                if random.random() < 0.5:
                    hijo.append(f)
        return hijo

    def _mutacion(self, individuo):
        mutado = list(individuo)
        # Flip bit: Quitar uno o Añadir uno
        if mutado and random.random() < 0.5:
            # Eliminar
            f_rem = random.choice(mutado)
            mutado.remove(f_rem)
        else:
            # Añadir
            candidatos = [f for f in self.freelancers if f not in mutado]
            if candidatos:
                f_add = random.choice(candidatos)
                mutado.append(f_add)
        return mutado

    def _reparar(self, individuo):
        """Asegura que el individuo cubra todos los requisitos añadiendo freelancers (Greedy)"""
        if self.local_search.es_solucion_valida(individuo):
            return individuo
            
        reparado = list(individuo)
        
        # Identificar qué falta
        faltantes = []
        for hab, nivel in self.proyecto.requisitos.items():
            cubierto = False
            for f in reparado:
                if f.tiene_habilidad(hab, nivel):
                    cubierto = True
                    break
            if not cubierto:
                faltantes.append((hab, nivel))
        
        # Cubrir faltantes (Greedy simple: el más barato que cubra el primero faltante)
        # Esto es mejorable, pero sirve para reparar.
        candidatos_pool = [f for f in self.freelancers if f not in reparado]
        
        while faltantes:
            hab_target, nivel_target = faltantes[0]
            
            # Buscar el más barato que cubra esta habilidad
            mejor_candidato = None
            mejor_costo = float('inf')
            
            for f in candidatos_pool:
                if f.tiene_habilidad(hab_target, nivel_target):
                    if f.costo < mejor_costo:
                        mejor_costo = f.costo
                        mejor_candidato = f
            
            if mejor_candidato:
                reparado.append(mejor_candidato)
                candidatos_pool.remove(mejor_candidato)
            else:
                # No se pudo cubrir, devolver lo que hay (será penalizado o inválido)
                # En teoría si la instancia es factible, siempre habrá candidato.
                pass
            
            # Recalcular faltantes
            # (Podríamos optimizar no recalculando todo, pero esto es seguro)
            faltantes = []
            for hab, nivel in self.proyecto.requisitos.items():
                cubierto = False
                for f in reparado:
                    if f.tiene_habilidad(hab, nivel):
                        cubierto = True
                        break
                if not cubierto:
                    faltantes.append((hab, nivel))
                    
        return reparado

    def _calcular_costo(self, individuo):
        return sum(f.costo for f in individuo)
