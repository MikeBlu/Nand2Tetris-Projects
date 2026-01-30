import sys, os, argparse, re
from Byte_To_String import bytes_to_binary_string
from Sym_Parser import HackSymbolicParser
import Instruction_table as hack_func

arg_flags = [
    (str,'-s','--label-path'),
    (str,'-r','--ref-path'),
    (str,'-o','--output'),
    (bool,'-p','--plain-text')
]

parser = argparse.ArgumentParser(prog='Hack assembler', 
    description='''
    Converts compliant Hack-16 assembly code (.asm) into a binary format (.hack),
    or newline delimited plaintext binary(0|1) if specified.
    '''
)

parser.add_argument('file', type=str)
for fl in arg_flags:
    arg_type, short, long = fl

    if arg_type is bool:
        parser.add_argument(short, long, action='store_true')
    else:
        parser.add_argument(short, long, type=arg_type)

if len(sys.argv)<2:
    sys.stderr.write('Expected at least 2 arguments: program {assembly-file} [..args]')
    sys.stderr.flush()
    exit(-1)

args = parser.parse_args()

def parse_C_Instruction(i: str, line: int = 0) -> bytes:
    bin_ins = 57344
    try:
        i_parts = i.split(';')
        if len(i_parts) > 2:
            sys.stderr.write(f'ln-{line}:ch1 error() Expected: {{optional dest}}=expr[;..jump]')
            return None
        exp = i_parts[0].split('=')
        if len(exp) > 2:
            sys.stderr.write(f'ln-{line}:ch1 error() Expected: {{optional dest}}=expr[;..jump]')
            return None
        jmp = i_parts[1] if len(i_parts)>1 else None
        
        # get expr
        bin_ins |= (hack_func.asm_expr_to_val(exp[-1].strip()) * 64) # multiply by pow(2,6) to pad 000000 for [dest][jump] instruction fragments

        # get dest
        if len(exp) > 1:
            dest = exp[0].strip()
            if inv := re.search(r'[^AMD]', dest):
                sys.stderr.write(f'ln-{line}:ch{inv.start()} error() Invalid storage code character provided "{inv.group()}"')
                return None
            bin_ins |= int('M' in dest) * 8
            bin_ins |= int('D' in dest) * 16
            bin_ins |= int('A' in dest) * 32
        
        # set jump
        if (jmp):
            jmp = jmp.strip()
            bin_ins |= hack_func.asm_jump_to_val(jmp)

        return bin_ins.to_bytes(2,byteorder='big')

    except Exception as e:
        sys.stderr.write(f'ln-{line}:ch1 error() Unable to evaluate expression >>{i}<<')
        return None


def parse_A_Instruction(i: str, symbols: HackSymbolicParser, line: int = 0) -> bytes:
    load_value = i[1:]
    if (sym_value := symbols.translate_reference(load_value)) is not None or (sym_value := symbols.translate_label(load_value)) is not None:
        load_value = sym_value
    else:
        try:
            load_value = int(load_value)
        except ValueError:
            sys.stderr.write(f'ln-{line}:ch1 error() Expected: address or data value')
            return None
    
    if load_value<0 or load_value>32767:
        sys.stderr.write(f'ln-{line}:ch1 error() Invalid value or incorrect address @[{load_value}]')
        return None
    
    return load_value.to_bytes(2,byteorder='big')

# Step 1: Symbolic Pass
symbols = HackSymbolicParser()
symbols.parse(os.path.join(os.getcwd(),args.file))
#######################

# Step 2: Store Symbols
label_path = os.path.join(os.getcwd(),args.label_path) if args.label_path else None
ref_path = os.path.join(os.getcwd(),args.ref_path)  if args.ref_path else None
symbols.write_label_file(label_path)
symbols.write_ref_file(ref_path)
#######################

# Step 3: Instruction Pass
def_output_path = os.path.join(os.getcwd(), re.sub(r'\.asm$','.hack', os.path.basename(args.file)))
output_path = os.path.join(os.getcwd(), args.output) if args.output else def_output_path
with open(args.file,'r',newline='\n') as asm_file, open(output_path,'wt' if args.plain_text else 'wb') as bin_file:
    lines = list(enumerate(asm_file, start=0))
    for line_indx, instruction in lines:
        instruction = instruction.split('//')[0].strip() # remove comments and leading/trailing whitespaces
        ins_type = 'a'
        # determine instruction type (a|c):
        if len(instruction) == 0:
            continue
        elif instruction[0] == '(' and instruction[-1] == ')':
            continue
        elif (instruction[0] != '@'):
            ins_type = 'c'
        
        byte_instruction = b''
        if ins_type == 'c':
            byte_instruction = parse_C_Instruction(instruction, line_indx)
        else:
            byte_instruction = parse_A_Instruction(instruction, symbols, line_indx)
        
        if byte_instruction is None:
            asm_file.close()
            bin_file.close()
            exit(-1)
        bin_file.write(bytes_to_binary_string(byte_instruction)+((line_indx != len(lines) - 1)*'\n') if args.plain_text else byte_instruction)
        bin_file.flush()
##########################