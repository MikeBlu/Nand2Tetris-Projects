import os, sys, yaml, re

class HackSymbolicParser:

    _label_dict = {}
    _ref_dict = {}
    _reserved_symbols = {
        'SP':0,
        'LCL':1,
        'ARG':2,
        'THIS':3,
        'THAT':4,
        'R0':0,
        'R1':1,
        'R2':2,
        'R3':3,
        'R4':4,
        'R5':5,
        'R6':6,
        'R7':7,
        'R8':8,
        'R9':9,
        'R10':10,
        'R11':11,
        'R12':12,
        'R13':13,
        'R14':14,
        'R15':15,
        'SCREEN':16384,
        'KEYBOARD':24576
    }
    _invalid_label_pattern = r'[^A-Za-z0-9_$.]' # disallow any char that is not alphanumeric or _, $, .
    _invalid_ref_pattern = r'[^A-Za-z0-9_$.]' # disallow any char that is not alphanumeric or _, $, .

    def __init__(self):
        for sym, val in self._reserved_symbols.items():
            self._ref_dict[sym] = val

    def parse(self, filePath):
        self.parse_labels(filePath)
        self.parse_refs(filePath)

    def parse_labels(self, filePath):
        with open(filePath,'rt',newline='\n') as asm_file:
            line_indx = 0
            for symbol in asm_file:
                symbol = symbol.split('//')[0].strip() # remove comments and leading/trailing whitespaces
                if len(symbol)==0:
                    continue
                elif symbol[-1]==')' and symbol[0]=='(': # interpret labels
                    label = symbol[1:-1]
                    if label in self._reserved_symbols:
                        sys.stderr.write(f'ln-{line_indx}:ch1 error() Reserved symbol "{label}" cannot be used as label\n')
                        sys.stderr.flush()
                        asm_file.close()
                        exit(-1)
                    elif len(label) == 0:
                        sys.stderr.write(f'ln-{line_indx}:ch1 error() Label body cannot be empty string ""')
                        sys.stderr.flush()
                        asm_file.close()
                        exit(-1)
                    elif inv := re.search(self._invalid_label_pattern, label):
                        sys.stderr.write(f'ln-{line_indx}:ch{inv.start()} error() Invalid char \'{inv.group()}\' specified in label "{label}"\n')
                        sys.stderr.flush()
                        asm_file.close()
                        exit(-1)
                    self._label_dict[label] = line_indx
                    if self.translate_reference(label):
                        self._ref_dict.pop(label)
                    continue

                line_indx += 1

    def parse_refs(self, filePath):
        with open(filePath,'rt',newline='\n') as asm_file:
            line_indx = 0
            for symbol in asm_file:
                symbol = symbol.split('//')[0].strip() # remove comments and leading/trailing whitespaces
                if len(symbol)==0:
                    continue
                elif symbol[0]=='@' and not symbol[1:].isdigit(): # interpret references
                    var = symbol[1:]
                    if len(var) == 0:
                        sys.stderr.write(f'ln-{line_indx}:ch1 error() Reference body cannot be empty string ""')
                        sys.stderr.flush()
                        asm_file.close()
                        exit(-1)
                    elif inv := re.search(self._invalid_ref_pattern, var):
                        sys.stderr.write(f'ln-{line_indx}:ch{inv.start()} error() Invalid char \'{inv.group()}\' specified in reference "{var}"\n')
                        sys.stderr.flush()
                        asm_file.close()
                        exit(-1)
                    elif var[0].isdigit():
                        sys.stderr.write(f'ln-{line_indx}:ch1 error() Reference body cannot contain leading digits\n')
                        sys.stderr.flush()
                        asm_file.close()
                        exit(-1)
                    elif var not in self._ref_dict and not self.translate_label(var):
                        self._ref_dict[var] = len(self._ref_dict)-len(self._reserved_symbols)+16
                line_indx += 1

    def read_label_file(self, filePath: str = None):
        with open(filePath) as label_file:
            self._label_dict = yaml.safe_load(label_file)

    def read_ref_file(self, filePath: str = None):
        with open(filePath) as ref_file:
            self._ref_dict = yaml.safe_load(ref_file)

    def write_label_file(self, filePath: str = None):
        os.makedirs("symbols", exist_ok=True)
        with open(filePath or os.path.join(os.getcwd(),'symbols','label.yaml'),'w') as label_file:
            yaml.dump(self._label_dict,label_file,default_flow_style=True)

    def write_ref_file(self, filePath: str = None):
        os.makedirs("symbols", exist_ok=True)
        with open(filePath or os.path.join(os.getcwd(),'symbols','ref.yaml'),'w') as ref_file:
            yaml.dump(self._ref_dict,ref_file,default_flow_style=True)

    def translate_label(self, label: str) -> int:
        return self._label_dict.get(label,None)
    
    def translate_reference(self, reference: str) -> int:
        return self._ref_dict.get(reference,None)