
import numpy as np
import os
# -------------------------------- HEADER
from .Navigate import _Field, _PART, _PIG

class ReadHeader:
    def __init__(self,field:_Field):
        if not isinstance(field,_Field):raise TypeError

        # Always make working base directory field
        self.path=field.path + os.sep + "header"

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

# ------------------------------------- SNAPSHOT ATTRIBUTE
class ReadAttribute:
    def __init__(self,snap:_PART|_PIG):
        if not (isinstance(snap,_PART) or isinstance(snap,_PIG)):
            print("[ERROR] Only PART and PIG have attributes")
            raise TypeError

        if (type(snap)==_PART):
            self.ReadAttribute_PART(snap)
        elif(type(snap)==_PIG):
            self.ReadAttribute_PIG(snap)

    def ReadAttribute_PART(self,snap:_PART):
        if not isinstance(snap,_PART):raise TypeError

        self.path = snap.path + os.sep + "Header" + os.sep + "attr-v2"

        # Read file
        with open(self.path) as f:
            self.text=f.read()

        # Extract data
        lines=self.text.split("\n")[:-1]

        self.BoxSize=float(lines[0].split("[")[-1].split("]")[0])
        self.BoxSizeUnit="Kilo-parsec"          #<---get thse from paramgadegt file

        self.CMBTemperature=float(lines[1].split("[")[-1].split("]")[0])
        self.CMBTemperatureUnit="Kelvin"

        self.HubbleParam=float(lines[5].split("[")[-1].split("]")[0])
        self.Omega0=float(lines[7].split("[")[-1].split("]")[0])
        self.OmegaBaryon=float(lines[8].split("[")[-1].split("]")[0])
        self.OmegaLambda=float(lines[9].split("[")[-1].split("]")[0])

        self.RSDFactor=float(lines[10].split("[")[-1].split("]")[0])
        self.Time=float(lines[11].split("[")[-1].split("]")[0])
        
        self.UnitLength_in_cm=float(lines[15].split("[")[-1].split("]")[0])
        self.UnitMass_in_g=float(lines[16].split("[")[-1].split("]")[0])
        self.UnitVelocity_in_cm_per_s=float(lines[17].split("[")[-1].split("]")[0])
        self.UsePeculiarVelocity=bool(lines[18].split("[")[-1].split("]")[0])

        self.MassTable=lines[6].split("[")[-1].split("]")[0].split(" ")[1:-1]
        self.MassTable=np.array([float(self.MassTable[i]) for i in range(len(self.MassTable))])

        self.MassTable=lines[6].split("[")[-1].split("]")[0].split(" ")[1:-1]
        self.MassTable=np.array([float(self.MassTable[i]) for i in range(len(self.MassTable))])

        self.TotNumPart=lines[13].split("[")[-1].split("]")[0].split(" ")[1:-1]
        self.TotNumPart=np.array([int(self.TotNumPart[i]) for i in range(len(self.TotNumPart))])

        self.TotNumPartInit=lines[14].split("[")[-1].split("]")[0].split(" ")[1:-1]
        self.TotNumPartInit=np.array([int(self.TotNumPartInit[i]) for i in range(len(self.TotNumPartInit))])

    def ReadAttribute_PIG(self,snap:_PIG):
        pass


# ------------------------ SNAPSHOT
from pathlib import Path        # For PART and PIG folder size

