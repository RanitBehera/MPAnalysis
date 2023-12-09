import numpy

class _DTYPE:
    def __init__(self,typestring):
        self.rawString          = typestring
        self.endianness         = self.rawString[0]
        self.character          = self.rawString[1]
        self.bytewidth          = int(self.rawString[2])
        self.typeString         = self.rawString[1:3]

class FieldHeader:
    def __init__(self,path:str):
        with open(path) as f:
            self.contents       = f.read()
        lines = self.contents.split("\n")[:-1]
        self.datatype           = _DTYPE(lines[0].split(" ")[1])
        self.memberLength       = int(lines[1].split(":")[1])
        self.fileLength         = int(lines[2].split(":")[1])
        self.dataLengthPerFile  = numpy.zeros(len(lines)-3,dtype=int)
        self.checksumOfFiles    = numpy.zeros(len(lines)-3,dtype=int)
        for i in range(3,len(lines)):
            self.dataLengthPerFile[i-3] = int(lines[i].split(":")[1])
            self.checksumOfFiles[i-3]   = int(lines[i].split(":")[3])

        self.dataLength         = sum(self.dataLengthPerFile)
