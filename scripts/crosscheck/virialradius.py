import galspec
import numpy
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import savgol_filter

BOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
SNAP = BOX.RSG(36)


# --- Cosmology
h   = 1
Om, Ol  = 0.2814, 0.7186


def H(z):
    H0  = (100*h)
    Ok  = (1-(Om+Ol))
    Hz  = H0 * (( (Om*(1+z)**3) + Ol + (Ok*(1+z)**2)))**(1/2)
    return Hz

# Mean universal matter density
rho_crit = 2.7754e11 * h**2 # M_solar / Mpc**3
rho_m = rho_crit * Om

# Overdensity of all halos
rvir = SNAP.RKSGroups.VirialRadius()/1000 # Kpc to Mpc
mvir = SNAP.RKSGroups.VirialMass()
mv_sort = numpy.argsort(mvir)[::-1]
halo_density = mvir / ((4/3)*numpy.pi*rvir**3)
halo_density = halo_density[mv_sort]
Delta_halo = halo_density/rho_m

# print(Delta_halo)
# plt.hist(Delta_halo,bins=100)
# plt.yscale("log")
# plt.show()



# ----- do it for one
offset=0
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
fig = plt.figure(figsize=(12,8))
gs = GridSpec(5,2,hspace=0.1)

ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[1,0],sharex=ax1)
ax3 = fig.add_subplot(gs[2,0],sharex=ax1)
ax4 = fig.add_subplot(gs[3,0],sharex=ax1)
ax5 = fig.add_subplot(gs[4,0],sharex=ax1)
for ax in [ax1,ax2,ax3,ax4]:
    ax.get_xaxis().set_visible(False)

ax6 = fig.add_subplot(gs[:,1])


# --- Shell particle count
Rdm,Ndm=GetHistogram(SNAP.DarkMatter)
Rgas,Ngas=GetHistogram(SNAP.Gas)

ax1.plot(Rdm,Ndm/200,c='m',label="DM")
ax1.plot(Rgas,Ngas/200,c='orange',label="Gas")
ax1.set_ylabel("Shell Count\n($\\times 200$)")


# --- Cumulative shell particle count
CNdm = numpy.cumsum(Ndm) 
CNgas = numpy.cumsum(Ngas)  

ax2.plot(Rdm,CNdm/2000,label="DM",c='m')
ax2.plot(Rgas,CNgas/2000,label="Gas",c='orange')
ax2.set_ylabel("Cumulative \nShell Count\n($\\times 2000$)")


# --- Cumulative Matter Mass (Contribution + Total)
CMdm  = CNdm * 0.00311013 * 1e10
CMgas = CNgas * 0.000614086 * 1e10
CM = ( CMdm+ CMgas )

ax3.plot(Rdm,CMdm/1e10,label="DM",c='m')
ax3.plot(Rgas,CMgas/1e10,c='orange',label="Gas")
ax3.plot(Rdm,CM/1e10,label="DM + Gas",c='g')
ax3.set_ylabel("Cumulative \nMass\n($\\times10^{11}M_{\odot}$)")
ax3.legend(loc="upper center",ncol=3,bbox_to_anchor=(0.5,3.6))


# --- Mean Density
den = CM / ((4/3)*numpy.pi*Rdm**3)
ax4.plot(Rdm,den,c="g")
ax4.set_yscale('log')
ax4.set_ylabel("Cumulative\nDensity\n($M_{\odot}/\\text{Mpc}^3$)")
ax4.axhline(rho_m,ls='--',c='k',lw=1)
ax4.annotate("$\\rho_m=\Omega_M\\rho_{\\text{crit},0}$",(ax4.get_xlim()[0],rho_m),va="bottom",textcoords="offset pixels",xytext=(5,5))


# --- Overdensity
delta_c = den/rho_m

# ax[1].plot(Rdm,delta_c,label="den")
# ax[1].set_yscale('log')ax4.axhline(rho_crit)


# ax[1].axvline(trvir)
# ax[1].axhline(178)




# PlotHistogram(SNAP.Star,label="star")

# x,y=PlotHistogram(SNAP.BlackHole,plot=False)
# mask=(x!=0)
# [plt.axvline(yi,color='k') for yi in y[mask]]





plt.show()





# print("rvir (cal) : ",rv,"kpc")






