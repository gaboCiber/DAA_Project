# Diseño de Soluciones Algorítmicas - Proyecto DAA

## 1. Introducción

Dada la demostración de que el problema **Minimum-Cost Skill-Cover (MCSC)** es NP-duro (mediante reducción desde Set Cover), proponemos un enfoque híbrido que combina algoritmos exactos para instancias pequeñas y metaheurísticas para instancias de gran escala.

## 2. Algoritmos Diseñados

### 2.1 Algoritmo Exacto: Fuerza Bruta con Podas
*Para instancias pequeñas ($m \le 20$)*

**Estrategia:** Backtracking con poda por costo y viabilidad.
- **Entrada:** Lista de freelancers $F$, Requisitos $R$.
- **Proceso:**
  - Explorar el árbol de decisión: incluir/excluir cada freelancer.
  - **Poda de Optimidad:** Si costo actual $\ge$ costo de mejor solución encontrada $\rightarrow$ podar.
  - **Poda de Viabilidad:** Si freelancers restantes no pueden cubrir habilidades faltantes $\rightarrow$ podar.
- **Complejidad:** $O(2^m \cdot m \cdot n)$.

### 2.2 Algoritmos de Aproximación: Greedy
*Para soluciones rápidas y línea base de heurísticas*

**Estrategia:** Selección voraz iterativa.
- **Variante 1 (Ratio Cobertura/Costo):** Seleccionar $f$ que maximice $\frac{|nuevas\_habilidades|}{costo}$.
- **Variante 2 (Costo Efectivo):** Seleccionar $f$ que minimice $\frac{costo}{|nuevas\_habilidades|}$.
- **Garantía Teórica:** Aproximación logarítmica $O(\ln n)$ similar a Set Cover.

### 2.3 Heurística de Búsqueda Local (Local Search)
*Para mejorar soluciones Greedy*

**Estrategia:** Hill Climbing / Descendo de Gradiente discreto.
- **Inicialización:** Solución generada por Greedy.
- **Vecindad:**
  1. **Intercambio (Swap) 2-1:** Reemplazar 2 freelancers por 1 más barato que cubra lo mismo.
  2. **Intercambio 1-1:** Reemplazar 1 freelancer por otro más barato.
  3. **Eliminación:** Eliminar freelancers redundantes.
- **Terminación:** Mínimo local (no hay mejoras en la vecindad).

### 2.4 Metaheurística: Algoritmo Genético
*Para instancias grandes ($m > 100$)*

**Estrategia:** Evolución poblacional.
- **Representación:** Cromosoma binario de longitud $m$ ($1=$ seleccionado, $0=$ no).
- **Fitness:** Función que penaliza fuertemente soluciones inválidas (no cubren $R$).
  $$Fitness(S) = \frac{1}{Costo(S) + Penalización \times HabilidadesFaltantes}$$
- **Operadores:**
  - **Selección:** Torneo o Ruleta.
  - **Cruce (Crossover):** Uniforme o de un punto.
  - **Mutación:** Flip bit con baja probabilidad.
  - **Reparación:** Aplicar Greedy para completar soluciones inválidas hijas.

### 2.5 Kernelization (Preprocesamiento)
Reglas de reducción para disminuir el tamaño de la instancia:
1. **Dominancia:** Si $f_A$ cuesta menos que $f_B$ y cubre un superconjunto de las habilidades de $f_B$ (con niveles $\ge$), eliminar $f_B$.
2. **Esencialidad:** Si una habilidad solo es cubierta por un único freelancer $f$, $f$ debe incluirse obligatoriamente.

## 3. Estrategia Híbrida

El solucionador final decidirá el algoritmo según el tamaño de la instancia:

| Tamaño ($m$) | Algoritmo Recomendado |
|--------------|-----------------------|
| $m \le 20$   | Fuerza Bruta (Exacto) |
| $20 < m \le 100$ | Greedy + Búsqueda Local |
| $m > 100$    | Algoritmo Genético |

Además, **siempre** se aplicará Kernelization al inicio para reducir el problema.
