import numpy as np
from .Navigate import _Field

# -------------------------------- HEADER
class ReadHeader:
    def __init__(self,field:_Field):
        # Always make working base directory field
        self.path=field.path + "\\" + "header"

        # Read file
        with open(self.path) as f:
            self.text=f.read()
        
        # Extract data
        lines=self.text.split("\n")[:-1]
        
        self.dataTypeString=lines[0].split("<")[1]
        self.memberLength=int(lines[1].split(":")[1]) # 3 for vector 1 for scalar 9 for tensor
        self.fileLength=int(lines[2].split(":")[1])

        self.dataLengthPerFile=np.zeros(len(lines)-3,dtype=int)
        for i in range(3,len(lines)):
            self.dataLengthPerFile[i-3]=int(lines[i].split(":")[1])

        self.dataLength=sum(self.dataLengthPerFile)


# ------------------------ Snaps









