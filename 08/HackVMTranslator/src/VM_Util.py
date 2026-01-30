import sys
from io import TextIOBase
from .Func_Control import func_comm

def memInitClassFile(fileStream: TextIOBase, global_ref=None) -> bool:
    if not (fileStream and isinstance(fileStream,TextIOBase)):
        sys.stderr.write(f'No valid plaintext file-stream specified to add Memory-Bootstrap: string\n')
        sys.stderr.flush()
        return False
    
    fileStream.write(f'@256\nD=A\n@SP\nM=D\n{'\n'.join(func_comm('call','Sys.init',num_args=0,line=0,global_ref=global_ref))}\n')
    fileStream.flush()
    
    return True
        