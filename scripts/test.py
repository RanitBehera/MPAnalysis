import numpy, galspec
import matplotlib.pyplot as plt



# --- SIMULATIONS
BOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
LBOX    = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640")
# LBOX    = galspec.NavigationRoot("/scratch/nkhandai/mp-gadget/50Mpc_640cube_alpha400")

if False:
    # --------------------------------
    print("rockstar")
    mass = BOX.RSG(36).Gas.Mass()
    id = BOX.RSG(36).Gas.ID()
    print("len id",len(id))
    print("len mass",len(id))
    # remove duplicates
    # u,i = numpy.unique(id,True)
    # mass=mass[i]
    # id = id[i]
    print("len uniq id",len(numpy.unique(id)))
    print("len uniq mass",len(numpy.unique(mass)))

    # -------------------------
    print("Part")
    lid = LBOX.PART(36).Gas.ID()
    lmass = LBOX.PART(36).Gas.Mass()

    print("len id :",len(lid))
    print("len mass :",len(lmass))
    print("len uniq id",len(numpy.unique(lid)))
    print("len uniq mass",len(numpy.unique(lmass)))

    exit()
    mask = numpy.isin(numpy.int64(lid),numpy.int64(id))
    lmass=lmass[mask]

    print(len(lmass))
    print(len(numpy.unique(lmass)))
if False:
    h=0.697
    BH_Mass = LBOX.PART(50).BlackHole.BlackholeMass()/h
    print(numpy.log10(numpy.max(BH_Mass)*1e10))
    BH_Mass = LBOX.PIG(50).BlackHole.BlackholeMass()/h
    print(numpy.log10(numpy.max(BH_Mass)*1e10))



if True:
    pass