from tabulate import tabulate
import graphviz

class LR_SLR_generate:
    def __init__(self, archivo_entrada):
        self.producciones = {}          # Diccionario para almacenar las producciones
        self.tokens = []                # Lista de tokens
        self.produs_u = {}              # Diccionario para almacenar las producciones u
        self.no_terminales = []         # Lista de símbolos no terminales
        self.terminales = []            # Lista de símbolos terminales

        try:
            with open(archivo_entrada, 'r') as f:
                produccion_actual = ''
                for linea in f:
                    linea = linea.strip()

                    if linea.startswith('/*') and linea.endswith('*/'):
                        continue

                    if linea.startswith('%token'):
                        self.tokens.extend(linea.split()[1:])

                    if linea.endswith(':'):
                        produccion_actual = linea[:-1]
                        self.producciones[produccion_actual] = []
                    elif produccion_actual != '':
                        self.producciones[produccion_actual].append(linea)
                    if linea.endswith(';'):
                        produccion_actual = ''

                self.produs_u = {key: ' '.join(value[:-1]) for key, value in self.producciones.items()}

            self.construir_terminales()

        except FileNotFoundError:
            print("Error: El archivo especificado no existe.")
            return

    def construir_terminales(self):
        # Construir la lista de símbolos terminales y no terminales
        for produccion in self.produs_u.values():
            palabras = produccion.split()
            for palabra in palabras:
                if palabra.islower() and palabra not in self.no_terminales:
                    self.no_terminales.append(palabra)
                elif palabra not in self.terminales and palabra != "|":
                    self.terminales.append(palabra)

    def mostrar_automata(self, estados, transiciones):
        # Crear un grafo dirigido de Graphviz
        G = graphviz.Digraph()

        # Agregar estados como nodos al grafo
        for i in range(len(estados)):
            G.node(str(i), label=f'E{i}')

        # Agregar transiciones como bordes al grafo
        for (source_state, symbol), target_state in transiciones.items():
            G.edge(str(source_state), str(target_state), label=symbol)

        # Mostrar el grafo
        return G.view()

    def obtener_tokens(self):
        return self.tokens

    def obtener_producciones(self):
        return self.produs_u

    def obtener_first(self, simbolo, conjuntos_first=None, visitados=None):
        if conjuntos_first is None:
            conjuntos_first = {nt: set() for nt in self.no_terminales}
        if visitados is None:
            visitados = set()

        if simbolo in self.terminales:
            return {simbolo}

        if simbolo not in visitados:
            visitados.add(simbolo)
            for produccion in self.produs_u[simbolo].split(' | '):
                primer_simbolo = produccion.split()[0]
                if primer_simbolo in self.no_terminales:
                    conjuntos_first[simbolo] |= self.obtener_first(primer_simbolo, conjuntos_first, visitados)
                elif primer_simbolo in self.terminales:
                    conjuntos_first[simbolo].add(primer_simbolo)

        return conjuntos_first[simbolo]

    def obtener_follow(self, simbolo, conjuntos_follow=None, visitados=None):
        if conjuntos_follow is None:
            conjuntos_follow = {nt: set() for nt in self.no_terminales}
            conjuntos_follow[self.no_terminales[0]].add('$')
        if visitados is None:
            visitados = set()

        for prod_clave, prod_valor in self.produs_u.items():
            for produccion in prod_valor.split(' | '):
                simbolos = produccion.split()
                if simbolo in simbolos:
                    indice = simbolos.index(simbolo)
                    if indice + 1 < len(simbolos):
                        siguiente_simbolo = simbolos[indice + 1]
                        if siguiente_simbolo in self.no_terminales:
                            conjuntos_follow[simbolo] |= self.obtener_first(siguiente_simbolo)
                        elif siguiente_simbolo in self.terminales:
                            conjuntos_follow[simbolo].add(siguiente_simbolo)

                    if indice + 1 == len(simbolos) or simbolos[indice + 1] in self.no_terminales:
                        if prod_clave != simbolo:
                            conjuntos_follow[simbolo] |= self._follow_helper(prod_clave, conjuntos_follow, visitados)

        return conjuntos_follow[simbolo]

    def _follow_helper(self, simbolo, conjuntos_follow, visitados=None):
        if visitados is None:
            visitados = set()

        if simbolo not in visitados:
            visitados.add(simbolo)
            conjuntos_follow[simbolo] = self.obtener_follow(simbolo, conjuntos_follow, visitados)

        return conjuntos_follow[simbolo]

    def closure(self, produccion):
        conjunto_closure = set()
        simbolos = produccion.split()

        for i, simbolo in enumerate(simbolos):
            if simbolo in self.no_terminales:
                nuevo_item = f"{simbolo} → • {self.produs_u[simbolo]}"
                if nuevo_item not in conjunto_closure:
                    conjunto_closure.add(nuevo_item)

        return conjunto_closure


    def obtener_simbolo_despues_punto(self, item):
        partes = item.split()
        indice = partes.index("•")
        return partes[indice + 1] if indice + 1 < len(partes) else None

    def mover_punto(self, item):
        partes = item.split()
        indice = partes.index("•")
        if indice + 1 < len(partes):
            partes[indice], partes[indice + 1] = partes[indice + 1], partes[indice]
        return " ".join(partes)

    def obtener_lr0_items(self):
        def closure(conjunto_items):
            nuevos_items = set(conjunto_items)
            while True:
                items_agregados = set()
                for item in nuevos_items:
                    simbolo_despues_punto = self.obtener_simbolo_despues_punto(item)
                    if simbolo_despues_punto in self.no_terminales:
                        for prod in self.produs_u[simbolo_despues_punto].split(' | '):
                            nuevo_item = f"{simbolo_despues_punto} → • {prod}"
                            if nuevo_item not in nuevos_items:
                                items_agregados.add(nuevo_item)
                nuevos_items |= items_agregados
                if not items_agregados:
                    break
            return nuevos_items
        

        def goto(conjunto_items, simbolo):
            conjunto_nuevos_items = set()
            for item in conjunto_items:
                simbolo_despues_punto = self.obtener_simbolo_despues_punto(item)
                if simbolo_despues_punto == simbolo:
                    nuevo_item = self.mover_punto(item)
                    conjunto_nuevos_items.add(nuevo_item)
            return closure(conjunto_nuevos_items)

        def obtener_todos_simbolos():
            return self.no_terminales + self.terminales

        def crear_estados():
            estados = []
            estado_inicial = closure({f"S' → • {self.no_terminales[0]}"})
            estados.append(estado_inicial)
            pila = [estado_inicial]
            while pila:
                estado_actual = pila.pop()
                for simbolo in obtener_todos_simbolos():
                    siguiente_estado = goto(estado_actual, simbolo)
                    if siguiente_estado and siguiente_estado not in estados:
                        estados.append(siguiente_estado)
                        pila.append(siguiente_estado)
            return estados

        def crear_transiciones(estados):
            transiciones = {}
            for i, estado in enumerate(estados):
                for simbolo in obtener_todos_simbolos():
                    siguiente_estado = goto(estado, simbolo)
                    if siguiente_estado:
                        transiciones[(i, simbolo)] = estados.index(siguiente_estado)
            return transiciones

        # Crear los conjuntos LR(0) items, estados y transiciones
        conjunto_inicial = {f"S' → • {self.no_terminales[0]}"}
        conjuntos_lr0_items = closure(conjunto_inicial)
        estados = crear_estados()
        transiciones = crear_transiciones(estados)

        return estados, transiciones
    
    def print_lr0_automaton(self, states, transitions):
        print("Autómata:")
        print()
        print("Transiciones:")
        for (source_state, symbol), target_state in transitions.items():
            print(f"Estado {source_state} --{symbol}--> Estado {target_state}")
    
    def create_action_table(self, states, transitions):
        action_table = {}
        for i, state in enumerate(states):
            action_table[i] = {}
            for item in state:
                if self.obtener_simbolo_despues_punto(item) is None:  # Si el punto está al final del item
                    if item.startswith("S'"):  # Si el item es de la producción inicial
                        action_table[i]['$'] = ('ACCEPT', None)
                    else:  # Si es otra producción
                        prod = item.split(' → ')[0]
                        for symbol in self.obtener_follow(prod):
                            action_table[i][symbol] = ('REDUCE', prod)
                else:  # Si el punto no está al final del item
                    symbol_after_dot = self.obtener_simbolo_despues_punto(item)
                    if symbol_after_dot in self.terminales:
                        next_state = transitions.get((i, symbol_after_dot), None)
                        if next_state is not None:
                            action_table[i][symbol_after_dot] = ('SHIFT', next_state)
        return action_table


    def create_goto_table(self, states, transitions):
        goto_table = {}
        for i, state in enumerate(states):
            goto_table[i] = {}
            for symbol in self.no_terminales:
                next_state = transitions.get((i, symbol), None)
                if next_state is not None:
                    goto_table[i][symbol] = next_state
        return goto_table

    def print_action_table(self, action_table):
        table_data = []
        headers = ['State'] + sorted(self.terminales + ['$'])
        for state, actions in sorted(action_table.items()):
            row = [state]
            for symbol in headers[1:]:
                action = actions.get(symbol, '')
                if action:
                    row.append(f"{action[0]} {action[1]}")
                else:
                    row.append('')
            table_data.append(row)
        print(tabulate(table_data, headers, tablefmt="fancy_grid"))

    def print_goto_table(self, goto_table):
        table_data = []
        headers = ['State'] + sorted(self.no_terminales)
        for state, gotos in sorted(goto_table.items()):
            row = [state]
            for symbol in headers[1:]:
                goto = gotos.get(symbol, '')
                if goto != '':
                    row.append(f"Estado {goto}")
                else:
                    row.append('')
            table_data.append(row)
        print(tabulate(table_data, headers, tablefmt="fancy_grid"))

