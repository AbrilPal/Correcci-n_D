action_table = {0: {'term': ('SHIFT', 2), 'LPAREN': ('SHIFT', 4), 'expression': ('SHIFT', 1), 'factor': ('SHIFT', 3), 'ID': ('SHIFT', 5)}, 1: {'PLUS': ('SHIFT', 7), '$': ('ACCEPT', None)}, 2: {'RPAREN': ('REDUCE', 'expression'), 'PLUS': ('REDUCE', 'expression'), '$': ('REDUCE', 'expression'), 'TIMES': ('SHIFT', 10)}, 3: {'RPAREN': ('REDUCE', 'term'), '$': ('REDUCE', 'term'), 'TIMES': ('REDUCE', 'term'), 'PLUS': ('REDUCE', 'term')}, 4: {'expression': ('SHIFT', 6), 'term': ('SHIFT', 2), 'LPAREN': ('SHIFT', 4), 'factor': ('SHIFT', 3), 'ID': ('SHIFT', 5)}, 5: {'RPAREN': ('REDUCE', 'factor'), '$': ('REDUCE', 'factor'), 'TIMES': ('REDUCE', 'factor'), 'PLUS': ('REDUCE', 'factor')}, 6: {'PLUS': ('SHIFT', 7), 'RPAREN': ('SHIFT', 8)}, 7: {'term': ('SHIFT', 9), 'LPAREN': ('SHIFT', 4), 'factor': ('SHIFT', 3), 'ID': ('SHIFT', 5)}, 8: {'RPAREN': ('REDUCE', 'factor'), '$': ('REDUCE', 'factor'), 'TIMES': ('REDUCE', 'factor'), 'PLUS': ('REDUCE', 'factor')}, 9: {'RPAREN': ('REDUCE', 'expression'), 'PLUS': ('REDUCE', 'expression'), '$': ('REDUCE', 'expression'), 'TIMES': ('SHIFT', 10)}, 10: {'factor': ('SHIFT', 11), 'ID': ('SHIFT', 5), 'LPAREN': ('SHIFT', 4)}, 11: {'RPAREN': ('REDUCE', 'term'), '$': ('REDUCE', 'term'), 'TIMES': ('REDUCE', 'term'), 'PLUS': ('REDUCE', 'term')}}
goto_table = {0: {'expression': 1, 'term': 2, 'factor': 3}, 1: {}, 2: {}, 3: {}, 4: {'expression': 6, 'term': 2, 'factor': 3}, 5: {}, 6: {}, 7: {'term': 9, 'factor': 3}, 8: {}, 9: {}, 10: {'factor': 11}, 11: {}}

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

    