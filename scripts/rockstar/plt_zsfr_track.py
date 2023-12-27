import numpy,os
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# --- Config
outdir = "/mnt/home/student/cranit/Work/PID_SFR_Track/Result"
z = 8
ehid = 74

# -Derived Config
filename = "zsfr_z" + str(z) + "_ehid" + str(ehid) + ".txt"
filepath = outdir + os.sep +filename

# --- Acessess data
# --- PLOT
# plt.plot(REDSHIFTS,zsfrs)
# plt.savefig("/mnt/home/student/cranit/Work/PID_SFR_Track/Result/zsfr_test.png",dpi=200)
# plt.savefig("/mnt/home/student/cranit/Work/PID_SFR_Track/Result/zsfr_test.svg")