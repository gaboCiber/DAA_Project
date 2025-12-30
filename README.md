# TalentBridge Connect - Minimum-Cost Skill-Cover Solver

**Asignatura:** Diseño y Análisis de Algoritmos (DAA)  
**Año:** 4to Año, Ciencia de la Computación  

## 1. Descripción del Proyecto
Este proyecto aborda el problema de selección óptima de equipos de freelancers ("Minimum-Cost Skill-Cover Problem"), un problema **NP-Completo** formalmente equivalente al **Set Cover Problem**.

El objetivo es seleccionar el subconjunto de freelancers más económico tal que se cubran todos los requisitos de habilidades de un proyecto con el nivel de experiencia requerido.

## 2. Estructura del Proyecto

```
DAA_Project/
├── algorithms/         # Implementación de Algoritmos
│   ├── brute_force.py  # Algoritmo Exacto (Backtracking)
│   ├── greedy.py       # Aproximación Voraz
│   ├── local_search.py # Heurística (Hill Climbing)
│   ├── genetic.py      # Metaheurística (Algoritmo Genético)
│   ├── kernelization.py# Preprocesamiento (Reglas de Reducción)
│   └── hybrid.py       # Solucionador Inteligente
├── models/             # Modelos de Datos (Freelancer, Proyecto)
├── utilities/          # Generadores de instancias de prueba
├── docs/               # Documentación Técnica
│   ├── NP-Completness.tex  # Demostración formal
│   ├── Analysis_Report.md  # Reporte de resultados
│   └── Algorithm_Design.md # Diseño detallado
├── main.py             # Script principal de demostración
└── comp.py             # Script de benchmarking comparativo
```

## 3. Algoritmos Implementados

El proyecto implementa una variedad de enfoques para atacar la complejidad del problema:

| Algoritmo | Tipo | Uso Recomendado |
|-----------|------|-----------------|
| **Fuerza Bruta** | Exacto | Instancias pequeñas ($m \le 20$) |
| **Greedy** | Aproximación | Respuesta inmediata, calidad variable |
| **Búsqueda Local** | Heurística | Mejora soluciones Greedy |
| **Genético** | Metaheurística | Instancias grandes y complejas |
| **Híbrido** | **Orquestador** | Estrategia final recomendada |

### 🔥 Kernelization (La Clave del Éxito)
Implementamos reglas de reducción (dominancia y esencialidad) que eliminan candidatos irrelevantes antes de ejecutar cualquier algoritmo. **Resultado:** Reduce drásticamente el espacio de búsqueda, permitiendo resolver instancias de 150+ freelancers de manera exacta en milisegundos.

## 4. Instrucciones de Ejecución

### Requisitos
- Python 3.8+

### Ejecución Básica
Para ver una demostración con instancias manuales y aleatorias:
```bash
python main.py
```

### Benchmarking (Comparativa)
Para ejecutar el análisis experimental que compara todos los algoritmos:
```bash
python comp.py
```

## 5. Resultados Destacados
El enfoque **Híbrido** demostró ser superior. En pruebas con 150 freelancers, el preprocesamiento redujo el problema a ~12 candidatos efectivos, permitiendo encontrar la **solución óptima** instantáneamente, superando en calidad a las aproximaciones tradicionales.

Ver `docs/Analysis_Report.md` para más detalles.
