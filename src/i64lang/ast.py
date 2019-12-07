from __future__ import annotations

from typing import List
from dataclasses import dataclass

@dataclass
class Program:
    functions: List[Function]

@dataclass
class Function:
    name: str
    arg_names: List[str]
    stmt: Statement

class Statement:
    pass

@dataclass
class BlockStmt(Statement):
    statements: List[Statement]

@dataclass
class ReturnStmt(Statement):
    expr: Expression

@dataclass
class WhileStmt(Statement):
    condition: Expression
    body_stmt: Statement

@dataclass
class IfStmt(Statement):
    condition: Expression
    then_stmt: Statement

@dataclass
class IfElseStmt(Statement):
    condition: Expression
    then_stmt: Statement
    else_stmt: Statement

@dataclass
class AssignmentStmt(Statement):
    name: str
    expr: Expression

class Expression:
    pass

@dataclass
class InfixExpr(Expression):
    operator: str
    left_expr: Expression
    right_expr: Expression

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class Int(Expression):
    value: int

@dataclass
class Call(Expression):
    ptr_expr: Expression
    args: List[Expression]
