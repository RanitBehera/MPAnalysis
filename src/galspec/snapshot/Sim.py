from galspec.snapshot.PART import _PART
from galspec.snapshot.PIG import _PIG
from galspec.snapshot.RSG import _RSG

class _Sim:
    def __init__(self,output_dir:str):
        if not isinstance(output_dir,str):raise TypeError
        self.path = output_dir

    def PART(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PART(snap_num,self.path)

    def PIG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PIG(snap_num,self.path)
    
    def RSG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _RSG(snap_num,self.path)
