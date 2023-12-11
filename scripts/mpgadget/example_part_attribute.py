import galspec.mpgadget as mpg
from galspec.mpgadget.PARTAttribute import _Attr

# --- Config Variables
ATTR_PATH = "/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/PART_017/Header/attr-v2"
RULE_WIDTH              = 100
TABLE_CELL_WIDTH = TCW  = 28
PRINT_RAW_CONTENTS      = True
PRINT_PARSED_CONTENET   = True

# --- Create Object
attr=mpg.PARTAttribute(ATTR_PATH)

# --- Present
if PRINT_RAW_CONTENTS:
    print(" Raw Contents ".center(RULE_WIDTH,"-"))
    print(attr)
    #print(att.contents)

if PRINT_PARSED_CONTENET:
    print(" Parsed Contents ".center(RULE_WIDTH,"-"))

    table_headers=th=["Name","Datatype","Length","Value"]
    print(f"{th[0]:<{TCW}}"
          f"{th[1]:<{int(TCW/2)}}"
          f"{th[2]:<{int(TCW/2)}}"
          f"{th[3]:<{TCW}}")


    print("".ljust(RULE_WIDTH,"-"))

    def PrintRow(field: _Attr):
        print(f"{field.name:<{TCW}}"
            f"{field.dtype:<{int(TCW/2)}}"
            f"{field.nmemb:<{int(TCW/2)}}"
            f"{str(field.value):<{TCW}}")

    PrintRow(attr.BoxSize)
    PrintRow(attr.CMBTemperatures)
    PrintRow(attr.HubbleParam)
    PrintRow(attr.Omega0)
    PrintRow(attr.OmegaBaryon)
    PrintRow(attr.OmegaLambda)
    PrintRow(attr.DensityKernel)
    PrintRow(attr.MassTable)
    PrintRow(attr.RSDFactor)
    PrintRow(attr.Time)
    PrintRow(attr.TimeIC)
    PrintRow(attr.TotNumPart)
    PrintRow(attr.TotNumPartInit)
    PrintRow(attr.UnitLength_in_cm)
    PrintRow(attr.UnitMass_in_g)
    PrintRow(attr.UnitVelocity_in_cm_per_s)
    PrintRow(attr.UsePeculiarVelocity)
    
    a=attr.BoxSize
    print(a) 
    # Not working due to python OOP.
    # Add __add__ magic methods to support maths 
    # Or return integer using __new__ to boxsize etc