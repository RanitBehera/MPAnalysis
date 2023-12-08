import sys, os, numpy
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
import galspec as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2/"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLE_FILENAME       = "halos_0.0.particles"
EHID                    = 2088
EXCLUDE_SUBSTRUCTURES   = True

# --- DERIVED PARAMETRS
HFILEPATH               = OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH               = OUTPUTDIR + os.sep + PARTICLE_FILENAME
op                      = mp.BaseDirectory("/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64/")
MASSTABLE               = op.PART(17).ReadAttribute().MassTable

# --- DATA BANK
halos                   = numpy.loadtxt(HFILEPATH)
particles               = numpy.loadtxt(PFILEPATH)


# if EXCLUDE_SUBSTRUCTURES:print("(Excluding Substructures)")
# else: print("(Including Substructures)")
print("External Halo ID".ljust(20)," : ",str(EHID),"\n")
print("Virial Mass".ljust(20)," : ",halos[EHID,mp.ascii.mvir]/1e10)
print("Bound Mass".ljust(20)," : ",halos[EHID,mp.ascii.mbound_vir]/1e10)
print("M200b Mass".ljust(20)," : ",halos[EHID,mp.ascii.m200b]/1e10)
print("M200c Mass".ljust(20)," : ",halos[EHID,mp.ascii.m200c]/1e10,"\n")
print("Virial Radius".ljust(20)," : ",numpy.round(halos[EHID,mp.ascii.rvir],2),"kpc\n")

print("--------------------------------------------------------------------------------")

# Filter particles
ehid_mask=(particles[:,mp.particles.external_haloid]==EHID)
root_mask=(particles[:,mp.particles.internal_haloid]==particles[:,mp.particles.assigned_internal_haloid])
ehid_mask=ehid_mask & root_mask


ehid_parts_id=particles[ehid_mask,mp.particles.particle_id]

# These two lines make it unique
uni,uindex=numpy.unique(ehid_parts_id,return_index=True)

# Check output of double unique fro single length of 1 to confirm
# ids=ehid_parts_id[uindex]
# uid,ucounts=numpy.unique(ids,return_counts=True)
# uucounts=numpy.unique(ucounts)
# print(uucounts)

# This select only dark matter
type0_mask=(particles[ehid_mask,mp.particles.type][uindex]==0)

# Get Halo velocity
h_vx=halos[EHID,mp.ascii.vx]
h_vy=halos[EHID,mp.ascii.vy]
h_vz=halos[EHID,mp.ascii.vz]

# print(h_vx,h_vy,h_vz)

vx=particles[ehid_mask,mp.particles.vx][uindex][type0_mask]-h_vx
vy=particles[ehid_mask,mp.particles.vy][uindex][type0_mask]-h_vy
vz=particles[ehid_mask,mp.particles.vz][uindex][type0_mask]-h_vz


# plt.hist(vx,histtype="step",label="abs-x")
# plt.hist(vy,histtype="step",label="abs-y")
# plt.hist(vz,histtype="step",label="abs-z")

# plt.hist(vx-h_vx,histtype="step",label="rel-x")
# plt.hist(vy-h_vy,histtype="step",label="rel-y")
# plt.hist(vz-h_vz,histtype="step",label="rel-z")

avg_vx_sq=numpy.average(numpy.square(vx))
avg_vy_sq=numpy.average(numpy.square(vy))
avg_vz_sq=numpy.average(numpy.square(vz))

# print(avg_vx_sq,avg_vy_sq,avg_vz_sq)

sigma=((1/3)*(avg_vx_sq+avg_vy_sq+avg_vz_sq))**0.5  #km/s

print("sigma=",sigma,"Km/sec")

cfg=mp.ConfigFile(OUTPUTDIR)
SCALE_NOW       = float(cfg.SCALE_NOW)
OMEGA_M         = float(cfg.Om)
OMEGA_LAM       = float(cfg.Ol)
HUBBLE_H        = float(cfg.h0)
W0              = float(cfg.W0)
WA              = float(cfg.WA)

Ol=OMEGA_LAM
Om=OMEGA_M
h=HUBBLE_H
a=SCALE_NOW
z=(1/a)-1
M_PI=numpy.pi


def weff(a): 
    if(not a == 1.0):
        return W0 + WA - WA*(a - 1.0)/numpy.log(a)
    else:
        return W0
  
def hubble_scaling(z):
    z1 = 1.0+z
    a = 1.0/z1
    return numpy.sqrt(Om * (z1*z1*z1) + Ol*numpy.power(a, -3.0*(1.0 + weff(a))))

def vir_density(a):
    x = (Om/(a**3))/(hubble_scaling(1.0/a-1.0)**2.0) - 1.0
    return ((18*M_PI*M_PI + 82.0*x - 39*x*x)/(1.0+x))



Delta_c=vir_density(a)

r_vir=((2/numpy.sqrt(Delta_c))/hubble_scaling(z))*sigma   #in Mpc
print("rvir",r_vir*1000)


# m_vir=((4/numpy.sqrt(Delta_c))/(G*H_z))*((1000*sigma)**3)

m_in_Mpc=3.086e22
m_sun=1.989e30
sigma_si=sigma*1000
r_vir_si=r_vir*m_in_Mpc
G_si=6.67430e-11

mass_si=(2*r_vir_si/G_si)*(sigma_si**2) #in kg

m_vir=mass_si/m_sun         # in solar mass

print("mvir",m_vir/1e10)



# plt.legend()
# plt.show()