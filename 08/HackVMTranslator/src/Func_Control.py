import sys
import re
from .Func_segment import segment_mod
from .State_control import branch_comm

def invalid_label(label: str):
    invalid_ref_pattern = r'[^A-Za-z0-9_$.]' # disallow any char that is not alphanumeric or _, $, .
    inv = re.search(invalid_ref_pattern, label)
    return inv


def func_comm(command: str, functionName: str, num_args: int = 0, line: int = 0, global_ref: str = None) -> list[str] | None:
    if inv := invalid_label(functionName):
        sys.stderr.write(f'ln-{line}:ch{inv.start()} error() Invalid char \'{inv.group()}\' specified in label "{functionName}"\n')
        sys.stderr.flush()
        return None
    
    if command == 'function':
        # initialize new label for functionName, and push locals
        return [f'({functionName})',  *(arg for _ in range(int(num_args)) for arg in segment_mod('push','constant',0,line,global_ref))]
    elif command == 'call':
        return_label = f'{global_ref}.{functionName}.return.{line}'
        return [
            f'@{return_label}', # push returnAddress
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@LCL', # push LCL
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@ARG', # push ARG
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@THIS', # push THIS
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@THAT', # push THAT
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@SP', # ARG = SP-5-nArgs
            'D=M',
            '@5',
            'D=D-A',
            f'@{num_args}',
            'D=D-A',
            '@ARG',
            'M=D',
            '@SP', # LCL = SP
            'D=M',
            '@LCL',
            'M=D',
            *branch_comm('goto',functionName,line), # goto functionName
            f'({return_label})' # (returnAddress)
        ]
    else:
        '''
            'return' is a little more involved in assembly, & is the most complex function command;
            in my case Register 14 is used to stored the Endframe value, Register 15 is used to 
            store the return-address to the caller
        '''
        return [
            # endframe = LCL #
            '@LCL', # get LCL
            'D=M',
            '@R14', # R14 [endframe] = LCL 
            'M=D',

            # retAddr = *(endframe - 5) #
            '@5', # A = endframe - 5
            'A=D-A',
            'D=M', # D = *(endframe - 5)
            '@R15', # get R15 [retAddr]
            'M=D', # retAddr = D

            # *ARG = pop() #
            '@SP', # get SP
            'M=M-1', # decrement SP
            'A=M', # A = SP (top of stack)
            'D=M', # D = *SP
            '@ARG', # get ARG
            'A=M', # A = ARG
            'M=D', # *ARG = D

            # SP = ARG + 1 #
            '@ARG', # get ARG + 1
            'D=M+1',
            '@SP', # set SP = ARG + 1
            'M=D',

            # THAT = *(endframe-1) #
            '@R14', # A & endframe = endframe-1
            'AM=M-1',
            'D=M', # D = *(endframe-1)
            '@THAT', # get THAT
            'M=D', # THAT = D

            # THIS = *(endframe-2) #
            '@R14', # A & endframe = (endframe-1)-1
            'AM=M-1',
            'D=M', # D = *(endframe-2)
            '@THIS', # get THIS
            'M=D', # THIS = D

            # ARG = *(endframe-3) #
            '@R14', # A & endframe = (endframe-2)-1
            'AM=M-1',
            'D=M', # D = *(endframe-3)
            '@ARG', # get ARG
            'M=D', # ARG = D

            # LCL = *(endframe-4) #
            '@R14', # A & endframe = (endframe-3)-1
            'AM=M-1',
            'D=M', # D = *(endframe-4)
            '@LCL', # get LCL
            'M=D', # ARG = D

            # goto retAddr #
            '@R15', # get retAddr
            'A=M',
            '0;JMP' # goto
        ]