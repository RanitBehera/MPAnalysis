import numpy,os
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# --- CONFIG
DIR_PATH = "/mnt/home/student/cranit/Work/PID_SFR_Track/RKSG_L50N640c/"
REDSHIFTS =  [8,9,10,11,12]


# --- DERIVED CONFIG
RED_TO_SNAP = {"8":"036", "9":"030", "10":"024", "11":"020", "12":"016"}
SNAP_TO_RED = {"036":"8", "030":"9", "024":"10", "020":"11", "016":"12"}
SNAPS = [RED_TO_SNAP[str(z)] for z in REDSHIFTS]
LOWEST_REDSHIFT = min(REDSHIFTS)
HIGHEST_SNAP = RED_TO_SNAP[str(LOWEST_REDSHIFT)]

# --- ROOT HALO
# Access highest snap (lowest redshift)
FILE_NAME = "halos_PART_" + HIGHEST_SNAP + ".0.particles"
FILE_PATH = DIR_PATH + os.sep + FILE_NAME
data = numpy.loadtxt(FILE_PATH)
mvir = data[:,0]
ehid = numpy.int64(data[:,8])
sfr  = data[:,5] 

# Sort halos with descending mass
sorted_args = numpy.argsort(mvir)[::-1]
sorted_mvir = mvir[sorted_args]
sorted_ehid = ehid[sorted_args]

# Get the massive halos
sidx=0   # Selection index : 0 - most massive, 1 - next massive
# print("Array Max Mass".ljust(20),":",max(mvir))
# print("Sorted Array[0]".ljust(20),":",sorted_mvir[0])
# print("Corresponding ID".ljust(20),":",sehid)

def GetZSFR(sidx):
    sehid=sorted_ehid[sidx] # Selected EHID
    # Get PIDs of correspoding ehid
    def GetPIDs(FILE_PATH,sehid):
        with open(FILE_PATH) as f:
            lines=f.readlines()
            # filter for '#' as frist charcter
            # skip first two rows for meta data
            lines=[l for l in lines if l[0]=="#"][2:]
            # split and ectract the ehid
            lines_ehid = [int(l.split(":")[0][1:]) for l in lines]
            # get index of selected ehid
            # can skip if output file is structured so that line N has EHID N info
            # we anyway do the general case
            sehid_match_index = numpy.where(lines_ehid==sehid)[0][0]
            # get the line
            sline = lines[sehid_match_index]
            # clear memory
            del lines
            # extract pids
            pids = numpy.int64((sline.split(":")[1][1:]).split(","))
            return pids
    sgpids = GetPIDs(FILE_PATH,sehid) # Selcted gas particle ids <----------

    # --- SEARCH PIDS
    # Acess original box (not rockstar)
    import galspec
    galspec.CONFIG.MPGADGET_OUTPUT_DIR="/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50Mpc_N640/"
    sim = galspec.InitConfig()

    # Find same pids in all needed snaps
    # Get their sfr and add them

    def TracedSFRinSnap(snap,sgpids):
        # Get all gas particle ids in box
        gpids = sim.PART(snap).Gas.ID()
        # get matched ids
        match_mask =  numpy.isin(gpids,sgpids)
        # Get all gas particle sfr in box
        gpids = sim.PART(snap).Gas.StarFormationRate()
        # Filter for intrested gas particle sfr with mask
        i_gpids = gpids[match_mask]
        # print("Length Match Check :",len(i_gpids),len(sgpids))
        
        return sum(i_gpids)

    # --- CORRECTNESS CHECK
    # - Give lowest snap (root) sgpids and get tracked sfr from same box
    # - Compare that with sfr you get within rokstart potput which should match
    # zsfr=TracedSFRinSnap(int(HIGHEST_SNAP),sgpids)
    # osfr=sfr[sehid]
    # print("SFR from MPGADGET Box".ljust(24),":",zsfr)
    # print("SFR from Rockstar Output".ljust(24),":",osfr)
    # print("Ratio".ljust(24),":",zsfr/osfr)
    # --- VARIFIED AS CORRECT


    zsfrs=numpy.zeros(len(REDSHIFTS))
    length = len(REDSHIFTS)
    for i in range(length):
        snap = int(SNAPS[i])
        print("Tracing BOX :",SNAPS[i],"at redshift",REDSHIFTS[i],":",end="")
        zsfrs[i]=TracedSFRinSnap(snap,sgpids)
        print("DONE (",i+1,"/",length,")")

    return zsfrs,len(sgpids)

sidx = range(10)
sehids = numpy.array(sorted_ehid[sidx]).reshape((len(sidx),1))
ehid_zsfrs = numpy.zeros((len(sidx),len(REDSHIFTS)))
ehid_sgpids = numpy.zeros(len(sidx))

for i in range(len(sidx)):
    ehid_zsfrs[i,:],ehid_sgpids[i]=GetZSFR(sidx[i])

tracked_numps = ehid_sgpids.reshape((len(sidx),1))

# --- SAVE
# path
outdir = "/mnt/home/student/cranit/Work/PID_SFR_Track/Result"
outfilename = "zsfr_z" + str(LOWEST_REDSHIFT) + ".txt"
outpath = outdir + os.sep + outfilename
# meta data
meta = "Z" + "[" + str(len(REDSHIFTS))+ "]"
for z in REDSHIFTS: meta+= " "+ str(z)
meta += "\nEHID TNUMP SFR_ARRAY" + "[" + str(len(REDSHIFTS))+ "]"
# save data
save_data = numpy.hstack((sehids,tracked_numps,ehid_zsfrs))
# column number format
fmt = "%d %d"
for z in REDSHIFTS: fmt+=" %.7f"


numpy.savetxt(outpath,save_data,fmt=fmt,header=meta)




