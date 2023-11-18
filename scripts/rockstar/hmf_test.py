from hmf import MassFunction
import matplotlib.pyplot as plt
import numpy as np
from hmf import cosmology

import sys
sys.path.append("/home/ranitbehera/MyDrive/Repos/MPAnalysis/")
import modules as mp



# Plotting Axis
f,(ac,ae)= plt.subplots(2,1,gridspec_kw={'height_ratios':[3,2]},figsize=(12,10))
plt.subplots_adjust(hspace=0.0)



# - Halo Mass Function
def SimHMF(Mass,LogBinStep,vol=50**3):
    log10_Mass=np.log10(Mass)

    log10_bin_start=np.floor(min(log10_Mass))
    log10_bin_end=np.ceil(max(log10_Mass))

    BinCount=np.zeros(int((log10_bin_end-log10_bin_start)/LogBinStep))

    for lm in log10_Mass:
        i=int((lm-log10_bin_start)/LogBinStep)
        BinCount[i]+=1

    log10_M=np.arange(log10_bin_start,log10_bin_end,LogBinStep)+(LogBinStep/2)
    dn_dlogM=BinCount/(vol*LogBinStep)
    error=np.sqrt(BinCount)/(vol*LogBinStep)

    return log10_M,dn_dlogM,error

# MP-Gadget FoF
op=mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/")
FOFMass=op.PIG(17).FOFGroups.MassByType.ReadValues()*1e10
cdm_mass=FOFMass[:,1]
log10_M,dn_dlogM,error=SimHMF(cdm_mass,0.2,10**3)
fi=4
fe=-4
error=error/2
ac.errorbar(10**log10_M[fi:fe],dn_dlogM[fi:fe],error[fi:fe],fmt='.--',capsize=2,color='k',label="FoF (MP-Gadget)",lw=1)

# Rockstar
rs=np.loadtxt("halos_0.0.ascii")
m_vir=rs[:,2]
log10_M,dn_dlogM,error=SimHMF(m_vir,0.2,10**3)
fi=9
fe=-4
error=error/2
ac.errorbar(10**log10_M[fi:fe],dn_dlogM[fi:fe],error[fi:fe],fmt='.-',capsize=2,color='k',label="ROCKSTAR")

# print(dn_dlogM)

# Fitting Models
def PlotMF(str1,**kwargs):
    # High Res
    mf = MassFunction(z = 0.0,hmf_model=str1,cosmo_params={"Om0":0.2814,"H0":69.7,"Tcmb0":2.7255})
    mf.Mmin=7
    mf.Mmax=12
    h=0.697
    ac.plot(mf.m,mf.dndlog10m*(h**3),**kwargs)
    
    # Low Res for Error
    mf_l=MassFunction(z=0.0,hmf_model=str1,cosmo_params={"Om0":0.2814,"H0":69.7,"Tcmb0":2.7255},dlog10m=0.2)
    mf_l.Mmin=7.1
    mf_l.Mmax=11.9
    
    # diff=mf_l.dndlog10m-dn_dlogM
    fact=mf_l.dndlog10m*(h**3)/dn_dlogM
    fi=9
    fe=-4
    ae.plot(mf_l.m[fi:fe],fact[fi:fe],'.-',**kwargs)

    fact_p=mf_l.dndlog10m*(h**3)/(dn_dlogM-error)
    fact_n=mf_l.dndlog10m*(h**3)/(dn_dlogM+error)

    ae.fill_between(mf_l.m[fi:fe],fact_p[fi:fe],fact_n[fi:fe],alpha=0.2,edgecolor=(0,0,0,0),**kwargs)
  

PlotMF("PS",label="Press-Schechter",color='b')
PlotMF("ST",label="Seith-Tormen",color='g')
PlotMF("Behroozi",label="Behroozi",color='m')

# PlotMF("Angulo",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Bhattacharya",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Courtin",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Crocce",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Ishiyama",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Jenkins",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Manera",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Peacock",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Pillepich",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Reed03",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Reed07",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Warren",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Watson",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Tinker08",alpha=0.5,lw=0.5,ls='--')
# PlotMF("Tinker10",alpha=0.5,lw=0.5,ls='--')





# Final Plot
ac.set_xscale('log')
ac.set_yscale('log')
ac.set_xlim([2e8,5e+11])
ac.set_ylim([1e-5,1e1])
ac.grid(alpha=0.5)
ac.legend()
# ac.set_xticks([])
ac.set_ylabel("$dn/dlog_{10}(M/M_\odot)$",fontsize=12)

ae.set_xscale('log')
ae.set_yscale('log')
ae.set_xlim([2e8,5e+11])
ae.set_ylim([0.4,2.5])
ae.grid(alpha=0.5)
ae.yaxis.tick_right()
ae.set_xlabel("Mass $log_{10}(M/M_\odot)$",fontsize=12)
ae.set_ylabel("Deviation By Factor\nRelative to ROCKSTAR",fontsize=12)
ae.axhline(1,color='k',ls='-',lw=1)

tick_ref = [0.4,0.5,0.6,0.7,0.8,0.9,1,2,]
tick_lable = ['','$\\times$ 0.5','','','','','$\\times$ 1','$\\times$ 2']

ae.set_yticks([])
ae.set_yticks(tick_ref)
ae.set_yticklabels(tick_lable, minor=False)

ac.set_title("Dark Matter Halo Mass Function Comparision (z=0)")
# plt.tight_layout()
# plt.show()
plt.savefig("Halo_Mass_Function.png",dpi=200)
plt.savefig("Halo_Mass_Function.svg")

