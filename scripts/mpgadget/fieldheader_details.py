import galspec.mpgadget as mpg

# --- Config Variables
HEDAER_PATH="/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/PART_017/1/Position/header"
RULE_WIDTH=64
LABEL_WIDTH=40

fh=mpg.FieldHeader(HEDAER_PATH)

# See contents of header file as text
print(" Raw Contents ".center(RULE_WIDTH,"-"))
print(fh.text)


print(" Parsed Contents ".center(RULE_WIDTH,"-"))

print("Datatype String".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatypeString)

print("Datatype Endianness (Byte Order)".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatypeEndianness,end="")
print("    ('<':LE ; '>':BE ; '=':ME)")

print("Datatype Character".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatypeCharacter)

print("Datatype Byte Width".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatypeByteWidth)

print("Number of Members".ljust(LABEL_WIDTH),": ",end="")
print(fh.memberLength)

print("Number of Files".ljust(LABEL_WIDTH),": ",end="")
print(fh.fileLength)

print("Data Length per file".ljust(LABEL_WIDTH),": ",end="")
print(fh.dataLengthPerFile)

print("Total Data length".ljust(LABEL_WIDTH),": ",end="")
print(fh.dataLength)