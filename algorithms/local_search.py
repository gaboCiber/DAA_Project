class SolucionLocalSearch:
    def __init__(self, freelancers, proyecto):
        self.freelancers = freelancers
        self.proyecto = proyecto

    def resolver_local_search(self, solucion_inicial):
        """
        Mejora una solución inicial usando búsqueda local (Hill Climbing).
        Operadores:
        1. Eliminar redundantes.
        2. Intercambio 1-1 (Swap): Reemplazar un freelancer por otro más barato.
        """
        mejor_solucion = list(solucion_inicial) # Copia
        mejor_costo = sum(f.costo for f in mejor_solucion)
        
        mejorando = True
        
        while mejorando:
            mejorando = False
            
            # 1. Intentar eliminar redundantes
            solucion_reducida = self.eliminar_redundantes(mejor_solucion)
            costo_reducido = sum(f.costo for f in solucion_reducida)
            
            if costo_reducido < mejor_costo:
                mejor_solucion = solucion_reducida
                mejor_costo = costo_reducido
                mejorando = True
                continue # Reiniciar búsqueda desde la nueva mejor
            
            # 2. Intentar intercambio 1-1
            # Para cada f_in (en solución) y f_out (fuera de solución)
            candidatos_fuera = [f for f in self.freelancers if f not in mejor_solucion]
            
            for i, f_in in enumerate(mejor_solucion):
                for f_out in candidatos_fuera:
                    # Condición de poda rápida: el entrante debe ser más barato
                    if f_out.costo >= f_in.costo:
                        continue
                        
                    # Probar intercambio
                    nueva_propuesta = mejor_solucion[:i] + mejor_solucion[i+1:] + [f_out]
                    
                    if self.es_solucion_valida(nueva_propuesta):
                        mejor_solucion = nueva_propuesta
                        mejor_costo = sum(f.costo for f in mejor_solucion)
                        mejorando = True
                        break # First Improvement
                
                if mejorando: break
            
            # Aquí podríamos agregar Swap 2-1 si fuera necesario para más calidad
            
        return mejor_solucion, mejor_costo

    def eliminar_redundantes(self, equipo):
        """Intenta eliminar freelancers sin romper la validez"""
        # Ordenar por costo descendente para intentar quitar los caros primero
        equipo_ordenado = sorted(equipo, key=lambda f: f.costo, reverse=True)
        equipo_final = equipo_ordenado.copy()
        
        for freelancer in equipo_ordenado:
            # Probar quitar este freelancer
            propuesta = [f for f in equipo_final if f.id != freelancer.id]
            if self.es_solucion_valida(propuesta):
                equipo_final = propuesta
                
        return equipo_final

    def es_solucion_valida(self, equipo):
        """Verifica si el equipo cubre todos los requisitos"""
        for hab, nivel_req in self.proyecto.requisitos.items():
            cubierto = False
            for f in equipo:
                if f.tiene_habilidad(hab, nivel_req):
                    cubierto = True
                    break
            if not cubierto:
                return False
        return True
