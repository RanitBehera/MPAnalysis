import galspec
import numpy
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

BOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
SNAP = BOX.RSG(36)

offset=0

# --- Cosmology
h   = 1
Om, Ol  = 0.2814, 0.7186

# Mean universal matter density
rho_crit = 2.7754e11 * h**2 # M_solar / Mpc**3
rho_m = rho_crit * Om

# Overdensity of all halos
rvir = SNAP.RKSGroups.VirialRadius()/1000 # Kpc to Mpc
mvir = SNAP.RKSGroups.VirialMass()
mv_sort = numpy.argsort(mvir)[::-1]

# ----- do it for one
tihid = SNAP.RKSGroups.InternalHaloID()[mv_sort][offset]
tpos = SNAP.RKSGroups.Position()[mv_sort][offset]
trvir = rvir[mv_sort][offset] 

def GetDistance(p_pos,p_ihids):
    p_mask = (p_ihids==tihid)
    p_pos = p_pos[p_mask]
    rel_p_pos = p_pos - tpos
    return numpy.linalg.norm(rel_p_pos,axis=1)

def GetHistogram(PTYPE):
    particle_distance   = GetDistance(PTYPE.Position(),PTYPE.InternalHaloID())
    bincount,binloc     = numpy.histogram(particle_distance,bins=numpy.linspace(0,3*trvir,100))
    binloc = binloc[:-1]+(binloc[1]-binloc[0])/2
    return binloc,bincount

# Prepare plot axes
fig = plt.figure(figsize=(7,8))
fig.subplots_adjust(left=0.15,right=0.95)


gs = GridSpec(5,1,hspace=0.1)

ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[1,0],sharex=ax1)
ax3 = fig.add_subplot(gs[2,0],sharex=ax1)
ax4 = fig.add_subplot(gs[3,0],sharex=ax1)
ax5 = fig.add_subplot(gs[4,0],sharex=ax1)
for ax in [ax1,ax2,ax3,ax4]:
    ax.get_xaxis().set_visible(False)
for ax in [ax1,ax2,ax3,ax4,ax5]:
    ax.spines[['right', 'top']].set_visible(False)

# ax6 = fig.add_subplot(gs[:,1])


# --- Shell particle count
Rdm,Ndm=GetHistogram(SNAP.DarkMatter)
Rgas,Ngas=GetHistogram(SNAP.Gas)

ax1.plot(Rdm,Ndm,c='m',label="DM")
ax1.plot(Rgas,Ngas,c='orange',label="Gas")
ax1.set_ylabel("Shell Count",fontsize=10)


# --- Cumulative shell particle count
CNdm = numpy.cumsum(Ndm) 
CNgas = numpy.cumsum(Ngas)  

ax2.plot(Rdm,CNdm,label="DM",c='m')
ax2.plot(Rgas,CNgas,label="Gas",c='orange')
ax2.set_ylabel("Cumulative \nShell Count",fontsize=10)


# --- Cumulative Matter Mass (Contribution + Total)
CMdm  = CNdm * 0.00311013 * 1e10
CMgas = CNgas * 0.000614086 * 1e10
CM = ( CMdm + CMgas )

ax3.plot(Rdm,CMdm/1e10,label="DM",c='m')
ax3.plot(Rgas,CMgas/1e10,c='orange',label="Gas")
ax3.plot(Rdm,CM/1e10,label="DM + Gas",c='g')
ax3.set_ylabel("Cumulative \nTotal Mass\n($\\times10^{11}M_{\odot}$)",fontsize=10)
ax3.legend(loc="upper center",ncol=3,bbox_to_anchor=(0.5,3.6),frameon=False)


# --- Mean Density
den = CM / ((4/3)*numpy.pi*Rdm**3)

ax4.plot(Rdm,den,c="g")
ax4.set_yscale('log')
ax4.set_ylabel("Cumulative\nDensity\n($M_{\odot}/\\text{Mpc}^3$)",fontsize=10)
ax4.axhline(rho_m,ls='--',c='k',lw=1)
ax4.annotate("Mean Universal\nMatter Density\n$\\rho_m=\Omega_M\\rho_{\\text{crit},0}$",
             (ax4.get_xlim()[0],rho_m),va="bottom",textcoords="offset pixels",fontsize=8,xytext=(5,5))


# --- Overdensity
Delta_c = den/rho_m
Delta_vir=178

ax5.plot(Rdm,Delta_c,c='g')
ax5.set_yscale("log")
ax5.set_ylabel("\nOver Density\n$\Delta(R)$",fontsize=10)
ax5.axhline(Delta_vir,ls='--',c='k',lw=1)
ax5.annotate("$\Delta_{\\text{vir}}=$"+str(numpy.round(Delta_vir,2)),
             (ax5.get_xlim()[0],Delta_vir),va="top",textcoords="offset pixels",fontsize=8,xytext=(5,-5))
ax5.axvline(trvir,ls='-',c='k',lw=1)
ax5.annotate("ROCKSTAR\n$R_{\\text{vir}}=$"+str(numpy.round(trvir,2))+" Mpc",
             (trvir,ax5.get_ylim()[1]),va="top",ha="left",textcoords="offset pixels",fontsize=8,xytext=(5,-5))
ax5.set_xlabel("Radius (cMpc)",fontsize=10)


ax1.set_title("Virial Radius",pad=40)
plt.show()







