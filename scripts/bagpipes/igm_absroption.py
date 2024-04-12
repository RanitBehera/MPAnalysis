import numpy
import matplotlib.pyplot as plt
from bagpipes.models.making.igm_inoue2014 import get_Inoue14_trans


wv = numpy.arange(10,1500,0.1)
fact = get_Inoue14_trans(wv,8)
plt.figure(figsize=(14,6))
plt.plot(wv,fact,lw=2)


# Y Reference
# plt.axhline(1,c='k',ls='--',lw=1)

# X Reference
def GetWavelength(nl,nh,Z=1):
    RH=1.09677e7
    k=(Z**2)*RH*((1/(nl**2))-(1/(nh**2)))
    return (1/k)/1e-10 # Returns wavelength in angstrom

def AnnotateLine(nl,nh,text=""):
    if text=="": text= f"${nl}\\longrightarrow{nh}$"
    line=GetWavelength(nl,nh)
    plt.axvline(line,c='k',ls='--',lw=1,alpha=0.3)
    texty = 10**(numpy.log10(min(fact))+0.1*(numpy.log10(max(fact))-numpy.log10(min(fact))))
    plt.annotate(text,
                 xy=(line,texty),xycoords="data",
                 xytext=(0,0),textcoords="offset pixels",
                 fontsize=12,rotation=90,
                 ha='center',backgroundcolor='white')
    return line
    
l12=AnnotateLine(1,2,"Ly - $\\alpha$")
l13=AnnotateLine(1,3,"Ly - $\\beta$")
# l1inf=AnnotateLine(1,1000,"$1\\longrightarrow\infty$")
l1inf=AnnotateLine(1,1000,"Ly - Limit")

# Lyman Series
# plt.fill_between([l1inf,l12],numpy.ones(2)*plt.ylim()[0],numpy.ones(2)*plt.ylim()[1],color='k',alpha=0.1)
# Supressed Area
plt.fill_between(wv,1,fact,color='r',alpha=0.05)

plt.title("IGM attenuation model - Inoue et al. (2014)",fontsize=20)
plt.yscale('log')
plt.xlabel("$\\mathrm{Rest\\ Frame\\ Wavelength\\ (\\AA)}$",fontsize=12)
plt.ylabel("Transmission",fontsize=12)
plt.xlim(min(wv),max(wv))
plt.ylim(top=1.5)


# plt.show()
plt.savefig("temp/plots/igm_trans.png",dpi=300)