class ReadSnapshot:
    def __init__(self,base_dir,snapshot_file="Snapshots.txt"):
        # Always make working base directory field
        self.BaseDirectory=base_dir
        self.Path=base_dir + os.sep + snapshot_file
        # Read file
        f=open(self.Path)
        text=f.readlines()
        f.close()
        # Number of lines representing number of snapshots taken
        self.SnapshotLength=len(text)
        # Extract Data
        self.Snapshots=np.zeros(self.SnapshotLength,dtype=int)
        self.ScaleFactors=np.zeros(self.SnapshotLength)
        for i in range(0,self.SnapshotLength):
            line=text[i]
            self.Snapshots[i]    = int(line.split(" ")[0])
            self.ScaleFactors[i] = float(line.split(" ")[1])
        # Auxilary Fileds
        self.Redshifts=(1/self.ScaleFactors)-1
        self.RoundedScaleFactor=np.round(self.ScaleFactors,3)
        self.RoundedRedshifts=np.round(self.Redshifts,3)



    # Extended will show disk size of PART and PIG folders too
    # Blank print for new line
    def ShowSummeryTable(self,extended=False):
        if extended:self.CalculateDiscSizes()

        # Pre Table Info
        print("Number of Snapshots : ",self.SnapshotLength)
        if extended:print("Disk Data in : ","Bytes")


        # Header Top Border
        print("|--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|",sep="",end="")
        if extended:print("--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|",sep="",end="")
        print()     

        # Header Title
        print("|  ","Snapshot Number".ljust(16),"  |  ","Scale Factor".ljust(16),"  |  ","Redshift".ljust(16),"  |",sep="",end="")
        if extended: print("  ","PART Disc Size".ljust(16),"  |  ","PIG Disc Size".ljust(16),"  |",sep="",end="")
        print()
        
        #Header BottomBorder
        print("|--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|",sep="",end="")
        if extended:print("--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|",sep="",end="")
        print() 

        # Rows
        for i in range(0,self.SnapshotLength):
            print("|  ",end="")
            print(str(self.Snapshots[i]).ljust(16),end="  |  ")
            print(str(self.RoundedScaleFactor[i]).ljust(16),end="  |  ")
            print(str(self.RoundedRedshifts[i]).ljust(16),end="  |")
            if extended:
                print("  ",end="")
                print(('{:,}'.format(self.DiscSizePARTs[i])).rjust(16),end="  |  ")
                print(('{:,}'.format(self.DiscSizePIGs[i])).rjust(16),end="  |")
            print()

         

        # Table Bottom Border
        print("|--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|",sep="",end="")
        if extended:print("--","".ljust(16,'-'),"--|--","".ljust(16,'-'),"--|",sep="",end="")
        print() 

    # Call this to access both variables
    def CalculateDiscSizes(self):
        # Disk Size - Memory
        self.DiscSizePARTs = np.zeros(self.SnapshotLength,dtype=int)
        self.DiscSizePIGs  = np.zeros(self.SnapshotLength,dtype=int)
        for i in range(0,self.SnapshotLength):
            snap_num_fix='{:03}'.format(i)
            dir_part=self.BaseDirectory + os.sep + "PART_"+snap_num_fix
            dir_pig=self.BaseDirectory + os.sep + "PIG_"+snap_num_fix
            self.DiscSizePARTs[i] = sum(file.stat().st_size for file in Path(dir_part).rglob('*'))
            self.DiscSizePIGs[i]  = sum(file.stat().st_size for file in Path(dir_pig).rglob('*'))



# --------------------------------- BINARY DATA

def ReadField(field:_Field):
    if not isinstance(field,_Field):raise TypeError

    # Extract Header information
    head=ReadHeader(field)
    type_map={'f4':np.float32,'f8':np.float64,'u8':np.uint64,'u4':np.uint32,'u1':np.uint8,'i4':None}        

    # Extract Data
    # Can be optimsed to read only relavant files if array range is specified
    data=np.zeros(head.dataLength*head.memberLength,type_map[head.dataTypeString])
    for i in range(0,head.fileLength):
        # filename='{:06}'.format(i)
        filename=("{:X}".format(i)).upper().rjust(6,'0')  
        filepath=field.path + os.sep + filename
        with open (filepath, mode='rb') as file:   # b is important -> binary
            fill_start_index = sum(head.dataLengthPerFile[0:i])   * head.memberLength
            fill_end_index   = sum(head.dataLengthPerFile[0:i+1]) * head.memberLength
            data[fill_start_index:fill_end_index]=np.fromfile(file,type_map[head.dataTypeString])

    # Reshape
    if head.memberLength>1:data=data.reshape(head.dataLength,head.memberLength)

    return data




