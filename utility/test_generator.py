import random
from models.models import Freelancer, Proyecto

def crear_instancia_aleatoria(m, n_habilidades, densidad=0.3, seed=None):
    """
    Crea una instancia aleatoria del problema
    
    Args:
        m: número de freelancers
        n_habilidades: número total de habilidades posibles
        densidad: probabilidad de que un freelancer tenga una habilidad
        seed: semilla para reproducibilidad
    """
    if seed is not None:
        random.seed(seed)
    
    # Crear habilidades (H1, H2, ..., Hn)
    habilidades = [f"H{i+1}" for i in range(n_habilidades)]
    
    # Crear freelancers
    freelancers = []
    for i in range(m):
        costo = random.randint(20, 100)  # Costo entre 20 y 100
        f = Freelancer(i + 1, costo)
        
        # Asignar habilidades aleatoriamente
        for habilidad in habilidades:
            if random.random() < densidad:  # Probabilidad de tener la habilidad
                nivel = random.randint(1, 5)  # Nivel entre 1 y 5
                f.agregar_habilidad(habilidad, nivel)
        
        freelancers.append(f)
    
    # Crear proyecto con requisitos aleatorios
    proyecto = Proyecto()
    n_requisitos = random.randint(1, min(5, n_habilidades))
    habilidades_requeridas = random.sample(habilidades, n_requisitos)
    
    for habilidad in habilidades_requeridas:
        nivel_min = random.randint(1, 3)  # Nivel mínimo requerido
        proyecto.agregar_requisito(habilidad, nivel_min)
    
    return freelancers, proyecto

def crear_instancia_manual():
    """Crea una instancia manual para testing"""
    # Ejemplo del documento
    freelancers = []
    
    f1 = Freelancer(1, 50)
    f1.agregar_habilidad("Frontend", 4)
    f1.agregar_habilidad("DB", 2)
    freelancers.append(f1)
    
    f2 = Freelancer(2, 40)
    f2.agregar_habilidad("DB", 4)
    f2.agregar_habilidad("UX", 3)
    freelancers.append(f2)
    
    f3 = Freelancer(3, 60)
    f3.agregar_habilidad("Frontend", 5)
    f3.agregar_habilidad("UX", 5)
    freelancers.append(f3)
    
    proyecto = Proyecto()
    proyecto.agregar_requisito("Frontend", 4)
    proyecto.agregar_requisito("DB", 3)
    proyecto.agregar_requisito("UX", 4)
    
    return freelancers, proyecto