from models.models import Freelancer, Proyecto

class Kernelizador:
    def __init__(self, freelancers, proyecto):
        self.freelancers = freelancers
        self.proyecto = proyecto
        self.esenciales = []
        self.removidos = [] # Lista de (freelancer, razon)

    def ejecutar(self):
        """
        Ejecuta las reglas de reducción y devuelve:
        - freelancers_reducidos: Lista de freelancers a considerar
        - esenciales: Lista de freelancers que DEBEN estar en la solución
        """
        # 1. Eliminar dominados
        # Hacemos copia para no modificar la lista mientras iteramos
        candidatos = self.freelancers.copy()
        
        # Iterar hasta que no haya más cambios (opcional, pero buena práctica si hubiera cadenas)
        # Para dominación simple, un pase n^2 suele ser suficiente si ordenamos, 
        # pero haremos un n^2 directo para simplificar.
        
        dominados = set()
        for i, f1 in enumerate(candidatos):
            if f1 in dominados: continue
            
            for j, f2 in enumerate(candidatos):
                if i == j: continue
                if f2 in dominados: continue
                
                if self._f1_domina_a_f2(f1, f2):
                    dominados.add(f2)
                    self.removidos.append((f2, f"Dominado por F{f1.id}"))
        
        candidatos = [f for f in candidatos if f not in dominados]
        
        # 2. Identificar esenciales
        # Un freelancer es esencial si es el ÚNICO en 'candidatos' 
        # que puede cubrir un requisito específico.
        esenciales_set = set()
        
        for hab, nivel_req in self.proyecto.requisitos.items():
            capaces = []
            for f in candidatos:
                if f.tiene_habilidad(hab, nivel_req):
                    capaces.append(f)
            
            if len(capaces) == 1:
                f_esencial = capaces[0]
                if f_esencial not in esenciales_set:
                    esenciales_set.add(f_esencial)
                    self.esenciales.append(f_esencial)
        
        # Nota: Los esenciales siguen estando en "candidatos" porque 
        # el algoritmo principal debe saber que están disponibles (o podemos devolverlos aparte).
        # La estrategia híbrida debería tomarlos, fijarlos en la solución, 
        # y luego buscar cubrir el resto de requisitos con el resto de candidatos.
        # Pero para ser limpios, devolveremos la lista filtrada Y la lista de esenciales.
        
        # Si un freelancer es esencial, técnicamente ya "está" en la solución.
        # ¿Deberíamos quitarlo de 'candidatos' para resolver el subproblema restante?
        # Depende de cómo lo maneje el solver. 
        # Generalmente, kernelization devuelve el problema reducido.
        # Pero dejaremos que el solver decida. Devolveremos todo limpio.
        
        return candidatos, self.esenciales

    def _f1_domina_a_f2(self, f1, f2):
        """
        Devuelve True si f1 domina a f2.
        Condiciones:
        1. Costo(f1) <= Costo(f2)
        2. Para toda habilidad requerida h:
           Si f2 la cubre (nivel >= req), entonces f1 TAMBIÉN la debe cubrir.
        
        Nota: f1 es "mejor" o igual que f2.
        """
        # Condición 1: Costo
        if f1.costo > f2.costo:
            return False
            
        # Condición 2: Cobertura de requisitos
        for hab, nivel_req in self.proyecto.requisitos.items():
            # Si f2 cubre el requisito...
            if f2.tiene_habilidad(hab, nivel_req):
                # ...f1 debe cubrirlo también
                if not f1.tiene_habilidad(hab, nivel_req):
                    return False
        
        # Si llegamos aquí, f1 es al menos tan bueno como f2
        # Para evitar eliminar iguales entre sí (A domina B y B domina A),
        # imponemos una regla de desempate por ID para dominación estricta
        if f1.costo == f2.costo and self._mismas_habilidades_relevantes(f1, f2):
             return f1.id < f2.id # Solo el de menor ID sobrevive si son idénticos
             
        return True

    def _mismas_habilidades_relevantes(self, f1, f2):
        """Auxiliar para verificar si cubren exactamente lo mismo en cuanto a requisitos"""
        for hab, nivel_req in self.proyecto.requisitos.items():
            cubierta1 = f1.tiene_habilidad(hab, nivel_req)
            cubierta2 = f2.tiene_habilidad(hab, nivel_req)
            if cubierta1 != cubierta2:
                return False
        return True
