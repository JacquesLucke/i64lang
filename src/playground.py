from i64lang.parser import parse_str
from i64lang import ast
from i64lang.ast_to_graph import ast_to_graph

a = parse_str("def hello(qwe, das) {a=-5;}")
graph = ast_to_graph(a)
# graph.render()
