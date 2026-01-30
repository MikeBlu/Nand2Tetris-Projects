from HackVMTranslator import linkClassFiles, vmTranslate
import argparse

if __name__ == '__main__':
    arg_flags = [
        (str,'-o','--output'),
        (bool,'-b','--bootstrap'),
        (bool,'-a','--annotate'),
        (list, "-i", "--include")
    ]

    parser = argparse.ArgumentParser(prog='VM-Translator', 
        description='''
        Converts compliant Hack-16 VM code (.vm) into valid Hack-16 assembly (.asm).
        '''
    )

    parser.add_argument('file', type=str)
    for fl in arg_flags:
        arg_type, short, long = fl

        if arg_type is bool:
            parser.add_argument(short, long, action='store_true')
        elif (arg_type is set) or (arg_type is list):
            parser.add_argument(short, long, nargs="+", required=False)
        else:
            parser.add_argument(short, long, type=arg_type)

    args = parser.parse_args()

    linked_ClassFile = linkClassFiles({
        "classFiles": [args.file, *(args.include or [])]
    })[1]
    
    vmTranslate({
        'file': linked_ClassFile,
        'output': args.output or 'output.asm',
        'bootstrap': args.bootstrap,
        'annotate': args.annotate
    })