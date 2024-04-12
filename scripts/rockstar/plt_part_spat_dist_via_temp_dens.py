import numpy,os
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# --- CONFIG
DIR_PATH = "/mnt/home/student/cranit/Work/PID_SFR_Track/RKSG_L50N640c/"
DIR_PATH = r"C:\Users\ranit\OneDrive\My Drive\4 My Collections\Projects\Python - MPAnalysis\TempResults"
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
sidx=1 # Selection index : 0 - most massive, 1 - next massive
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
galspec.CONFIG.MPGADGET_OUTPUT_DIR=r"C:\Users\ranit\OneDrive\My Drive\4 My Collections\Projects\Python - MPAnalysis\TempResults"
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
    pos = sim.PART(snap).Gas.Position()                #<----- Fields of interest
    
    # Filter for intrested gas particle sfr with mask
    i_dens = dens[match_mask]
    i_temp = temp[match_mask]
    i_pos = pos[match_mask]
    # print("Length Match Check :",len(i_gpids),len(sgpids))
    
    return i_dens,i_temp, i_pos

dens,temp,pos = FieldOfHaloinSnap(SNAP,pids)
x=pos[:,0]
y=pos[:,1]
z=pos[:,2]




# --- Logic for color mapping
from matplotlib.colors import LinearSegmentedColormap
def gradient_color(color1, color2, value):
    colors = [color1, color2]
    cm = LinearSegmentedColormap.from_list("Custom", colors, N=20)
    mat = numpy.indices((10,10))[1]
    plt.imshow(mat, cmap=cm)
    plt.show()




    

# ---- Mask ------------------
temp_mask = (temp>150) & (temp<5*10**3) 
den_mask  = (dens>10**-6) & (dens<10**-5)
mask1= temp_mask & den_mask

temp_mask = (temp>5*10**3) & (temp<10**5) 
den_mask  = (dens>10**-6) & (dens<10**-3)
mask2= temp_mask & den_mask


temp_mask = (temp<300)
mask3 = temp_mask
mask=mask3

temp_mask = (temp>10**3)
den_mask  = (dens<10**-6)
mask4= temp_mask & den_mask


mask_a = (temp<200) & (dens>3*10**-6)
mask_b = (temp<400) & (dens<3*10**-6)

mask_com = mask_a | mask_b

mask = mask_a

#------------------------------


mask_inv = ~mask_com

plt.plot(dens[~mask],temp[~mask],'o',ms=5,color=(0.8,0.8,0.8),alpha=1,markeredgecolor='none')
plt.plot(dens[mask_a],temp[mask_a],'o',ms=5,color='m',markeredgecolor='none')
plt.plot(dens[mask_b],temp[mask_b],'o',ms=5,color='c',markeredgecolor='none')
plt.plot(dens[mask_inv],temp[mask_inv],'o',ms=5,color='y',markeredgecolor='none')
plt.yscale("log")
plt.xscale("log")
plt.grid(alpha=0.3)
plt.axis("equal")

# plt.savefig("/mnt/home/student/cranit/Work/PID_SFR_Track/Result/test_spat_dist_z8.png",dpi=200)
plt.savefig(r"C:\Users\ranit\OneDrive\My Drive\4 My Collections\Projects\Python - MPAnalysis\TempResults\Result\test_spat_dist_z8.png",dpi=200)

import sys
sys.path.append(os.getcwd())
import galspecold as mp

win=mp.Open3D.GADGET()
win.DarkMatter(numpy.column_stack((x[mask_a],y[mask_a],z[mask_a])))
win.Gas(numpy.column_stack((x[mask_b],y[mask_b],z[mask_b])))
win.Star(numpy.column_stack((x[mask_inv],y[mask_inv],z[mask_inv])))



win.Run()











