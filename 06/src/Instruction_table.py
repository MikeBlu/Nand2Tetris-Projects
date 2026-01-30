func_codes = {
    '0':   b'0101010',
    '1':   b'0111111',
    '-1':  b'0111010',
    'D':   b'0001100',
    'A':   b'0110000',
    'M':   b'1110000',
    '!D':  b'0001101',
    '!A':  b'0110001',
    '!M':  b'1110001',
    '-D':  b'0001111',
    '-A':  b'0110011',
    '-M':  b'1110011',
    'D+1': b'0011111',
    'A+1': b'0110111',
    'M+1': b'1110111',
    'D-1': b'0001110',
    'A-1': b'0110010',
    'M-1': b'1110010',
    'D+A': b'0000010',
    'D+M': b'1000010',
    'D-A': b'0010011',
    'D-M': b'1010011',
    'A-D': b'0000111',
    'M-D': b'1000111',
    'D&A': b'0000000',
    'D&M': b'1000000',
    'D|A': b'0010101',
    'D|M': b'1010101'
}

jump_codes = {
    'JGT': b'001',     # greater than 0
    'JEQ': b'010',     # equal to 0
    'JGE': b'011',     # greater or equal to 0
    'JLT': b'100',     # less than 0
    'JNE': b'101',     # not equal to 0
    'JLE': b'110',     # less or equal to 0
    'JMP': b'111',     # unconditional
}

def asm_expr_to_val(func_str: str):
    val_int = int(func_codes.get(func_str,b'0'),2)
    return val_int

def asm_jump_to_val(jmp_str: str):
    jmp_int = int(jump_codes.get(jmp_str,b'0'),2)
    return jmp_int
