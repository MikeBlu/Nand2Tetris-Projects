from .Func_segment import segment_mod
from .Func_operation import stack_op
from .State_control import branch_comm
from .Func_Control import func_comm

from .VM_Util import memInitClassFile

import os
import sys

def parse_stack_modification(command: str, args: list[str], line: int = 0, **kwargs) -> list[str] | None:
    if command == 'push' or command == 'pop':
        segment = args[0]
        index = args[1]
        return segment_mod(command, segment, int(index), line, global_ref=kwargs.get('global_ref'))
    else:
        sys.stderr.write(f'ln-{line}:ch1 error() Expected: valid stack modifier (push|pop)\n')
        sys.stderr.flush()
        return None
    
def parse_stack_operation(command: str, line: int = 0) -> list[str] | None:
    return stack_op(command, line)

def parse_branch_command(command: str, args: list[str], line: int = 0) -> list[str] | None:
    if len(args) > 0:
        return branch_comm(command,args[0],line)
    else:
        sys.stderr.write(f'ln-{line}:ch{len(command)+2} error() Not Enough arguments provided for branch/label statement\n')
        sys.stderr.flush()
        return None
    
def parse_function_command(command: str, args: list[str], line: int = 0, **kwargs) -> list[str] | None:
    if (len(args) > 1 and command != 'return'):
        return func_comm(command, args[0], num_args=args[1], line=line, global_ref=kwargs.get('global_ref'))
    elif (command == 'return'):
        return func_comm(command, 'return', line=line)
    else:
        sys.stderr.write(f'ln-{line}:ch{len(command)+2} error() Not Enough arguments provided for {command} statement\n')
        sys.stderr.flush()
        return None

def vmTranslate(kwargs: dict) -> bool:
    input_path = kwargs.get('file')
    if not (input_path and isinstance(input_path,str)):
        sys.stderr.write(f'No input file specified: string\n')
        sys.stderr.flush()
        return False
    main_class = os.path.splitext(os.path.basename(input_path))[0]
    with open(input_path,'r',newline='\n') as vm_file, open(kwargs.get('output') or (main_class+'.asm'),'w',newline='\n') as asm_file:
        class_ref = main_class
        kwargs.get('bootstrap') and memInitClassFile(asm_file,global_ref=class_ref)
        lines = list(enumerate(vm_file, start=0))
        for line_indx, instruction in lines:
            line = instruction.split('//')[0].strip()
            if not line:
                continue
            line_parts = line.split()
            command = line_parts[0]
            args = line_parts[1:]
            asm_instructions = []
            if command in ['push','pop']:
                asm_instructions = parse_stack_modification(command, args, line_indx, global_ref=class_ref)
            elif command in ['label','goto','if-goto']:
                asm_instructions = parse_branch_command(command,args,line_indx)
            elif command in ['function','call','return']:
                asm_instructions = parse_function_command(command, args, line_indx, global_ref=class_ref)
            elif command in ['%CLASS-REF%']: # sepcify static environment
                class_ref = args[0]
                continue
            else:
                asm_instructions = parse_stack_operation(command, line_indx)

            if asm_instructions is None:
                vm_file.close()
                asm_file.close()
                return False
            else:
                kwargs.get('annotate') and asm_file.write(f'// {line}\n')
                asm_file.write('\n'.join(asm_instructions)+'\n')
                asm_file.flush()

        asm_file.truncate(asm_file.tell() - 1) # remove last trailing newline

    return True