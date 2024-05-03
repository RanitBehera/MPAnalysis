import numpy
import matplotlib.pyplot as plt

import seaborn as sns

# offset,stellar_mass,sfr,beta,Luv = numpy.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp/spectra/bagdata.txt").T
offset,stellar_mass,sfr,beta,Luv,Av = numpy.loadtxt("/mnt/home/student/cranit/Repo/MPAnalysis/temp/spectra/bagdata_Av_M_CZ.txt").T


ms=numpy.log10(32*0.000153522*1e10)
mask = (ms<=stellar_mass)
stellar_mass,beta,Av = stellar_mass[mask],beta[mask],Av[mask]


# -------
if True:
    fig = plt.figure(figsize=(6,6))
    sort=numpy.argsort(Av)
    plt.plot(stellar_mass[sort],Av[sort],'.-')
    # plt.yscale("log")
    plt.xlabel("$\log (M_*/M_\odot) $")
    plt.ylabel("$A_V$")
    plt.title("$A_V = 0.01\left[\log\left(\\frac{M_*}{10^6 M_\odot}\\right)\\right]^4$ \n ["
            + str(round(min(Av),2)) + "," + str(round(max(Av),2))  +"]")
# -------


# -------
if True:
    fig = plt.figure(figsize=(6,6))
    sort=numpy.argsort(Av)
    plt.plot(Av[sort],beta[sort],'.-')
    # plt.yscale("log")
    plt.xlabel("$A_V$")
    plt.ylabel("$\\beta$")
    # plt.title("$A_V = 0.01\left[\log\left(\\frac{M_*}{10^6 M_\odot}\\right)\\right]^4$ \n ["
            #   + str(round(min(Av),2)) + "," + str(round(max(Av),2))  +"]")
# -------




# PLOTS
fig = plt.figure(figsize=(6, 6))
gs = fig.add_gridspec(2, 2,  width_ratios=(5, 1), height_ratios=(1, 5),
                      left=0.1, right=0.9, bottom=0.1, top=0.9,
                      wspace=0.0, hspace=0.0)

ax = fig.add_subplot(gs[1, 0])
ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)


for axi in [ax_histx,ax_histy]:
    axi.minorticks_on()
    axi.spines['right'].set_visible(False)
    axi.spines['left'].set_visible(False)
    axi.spines['top'].set_visible(False)
    axi.spines['bottom'].set_visible(False)
    axi.tick_params(axis="both",direction="out",labelsize=12,which="major",width=1,length=8)
    axi.tick_params(axis="both",direction="out",labelsize=12,which="minor",width=0.5,length=4)

ax_histx.spines['bottom'].set_visible(True)
ax_histy.spines['left'].set_visible(True)
ax_histx.axes.get_yaxis().set_visible(False)
ax_histy.axes.get_xaxis().set_visible(False)
ax_histx.spines["bottom"].set(lw=1.5)

ax.minorticks_on()
ax.tick_params(axis="both",direction="in",labelsize=12,which="major",width=1,length=8)
ax.tick_params(axis="both",direction="in",labelsize=12,which="minor",width=0.5,length=4)

for side in ['top', 'bottom', 'left', 'right']:
    ax.spines[side].set(lw=1.5)

ax.set_xticks(range(6,13))
ax.set_yticks([-3,-2,-1,0,1])

plt.setp(ax_histx.get_xticklabels(), visible=False)
plt.setp(ax_histy.get_yticklabels(), visible=False)


ax.plot(stellar_mass,beta,'.',ms=1)
sns.kdeplot(x=stellar_mass,y=beta, fill=True,ax=ax)
sns.kdeplot(x=stellar_mass,ax=ax_histx,fill=True)
sns.kdeplot(y=beta,ax=ax_histy,fill=True)




ax.set_ylim(-4,1)
ax.set_xlim(6,12)

ax.set_xlabel("$\log(M_*/M_\odot)$",fontsize=14)
ax.set_ylabel("UV slope $\\beta$",fontsize=14)

plt.show()