from . import ast
from . token_stream import TokenStream

from . tokens import (
    Token,
)

from typing import List, Iterator, Callable, Any, Union

def parse_str(code: str) -> ast.Program:
    from . lexer import tokenize_str
    tokens = tokenize_str(code)
    return parse(tokens)

def parse(tokens: List[Token]) -> ast.Program:
    return parse_program(TokenStream(tokens))

def parse_program(tokens: TokenStream) -> ast.Program:
    functions = list(parse_functions(tokens))
    return ast.Program(functions)

def parse_functions(tokens: TokenStream) -> Iterator[ast.Function]:
    while tokens.next_is_name("def"):
        yield parse_function(tokens)

def parse_function(tokens: TokenStream) -> ast.Function:
    tokens.consume_expected_name("def")
    name = tokens.consume_name_or_raise()
    arg_names = parse_argument_names(tokens)
    stmt = parse_statement(tokens)
    return ast.Function(name, arg_names, stmt)

def parse_argument_names(tokens: TokenStream) -> List[str]:
    return parse_list(tokens, parse_argument_name, "(", ")", ",")

def parse_argument_name(tokens: TokenStream) -> str:
    return tokens.consume_name_or_raise()

def parse_statement(tokens: TokenStream) -> ast.Statement:
    if tokens.next_is_symbol("{"):
        return parse_statement__block(tokens)
    elif tokens.next_is_name("return"):
        return parse_statement__return(tokens)
    elif tokens.next_is_name("while"):
        return parse_statement__while(tokens)
    elif tokens.next_is_name("if"):
        return parse_statement__if(tokens)
    elif tokens.next_is_any_name():
        return parse_statement__assignment(tokens)
    else:
        raise RuntimeError("unexpected token")

def parse_statement__block(tokens: TokenStream) -> ast.BlockStmt:
    statements = parse_list(tokens, parse_statement, "{", "}")
    return ast.BlockStmt(statements)

def parse_statement__return(tokens: TokenStream) -> ast.ReturnStmt:
    tokens.consume_expected_name("return")
    expr = parse_expression(tokens)
    return ast.ReturnStmt(expr)

def parse_statement__while(tokens: TokenStream) -> ast.WhileStmt:
    tokens.consume_expected_name("while")
    tokens.consume_expected_symbol_or_raise("(")
    condition = parse_expression(tokens)
    tokens.consume_expected_symbol_or_raise(")")
    body_stmt = parse_statement(tokens)
    return ast.WhileStmt(condition, body_stmt)

def parse_statement__if(tokens: TokenStream) -> Union[ast.IfStmt, ast.IfElseStmt]:
    tokens.consume_expected_name("if")
    tokens.consume_expected_symbol_or_raise("(")
    condition = parse_expression(tokens)
    tokens.consume_expected_symbol_or_raise(")")
    then_stmt = parse_statement(tokens)
    if tokens.next_is_name("else"):
        tokens.consume_expected_name("else")
        else_stmt = parse_statement(tokens)
        return ast.IfElseStmt(condition, then_stmt, else_stmt)
    else:
        return ast.IfStmt(condition, then_stmt)

def parse_statement__assignment(tokens: TokenStream) -> ast.AssignmentStmt:
    name = tokens.consume_name_or_raise()
    tokens.consume_expected_symbol_or_raise("=")
    expr = parse_expression(tokens)
    tokens.consume_expected_symbol_or_raise(";")
    return ast.AssignmentStmt(name, expr)

def parse_list(tokens: TokenStream,
               parse_element: Callable[[TokenStream], Any],
               start_symbol: str,
               end_symbol: str,
               separator_symbol: Optional[str] = None) -> Iterator[Any]:
    tokens.consume_expected_symbol_or_raise(start_symbol)

    while not tokens.next_is_symbol(end_symbol):
        yield parse_element(tokens)

        if separator_symbol is not None:
            if tokens.next_is_symbol(separator_symbol):
                tokens.consume_expected_symbol(separator_symbol)
            else:
                break

    tokens.consume_expected_symbol_or_raise(end_symbol)
