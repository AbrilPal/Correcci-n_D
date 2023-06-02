from graphviz import Digraph

class Estado:
    def __init__(self, id):
        self.id = id
        self.transiciones = {}

class Automata:
    def __init__(self):
        self.estados = []
        self.estado_inicial = None
        self.estado_final = None

    def imprimir_transiciones(self):
        for estado in self.estados:
            print(f"Estado {estado.id}:")
            for simbolo, estado_destino in estado.transiciones.items():
                print(f"    {simbolo} -> Estado {estado_destino.id}")

def nuevo_estado(automata):
    estado = Estado(len(automata.estados))
    automata.estados.append(estado)
    return estado

def automata_simbolo(automata, pila, simbolo):
    estado_inicial = nuevo_estado(automata)
    estado_final = nuevo_estado(automata)
    estado_inicial.transiciones[simbolo] = estado_final
    pila.append((estado_inicial, estado_final))

def automata_concatenacion(automata, pila):
    estado2_inicial, estado2_final = pila.pop()
    estado1_inicial, estado1_final = pila.pop()
    estado1_final.transiciones[''] = estado2_inicial
    pila.append((estado1_inicial, estado2_final))

def automata_alternativa(automata, pila):
    estado_inicial2, estado_final2 = pila.pop()
    estado_inicial1, estado_final1 = pila.pop()
    estado_nuevo_inicial = nuevo_estado(automata)
    estado_nuevo_final = nuevo_estado(automata)
    estado_nuevo_inicial.transiciones[''] = estado_inicial1
    estado_nuevo_inicial.transiciones[''] = estado_inicial2
    estado_final1.transiciones[''] = estado_nuevo_final
    estado_final2.transiciones[''] = estado_nuevo_final
    pila.append((estado_nuevo_inicial, estado_nuevo_final))

def automata_repeticion(automata, pila):
    estado_inicial, estado_final = pila.pop()
    estado_nuevo_inicial = nuevo_estado(automata)
    estado_nuevo_final = nuevo_estado(automata)
    estado_nuevo_inicial.transiciones[''] = estado_inicial
    estado_nuevo_inicial.transiciones[''] = estado_nuevo_final
    estado_final.transiciones[''] = estado_inicial
    estado_final.transiciones[''] = estado_nuevo_final
    pila.append((estado_nuevo_inicial, estado_nuevo_final))

def automata_repeticion_positiva(automata, pila):
    estado_inicial, estado_final = pila.pop()
    estado_nuevo_inicial = nuevo_estado(automata)
    estado_nuevo_final = nuevo_estado(automata)
    estado_nuevo_inicial.transiciones[''] = estado_inicial
    estado_final.transiciones[''] = estado_inicial
    estado_final.transiciones[''] = estado_nuevo_final
    pila.append((estado_nuevo_inicial, estado_nuevo_final))

def automata_opcional(automata, pila):
    estado_inicial, estado_final = pila.pop()
    estado_nuevo_inicial = nuevo_estado(automata)
    estado_nuevo_final = nuevo_estado(automata)
    estado_nuevo_inicial.transiciones[''] = estado_inicial
    estado_nuevo_inicial.transiciones[''] = estado_nuevo_final
    estado_final.transiciones[''] = estado_nuevo_final
    pila.append((estado_nuevo_inicial, estado_nuevo_final))




def construir_automata(expresion_regular):
    automata = Automata()
    pila = []

    for simbolo in expresion_regular:
        if simbolo == '|':
            automata_alternativa(automata, pila)
        elif simbolo == '.':
            automata_concatenacion(automata, pila)
        elif simbolo == '*':
            automata_repeticion(automata, pila)
        elif simbolo == '+':
            automata_repeticion_positiva(automata, pila)
        elif simbolo == '?':
            automata_opcional(automata, pila)
        else:
            automata_simbolo(automata, pila, simbolo)

    while len(pila) > 1:
        automata_concatenacion(automata, pila)

    automata.estado_inicial = pila[0][0]
    automata.estado_final = pila[0][1]

    return automata

def simular_automata(automata, cadena):
    estado_actual = automata.estado_inicial
    for simbolo in cadena:
        if simbolo not in estado_actual.transiciones:
            return False
        estado_actual = estado_actual.transiciones[simbolo]
    return estado_actual == automata.estado_final

def graficar_automata(automata):
    g = Digraph('G', filename='automata.gv')
    g.attr(rankdir='LR', size='8,5')
    g.attr('node', shape='doublecircle')
    g.node(str(automata.estado_final.id))
    g.attr('node', shape='circle')
    g.node(str(automata.estado_inicial.id))
    g.attr('node', shape='circle')
    for estado in automata.estados:
        for simbolo, estado_destino in estado.transiciones.items():
            g.edge(str(estado.id), str(estado_destino.id), label=simbolo)
    g.view()
