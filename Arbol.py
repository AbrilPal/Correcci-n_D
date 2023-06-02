"""
    Andrea Abril Palencia Gutierrez, 18198
    Diseño de Lenguajes de Programacion
    23 de febrero del 2023

    Arbol: crea el arbol sintactico a partir de la expresion POSTFIX
    para luego este ser utilizado para la creacion del AFN.
"""

from Lab_A.Nodo import *
import graphviz

def construir_arbol(postfix):
    stack = []
    for c in postfix:
        if c == '*' or c == '+' or c == '?':
            child = stack.pop()
            node = Node(c, child)
            stack.append(node)
        elif c == '.' or c == '|':
            right_child = stack.pop()
            left_child = stack.pop()
            node = Node(c, left_child, right_child)
            stack.append(node)
        else:
            node = Node(c)
            stack.append(node)
    return stack[0]

def imprimir_arbol(nodo, nombre_archivo):
    dot = graphviz.Digraph(comment='Árbol sintáctico')
    _agregar_nodo(dot, nodo)
    dot.render(nombre_archivo, view=True)

def _agregar_nodo(dot, nodo):
    if nodo is None:
        return
    _agregar_nodo(dot, nodo.left)
    _agregar_nodo(dot, nodo.right)
    dot.node(str(nodo), str(nodo.value))
    if nodo.left is not None:
        dot.edge(str(nodo), str(nodo.left))
    if nodo.right is not None:
        dot.edge(str(nodo), str(nodo.right))



