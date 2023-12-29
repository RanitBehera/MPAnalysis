import numpy,os
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# --- Config
outdir = "/mnt/home/student/cranit/Work/PID_SFR_Track/Result"
z = 8

# -Derived Config
filename = "zsfr_z" + str(z) + ".txt"
filepath = outdir + os.sep +filename

# --- Access data
data=numpy.loadtxt(filepath)
ehid=numpy.int64(data[:,0])
tnump=numpy.int64(data[:,1])
mt_gas= 0.000614086
mu=10**10
# mgas=tnump*mt_gas*mu
# log10_mgas=numpy.log10(mgas)
zsfr=data[:,2:]

# ---- Access Meta Data
z=numpy.zeros(len(zsfr[0]))
with open(filepath) as f:
    line = f.readline()
    z = numpy.int64(line.split(" ")[2:])

# --- PLOT
for i in range(len(zsfr)):
    tag = ("ID " + str(ehid[i])) + " : " + str(tnump[i])
    plt.plot(z,zsfr[i],'.',label=tag,lw=1,ls='-',ms=5)


plt.ylim([10**-2,10**3])
plt.yscale("log")


legtitle = "Number of back-tracked gas particles each having mass $10^{" + str (round(numpy.log10(mt_gas*mu),2)) + "} M_{\odot}$."
leg=plt.legend(title=legtitle,fontsize=6,ncol=5,frameon=False,loc="upper center")
plt.setp(leg.get_title(),fontsize=8)

plt.xlabel("Redshift")
plt.ylabel("$\log_{10}\left(\\frac{SFR}{M_{\odot}yr^{-1}}\\right)$")

plt.xticks(z)
plt.title("SFR vs Redshift",pad=10)

plt.gcf().subplots_adjust(bottom=0.28)
text = "$\\bf{Figure}$ : "
text += "The SFR vs redshift plots for top ten massive halos by virial mass at redshift z=" + str(min(z)) + " are shown. "
text += "The SFR for these halos at higher redshifts are obtained by adding SFRs of back-tracked gas particles found within the halo at lower redshift z=" + str(min(z)) +". "
text += "The IDs (external) of selected halos at redshift z=" + str(min(z)) + " are shown in legend with corresponding number of gas particles back-tracked. "
txt=plt.gcf().text(0.5,0.16,text,fontsize=8,wrap=True,ma="left",ha="center",va="top")
txt._get_wrap_line_width = lambda : 1100

plt.savefig("/mnt/home/student/cranit/Work/PID_SFR_Track/Result/zsfr_test.png",dpi=200)
# plt.savefig("/mnt/home/student/cranit/Work/PID_SFR_Track/Result/zsfr_test.svg")