ruta_archivo = input('Ingrese la ruta del archivo de entrada: ')
yapar = LR_SLR_generate(ruta_archivo)
estados, transiciones = yapar.obtener_lr0_items()
yapar.mostrar_automata(estados, transiciones)
action_table = yapar.create_action_table(estados, transiciones)
goto_table = yapar.create_goto_table(estados, transiciones)

# yapar.print_lr0_automaton(estados, transiciones)

# print("\nFIRST:")
# first_table = []
# for nt in yapar.no_terminales:
#     first_set = yapar.obtener_first(nt)
#     first_table.append([nt, ', '.join(first_set)])
# print(tabulate(first_table, headers=["No Terminal", "FIRST"], tablefmt="fancy_grid"))

# print("\nFOLLOW:")
# follow_table = []
# for nt in yapar.no_terminales:
#     follow_set = yapar.obtener_follow(nt)
#     follow_table.append([nt, ', '.join(follow_set)])
# print(tabulate(follow_table, headers=["No Terminal", "FOLLOW"], tablefmt="fancy_grid"))

print("\nACTION TABLE:")
yapar.print_action_table(action_table)
print("\nGOTO TABLE:")
yapar.print_goto_table(goto_table)

def generate_scanner_file(action_table, goto_table):
    codigo = '''
import re

def parse_slr1_string(input_string, action_table, goto_table):
    stack = [0]
    input_tokens = re.findall(r'\w+|\S', input_string)
    input_tokens.append('$')
    output = []

    while True:
        state = stack[-1]
        current_token = input_tokens[0]

        action = action_table[state].get(current_token, None)

        if action is None:
            raise ValueError(f"Error de análisis sintáctico en la entrada '{input_string}'. No se encontró una acción válida para el token '{current_token}' en el estado {state}.")

        action_type, action_value = action

        if action_type == 'SHIFT':
            stack.append(action_value)
            input_tokens = input_tokens[1:]
        elif action_type == 'REDUCE':
            production = action_value
            prod_left, prod_right = production.split(' → ')

            for _ in prod_right.split():
                stack.pop()

            goto_state = goto_table[stack[-1]].get(prod_left, None)

            if goto_state is None:
                raise ValueError(f"Error de análisis sintáctico en la entrada '{input_string}'. No se encontró una acción válida para el símbolo no terminal '{prod_left}' en el estado {stack[-1]}.")

            stack.append(goto_state)
            output.append(production)
        elif action_type == 'ACCEPT':
            output.append("S' → " + ' '.join(input_tokens))
            break

    return output

# Lee el archivo de entrada
nombre_archivo = input("Ingrese el nombre del archivo de entrada: ")

try:
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
except FileNotFoundError:
    print(f"No se encontró el archivo '{nombre_archivo}'. Verifica el nombre y la ubicación del archivo.")
    exit()

for indice, linea in enumerate(lineas):
    try:
        print()
        resultado = parse_slr1_string(linea.strip(), action_table, goto_table)
        print()
        print("Resultado del análisis sintáctico para la línea ", {indice + 1})
        print()
        print("".join(resultado))
        print()
        print("La cadena en la línea ", {indice + 1} ," es válida según la gramática.")
    except ValueError as e:
        print()
        print("La cadena en la línea ",{indice + 1}, " no es válida según la gramática.")
        print("Error en la línea ",{indice + 1}, ":", str(e))

    '''
    with open('scanner_SLR.py', 'w') as file:
        file.write("action_table = " + str(action_table) + "\n")
        file.write("goto_table = " + str(goto_table) + "\n")
        file.write(codigo)

generate_scanner_file(action_table, goto_table)

