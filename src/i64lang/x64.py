from dataclasses import dataclass
from . bits import Bits

@dataclass
class Register:
    # e.g. rax, r12, ...
    name: str

    # 0 for rax, rbx, ...
    # 1 for r8 - r15
    group: int

    # 0 for rax, r8
    # 1 for rbx, r9
    # ...
    # 7 for rdi, r15
    number: int

    bits: Bits = Bits("")

    def __post_init__(self):
        self.bits = Bits.from_int(self.number, length=3)

class Instruction:
    def to_intel_syntax(self) -> str:
        raise NotImplementedError()

    def to_machine_code(self) -> str:
        raise NotImplementedError()

@dataclass
class MovImmToReg(Instruction):
    reg: Register
    value: int

    def to_intel_syntax(self):
        return f"mov {self.reg.name}, {self.value}"

    def to_machine_code(self):
        prefix = Bits.from_hex("48" if self.reg.group == 0 else "49")

        imm_size = get_imm_size(self.value)
        if imm_size <= 4:
            opcode = Bits.from_hex("c7")
            args = Bits("11000") + self.reg.bits
            imm = Bits.from_int(self.value, 32).reversed_bytes()
            return prefix + opcode + args + imm
        else:
            opcode = Bits.from_hex_and_offset("b8", self.reg.number)
            imm = Bits.from_int(self.value, 64).reversed_bytes()
            return prefix + opcode + imm

@dataclass
class MovRegToMem(Instruction):
    addr_reg: Register
    src_reg: Register

    def to_intel_syntax(self):
        return f"mov [{self.addr_reg.name}], {self.src_reg.name}"

    def to_machine_code(self):
        prefix = get_register_group_prefix(self.addr_reg, self.src_reg)
        opcode = Bits.from_hex("89")

        if self.addr_reg.number != 5:
            mod_bits = Bits("00")
            imm = Bits("")
        else:
            mod_bits = Bits("01")
            imm = Bits.zeros(8)

        args = mod_bits + self.src_reg.bits + self.addr_reg.bits
        if self.addr_reg.number == 4:
            args += Bits.from_hex("24")

        return prefix + opcode + args + imm

@dataclass
class MovMemToReg(Instruction):
    dst_reg: Register
    addr_reg: Register

    def to_intel_syntax(self):
        return f"mov {self.dst_reg.name}, [{self.addr_reg.name}]"

    def to_machine_code(self):
        prefix = get_register_group_prefix(self.addr_reg, self.dst_reg)
        opcode = Bits.from_hex("8b")

        if self.addr_reg.number != 5:
            mod_bits = Bits("00")
            imm = Bits("")
        else:
            mod_bits = Bits("01")
            imm = Bits.zeros(8)

        args = mod_bits + self.dst_reg.bits + self.addr_reg.bits
        if self.addr_reg.number == 4:
            args += Bits.from_hex("24")

        return prefix + opcode + args + imm

@dataclass
class SimpleTwoRegisterInstruction(Instruction):
    opcode_hex = NotImplemented
    intel_syntax_name = NotImplemented

    dst_reg: Register
    src_reg: Register

    def to_machine_code(self):
        prefix = get_register_group_prefix(self.dst_reg, self.src_reg)
        opcode = Bits.from_hex(self.opcode_hex)
        args = Bits("11") + self.src_reg.bits + self.dst_reg.bits
        return prefix + opcode + args

    def to_intel_syntax(self):
        return f"{self.intel_syntax_name} {self.dst_reg.name}, {self.src_reg.name}"

class AddRegToReg(SimpleTwoRegisterInstruction):
    opcode_hex = "01"
    intel_syntax_name = "add"

class SubRegFromReg(SimpleTwoRegisterInstruction):
    opcode_hex = "29"
    intel_syntax_name = "sub"

class Compare(SimpleTwoRegisterInstruction):
    opcode_hex = "39"
    intel_syntax_name = "cmp"

@dataclass
class SetOnConditionInstruction(Instruction):
    opcode_hex = NotImplemented
    intel_syntax_name = NotImplemented

    reg: Register

    def to_machine_code(self):
        zeroing = MovImmToReg(self.reg, 0).to_machine_code()

        prefix = Bits.from_hex("41" if self.reg.group == 1 else "")
        opcode = Bits.from_hex(self.opcode_hex)
        args = Bits("11000") + self.reg.bits
        set_byte_on_condition = prefix + opcode + args

        return zeroing + set_byte_on_condition

    def to_intel_syntax(self):
        # This is a combination of two instructions.
        return f"{self.intel_syntax_name} {self.reg.name}"

class SetIfNotEqual(SetOnConditionInstruction):
    opcode_hex = "0f95"
    intel_syntax_name = "setne"

class SetIfEqual(SetOnConditionInstruction):
    opcode_hex = "0f94"
    intel_syntax_name = "sete"

class SetIfGreater(SetOnConditionInstruction):
    opcode_hex = "0f9f"
    intel_syntax_name = "setg"

class SetIfLess(SetOnConditionInstruction):
    opcode_hex = "0f9c"
    intel_syntax_name = "setl"

class SetIfGreaterOrEqual(SetOnConditionInstruction):
    opcode_hex = "0f9d"
    intel_syntax_name = "setge"

class SetIfLessOrEqual(SetOnConditionInstruction):
    opcode_hex = "0f9e"
    intel_syntax_name = "setle"

class Return(Instruction):
    def to_machine_code(self):
        return Bits.from_hex("c3")

    def to_intel_syntax(self):
        return "ret"

def get_register_group_prefix(reg1: Register, reg2: Register) -> Bits:
    return prefixes_for_64_bit_registers[(reg1.group, reg2.group)]

def get_imm_size(n):
    if n == 0:
        return 0
    elif -2**7 <= n <= 2**7 - 1:
        return 1
    elif -2**15 <= n <= 2**15 - 1:
        return 2
    elif -2**31 <= n <= 2**31 - 1:
        return 4
    elif -2**63 <= n <= 2**64 - 1:
        return 8
    else:
        raise NotImplementedError("unsupported immediate value size")

prefixes_for_64_bit_registers = {
    (0, 0) : Bits.from_hex("48"),
    (1, 0) : Bits.from_hex("49"),
    (0, 1) : Bits.from_hex("4c"),
    (1, 1) : Bits.from_hex("4d")
}

rax = Register("rax", 0, 0)
rcx = Register("rcx", 0, 1)
rdx = Register("rdx", 0, 2)
rbx = Register("rbx", 0, 3)

rsp = Register("rsp", 0, 4)
rbp = Register("rbp", 0, 5)
rsi = Register("rsi", 0, 6)
rdi = Register("rdi", 0, 7)

r8 = Register("r8", 1, 0)
r9 = Register("r9", 1, 1)
r10 = Register("r10", 1, 2)
r11 = Register("r11", 1, 3)

r12 = Register("r12", 1, 4)
r13 = Register("r13", 1, 5)
r14 = Register("r14", 1, 6)
r15 = Register("r15", 1, 7)
