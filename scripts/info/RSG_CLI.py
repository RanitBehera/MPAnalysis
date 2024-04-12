import numpy, os
import galspec

BOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N1008")


# TERMINAL
def GetPromot():
    PROMT = ""

    # Get Box Last Name
    PROMT += os.path.basename(BOX.path)

    return PROMT + " $ "


while True:
    cmd = input(GetPromot())
    print(cmd)




