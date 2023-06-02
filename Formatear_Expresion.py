"""
    Andrea Abril Palencia Gutierrez, 18198
    Diseño de Lenguajes de Programacion
    23 de febrero del 2023

    Formatear Expresion Regular: usa como parametro una cadena y devulve
    una cadena formateada para convertir de INFIX a POSTFIX.
"""

def Formatear(expresion_reg):
    expresion_form = []
    print("\nLa expresion regular ingresada es: ", expresion_reg, "\n")
    todosOperadores = ['|', '?', '+' , '*', '^']
    operadoresBinarios = ['|', '^']
    if len(expresion_reg) > 0:
        for i in range (len(expresion_reg)):
            c1 = expresion_reg[i]
            if (i + 1) < len(expresion_reg):
                c2 = expresion_reg[i + 1]
                expresion_form.append(c1)
                if (c1 != '(') and (c2 != ')') and (c2 not in todosOperadores) and (c1 not in operadoresBinarios):
                    expresion_form.append('.')
        expresion_form.append(expresion_reg[len(expresion_reg) - 1])
        expresion_form_final = ''.join(expresion_form)
        print("La expresion regular formateada es: ", expresion_form_final, "\n")
        return expresion_form_final
    else:
        print("La Expresion Regular ingresada esta vacia\n")
        return 
