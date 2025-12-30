from models.models import Freelancer, Proyecto
from algorithms.kernelization import Kernelizador

def test_kernelization():
    print("=== TEST KERNELIZATION ===\n")
    
    # Setup Proyecto
    proyecto = Proyecto()
    proyecto.agregar_requisito("Java", 3)
    proyecto.agregar_requisito("Python", 2)
    proyecto.agregar_requisito("SQL", 1)
    
    print(f"Proyecto: {proyecto.requisitos}")
    
    # Crear Freelancers
    # F1: Caro, cubre todo (No esencial si hay otros)
    f1 = Freelancer(1, 100)
    f1.agregar_habilidad("Java", 5)
    f1.agregar_habilidad("Python", 5)
    f1.agregar_habilidad("SQL", 5)
    
    # F2: Barato, cubre todo (Domina a F1)
    f2 = Freelancer(2, 50)
    f2.agregar_habilidad("Java", 5)
    f2.agregar_habilidad("Python", 5)
    f2.agregar_habilidad("SQL", 5)
    
    # F3: Muy barato, pero solo Python (No dominado por F2 porque F2 es más caro? No, F2 cubre más. F2 no domina a F3 costo 50 vs ??. 
    # Espera, para dominar, F2 debe costar MENOS y cubrir MAS.
    # Si F3 cuesta 10, F2 cuesta 50. F3 es más barato. F2 no domina a F3.
    # ¿F3 domina a F2? No, F3 cubre menos.
    f3 = Freelancer(3, 10)
    f3.agregar_habilidad("Python", 5)
    
    # F4: Igual a F3 pero más caro (Dominado por F3)
    f4 = Freelancer(4, 20)
    f4.agregar_habilidad("Python", 5)

    # F5: Esencial para SQL (si quitamos a F1/F2 o si definimos que solo él la tiene)
    # Pero aquí F1 y F2 tienen SQL.
    # Vamos a crear un requerimiento nuevo y un freelancer único para probar esencialidad.
    proyecto.agregar_requisito("Rust", 1)
    f_rust = Freelancer(99, 50)
    f_rust.agregar_habilidad("Rust", 5)
    
    freelancers = [f1, f2, f3, f4, f_rust]
    
    print(f"\nFreelancers iniciales ({len(freelancers)}):")
    for f in freelancers:
        print(f)
        
    kernel = Kernelizador(freelancers, proyecto)
    candidatos, esenciales = kernel.ejecutar()
    
    print(f"\nResultados:")
    print(f"Candidatos restantes ({len(candidatos)}): {[f.id for f in candidatos]}")
    print(f"Esenciales ({len(esenciales)}): {[f.id for f in esenciales]}")
    print(f"Removidos: {kernel.removidos}")
    
    # Verificaciones
    ids_candidatos = [f.id for f in candidatos]
    
    # 1. F1 dominado por F2?
    # F2 (50) vs F1 (100). F2 cubre lo mismo. F2 < F1 costo. -> F1 eliminado.
    assert 1 not in ids_candidatos, "F1 debería estar eliminado (dominado por F2)"
    
    # 2. F4 dominado por F3?
    # F3 (10) vs F4 (20). Mismas habs. -> F4 eliminado.
    assert 4 not in ids_candidatos, "F4 debería estar eliminado (dominado por F3)"
    
    # 3. F_Rust esencial?
    # Es el único con Rust. -> Debe estar en esenciales.
    ids_esenciales = [f.id for f in esenciales]
    assert 99 in ids_esenciales, "F99 debería ser esencial (único con Rust)"
    
    print("\n✅ Todos los tests pasaron correctamente.")

if __name__ == "__main__":
    test_kernelization()
