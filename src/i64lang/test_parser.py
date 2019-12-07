import pytest
from . import ast
from . lexer import tokenize_str
from . token_stream import TokenStream

from . parser import (
    parse_str,
    parse__function,
    parse__argument_names,
    parse__statement,
    parse__statement__block,
    parse__statement__return,
    parse__statement__while,
    parse__statement__if,
    parse__statement__assignment,
    parse__expression__comparison_level,
    parse__expression__add_sub_level,
    parse__expression__mul_div_level,
    parse__expression__call_level,
    parse__expression__atom_level,
)

def stream(code):
    tokens = tokenize_str(code)
    return TokenStream(tokens)

class Test_parse_str:
    def test__empty(self):
        program = parse_str("")
        assert program.functions == []

    def test__single_function(self):
        program = parse_str("def hello() {}")
        assert len(program.functions) == 1
        assert program.functions[0].name == "hello"

    def test__multiple_functions(self):
        program = parse_str("def h1(){} def h2(a, b) {} def hello() {}")
        assert len(program.functions) == 3
        assert program.functions[0].name == "h1"
        assert program.functions[1].name == "h2"
        assert program.functions[2].name == "hello"
        assert program.functions[1].arg_names == ["a", "b"]

    def test__missing_name(self):
        with pytest.raises(Exception):
            parse_str("def () {}")

    def test__missing_arguments(self):
        with pytest.raises(Exception):
            parse_str("def hello {}")

class Test_parse__function:
    def test__zero_arguments(self):
        function = parse__function(stream("def hello() {}"))
        assert isinstance(function, ast.Function)
        assert function.name == "hello"
        assert function.arg_names == []

    def test__multiple_arguments(self):
        function = parse__function(stream("def hello(a, bc, d) {}"))
        assert isinstance(function, ast.Function)
        assert function.name == "hello"
        assert function.arg_names == ["a", "bc", "d"]

class Test_parse__argument_names:
    def test__zero_arguments(self):
        arg_names = parse__argument_names(stream("()"))
        assert arg_names == []

    def test__one_argument(self):
        arg_names = parse__argument_names(stream("(abc)"))
        assert arg_names == ["abc"]

    def test__multiple_arguments(self):
        arg_names = parse__argument_names(stream("(abc, d, ef)"))
        assert arg_names == ["abc", "d", "ef"]

class Test_parse__statement:
    def test__block(self):
        stmt = parse__statement(stream("{a=b; c=d;}"))
        assert isinstance(stmt, ast.BlockStmt)
        assert stmt.statements[1].name == "c"

    def test__return(self):
        stmt = parse__statement(stream("return a;"))
        assert isinstance(stmt, ast.ReturnStmt)
        assert stmt.expr.name == "a"

    def test__while(self):
        stmt = parse__statement(stream("while (a < b) {a = 5;}"))
        assert isinstance(stmt, ast.WhileStmt)
        assert stmt.body_stmt.statements[0].expr.value == 5

    def test__if(self):
        stmt = parse__statement(stream("if (a < b) a = 5;"))
        assert isinstance(stmt, ast.IfStmt)

    def test__assignment(self):
        stmt = parse__statement(stream("a = b;"))
        assert isinstance(stmt, ast.AssignmentStmt)

    def test__invalid_statement(self):
        with pytest.raises(Exception):
            parse__statement(stream("a+b"))

class Test_parse__statement__block:
    def test__empty_block(self):
        stmt = parse__statement__block(stream("{}"))
        assert isinstance(stmt, ast.BlockStmt)
        assert stmt.statements == []

    def test__single_statement(self):
        stmt = parse__statement__block(stream("{a=b;}"))
        assert isinstance(stmt, ast.BlockStmt)
        assert len(stmt.statements) == 1
        assert isinstance(stmt.statements[0], ast.AssignmentStmt)

    def test__multiple_statements(self):
        stmt = parse__statement__block(stream("{a=b;c=5;}"))
        assert isinstance(stmt, ast.BlockStmt)
        assert len(stmt.statements) == 2
        assert stmt.statements[0].name == "a"
        assert stmt.statements[0].expr.name == "b"
        assert stmt.statements[1].name == "c"
        assert stmt.statements[1].expr.value == 5

    def test__missing_semicolon(self):
        with pytest.raises(Exception):
            parse__statement__block(stream("{a=b;c=5}"))

class Test_parse__statement__return:
    def test_simple(self):
        stmt = parse__statement__return(stream("return a;"))
        assert isinstance(stmt, ast.ReturnStmt)
        assert stmt.expr.name == "a"

class Test_parse__statement__while:
    def test__simple(self):
        stmt = parse__statement__while(stream("while (a < b) a = 6;"))
        assert isinstance(stmt, ast.WhileStmt)

