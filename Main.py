"""
    Andrea Abril Palencia Gutierrez, 18198
    Diseño de Lenguajes de Programacion
    23 de febrero del 2023

    Main: programa principal que manda a llamar las funciones
    de los otros archivos.
"""

from Lab_A.Arbol import *
from Lab_A.Infix_a_Postfix import *
from Lab_A.To_afn import *
from to_AFD import *
from to_AFD_direct import *
import sys

abiertos = 0
cerrados = 0

# EXPRESION REGULAR
expresion_regular = input("Ingrese la expresion regular: ")
for caracter in expresion_regular:
    if caracter == "(":
        abiertos += 1
    elif caracter == ")":
        cerrados += 1
if (abiertos > cerrados) or (abiertos < cerrados):
    print("\nERROR: Verifique los paréntesis, ya que hay", abiertos,  "paréntesis abiertos y", cerrados, "paréntesis cerrados.")
    sys.exit()
else:
    expresion_regular_nuevo = expresion_regular.replace(".", "$")
    # expresion_regular_nuevo = expresion_regular_nuevo.replace("?", "|ε")

    # POSTFIX
    expresion_postfix = Infix_Postfix(expresion_regular_nuevo)

    # ARBOL SINTACTICO
    tree = construir_arbol(expresion_postfix)
    imprimir_arbol(tree, "arbol_sintactico")

    # AFN
    afn = construir_AFN_desde_arbol(tree)
    print(afn)
    g = generar_grafo_AFN(afn)
    g.view()
    a = obtener_alfabeto(afn)

    # AFD apartir de AFN
    afd = construir_AFD_desde_AFN(afn, a)
    afd.print_transiciones()
    afd_grafica = graficar_AFD(afd)
    afd_grafica.render('afd', view=True)
    afd_mini = afd.minimizar(a)
    afd_mini.print_transiciones()

    # AFD directo
    print()
    print("----------- AFD DIRECTO --------------")
    print()
    print("transiciones:\n")
    automata = construir_automata(expresion_regular_nuevo)
    automata.imprimir_transiciones()
    graficar_automata(automata)

    # primera expresion

    # subconjuntos
    # print()
    # print("----------- SUBCONJUNTOS --------------")
    # print()
    # print(afd.procesar_cadena("bbabb"))
    # print(afd.procesar_cadena("babb"))
    # print(afd.procesar_cadena("aaaaaaaaaabbbbbbabababababababababababababbb"))
    # print(afd.procesar_cadena("abb"))

    # # directo
    # print()
    # print("----------- directo --------------")
    # print()
    # print(simular_automata(automata, 'bbabb')) 
    # print(simular_automata(automata, 'babb')) 
    # print(simular_automata(automata, 'aaaaaaaaaabbbbbbabababababababababababababbb')) 
    # print(simular_automata(automata, 'abb')) 

    # segunda expresion

    # subconjuntos
    # print()
    # print("----------- SUBCONJUNTOS --------------")
    # print()
    # print(afd.procesar_cadena(" "))
    # print(afd.procesar_cadena("a"))
    # print(afd.procesar_cadena("aba"))
    # print(afd.procesar_cadena("abba"))

    # # directo
    # print()
    # print("----------- directo --------------")
    # print()
    # print(simular_automata(automata, ' ')) 
    # print(simular_automata(automata, 'a')) 
    # print(simular_automata(automata, 'aba')) 
    # print(simular_automata(automata, 'abba')) 

    # tercera expresion

    # subconjuntos
    # print()
    # print("----------- SUBCONJUNTOS --------------")
    # print()
    # print(afd.procesar_cadena("$;-/$"))
    # print(afd.procesar_cadena("-/$$;"))
    # print(afd.procesar_cadena("-/$"))
    # print(afd.procesar_cadena(";;;;;;;$$$$$$;$;$;$;$;$;$;$/$;$;$;$;$;"))

    # # directo
    # print()
    # print("----------- directo --------------")
    # print()
    # print(simular_automata(automata, '("$;-/$"))')) 
    # print(simular_automata(automata, "-/$$;")) 
    # print(simular_automata(automata, "-/$")) 
    # print(simular_automata(automata, ";;;;;;;$$$$$$;$;$;$;$;$;$;$/$;$;$;$;$;"))

    # cuarta expresion

    # subconjuntos
    # print()
    # print("----------- SUBCONJUNTOS --------------")
    # print()
    # print(afd.procesar_cadena("x"))
    # print(afd.procesar_cadena("txm"))
    # print(afd.procesar_cadena("ma"))
    # print(afd.procesar_cadena("a"))

    # # directo
    # print()
    # print("----------- directo --------------")
    # print()
    # print(simular_automata(automata, 'x')) 
    # print(simular_automata(automata, 'txm')) 
    # print(simular_automata(automata, 'ma')) 
    # print(simular_automata(automata, 'a')) 

    # quinta expresion

    # subconjuntos
    print()
    print("----------- SUBCONJUNTOS --------------")
    print()
    print(afd.procesar_cadena("&;&;&"))
    print(afd.procesar_cadena("$;$;;$"))
    print(afd.procesar_cadena("$;$;"))
    print(afd.procesar_cadena(" "))
    print(afd.procesar_cadena("$;;$"))

    # directo
    print()
    print("----------- directo --------------")
    print()
    print(simular_automata(automata, "&;&;&")) 
    print(simular_automata(automata, "$;$;;$")) 
    print(simular_automata(automata, "$;$;"))
    print(simular_automata(automata, ' '))
    print(simular_automata(automata, '$;;$'))