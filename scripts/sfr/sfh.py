import numpy,os
import matplotlib.pyplot as plt
import astropy


from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roboto']})
rc('text', usetex=True)


SAVED_PATH = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank"

# Get table
lbage_in_Myr=[]
sfr = []
N_sample = 100
for offset in range(N_sample):
    clbage,csfr = numpy.loadtxt(os.path.join(SAVED_PATH,"off_"+str(offset)+".txt")).T
    clbage /= 1e6

    lbage_in_Myr = clbage
    sfr.append(list(csfr))

sfr=numpy.array(sfr)
sfr = numpy.log10(sfr+1e-10)


# # -----
# # Gaussian Check
# plt.hist(sfr[:,-1],bins=10)
# plt.show()
# exit()
# # -----

# Get stats
sfh_mean    = []
sfh_var     = []
sfh_max     = []
sfh_min     = []

quant_values = [0.5-0.997/2,0.5-0.95/2,0.5-0.68/2,0.5,0.5+0.68/2,0.5+0.95/2,0.5+0.997/2]
sfh_quantile = numpy.empty((7,21))
# print(numpy.shape(sfr))
# exit()

for i in range(numpy.shape(sfr)[1]):
    sfh_mean.append(numpy.mean(sfr[:,i]))
    sfh_var.append(numpy.var(sfr[:,i]))
    sfh_max.append(numpy.max(sfr[:,i]))
    sfh_min.append(numpy.min(sfr[:,i]))

    sfh_quantile [:,i] = numpy.quantile(sfr[:,i],quant_values)

sfh_mean = numpy.array(sfh_mean)
sfh_var = numpy.array(sfh_var)
sfh_max = numpy.array(sfh_max)
sfh_min = numpy.array(sfh_min)


# --- PLOT
fig,ax=plt.subplots(1,1,figsize=(8,6))

# for i in range(len(sfr)):
    # plt.plot(lbage_in_Myr,sfr[i,:],color='k',alpha=0.05)


ax.plot(lbage_in_Myr,sfh_mean,'-',color='b',alpha=1)

ax.plot(lbage_in_Myr,sfh_max,'--',color='k',alpha=0.5,lw=1)
ax.plot(lbage_in_Myr,sfh_min,'--',color='k',alpha=0.5,lw=1)
# ax.fill_between(lbage_in_Myr,(sfh_max),(sfh_min),color='k',ec=None,alpha=0.05)

# for s in [1,2,3]:
    # ax.fill_between(lbage_in_Myr,(sfh_mean+s*sfh_var),(sfh_mean-s*sfh_var),color='b',ec=None,alpha=0.20-s*0.05)

# Quantile
Q_Alpha_map = {0:0.1,1:0.2,2:0.3,3:0.3,4:0.2,5:0.1}
ax.plot(lbage_in_Myr,sfh_quantile[3],'.-',color="r")
for i in range(len(sfh_quantile)-1):
    ax.fill_between(lbage_in_Myr,sfh_quantile[i],sfh_quantile[i+1],color='r',alpha=Q_Alpha_map[i],ec=None)


ax.set_xlabel("Lookback Age (Myr)",fontsize=20)
ax.set_ylabel("$\log($SFR$/M_\odot $yr$^{-1})$",fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=16)
ax.tick_params(axis='both', which='minor', labelsize=12)

ax.invert_xaxis()
# ax.axvline(0,ls='--',color='k')
ax.margins(x=0)

# --------- linked redshift
ax2 = ax.twiny()

new_tick_locations = numpy.array(lbage_in_Myr[[0,4,8,14,20]])


scale = [0.0769231,0.0789216,0.0809721,0.0830759,0.0833333,0.0852343,0.0874488,0.0897208,0.0909091,0.0920519,0.0944435,0.0952381,0.0968973,0.0994148,0.1,0.101998,0.104648,0.105263,0.107367,0.110156,0.111111]
scale = numpy.array(scale)
z=(1/scale)-1
z=numpy.round(z,2)

def tick_function(age):
    zarr=[]
    for a in age:
        ind = numpy.where(a==lbage_in_Myr)
        zarr.append(list(z[ind])[0])
    return zarr

ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(tick_function(new_tick_locations))
ax2.invert_xaxis()
ax2.set_xlabel("Redshift",fontsize=16)
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.tick_params(axis='both', which='minor', labelsize=8)
# --------- linked redshift


plt.grid(alpha=0.3)
plt.annotate("L50N640",(1,0),(-10,10),'axes fraction','offset pixels',ha="right",va="bottom",fontsize=16)
plt.annotate("$N_{\\textnormal{sample}}={"+str(N_sample)+"}$",(0,1),(10,-10),'axes fraction','offset pixels',ha="left",va="top",fontsize=12)

# --- SAVE
plt.show()
# plt.savefig(SAVE_PATH,dpi=200)