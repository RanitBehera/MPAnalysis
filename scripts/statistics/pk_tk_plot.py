import numpy,os
import matplotlib.pyplot as plt


PATH = "/mnt/home/student/cranit/Work/RSGBank/PKTK_L50N640"
PK_PATH = os.path.join(PATH,"class_pk_99.dat")
TK_PATH = os.path.join(PATH,"class_tk_99.dat")


fig = plt.figure(figsize=(14,8))
gs = fig.add_gridspec(5,2,hspace=0.1,wspace=0.05)
ax_pk = fig.add_subplot(gs[:, 0])
ax_dk_p = fig.add_subplot(gs[0, 1])
ax_dk_b = fig.add_subplot(gs[1, 1])
ax_dk_c = fig.add_subplot(gs[2, 1])
ax_dk_u = fig.add_subplot(gs[3, 1])
ax_dk_n = fig.add_subplot(gs[4, 1])



# PK
pkd = numpy.loadtxt(PK_PATH)
ax_pk.plot(pkd[:,0],pkd[:,1])
ax_pk.set_xscale("log")
ax_pk.set_yscale("log")
ax_pk.set_xlabel("$k$ (h/Mpc)",fontsize=16)
ax_pk.set_ylabel("$P(k)$",fontsize=16)
ax_pk.set_title("Power Spectrum",fontsize=16)
ax_pk.grid(alpha=0.3)


# TK
tkd = numpy.loadtxt(TK_PATH)
def Plot(axis,x,y,ylabel,leg):
    axis.plot(x,y,label=leg)
    axis.set_xscale("log")
    axis.get_xaxis().set_visible(False)
    axis.legend(loc="lower left")
    axis.set_ylabel(ylabel,fontsize=16)
    axis.yaxis.set_label_position("right")
    axis.yaxis.tick_right()

Plot(ax_dk_p,tkd[:,0],tkd[:,1],"$\delta_{\gamma}$","Photon")
Plot(ax_dk_b,tkd[:,0],tkd[:,2],"$\delta_{b}$","Baryon")
Plot(ax_dk_c,tkd[:,0],tkd[:,3],"$\delta_{cdm}$","CDM")
Plot(ax_dk_u,tkd[:,0],tkd[:,4],"$\delta_{\\nu}$","UR")
Plot(ax_dk_n,tkd[:,0],tkd[:,3],"$\delta_{ncdm}$","NCDM")

ax_dk_n.get_xaxis().set_visible(True)
ax_dk_n.set_xlabel("$k$ (h/Mpc)",fontsize=16)
ax_dk_p.set_title("Transfer Function",fontsize=16)

plt.suptitle("INITIAL CONDITIONS : CLASS (z=99)",fontsize=20)

plt.savefig("/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/pk_tk.png",dpi=300)
# plt.show()
