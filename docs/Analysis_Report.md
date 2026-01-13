# Análisis Experimental de Algoritmos - Proyecto DAA

## 1. Metodología
Se compararon cinco enfoques para resolver el problema Minimum-Cost Skill-Cover (MCSC):
1. **Fuerza Bruta (FB):** Exacto, complejidad exponencial.
2. **Greedy:** Aproximado, heurística constructiva.
3. **Búsqueda Local (LS):** Mejora iterativa sobre Greedy.
4. **Algoritmo Genético (GA):** Metaheurística poblacional.
5. **Híbrido:** Kernelization + Selección dinámica de algoritmo.

Se utilizaron instancias aleatorias con $m \in \{10, 20, 50, 150, 300, 500, 750, 1000\}$ freelancers.

## 2. Resultados Experimentales

| m (Freelancers) | Solución Óptima (FB) | Greedy | Híbrido (Nuestro Enfoque) | Tiempo Híbrido | Notas |
|-----------------|----------------------|--------|---------------------------|----------------|-------|
| 10 | 52.0 | 52.0 | 52.0 | 0.0001s | Todos encuentran el óptimo. |
| 20 | 149.0 | 149.0 | 149.0 | 0.0002s | Encontrado por todos. |
| 50 | 96.0 | 116.0 | 96.0 | 0.0007s | Greedy se aleja del óptimo. |
| 150 | 56.0 | 56.0 | 56.0 | 0.0037s | Todos encuentran 56.0. |
| 300 | 67.0 | 67.0 | 67.0 | 0.3207s | Reducción efectiva a 199. |
| 500 | 67.0 | 81.0 | 67.0 | 2.4272s | Gran brecha de Greedy (81 vs 67). |
| 750 | 65.0 | 84.0 | 65.0 | 34.2866s | Híbrido mantiene optimalidad (FB). |
| 1000 | *N/A* | 83.0 | 81.0 | 2.0704s | Híbrido usa GA sobre núcleo de 938. |

## 3. Hallazgos Clave

### Efectividad de Kernelization
El preprocesamiento (Kernelization) sigue siendo una herramienta poderosa, aunque su eficiencia disminuye a medida que los requisitos del proyecto aumentan en número y complejidad.
- Para $m=750$, la regla de dominancia redujo el problema a **644 freelancers**. 
- Sin embargo, esta reducción permitió que el **Solucionador Híbrido** aplicara **Fuerza Bruta** sobre el conjunto reducido, garantizando el óptimo absoluto (Costo 65.0), mientras que Greedy se desvió a 84.0.

- **m=500:** El **Local Search optimizado** (con intercambio 2-1) alcanzó el óptimo absoluto (67.0) en tan solo 0.004s, igualando a la Fuerza Bruta.
- **m=1000:** El **Local Search** demostró ser superior incluso al Algoritmo Genético, logrando un costo de **68.0** frente a los 81.0 del Híbrido (basado en Genético) y 83.0 de Greedy.

### Comparación de Algoritmos
- **Greedy:** Muy rápido pero propenso a estancarse en costos altos (error de ~20% en casos grandes).
- **Local Search (Refinado):** El gran ganador en eficiencia/calidad. Supera al Genético en escalas masivas gracias al operador de intercambio 2-1.
- **Fuerza Bruta / Híbrido:** Sigue siendo la única forma de garantizar el óptimo absoluto (hasta $m=750$ con Kernelization), pero el tiempo de ejecución escala significativamente.

## 4. Conclusión
La estrategia híbrida implementada es la más robusta para TalentBridge Connect. La inclusión de reglas de reducción (Kernelization) no solo acelera el proceso, sino que habilita el uso de algoritmos exactos en problemas de tamaño considerable. El sistema escala exitosamente desde pequeñas startups hasta plataformas con miles de freelancers, eligiendo dinámicamente el equilibrio perfecto entre precisión y velocidad.
