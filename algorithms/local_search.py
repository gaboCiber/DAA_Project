class SolucionLocalSearch:
    def __init__(self, freelancers, proyecto):
        self.freelancers = freelancers
        self.proyecto = proyecto

class SolucionLocalSearch:
    def __init__(self, freelancers, proyecto):
        self.freelancers = freelancers
        self.proyecto = proyecto

    def resolver_local_search(self, solucion_inicial):
        """
        Mejora una solución inicial usando búsqueda local.
        Sigue fielmente el Algoritmo 4.3 del informe:
        1. Intercambio 2-1: Reemplazar dos freelancers por uno más barato.
        2. Eliminación redundante: Quitar freelancers innecesarios.
        3. Intercambio 1-1: Reemplazar uno por uno (Extensión adicional).
        """
        mejor_solucion = list(solucion_inicial)
        mejor_costo = sum(f.costo for f in mejor_solucion)
        
        mejorando = True
        while mejorando:
            mejorando = False
            
            # Buscamos dos freelancers (f1, f2) que puedan ser reemplazados por f3
            for i in range(len(mejor_solucion)):
                for j in range(i + 1, len(mejor_solucion)):
                    f1 = mejor_solucion[i]
                    f2 = mejor_solucion[j]
                    
                    candidatos_fuera = [f for f in self.freelancers if f not in mejor_solucion]
                    for f3 in candidatos_fuera:
                        # Condición de costo: f3 debe ser más barato que la suma de f1 y f2
                        if f3.costo < (f1.costo + f2.costo):
                            # Probar reemplazo
                            propuesta = [f for f in mejor_solucion if f is not f1 and f is not f2]
                            propuesta.append(f3)
                            
                            if self.es_solucion_valida(propuesta):
                                mejor_solucion = propuesta
                                mejor_costo = sum(f.costo for f in mejor_solucion)
                                mejorando = True
                                break
                    if mejorando: break
                if mejorando: break
            if mejorando: continue # Reiniciar bucle principal (First Improvement)

            for freelancer in mejor_solucion:
                propuesta = [f for f in mejor_solucion if f is not freelancer]
                if self.es_solucion_valida(propuesta):
                    mejor_solucion = propuesta
                    mejor_costo = sum(f.costo for f in mejor_solucion)
                    mejorando = True
                    break
            if mejorando: continue

            candidatos_fuera = [f for f in self.freelancers if f not in mejor_solucion]
            for i, f_in in enumerate(mejor_solucion):
                for f_out in candidatos_fuera:
                    # Solo intentamos si el nuevo costo total es menor
                    nuevo_costo = mejor_costo - f_in.costo + f_out.costo
                    if nuevo_costo < mejor_costo:
                        propuesta = mejor_solucion[:i] + mejor_solucion[i+1:] + [f_out]
                        if self.es_solucion_valida(propuesta):
                            mejor_solucion = propuesta
                            mejor_costo = nuevo_costo
                            mejorando = True
                            break
                if mejorando: break
            
        return mejor_solucion, mejor_costo

    def eliminar_redundantes(self, equipo):
        """Versión batch-greedy (usada por el Genético)"""
        equipo_ordenado = sorted(equipo, key=lambda f: f.costo, reverse=True)
        equipo_final = list(equipo_ordenado)
        
        for freelancer in equipo_ordenado:
            propuesta = [f for f in equipo_final if f is not freelancer]
            if self.es_solucion_valida(propuesta):
                equipo_final = propuesta
                
        return equipo_final

    def es_solucion_valida(self, equipo):
        """Verifica si el equipo cubre todos los requisitos"""
        if not equipo and self.proyecto.requisitos:
            return False
        for hab, nivel_req in self.proyecto.requisitos.items():
            cubierto = False
            for f in equipo:
                if f.tiene_habilidad(hab, nivel_req):
                    cubierto = True
                    break
            if not cubierto:
                return False
        return True
