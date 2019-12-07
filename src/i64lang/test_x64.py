'''
Online assembler:
    https://defuse.ca/online-x86-assembler.htm
'''

import pytest
from . import x64
from . bits import Bits

def get_instruction_tester(instruction_cls):
    def tester(params, machine_code, intel_syntax):
        instruction: x64.Instruction = instruction_cls(*params)
        assert instruction.to_machine_code() == Bits.from_hex(machine_code)
        assert instruction.to_intel() == intel_syntax
    return tester


def test_MovImmToReg():
    test = get_instruction_tester(x64.MovImmToReg)

    test([x64.rax, 20],                   "48c7c014000000", "mov rax, 20")
    test([x64.rbp, 40],                   "48c7c528000000", "mov rbp, 40")
    test([x64.rsp, 1234567],              "48c7c487d61200", "mov rsp, 1234567")
    test([x64.r8, 20],                    "49c7c014000000", "mov r8, 20")
    test([x64.r14, 42],                   "49c7c62a000000", "mov r14, 42")
    test([x64.rbx, 1345678900],           "48C7C3346E3550", "mov rbx, 1345678900")
    test([x64.rdx, 98765432111],          "48ba2fe5e0fe16000000", "mov rdx, 98765432111")
    test([x64.r8, -1234567890000],        "49b8b0fb048ee0feffff", "mov r8, -1234567890000")
    test([x64.r12, 12345678900000000001], "49bc010889a18ca954ab", "mov r12, 12345678900000000001")

def test_MovRegToMem():
    test = get_instruction_tester(x64.MovRegToMem)

    test([x64.rax, x64.rax], "488900",   "mov [rax], rax")
    test([x64.rbx, x64.rdx], "488913",   "mov [rbx], rdx")
    test([x64.r15, x64.r9],  "4d890f",   "mov [r15], r9")
    test([x64.rax, x64.r10], "4c8910",   "mov [rax], r10")
    test([x64.r14, x64.rsp], "498926",   "mov [r14], rsp")
    test([x64.r14, x64.rax], "498906",   "mov [r14], rax")
    test([x64.rsp, x64.rax], "48890424", "mov [rsp], rax")
    test([x64.rbp, x64.rcx], "48894d00", "mov [rbp], rcx")
    test([x64.r12, x64.r8],  "4d890424", "mov [r12], r8")

def test_MovMemToReg():
    test = get_instruction_tester(x64.MovMemToReg)

    test([x64.rax, x64.rax], "488b00", "mov rax, [rax]")
    test([x64.rbx, x64.rdx], "488b1a", "mov rbx, [rdx]")
    test([x64.r8, x64.r8], "4d8b00", "mov r8, [r8]")
    test([x64.r12, x64.r15], "4d8b27", "mov r12, [r15]")
    test([x64.r10, x64.rax], "4c8b10", "mov r10, [rax]")
    test([x64.r11, x64.rbx], "4c8b1b", "mov r11, [rbx]")
    test([x64.rax, x64.r11], "498b03", "mov rax, [r11]")
    test([x64.rax, x64.rsp], "488b0424", "mov rax, [rsp]")
    test([x64.rax, x64.rbp], "488b4500", "mov rax, [rbp]")
    test([x64.rbx, x64.r13], "498b5d00", "mov rbx, [r13]")
    test([x64.rdx, x64.r12], "498b1424", "mov rdx, [r12]")

def test_AddRegToReg():
    test = get_instruction_tester(x64.AddRegToReg)

    test([x64.rax, x64.rax], "4801c0", "add rax, rax")
    test([x64.rdx, x64.rsp], "4801e2", "add rdx, rsp")
    test([x64.r13, x64.r15], "4d01fd", "add r13, r15")
    test([x64.r8, x64.r10], "4d01d0", "add r8, r10")
    test([x64.rbx, x64.r13], "4c01eb", "add rbx, r13")
    test([x64.rdi, x64.r14], "4c01f7", "add rdi, r14")
    test([x64.r9, x64.rbp], "4901e9", "add r9, rbp")
    test([x64.r11, x64.rsp], "4901e3", "add r11, rsp")

def test_SubRegFromReg():
    test = get_instruction_tester(x64.SubRegFromReg)

    test([x64.rax, x64.rbx], "4829d8", "sub rax, rbx")
    test([x64.r12, x64.r14], "4d29f4", "sub r12, r14")
    test([x64.rsp, x64.r9], "4c29cc", "sub rsp, r9")
    test([x64.r8, x64.rdx], "4929d0", "sub r8, rdx")

def test_Compare():
    test = get_instruction_tester(x64.Compare)

    test([x64.rax, x64.rbx], "4839d8", "cmp rax, rbx")
    test([x64.r12, x64.r14], "4d39f4", "cmp r12, r14")
    test([x64.rsp, x64.r9], "4c39cc", "cmp rsp, r9")
    test([x64.r8, x64.rdx], "4939d0", "cmp r8, rdx")
