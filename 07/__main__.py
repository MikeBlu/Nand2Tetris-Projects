from HackVMTranslator import vmTranslate
import argparse
import sys

if __name__ == '__main__':
    arg_flags = [
        (str,'-o','--output')
    ]

    parser = argparse.ArgumentParser(prog='VM Translator', 
        description='''
        Converts compliant Hack-16 VM code (.vm) into valid Hack-16 assembly (.asm).
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

    vmTranslate({
        'file': args.file,
        'output': args.output,
    })