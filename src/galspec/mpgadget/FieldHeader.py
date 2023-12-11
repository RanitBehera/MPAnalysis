from typing import Any
import numpy

class _DTYPE:
    def __init__(self, typestring: str) -> None:
        self.raw_string         = typestring
        self.endianness         = self.raw_string[0]
        self.character          = self.raw_string[1]
        self.byte_width         = int(self.raw_string[2])
        self._char_width_string = self.raw_string[1:3]

    def __repr__(self) -> str:
        return self.raw_string

    @property
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.raw_string

class FieldHeader:
    def __init__(self, path: str) -> None:
        self.path               = path

        with open(self.path) as f:
            self.contents       = f.read()
        
        lines = self.contents.split("\n")[:-1]
        
        self.dtype              = _DTYPE(lines[0].split(" ")[1])
        self.nmemb              = int(lines[1].split(":")[1])
        self.nfile              = int(lines[2].split(":")[1])

        self.filenames          = ()
        self.datalength_per_file    = numpy.zeros(len(lines)-3,dtype=int)
        self.checksum_of_files  = numpy.zeros(len(lines)-3,dtype=int)
        for i in range(3,len(lines)):
            self.filenames+=(lines[i].split(":")[0],)
            self.datalength_per_file[i-3]   = int(lines[i].split(":")[1])
            self.checksum_of_files[i-3] = int(lines[i].split(":")[3])

        self.total_data_length         = sum(self.datalength_per_file)

    def __repr__(self) -> str:
        return self.contents