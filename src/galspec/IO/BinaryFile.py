import os,sys,numpy


class _BinaryFile:
    def __init__(self,path:str,dtype:numpy.dtype) -> None:
        self.path = path
        self.dtype = dtype

    def Read(self):
        with open (self.path, mode='rb') as file:
            return numpy.fromfile(file,self.dtype)
    


# Seperate from class to avoid accidental writes
# Further safe-keeping by using "xb" mode instead of "wb" mode for file opening
def _WriteHeader(path,variable:numpy.ndarray,nfile=1):
    # Get DTYPE
    dt = str(variable.dtype)
    bo = sys.byteorder
    dtype = ""

    if bo=="little":dtype+="<"
    elif bo=="big":dtype+=">"
    else:dtype+="="
    
    if "int" in dt:dtype+="i" + str(int(int(dt[3:])/8))
    elif "float" in dt:dtype+="f" + str(int(int(dt[5:])/8))

    # Write Header
    header = ""
    header += "DTYPE: " + dtype + "\n"
    header += "NMEMB: " + str((variable.shape)[1]) + "\n"
    header += "NFILE: " + str(nfile) +"\n"

    header += "000000: " + str((variable.shape)[0]) + " : 0 : 0\n"
    with open(path,"w") as f:f.write(header)


def Write(path:str,fieldname:str,variable):
    # Validation
    path = path.strip()
    fieldname = fieldname.strip()
    variable = numpy.array(variable)
    if (len(variable.shape)==1):variable=variable.reshape(len(variable),1)
    elif (len(variable.shape)==0):variable=variable.reshape(1,1)

    field_path = path + os.sep + fieldname
    os.makedirs(field_path,exist_ok=True)
    # os.makedirs()

    with open(field_path + os.sep + "000000",'xb') as f: variable.tofile(f)
    _WriteHeader(field_path + os.sep + "header",variable)

