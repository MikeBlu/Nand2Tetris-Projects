import sys

dynamic_segments = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
}
fixed_segments = {
    'temp': 5,
    'pointer': 3 # pointer 0 -> 3, pointer 1 -> 4
}

def segment_mod(command: str, segment: str, index: int, line: int = 0, global_ref=None) -> list[str] | None:
    if segment in dynamic_segments:
        base = dynamic_segments[segment]
        if (segment == 'pointer' and index not in [0,1]) or (segment != 'pointer' and index < 0):
            sys.stderr.write(f'ln-{line}:ch1 error() Invalid index [{index}] for segment "{segment}"\n')
            sys.stderr.flush()
            return None
        if command == 'push':
            return [
                f'@{base}', # get base address
                'D=M', # D = base address
                f'@{index}', # get index
                'A=D+A', # A = base + index (offset)
                'D=M', # D = RAM[base + index]
                '@SP', # SP points to next free location
                'A=M', # A = SP (top of stack)
                'M=D', # *SP = D
                '@SP', # get SP
                'M=M+1' # advance SP
            ]
        elif command == 'pop':
            return [
                f'@{base}',  # get base address
                'D=M', # D = base address
                f'@{index}', # get index
                'D=D+A', # D = base + index (offset)
                '@5', # use first temp address RAM[5]
                'M=D', # RAM[5] = dest address
                '@SP', # get SP
                'M=M-1', # decrement SP
                'A=M', # A = SP (top of stack)
                'D=M', # D = *SP
                '@5', # get temp address
                'A=M', # A = dest address
                'M=D' # RAM[dest address] = D
            ]
    elif segment in fixed_segments:
        base_addr = fixed_segments[segment]
        if (segment == 'pointer' and index not in [0,1]) or (segment != 'temp' and index < 0) or (segment == 'temp' and (index < 0 or index > 7)):
            sys.stderr.write(f'ln-{line}:ch1 error() Invalid index [{index}] for segment "{segment}"\n')
            sys.stderr.flush()
            return None
        target_addr = base_addr + index
        if command == 'push':
            return [
                f'@{target_addr}', # get target address
                'D=M', # D = RAM[target address]
                '@SP', # SP points to next free location
                'A=M', # A = SP (top of stack)
                'M=D', # *SP = D
                '@SP', # get SP
                'M=M+1' # advance SP
            ]
        elif command == 'pop':
            return [
                '@SP', # get SP
                'M=M-1', # decrement SP
                'A=M', # A = SP (top of stack)
                'D=M', # D = *SP
                f'@{target_addr}', # get target address
                'M=D' # RAM[target address] = D
            ]
    elif segment == 'constant':
        if command == 'push':
            return [
                f'@{index}', # get constant value
                'D=A', # D = constant value
                '@SP', # SP points to next free location
                'A=M', # A = SP (top of stack)
                'M=D', # *SP = D
                '@SP', # get SP
                'M=M+1' # advance SP
            ]
        else:
            sys.stdout.write(f'ln-{line}:ch1 warning() Cannot pop to constant segment, (ignored).\n')
            sys.stdout.flush()
            return []
    elif segment == 'static':
        var_name = f'{global_ref}.{index}' if global_ref else f'Static.{index}'
        if command == 'push':
            return [
                f'@{var_name}', # get static variable
                'D=M', # D = RAM[static variable]
                '@SP', # SP points to next free location
                'A=M', # A = SP (top of stack)
                'M=D', # *SP = D
                '@SP', # get SP
                'M=M+1' # advance SP
            ]
        elif command == 'pop':
            return [
                '@SP', # get SP
                'M=M-1', # decrement SP
                'A=M', # A = SP (top of stack)
                'D=M', # D = *SP
                f'@{var_name}', # get static variable
                'M=D' # RAM[static variable] = D
            ]
    else:
        sys.stderr.write(f'ln-{line}:ch1 error() Unknown segment "{segment}"\n')
        sys.stderr.flush()
        return None
