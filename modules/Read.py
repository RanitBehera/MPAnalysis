
import numpy as np

# -------------------------------- HEADER
from .Navigate import _Field

class ReadHeader:
    def __init__(self,field:_Field):
        if not isinstance(field,_Field):raise TypeError

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


# ------------------------ SNAPSHOT
from pathlib import Path        # For PART and PIG folder size

class ReadSnapshot:
    def __init__(self,base_dir,snapshot_file="Snapshots.txt"):
        # Always make working base directory field
        self.BaseDirectory=base_dir
        self.Path=base_dir + "\\" + snapshot_file
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
            dir_part=self.BaseDirectory + "\\" + "PART_"+snap_num_fix
            dir_pig=self.BaseDirectory + "\\" + "PIG_"+snap_num_fix
            self.DiscSizePARTs[i] = sum(file.stat().st_size for file in Path(dir_part).rglob('*'))
            self.DiscSizePIGs[i]  = sum(file.stat().st_size for file in Path(dir_pig).rglob('*'))



# --------------------------------- BINARY DATA
from struct import iter_unpack

def ReadField(field:_Field):
    if not isinstance(field,_Field):raise TypeError

    # Extract Header information
    head=ReadHeader(field)
    def ConvertChar(mpchar):
        if mpchar=='f4':return 'f'          # float
        elif mpchar=='f8':return 'd'        # double
        elif mpchar=='u8':return 'Q'        # unsigned long int
        elif mpchar=='u4':return 'I'        # unsigned int
        # elif mpchar=='u1':return 'I'        # 
        # elif mpchar=='i4':return 'I'        # 
    char=ConvertChar(head.dataTypeString)                  # data type character for struct

    # Extract Data
    # Can be optimsed to read only relavant files if array range is specified
    data=np.zeros(head.dataLength*head.memberLength)
        
    for i in range(0,head.fileLength):
        filename='{:06}'.format(i)
        filepath=field.path+"\\"+filename
        with open (filepath, mode='rb') as file:   # b is important -> binary
            fileContent = file.read ()
            # data = unpack ("f", fileContent [0:4])
            filedata=np.array([x[0] for x in iter_unpack (char, fileContent)])
            # fill current file data
            fill_start_index = sum(head.dataLengthPerFile[0:i])   * head.memberLength
            fill_end_index   = sum(head.dataLengthPerFile[0:i+1]) * head.memberLength
            data[fill_start_index:fill_end_index]=filedata
    
    if head.memberLength>1:data=data.reshape(head.dataLength,head.memberLength)

    # Convert to integer if needed
    intlist=['u4','u8']
    if head.dataTypeString in intlist:
        data=np.array([int(d) for d in data])

    return data










