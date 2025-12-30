import time
from models.models import Freelancer, Proyecto
from algorithms.brute_force import SolucionFuerzaBruta
from utility.test_generator import crear_instancia_aleatoria, crear_instancia_manual

def main():
    print("=== ALGORITMO DE FUERZA BRUTA - TALENTBRIDGE CONNECT ===\n")
    
    # Prueba con instancia manual
    print("1. Instancia Manual (Ejemplo del documento):")
    freelancers, proyecto = crear_instancia_manual()
    
    print(f"Proyecto: {proyecto}")
    print(f"Freelancers disponibles ({len(freelancers)}):")
    for f in freelancers:
        print(f"  {f}")
    print()
    
    # Probar diferentes versiones del algoritmo
    solucionador = SolucionFuerzaBruta(freelancers, proyecto)
    
    # Versión 1: Enumeración exhaustiva
    start_time = time.time()
    equipo_optimo, costo_optimo = solucionador.resolver_por_enumeration()
    elapsed = time.time() - start_time
    
    print("a) Enumeración Exhaustiva:")
    print(f"   Tiempo: {elapsed:.6f} segundos")
    print(f"   Nodos explorados: {solucionador.nodos_explorados}")
    print(f"   Equipo óptimo ({len(equipo_optimo)} freelancers):")
    for f in equipo_optimo:
        print(f"     - {f}")
    print(f"   Costo total: {costo_optimo}")
    print()
    
    # Versión 2: Backtracking simple
    start_time = time.time()
    equipo_optimo, costo_optimo = solucionador.resolver_backtracking()
    elapsed = time.time() - start_time
    
    print("b) Backtracking Simple:")
    print(f"   Tiempo: {elapsed:.6f} segundos")
    print(f"   Nodos explorados: {solucionador.nodos_explorados}")
    print(f"   Equipo óptimo ({len(equipo_optimo)} freelancers):")
    for f in equipo_optimo:
        print(f"     - {f}")
    print(f"   Costo total: {costo_optimo}")
    print()
    
    # Versión 3: Backtracking con podas avanzadas
    start_time = time.time()
    equipo_optimo, costo_optimo = solucionador.resolver_backtracking_con_podas_avanzadas()
    elapsed = time.time() - start_time
    
    print("c) Backtracking con Podas Avanzadas:")
    print(f"   Tiempo: {elapsed:.6f} segundos")
    print(f"   Nodos explorados: {solucionador.nodos_explorados}")
    print(f"   Equipo óptimo ({len(equipo_optimo)} freelancers):")
    for f in equipo_optimo:
        print(f"     - {f}")
    print(f"   Costo total: {costo_optimo}")
    print()
    
    # Prueba con instancia aleatoria pequeña
    print("\n2. Instancia Aleatoria Pequeña (m=10, n_habilidades=6):")
    freelancers, proyecto = crear_instancia_aleatoria(
        m=10, 
        n_habilidades=6, 
        densidad=0.4,
        seed=42
    )
    
    print(f"Proyecto: {proyecto}")
    print(f"Número de freelancers: {len(freelancers)}")
    
    solucionador = SolucionFuerzaBruta(freelancers, proyecto)
    
    start_time = time.time()
    equipo_optimo, costo_optimo = solucionador.resolver_backtracking_con_podas_avanzadas()
    elapsed = time.time() - start_time
    
    print(f"Tiempo de ejecución: {elapsed:.4f} segundos")
    print(f"Nodos explorados: {solucionador.nodos_explorados}")
    print(f"Costo óptimo: {costo_optimo}")
    print(f"Tamaño del equipo óptimo: {len(equipo_optimo)}")
    
    # Análisis de complejidad experimental
    print("\n3. Análisis de Tiempo de Ejecución (Backtracking con Podas):")
    print("   m | Tiempo (s) | Nodos Explorados | Solución Encontrada")
    print("   " + "-" * 50)
    
    for m in [5, 10, 12, 15, 18]:
        freelancers, proyecto = crear_instancia_aleatoria(
            m=m, 
            n_habilidades=8,
            densidad=0.3,
            seed=m
        )
        
        solucionador = SolucionFuerzaBruta(freelancers, proyecto)
        start_time = time.time()
        equipo_optimo, costo_optimo = solucionador.resolver_backtracking_con_podas_avanzadas()
        elapsed = time.time() - start_time
        
        encontrada = "Sí" if equipo_optimo else "No"
        print(f"   {m:2d} | {elapsed:10.6f} | {solucionador.nodos_explorados:15d} | {encontrada}")

def test_casos_especiales():
    """Prueba casos especiales"""
    print("\n=== CASOS ESPECIALES ===\n")
    
    # Caso 1: Un freelancer cubre todo
    print("Caso 1: Un freelancer cubre todo")
    freelancers = []
    f1 = Freelancer(1, 50)
    f1.agregar_habilidad("A", 5)
    f1.agregar_habilidad("B", 5)
    f1.agregar_habilidad("C", 5)
    freelancers.append(f1)
    
    f2 = Freelancer(2, 30)
    f2.agregar_habilidad("A", 3)
    freelancers.append(f2)
    
    proyecto = Proyecto()
    proyecto.agregar_requisito("A", 3)
    proyecto.agregar_requisito("B", 2)
    proyecto.agregar_requisito("C", 1)
    
    solucionador = SolucionFuerzaBruta(freelancers, proyecto)
    equipo, costo = solucionador.resolver_backtracking_con_podas_avanzadas()
    
    print(f"Equipo: {[f.id for f in equipo]}, Costo: {costo}")
    print(f"Esperado: Solo freelancer 1, Costo: 50")
    
    # Caso 2: No hay solución
    print("\nCaso 2: No hay solución posible")
    freelancers = []
    f1 = Freelancer(1, 50)
    f1.agregar_habilidad("A", 2)  # Necesita nivel 3
    freelancers.append(f1)
    
    proyecto = Proyecto()
    proyecto.agregar_requisito("A", 3)
    
    solucionador = SolucionFuerzaBruta(freelancers, proyecto)
    equipo, costo = solucionador.resolver_backtracking_con_podas_avanzadas()
    
    if not equipo:
        print("Correcto: No se encontró solución")
    else:
        print(f"Equipo encontrado: {[f.id for f in equipo]}")

if __name__ == "__main__":
    main()
    test_casos_especiales()