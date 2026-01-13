import time
import math
from models.models import Freelancer, Proyecto
from algorithms.brute_force import SolucionFuerzaBruta
from utility.test_generator import crear_instancia_aleatoria
from algorithms.greedy import SolucionGreedy
from algorithms.local_search import SolucionLocalSearch
from algorithms.genetic import SolucionGenetico
from algorithms.hybrid import SolucionHibrida
from main import main, test_casos_especiales

def comparar_algoritmos():
    """Compara todos los algoritmos implementados"""
    print("=== COMPARATIVA DE ALGORITMOS: MCSC PROJECT ===\n")
    
    resultados = []
    
    # Rango de pruebas (ajustar según tiempo)
    instancias = [10, 20, 50, 150, 300, 500, 750, 1000]
    
    for m in instancias:
        print(f"\n--- Instancia con m={m} freelancers ---")
        
        # Crear instancia
        freelancers, proyecto = crear_instancia_aleatoria(
            m=m, 
            n_habilidades=max(10, m//2 + 2),
            n_requisitos=int(math.sqrt(m)),
            densidad=0.4,
            seed=m*10
        )
        
        print(f"Habilidades requeridas: {len(proyecto.requisitos)}")
        
        row = {'m': m}
        
        # 1. Fuerza Bruta (Solo para m <= 20)
        costo_fb = float('inf')
        if m <= 900:
            print("1. Fuerza Bruta: ", end="", flush=True)
            sol_fb = SolucionFuerzaBruta(freelancers, proyecto)
            start = time.time()
            equipo_fb, costo_fb = sol_fb.resolver_backtracking_con_podas_avanzadas()
            tiempo_fb = time.time() - start
            print(f"{costo_fb} ({tiempo_fb:.4f}s)")
            row['fb_costo'] = costo_fb
            row['fb_tiempo'] = tiempo_fb
        else:
            print("1. Fuerza Bruta: Skipped (m > 20)")
            row['fb_costo'] = -1
            row['fb_tiempo'] = -1
            
        # 2. Greedy (Ratio)
        print("2. Greedy: ", end="", flush=True)
        sol_greedy = SolucionGreedy(freelancers, proyecto)
        start = time.time()
        equipo_gr, costo_gr = sol_greedy.resolver_greedy_ratio()
        tiempo_gr = time.time() - start
        print(f"{costo_gr} ({tiempo_gr:.4f}s)")
        row['greedy_costo'] = costo_gr
        row['greedy_tiempo'] = tiempo_gr
        
        # 3. Local Search (Mejorando Greedy)
        print("3. Local Search: ", end="", flush=True)
        # Necesita solución inicial
        if equipo_gr:
            ls = SolucionLocalSearch(freelancers, proyecto)
            start = time.time()
            equipo_ls, costo_ls = ls.resolver_local_search(equipo_gr)
            tiempo_ls = time.time() - start + tiempo_gr # Sumamos el tiempo de greedy
            print(f"{costo_ls} ({tiempo_ls:.4f}s)")
            row['ls_costo'] = costo_ls
            row['ls_tiempo'] = tiempo_ls
        else:
             print("Skipped (Greedy failed)")
             row['ls_costo'] = float('inf')
             row['ls_tiempo'] = -1

        # 4. Genético
        print("4. Genético: ", end="", flush=True)
        # Menos generaciones para la prueba rápida
        genetico = SolucionGenetico(freelancers, proyecto, pop_size=40, generations=50)
        start = time.time()
        equipo_gen, costo_gen = genetico.resolver_genetico()
        tiempo_gen = time.time() - start
        print(f"{costo_gen} ({tiempo_gen:.4f}s)")
        row['gen_costo'] = costo_gen
        row['gen_tiempo'] = tiempo_gen
        
        # 5. Híbrido
        print("5. Híbrido: ", end="", flush=True)
        hibrido = SolucionHibrida(freelancers, proyecto)
        start = time.time()
        equipo_hib, costo_hib, log_hib = hibrido.resolver()
        tiempo_hib = time.time() - start
        print(f"{costo_hib} ({tiempo_hib:.4f}s) [{log_hib}]")
        row['hib_costo'] = costo_hib
        row['hib_tiempo'] = tiempo_hib
        
        resultados.append(row)
    
    # Resumen
    print("\n" + "="*100)
    print("RESUMEN DE RESULTADOS (Costos):")
    print("="*100)
    print(f"{'m':>4} | {'FB':>8} | {'Greedy':>8} | {'LS':>8} | {'Genético':>8} | {'Híbrido':>8}")
    print("-" * 100)
    
    for r in resultados:
        fb = f"{r['fb_costo']:.1f}" if r['fb_costo'] != -1 else "N/A"
        print(f"{r['m']:4d} | {fb:>8} | {r['greedy_costo']:8.1f} | {r['ls_costo']:8.1f} | {r['gen_costo']:8.1f} | {r['hib_costo']:8.1f}")

if __name__ == "__main__":
    comparar_algoritmos()