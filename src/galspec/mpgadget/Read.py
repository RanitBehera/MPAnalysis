import numpy

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