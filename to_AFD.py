"""
    Andrea Abril Palencia Gutierrez, 18198
    Diseño de Lenguajes de Programacion
    18 de marzo del 2023

    AFD: este archivo crea el AFD a partir del AFN, esto lo hace con el
    algoritmo de construccion de subconjuntos. Ademas minimiza el AFD que 
    se genera.
"""

import graphviz

class EstadoAFD:
    contador_ids = 0

    def __init__(self, estados_afn):
        self.id = EstadoAFD.contador_ids
        EstadoAFD.contador_ids += 1
        self.estados_afn = estados_afn
        self.transiciones = {}

    def add_transition(self, simbolo, estado):
        self.transiciones[simbolo] = estado

    def __str__(self):
        return f"{self.id}"
    
class AFDM:
    def __init__(self, inicial, finales, transiciones):
        self.inicial = inicial
        self.finales = finales
        self.estados = set([inicial] + list(finales))
        self.transiciones = transiciones
    
    def procesar_cadena(self, cadena):
        estado_actual = self.inicial
        for simbolo in cadena:
            if simbolo not in estado_actual.transiciones:
                return False
            estado_actual = estado_actual.transiciones[simbolo]
        return estado_actual in self.finales
    
    def print_transiciones(self):
        print()
        print("----------- AFD MINIMIZADO --------------")
        print()
        print("transiciones:\n")
        for estado in self.estados:
            print(f"Estado {estado.id}:")
            for simbolo, transicion in estado.transiciones.items():
                print(f"  {simbolo} -> {transicion.id}")


class AFD:
    def __init__(self, inicial, finales):
        self.inicial = inicial
        self.finales = finales
        self.estados = set([inicial] + list(finales))
    
    def procesar_cadena(self, cadena):
        estado_actual = self.inicial
        for simbolo in cadena:
            if simbolo not in estado_actual.transiciones:
                return False
            estado_actual = estado_actual.transiciones[simbolo]
        return estado_actual in self.finales
    
    def print_transiciones(self):
        print()
        print("----------- AFD SUBCONJUNTOS --------------")
        print()
        print("transiciones:\n")
        for estado in self.estados:
            print(f"Estado {estado.id}:")
            for simbolo, transicion in estado.transiciones.items():
                print(f"  {simbolo} -> {transicion.id}")

    def minimizar(self, alfabeto):
        # Partition the states into two sets: final and non-final
        P = [self.finales, self.estados - self.finales]
        
        # Initialize the set of active partitions and the worklist
        W = [self.finales, self.estados - self.finales]
        active = set([0])
        
        # Initialize the equivalence classes for each state
        classes = {}
        for i, partition in enumerate(P):
            for estado in partition:
                classes[estado] = i
        
        # Repeat until the worklist is empty
        while active:
            A = active.pop()
            for simbolo in alfabeto:
                X = set()
                for estado in P[A]:
                    X.add(estado.transiciones[simbolo])
                for i, partition in enumerate(P):
                    Y = partition.intersection(X)
                    Z = partition - X
                    if Y and Z:
                        P.remove(partition)
                        P.append(Y)
                        P.append(Z)
                        if i in active:
                            active.remove(i)
                            active.add(len(P)-2)
                            active.add(len(P)-1)
                        else:
                            if len(Y) <= len(Z):
                                active.add(len(P)-2)
                            else:
                                active.add(len(P)-1)
                        for estado in Y:
                            classes[estado] = len(P)-2
                        for estado in Z:
                            classes[estado] = len(P)-1
        
        # Construct the new minimized DFA
        new_estados = set()
        new_inicial = None
        new_finales = set()
        new_transiciones = {}
        for i, partition in enumerate(P):
            new_estado = EstadoAFD(partition)
            new_estados.add(new_estado)
            if self.inicial in partition:
                new_inicial = new_estado
            if partition & self.finales:
                new_finales.add(new_estado)
            for estado in partition:
                for simbolo, transicion in estado.transiciones.items():
                    if transicion in partition:
                        new_transiciones[(new_estado, simbolo)] = new_estado if transicion == estado else next((e for e in new_estados if transicion in e.estados_afn), None)
        
        return AFDM(new_inicial, new_finales, new_transiciones)


def construir_AFD_desde_AFN(afn, alfabeto):
    inicial = EstadoAFD(afn.inicial.get_closure())
    estados_afd = {inicial}
    nodos = [inicial]

    while nodos:
        estado_afd = nodos.pop()

        for simbolo in alfabeto:
            estados_afn_transicion = set()

            for estado_afn in estado_afd.estados_afn:
                estados_afn_transicion |= estado_afn.get_transitions(simbolo)

            estados_afn_transicion_closure = set()
            for estado_afn_transicion in estados_afn_transicion:
                estados_afn_transicion_closure |= set(estado_afn_transicion.get_closure())

            nuevo_estado_afd = None
            for estado_afd_existente in estados_afd:
                if estado_afd_existente.estados_afn == estados_afn_transicion_closure:
                    nuevo_estado_afd = estado_afd_existente
                    break

            if nuevo_estado_afd is None:
                nuevo_estado_afd = EstadoAFD(estados_afn_transicion_closure)
                estados_afd.add(nuevo_estado_afd)
                nodos.append(nuevo_estado_afd)

            estado_afd.add_transition(simbolo, nuevo_estado_afd)

    finales_afd = set()
    for estado_afd in estados_afd:
        for estado_afn in estado_afd.estados_afn:
            if estado_afn == afn.final:
                finales_afd.add(estado_afd)

    return AFD(inicial, finales_afd)

def graficar_AFD(afd):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')
    dot.node(str(afd.inicial.id), shape='point', color='blue')
    for estado in afd.estados:
        dot.node(str(estado.id), shape='doublecircle' if estado in afd.finales else 'circle', 
                 peripheries='2' if estado in afd.finales else '1', 
                 style='bold' if estado in afd.finales else '', 
                 color='red' if estado in afd.finales else 'blue' if estado == afd.inicial else 'black')
        for simbolo, transicion in estado.transiciones.items():
            dot.edge(str(estado.id), str(transicion.id), label=simbolo)
    return dot

