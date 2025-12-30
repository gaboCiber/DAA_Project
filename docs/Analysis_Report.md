# Análisis Experimental de Algoritmos - Proyecto DAA

## 1. Metodología
Se compararon cuatro enfoques para resolver el problema Minimum-Cost Skill-Cover (MCSC):
1. **Fuerza Bruta (FB):** Exacto, complejidad exponencial.
2. **Greedy:** Aproximado, heurística constructiva.
3. **Búsqueda Local (LS):** Mejora iterativa sobre Greedy.
4. **Algoritmo Genético (GA):** Metaheurística poblacional.
5. **Híbrido:** Kernelization + Selección dinámica de algoritmo.

Se utilizaron instancias aleatorias con $m \in \{10, 20, 50, 150\}$ freelancers.

## 2. Resultados Experimentales

| m (Freelancers) | Solución Óptima (Costo) | Greedy | Híbrido (Nuestro Enfoque) | Tiempo Híbrido | Notas |
|-----------------|-------------------------|--------|---------------------------|----------------|-------|
| 10 | 108.0 | 108.0 | 108.0 | 0.0001s | Todos encuentran el óptimo. |
| 20 | 77.0 | 84.0 | 77.0 | 0.0001s | Greedy falla en óptimo. Híbrido lo encuentra. |
| 50 | *N/A* | 115.0 | 115.0 | 0.0003s | Kernel reduce a 11 freelancers -> FB exacto. |
| 150 | *N/A* | 43.0 | 41.0 | 0.0006s | Kernel reduce a 12 freelancers -> FB exacto. |

## 3. Hallazgos Clave

### Efectividad de Kernelization
El preprocesamiento (Kernelization) demostró ser extremadamente efectivo en las instancias aleatorias generadas.
- Para $m=150$, la regla de dominancia redujo el problema a solo **12 freelancers** candidatos reales.
- Esto permitió que el **Solucionador Híbrido** aplicara **Fuerza Bruta** sobre el conjunto reducido, garantizando la **solución óptima** en tiempo insignificante ($< 1ms$), superando a la aproximación Greedy (Costo 41 vs 43).

### Comparación de Algoritmos
- **Greedy:** Muy rápido, pero no garantiza optimalidad (error del ~9% en caso $m=20$).
- **Genético:** Robusto, alcanzó el óptimo en casos grandes pero requiere más tiempo ($0.02s$).
- **Híbrido:** Es el claro ganador. La combinación de reducción drástica + algoritmo exacto ofrece lo mejor de ambos mundos: garantía de calidad y velocidad extrema.

## 4. Conclusión
La estrategia híbrida implementada es exitosa. La inclusión de reglas de reducción (Kernelization) transforma instancias aparentemente intratables en problemas triviales para estas distribuciones de datos, validando la importancia del análisis teórico previo a la implementación.
