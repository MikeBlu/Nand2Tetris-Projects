import sys
import os
from typing import Tuple

def linkClassFiles(kwargs: dict) -> Tuple[bool,str]:
    classList = kwargs.get('classFiles')
    if not (classList and isinstance(classList,(list,set)) and len(classList) >= 1):
        sys.stderr.write(f'No hack VM classes provided to link: set[Class-File]\n')
        sys.stderr.flush()
        return (False,None)
    
    classList = dict.fromkeys(classList)
    
    '''
        First classfile specified will be the file to link against the rest of the classfiles,
        this is -- by convention -- 'Main' for programs and 'Sys' for system-implementation files
    '''
    main_classFile_path = next(iter(classList))
    del classList[main_classFile_path]

    linked_classFile_path = 'Out.vm'
    with open(linked_classFile_path,'w') as linked_classFile:
        with open(main_classFile_path,'r') as main_classFile:
            for vm_instruction in main_classFile:
                linked_classFile.write(vm_instruction)
        linked_classFile.write('\n')
        linked_classFile.flush()
        for class_classFile_path in classList:
            with open(class_classFile_path,'r') as class_classFile:
                # extra meta-info to distinguish static environments between classes
                linked_classFile.write(f'%CLASS-REF% {os.path.splitext(os.path.basename(class_classFile_path))[0]}\n')
                for vm_instruction in class_classFile:
                    line = vm_instruction.split('//')[0].rstrip()
                    if not line:
                        continue
                    line += '\n'
                    linked_classFile.write(line)
                linked_classFile.flush()
    
    return (True,linked_classFile_path)