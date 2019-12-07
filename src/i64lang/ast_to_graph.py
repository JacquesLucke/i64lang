from graphviz import Digraph
from . import ast

def ast_to_graph(element):
    graph = Digraph()
    build_subtree(graph, element)
    return graph

def node_id(element):
    return str(id(element))

def build_subtree(graph, element):
    def make_edge_to_subtree(to_element, label=""):
        build_subtree(graph, to_element)
        graph.edge(node_id(element), node_id(to_element), label)

    def current_label(label):
        graph.node(node_id(element), label)

    if isinstance(element, ast.Program):
        current_label("Program")
        for function in element.functions:
            make_edge_to_subtree(function)
    elif isinstance(element, ast.Function):
        current_label(f"{element.name}({', '.join(element.arg_names)})")
        make_edge_to_subtree(element.stmt)
    elif isinstance(element, ast.BlockStmt):
        current_label("Block")
        for stmt in element.statements:
            make_edge_to_subtree(stmt)
    elif isinstance(element, ast.ReturnStmt):
        current_label("return")
        make_edge_to_subtree(element.expr)
    elif isinstance(element, ast.IfStmt):
        current_label("if then")
        make_edge_to_subtree(element.condition, "if")
        make_edge_to_subtree(element.then_stmt, "then")
    elif isinstance(element, ast.IfElseStmt):
        current_label("if then else")
        make_edge_to_subtree(element.condition, "if")
        make_edge_to_subtree(element.then_stmt, "then")
        make_edge_to_subtree(element.else_stmt, "else")
    elif isinstance(element, ast.AssignmentStmt):
        current_label(f"{element.name} =")
        make_edge_to_subtree(element.expr)
    elif isinstance(element, ast.InfixExpr):
        current_label(element.operator)
        make_edge_to_subtree(element.left_expr, "left")
        make_edge_to_subtree(element.right_expr, "right")
    elif isinstance(element, ast.Identifier):
        current_label(element.name)
    elif isinstance(element, ast.Int):
        current_label(str(element.value))
    else:
        assert False
