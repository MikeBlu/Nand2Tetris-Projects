from .Func_segment import segment_mod
from .Func_operation import stack_op

import os
import sys

def parse_stack_modification(command: str, args: list[str], line: int = 0, **kwargs) -> list[str] | None:
    if command == 'push' or command == 'pop':
        segment = args[0]
        index = args[1]
        return segment_mod(command, segment, int(index), line, global_ref=kwargs.get('global_ref'))
    else:
        sys.stderr.write(f'ln-{line}:ch1 error() Expected: valid stack modifier (push|pop)')
        sys.stderr.flush()
        return None
    
def parse_stack_operation(command: str, line: int = 0) -> list[str] | None:
    return stack_op(command, line)

def vmTranslate(kwargs):
    with open(kwargs.get('file'),'r',newline='\n') as vm_file, open(kwargs.get('output'),'w',newline='\n') as asm_file:
        lines = list(enumerate(vm_file, start=0))
        for line_indx, instruction in lines:
            line = instruction.strip()
            if line=='' or line.startswith('//'):
                continue
            line_parts = line.split()
            command = line_parts[0]
            args = line_parts[1:]
            asm_instructions = []
            if command in ['push','pop']:
                asm_instructions = parse_stack_modification(command, args, line_indx, global_ref=os.path.splitext(os.path.basename(kwargs.get('file')))[0])
            else:
                asm_instructions = parse_stack_operation(command, line_indx)

            if asm_instructions is None:
                vm_file.close()
                return False
            else:
                asm_file.write(f'// {line}\n')
                for asm_instruction in asm_instructions:
                    asm_file.write(asm_instruction+'\n')
                asm_file.flush()