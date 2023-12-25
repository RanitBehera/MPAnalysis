import os,numpy
import matplotlib.pyplot as plt


# --- Config
DIR = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L50N640c"
SNAP_NUM = 36
CELL_WIDTH=24


# --- Derived Config
FF_SNAP_NUM='{:03}'.format(SNAP_NUM)    # Fixed Format
FILE_NAME = "halos_PART_" + FF_SNAP_NUM + ".0.particles"
SNAP_RED_DICT={"016":"12", "020":"11", "024":"10", "030":"9", "036":"8", "050":"6"}
REDSHIFT = SNAP_RED_DICT[FF_SNAP_NUM]
FILE_PATH = DIR + os.sep + FILE_NAME

# --- Data Access
data = numpy.loadtxt(FILE_PATH)
sfr         =   data[:,5]                       # < ---- sfr column number may change in future
halo_mass   =   data[:,0]

# --- Report
print("")
print(" NON-ZERO SFR CHECK ".center(80,"="))
print("")
print("Particles".rjust(20),"=","640 cube *")
print("Redshift".rjust(20),"=",REDSHIFT)
print("Number of Halos".rjust(20),"=",len(data))
print("")
print("Halo Mass Range (Log10)".center(CELL_WIDTH),"|","In Range Halos (#,%)".center(CELL_WIDTH),"|","# NZ-SFR".center(CELL_WIDTH))
print("".ljust(3*CELL_WIDTH+10,'-'))

def Print_For_Mass_Range(start,end):
    log10_mh = numpy.log10(halo_mass)
    mask_mass = ((log10_mh>=start) & (log10_mh<end))    
    # selected_halo_mass = halo_mass[mask_mass]
    # print(list(numpy.round(numpy.log10(selected_halo_mass),1)))
    selected_sfr    = sfr[mask_mass]        # length same as selected halos within mass range
    halo_fraction   = len(selected_sfr)/len(sfr)
    if not len(selected_sfr)==0:
        selected_nz_sfr = selected_sfr[selected_sfr!=0]
        nz_sfr_fraction = len(selected_nz_sfr)/len(selected_sfr)
    
    print(str(start).rjust(int(CELL_WIDTH/2)-1),"-",str(end).ljust(int(CELL_WIDTH/2)-2),
          "|",
          str(len(selected_sfr)).rjust(int(CELL_WIDTH/2)),
          (": " + str(round((halo_fraction)*100,2)) + "%").ljust(int(CELL_WIDTH/2)-1),
          "|",
          end="")
    
    if len(selected_sfr)==0 : print("-".center(CELL_WIDTH))
    else: print(str(len(selected_nz_sfr)).rjust(int(CELL_WIDTH/2)),
          (": " + str(round((nz_sfr_fraction)*100,2)) + "%").ljust(int(CELL_WIDTH/2)-1),)


for i in range(5,14):
    Print_For_Mass_Range(i,i+1)

print("".ljust(3*CELL_WIDTH+10,'-'))
print("")





