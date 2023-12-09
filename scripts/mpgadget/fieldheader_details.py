import galspec.mpgadget as mpg

# --- Config Variables
HEDAER_PATH="/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/PART_017/1/Position/header"
RULE_WIDTH=64
LABEL_WIDTH=24

fh=mpg.FieldHeader(HEDAER_PATH)

print(" Raw Contents ".center(RULE_WIDTH,"-"))

print(fh.contents)


print(" Parsed Contents ".center(RULE_WIDTH,"-"))

print("- Datatype String".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatype.rawString)

print("- Datatype Endianness".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatype.endianness)

print("- Datatype Character".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatype.character)

print("- Datatype Byte Width".ljust(LABEL_WIDTH),": ",end="")
print(fh.datatype.bytewidth)

print("- Number of Members".ljust(LABEL_WIDTH),": ",end="")
print(fh.memberLength)

print("- Number of Files".ljust(LABEL_WIDTH),": ",end="")
print(fh.fileLength)

print("- Data Length per file".ljust(LABEL_WIDTH),": ",end="")
print(fh.dataLengthPerFile)

print("- Total Data length".ljust(LABEL_WIDTH),": ",end="")
print(fh.dataLength)

print("- Checksum of files".ljust(LABEL_WIDTH),": ",end="")
print(fh.checksumOfFiles)