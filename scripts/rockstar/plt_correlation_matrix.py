import os,sys,numpy,seaborn
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
import galspec as mp

# --- CONFIG PARAMETRS
OUTPUTDIR           = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME       = "halos_0.0.ascii"
PARTICLE_FILENAME   = "halos_0.0.particles"
FIELDS              = [mp.ascii.num_p,mp.ascii.mvir,mp.ascii.mbound_vir,mp.ascii.m200b,mp.ascii.m200c,mp.ascii.rvir,mp.ascii.vmax,mp.ascii.rvmax,mp.ascii.vrms]
LABELS              = ["$N_p$","$M_{vir}$","$M_{vir}^{bound}$","$M_{200b}$","$M_{200c}$","$R_{vir}$","$V_{max}$","$V_{rvmax}$","$V_{rms}$"]

# --- DERIVED PARAMETRS
HALO_FILEPATH       = OUTPUTDIR + os.sep + HALO_FILENAME
PARTICLE_FILEPATH   = OUTPUTDIR + os.sep + PARTICLE_FILENAME

# --- DATA BANK
halos       = numpy.loadtxt(HALO_FILEPATH)
particles   = numpy.loadtxt(PARTICLE_FILEPATH)

# --- DIMENSION VALIDATION
field_dat_lenth=[]
for f in FIELDS:
    field_dat_lenth.append(len(halos[:,f]))

uarr=numpy.unique(field_dat_lenth)
if not len(uarr)==1:
    print("[ERROR] Inconsistent Dimensions")
    print("Max Length : " + str(max(uarr)))
    print("Min Length : " + str(min(uarr)))
    exit()

if not len(FIELDS)==len(LABELS):
    print("[ERROR] Inconsistent Length.")
    print("Please add labels for all field.")

# --- CORRELATION
lenr,lenc=len(FIELDS),uarr[0]
matrix=numpy.zeros((lenr,lenc))
for i in range(0,lenr):
    matrix[i,:]=halos[:,FIELDS[i]].transpose()

R=numpy.corrcoef(matrix)

# --- HEAT MAP
ax = seaborn.heatmap(R,
                # vmin=-1,
                # vmax=1,
                annot=True,
                fmt=".2f",
                linewidths=0.5,
                xticklabels=LABELS,
                yticklabels=LABELS,
                )
ax.tick_params(labelsize=12)
ax.axes.set_title("Correlation Matrix",fontsize=16)
# ax.xaxis.tick_top()

plt.show()