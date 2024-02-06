import numpy,sys,os
from typing import Literal



def Get_DTYPE(variable:numpy.ndarray):
    dt = str(variable.dtype)
    bo = sys.byteorder
    gen = ""

    if bo=="little":gen+="<"
    elif bo=="big":gen+=">"
    else:gen+="="
    
    if "int" in dt:gen+="i" + str(int(int(dt[3:])/8))
    elif "float" in dt:gen+="f" + str(int(int(dt[5:])/8))
    
    return gen


def Get_NMEMB(variable:numpy.ndarray):
    return str((variable.shape)[1])

def Get_DataLength(variable:numpy.ndarray):
    return str((variable.shape)[0])


def WriteHeader(path,variable,nfile=1):
    header = ""
    header += "DTYPE: " + Get_DTYPE(variable) + "\n"
    header += "NMEMB: " + Get_NMEMB(variable) + "\n"
    header += "NFILE: " + str(nfile) +"\n"
    # Multi file not implemented for now
    header += "000000: " + str(Get_DataLength(variable)) + " : 0 : 0\n"
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

    with open(field_path + os.sep + "000000",'wb') as f: variable.tofile(f)
    WriteHeader(field_path + os.sep + "header",variable)




