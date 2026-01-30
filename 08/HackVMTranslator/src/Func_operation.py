import sys

def stack_op(command: str, line: int = 0) -> list[str] | None:
    if command == 'add':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP (y)
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (next top of stack)
            'M=D+M',  # *SP = *SP + D (x + y)
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command == 'sub':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP (y)
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (next top of stack)
            'M=M-D',  # *SP = *SP - D (x - y)
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command == 'neg':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'M=-M',   # *SP = -(*SP)
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command == 'eq':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP (y)
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (next top of stack)
            'D=M-D',  # D = x - y
            '@EQ_TRUE_'+str(line), # if D==0 jump to EQ_TRUE
            'D;JEQ',
            '@SP',    # get SP
            'A=M',    # A = SP (top of stack)
            'M=0',    # *SP = false (0)
            '@EQ_END_'+str(line),  # jump to end
            '0;JMP',
            '(EQ_TRUE_'+str(line)+')',
            '@SP',    # get SP
            'A=M',    # A = SP (top of stack)
            'M=-1',   # *SP = true (-1)
            '(EQ_END_'+str(line)+')',
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command=='gt':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP (y)
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (next top of stack)
            'D=M-D',  # D = x - y
            '@GT_TRUE_'+str(line), # if D>0 jump to GT_TRUE
            'D;JGT',
            '@SP',    # get SP
            'A=M',    # A = SP (top of stack)
            'M=0',    # *SP = false (0)
            '@GT_END_'+str(line),  # jump to end
            '0;JMP',
            '(GT_TRUE_'+str(line)+')',
            '@SP',    # get SP
            'A=M',    # A = SP (top of stack)
            'M=-1',   # *SP = true (-1)
            '(GT_END_'+str(line)+')',
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command=='lt':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP (y)
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (next top of stack)
            'D=M-D',  # D = x - y
            '@LT_TRUE_'+str(line), # if D<0 jump to LT_TRUE
            'D;JLT',
            '@SP',    # get SP
            'A=M',    # A = SP (top of stack)
            'M=0',    # *SP = false (0)
            '@LT_END_'+str(line),  # jump to end
            '0;JMP',
            '(LT_TRUE_'+str(line)+')',
            '@SP',    # get SP
            'A=M',    # A = SP (top of stack)
            'M=-1',   # *SP = true (-1)
            '(LT_END_'+str(line)+')',
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command=='and':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP (y)
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (next top of stack)
            'D=D&M',  # D = x & y
            'M=D',    # *SP = x & y
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command=='or':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP (y)
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (next top of stack)
            'D=D|M',  # D = x | y
            'M=D',    # *SP = x | y
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    elif command=='not':
        return [
            '@SP',    # get SP
            'M=M-1',  # decrement SP
            'A=M',    # A = SP (top of stack)
            'D=M',    # D = *SP
            'D=!D',   # D = !D
            'M=D',    # *SP = D
            '@SP',    # get SP
            'M=M+1'   # advance SP
        ]
    else:
        sys.stderr.write(f'ln-{line}:ch1 error() Expected: valid stack operation (add|sub|neg|eq), got \'{command}\'\n')
        sys.stderr.flush()
        return None