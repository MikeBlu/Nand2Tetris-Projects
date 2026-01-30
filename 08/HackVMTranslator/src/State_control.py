import sys
import re

def invalid_label(label: str):
    invalid_ref_pattern = r'[^A-Za-z0-9_$.]' # disallow any char that is not alphanumeric or _, $, .
    inv = re.search(invalid_ref_pattern, label)
    return inv


def branch_comm(command: str, label: str, line: int = 0) -> list[str] | None:
    if inv := invalid_label(label):
        sys.stderr.write(f'ln-{line}:ch{inv.start()} error() Invalid char \'{inv.group()}\' specified in label "{label}"\n')
        sys.stderr.flush()
        return None
    
    if command == 'label':
        return [f'({label})'] # initialize new label
    elif command == 'if-goto':
        return [
            '@SP', # get SP
            'M=M-1', # decrement SP
            'A=M',
            'D=M', # D = *(SP-1)
            f'@{label}', # set label for jump
            'D;JNE' # jump if last stack item is not zero (false)
        ]
    else: # goto
        return [
            f'@{label}', # set label for jump
            '0;JMP' # jump to label
        ]
