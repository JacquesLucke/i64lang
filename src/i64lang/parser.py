__all__ = [
    "parse",
    "parse_str",
]

from typing import List, Iterator, Callable, Any, Union, Optional

from . import ast
from . token_stream import TokenStream
from . tokens import Token

def parse_str(code: str) -> ast.Program:
    from . lexer import tokenize_str
    tokens = tokenize_str(code)
    return parse(tokens)

def parse(tokens: List[Token]) -> ast.Program:
    return parse__program(TokenStream(tokens))

def parse__program(tokens: TokenStream) -> ast.Program:
    functions = list(parse__functions(tokens))
    return ast.Program(functions)

def parse__functions(tokens: TokenStream) -> Iterator[ast.Function]:
    while tokens.next_is_name("def"):
        yield parse__function(tokens)

def parse__function(tokens: TokenStream) -> ast.Function:
    tokens.skip_name("def")
    name = tokens.consume_name()
    arg_names = parse__argument_names(tokens)
    stmt = parse__statement(tokens)
    return ast.Function(name, arg_names, stmt)

def parse__argument_names(tokens: TokenStream) -> List[str]:
    return list(parse__list(tokens, parse__argument_name, "(", ")", ","))

def parse__argument_name(tokens: TokenStream) -> str:
    return tokens.consume_name()

def parse__statement(tokens: TokenStream) -> ast.Statement:
    if tokens.next_is_symbol("{"):
        return parse__statement__block(tokens)
    elif tokens.next_is_name("return"):
        return parse__statement__return(tokens)
    elif tokens.next_is_name("while"):
        return parse__statement__while(tokens)
    elif tokens.next_is_name("if"):
        return parse__statement__if(tokens)
    elif tokens.next_is_any_name():
        return parse__statement__assignment(tokens)
    else:
        raise RuntimeError("unexpected token")

def parse__statement__block(tokens: TokenStream) -> ast.BlockStmt:
    statements = list(parse__list(tokens, parse__statement, "{", "}"))
    return ast.BlockStmt(statements)

def parse__statement__return(tokens: TokenStream) -> ast.ReturnStmt:
    tokens.skip_name("return")
    expr = parse__expression(tokens)
    return ast.ReturnStmt(expr)

def parse__statement__while(tokens: TokenStream) -> ast.WhileStmt:
    tokens.skip_name("while")
    tokens.skip_symbol("(")
    condition = parse__expression(tokens)
    tokens.skip_symbol(")")
    body_stmt = parse__statement(tokens)
    return ast.WhileStmt(condition, body_stmt)

def parse__statement__if(tokens: TokenStream) -> Union[ast.IfStmt, ast.IfElseStmt]:
    tokens.skip_name("if")
    tokens.skip_symbol("(")
    condition = parse__expression(tokens)
    tokens.skip_symbol(")")
    then_stmt = parse__statement(tokens)
    if tokens.next_is_name("else"):
        tokens.skip_name("else")
        else_stmt = parse__statement(tokens)
        return ast.IfElseStmt(condition, then_stmt, else_stmt)
    else:
        return ast.IfStmt(condition, then_stmt)

def parse__statement__assignment(tokens: TokenStream) -> ast.AssignmentStmt:
    name = tokens.consume_name()
    tokens.skip_symbol("=")
    expr = parse__expression(tokens)
    tokens.skip_symbol(";")
    return ast.AssignmentStmt(name, expr)

def parse__expression(tokens: TokenStream) -> ast.Expression:
    return parse__expression__comparison_level(tokens)

def parse__expression__comparison_level(tokens: TokenStream) -> ast.Expression:
    left_expr = parse__expression__add_sub_level(tokens)
    if tokens.next_is_any_symbol_of({"==", "<=", ">=", "!=", "<", ">"}):
        operator = tokens.consume_symbol()
        right_expr = parse__expression__add_sub_level(tokens)
        return ast.InfixExpr(operator, left_expr, right_expr)
    else:
        return left_expr

def parse__expression__add_sub_level(tokens: TokenStream) -> ast.Expression:
    left_expr = parse__expression__mul_div_level(tokens)
    while tokens.next_is_any_symbol_of({"+", "-"}):
        operator = tokens.consume_symbol()
        right_expr = parse__expression__mul_div_level(tokens)
        left_expr = ast.InfixExpr(operator, left_expr, right_expr)
    return left_expr

def parse__expression__mul_div_level(tokens: TokenStream) -> ast.Expression:
    left_expr = parse__expression__call_level(tokens)
    while tokens.next_is_any_symbol_of({"*", "/"}):
        operator = tokens.consume_symbol()
        right_expr = parse__expression__call_level(tokens)
        left_expr = ast.InfixExpr(operator, left_expr, right_expr)
    return left_expr

def parse__expression__call_level(tokens: TokenStream) -> ast.Expression:
    ptr_expr = parse__expression__atom_level(tokens)
    if tokens.next_is_symbol("("):
        args = parse__call_arguments(tokens)
        return ast.Call(ptr_expr, args)
    else:
        return ptr_expr

def parse__call_arguments(tokens: TokenStream) -> List[ast.Expression]:
    return list(parse__list(tokens, parse__expression__comparison_level, "(", ")", ","))

def parse__expression__atom_level(tokens: TokenStream) -> ast.Expression:
    if tokens.next_is_any_name():
        name = tokens.consume_name()
        return ast.Identifier(name)
    elif tokens.next_is_int():
        value = tokens.consume_int()
        return ast.Int(value)
    elif tokens.next_is_symbol("("):
        tokens.skip_symbol("(")
        expr = parse__expression(tokens)
        tokens.skip_symbol(")")
        return expr
    elif tokens.next_is_symbol("-"):
        tokens.skip_symbol("-")
        left_expr = ast.Int(0)
        right_expr = parse__expression__call_level(tokens)
        return ast.InfixExpr("-", left_expr, right_expr)

def parse__list(tokens: TokenStream,
               parse_element: Callable[[TokenStream], Any],
               start_symbol: str,
               end_symbol: str,
               separator_symbol: Optional[str] = None) -> Iterator[Any]:
    tokens.skip_symbol(start_symbol)

    while not tokens.next_is_symbol(end_symbol):
        yield parse_element(tokens)

        if separator_symbol is not None:
            if tokens.next_is_symbol(separator_symbol):
                tokens.skip_symbol(separator_symbol)
            else:
                break

    tokens.skip_symbol(end_symbol)
