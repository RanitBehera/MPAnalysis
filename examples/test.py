with open("/home/ranitbehera/MyDrive/Repos/MPAnalysis/examples/test.txt") as f:
    text=f.read()

import numpy as np

lines=text.split("\n")[:-1]

BoxSize=float(lines[0].split("[")[-1].split("]")[0])
BoxSizeUnit="Kilo-parsec"          #<---get thse from paramgadegt file
CMBTemperature=float(lines[1].split("[")[-1].split("]")[0])
CMBTemperatureUnit="Kelvin"

HubbleParam=float(lines[5].split("[")[-1].split("]")[0])
Omega0=float(lines[7].split("[")[-1].split("]")[0])
OmegaBaryon=float(lines[8].split("[")[-1].split("]")[0])
OmegaLambda=float(lines[9].split("[")[-1].split("]")[0])

RSDFactor=float(lines[10].split("[")[-1].split("]")[0])
Time=float(lines[11].split("[")[-1].split("]")[0])
        
UnitLength_in_cm=float(lines[15].split("[")[-1].split("]")[0])
UnitMass_in_g=float(lines[16].split("[")[-1].split("]")[0])
UnitVelocity_in_cm_per_s=float(lines[17].split("[")[-1].split("]")[0])
UsePeculiarVelocity=bool(lines[18].split("[")[-1].split("]")[0])

MassTable=lines[6].split("[")[-1].split("]")[0].split(" ")[1:-1]
MassTable=np.array([float(MassTable[i]) for i in range(len(MassTable))])

MassTable=lines[6].split("[")[-1].split("]")[0].split(" ")[1:-1]
MassTable=np.array([float(MassTable[i]) for i in range(len(MassTable))])

TotNumPart=lines[13].split("[")[-1].split("]")[0].split(" ")[1:-1]
TotNumPart=np.array([int(TotNumPart[i]) for i in range(len(TotNumPart))])

TotNumPartInit=lines[14].split("[")[-1].split("]")[0].split(" ")[1:-1]
TotNumPartInit=np.array([int(TotNumPartInit[i]) for i in range(len(TotNumPartInit))])

print(TotNumPartInit)