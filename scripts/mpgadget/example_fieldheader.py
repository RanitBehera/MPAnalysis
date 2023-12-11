import galspec.mpgadget as mpg

# --- Config Variables
HEDAER_PATH = "/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/PART_017/1/Position/header"
RULE_WIDTH              = 100
LABEL_WIDTH             = 32
PRINT_RAW_CONTENTS      = True
PRINT_PARSED_CONTENTS   = True

# --- Create Object
fh=mpg.FieldHeader(HEDAER_PATH)

# --- Present
if PRINT_RAW_CONTENTS:
    print(" Raw Contents ".center(RULE_WIDTH,"-"))
    print(fh)
    #print(fh.contents)

if PRINT_PARSED_CONTENTS:
    print(" Parsed Contents ".center(RULE_WIDTH,"-"))

    table=[ ["Header Path",fh.path],
            ["Datatype String",fh.dtype],
            ["Datatype Endianness",fh.dtype.endianness],
            ["Datatype Character",fh.dtype.character],
            ["Datatype Byte Width",fh.dtype.byte_width],
            ["Datatype Char Width String",fh.dtype._char_width_string],
            ["Number of Members",fh.nmemb],
            ["Number of Files",fh.nfile],
            ["File Names",fh.filenames],
            ["Data Length per File",fh.datalength_per_file],
            ["Total Data length",fh.total_data_length],
            ["Sysv Checksum of Files",fh.checksum_of_files] ]

    for row in table:print(f"* {row[0]:<{LABEL_WIDTH}} : {row[1]}")


print()