import numpy,os
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# --- CONFIG
DIR_PATH = "/mnt/home/student/cranit/Work/PID_SFR_Track/RKSG_L50N640c/"
SNAP=36
FILE_NAME = "halos_PART_" + '{:03}'.format(SNAP)  +  ".0.particles"
FILE_PATH = DIR_PATH + os.sep + FILE_NAME



# --- Read Data
data = numpy.loadtxt(FILE_PATH)
mvir = data[:,0]
ehid = numpy.int64(data[:,8])
sorted_args = numpy.argsort(mvir)[::-1]
sorted_mvir = mvir[sorted_args]
sorted_ehid = ehid[sorted_args]


# --- READ RKS HALO FILE FOR PIDS
sidx=0 # Selection index : 0 - most massive, 1 - next massive
sehid=sorted_ehid[sidx] # Selected EHID
with open(FILE_PATH) as f:
    lines=f.readlines()
    # filter for '#' as frist charcter
    # skip first two rows for meta data
    lines=[l for l in lines if l[0]=="#"][2:]
    # split and extract the ehid
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


# --- SEARCH PIDS
# Acess original box (not rockstar)
import galspec
galspec.CONFIG.MPGADGET_OUTPUT_DIR="/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50Mpc_N640/"
sim = galspec.InitConfig()


def FieldOfHaloinSnap(snap,sgpids):
    # Get all gas particle ids in box
    gpids = sim.PART(snap).Gas.ID()
    # get matched ids
    match_mask =  numpy.isin(gpids,sgpids)
    # Get all gas particle sfr in box
    # gpids = sim.PART(snap).Gas.InternalEnergy()      #<----- Fields of interest
    # gpids = sim.PART(snap).Gas.Metallicity()                #<----- Fields of interest
    # gpids = sim.PART(snap).Gas.Generation()                #<----- Fields of interest
    # i_gpids = gpids[match_mask]
    
    dens = sim.PART(snap).Gas.Density()                #<----- Fields of interest
    temp = sim.PART(snap).Gas.InternalEnergy()                #<----- Fields of interest
    
    # Filter for intrested gas particle sfr with mask
    i_dens = dens[match_mask]
    i_temp = temp[match_mask]
    # print("Length Match Check :",len(i_gpids),len(sgpids))
    
    return i_dens,i_temp


dens,temp = FieldOfHaloinSnap(SNAP,pids)

# ---- Plot histogram for distrbution
# mybins=numpy.logspace(1.5,5.5,50)
# plt.hist(Ifield,bins=100,density=False)
plt.yscale("log")
plt.xscale("log")
# plt.ylim([0,500])
plt.grid(alpha=0.3)

plt.axis("equal")
plt.plot(dens,temp,'.',ms=5)



# --- For Temperature
# plt.xlabel("Temperature (InternalEnergy)")
# plt.ylabel("Bin Weight")
# plt.title("Temperature Distribution ( z = 8, ID : " + str(sehid) + ", $N_{\\text{gas}}$=" + str(len(Ifield))  + " )")

# --- For Metalicity
# plt.xlabel("Metalicity")
# plt.ylabel("Bin Weight")
# plt.title("Metalicity Distribution ( z = 8, ID : " + str(sehid) + ", $N_{\\text{gas}}$=" + str(len(Ifield))  + " )")
# plt.axvline(0.0134,ls='--',color='k')
# plt.text(0.014,1000,"$Z_{\odot}=0.0134$")


plt.savefig("/mnt/home/student/cranit/Work/PID_SFR_Track/Result/test_dist_z8.png",dpi=200)