class Test_parse__statement__if:
    def test__if_then(self):
        stmt = parse__statement__if(stream("if (a < b) a = 6;"))
        assert isinstance(stmt, ast.IfStmt)
        assert stmt.condition.operator == "<"
        assert isinstance(stmt.then_stmt, ast.AssignmentStmt)

    def test__if_then_else(self):
        stmt = parse__statement__if(stream("if (a < b) a = 6; else b = 6;"))
        assert isinstance(stmt, ast.IfElseStmt)
        assert stmt.condition.operator == "<"
        assert stmt.then_stmt.name == "a"
        assert stmt.else_stmt.name == "b"

    def test__missing_body(self):
        with pytest.raises(Exception):
            parse__statement__if(stream("if (a < b)"))

class Test_parse__statement__assignment:
    def test__simple(self):
        stmt = parse__statement__assignment(stream("a = b;"))
        assert isinstance(stmt, ast.AssignmentStmt)
        assert stmt.name == "a"
        assert stmt.expr.name == "b"

    def test__missing_semicolon(self):
        with pytest.raises(Exception):
            parse__statement__assignment(stream("a = b"))

class Test_parse__expression__comparison_level:
    def test__no_comparison(self):
        expr = parse__expression__comparison_level(stream("a"))
        assert isinstance(expr, ast.Identifier)

    def test__simple_subexpressions(self):
        expr = parse__expression__comparison_level(stream("a < b"))
        assert isinstance(expr, ast.InfixExpr)
        assert expr.operator == "<"

    def test__complex_subexpressions(self):
        expr = parse__expression__comparison_level(stream("a + b - (a < b) >= a * b"))
        assert isinstance(expr, ast.InfixExpr)
        assert expr.operator == ">="

class Test_parse__expression__add_sub_level:
    def test__no_operation(self):
        expr = parse__expression__add_sub_level(stream("a"))
        assert isinstance(expr, ast.Identifier)

    def test__single_multiplication(self):
        expr = parse__expression__add_sub_level(stream("a+b"))
        assert isinstance(expr, ast.InfixExpr)
        assert expr.operator == "+"
        assert expr.left_expr.name == "a"
        assert expr.right_expr.name == "b"

    def test__multiple_operations(self):
        expr = parse__expression__add_sub_level(stream("a+b-c+d+e"))
        assert expr.operator == "+"
        assert expr.left_expr.operator == "+"
        assert expr.left_expr.left_expr.operator == "-"
        assert expr.left_expr.left_expr.left_expr.operator == "+"

    def test__invalid_syntax(self):
        with pytest.raises(Exception):
            parse__expression__add_sub_level(stream("a+"))

class Test_parse__expression__mul_div_level:
    def test__no_operation(self):
        expr = parse__expression__mul_div_level(stream("a"))
        assert isinstance(expr, ast.Identifier)

    def test__single_multiplication(self):
        expr = parse__expression__mul_div_level(stream("a*b"))
        assert isinstance(expr, ast.InfixExpr)
        assert expr.operator == "*"
        assert expr.left_expr.name == "a"
        assert expr.right_expr.name == "b"

    def test__multiple_operations(self):
        expr = parse__expression__mul_div_level(stream("a*b/c*d*e"))
        assert expr.operator == "*"
        assert expr.left_expr.operator == "*"
        assert expr.left_expr.left_expr.operator == "/"
        assert expr.left_expr.left_expr.left_expr.operator == "*"

class Test_parse__expression__call_level:
    def test__zero_arguments(self):
        expr = parse__expression__call_level(stream("f()"))
        assert isinstance(expr, ast.Call)
        assert expr.args == []

    def test__multiple_arguments(self):
        expr = parse__expression__call_level(stream("f(4, a+b, c)"))
        assert isinstance(expr, ast.Call)
        assert len(expr.args) == 3
        assert expr.args[0].value == 4
        assert expr.args[1].operator == "+"
        assert expr.args[2].name == "c"

    def test__expression_as_function(self):
        expr = parse__expression__call_level(stream("(a+b)(42)"))
        assert isinstance(expr, ast.Call)
        assert expr.ptr_expr.operator == "+"
        assert expr.args[0].value == 42

class Test_parse__expression__atom_level:
    def test__recognizes_identifier(self):
        expr = parse__expression__atom_level(stream("a+b"))
        assert isinstance(expr, ast.Identifier)
        assert expr.name == "a"

    def test__recognizes_int(self):
        expr = parse__expression__atom_level(stream("4+a"))
        assert isinstance(expr, ast.Int)
        assert expr.value == 4

    def test__recognizes_subexpression(self):
        expr = parse__expression__atom_level(stream("(a+b)"))
        assert isinstance(expr, ast.InfixExpr)
        assert expr.operator == "+"

    def test__recognizes_unary_int(self):
        expr = parse__expression__atom_level(stream("-ab"))
        assert isinstance(expr, ast.InfixExpr)
        assert expr.operator == "-"
