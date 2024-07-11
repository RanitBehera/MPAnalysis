import galspec
import matplotlib.pyplot as plt
import numpy as np


BOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
LBOX = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640")

h=0.697

BOXSIZE = 50/h
VOLUME = BOXSIZE**3

kuv = 1.15e-28 #M0/yr / (erg/s/Hz)

jy = 1e-23 # erg s-1 Hz-1 cm-2


from astropy.cosmology import FlatLambdaCDM

# Set for luminosity distance
HUBBLE = 69.7
OMEGA_M = 0.2814
CMBT = 2.7255
REDSHIFT = 8
lcdm = FlatLambdaCDM(H0=HUBBLE, Om0=OMEGA_M, Tcmb0=CMBT)
DL=lcdm.luminosity_distance(REDSHIFT).value #In Mpc
DL *= 3.086e24   # Mpc to cm
Area = 4*np.pi*(DL**2) #cm**2

cm_in_pc = 3.086e+18
DL_in_pc = DL/cm_in_pc


z_to_snap = {
            # 12:16,
            # 11:20,
            10:24,
            9:30,
            8:36,
            7:42,
            6:50,
            # 5:60,
            # 4:71,
            # 3:83
            }


z=list(z_to_snap.keys())



fig,ax = plt.subplots(1,1)


def Plot(ax,zi):
    print(zi,flush=True)
    snap = z_to_snap[zi]


    halo_sfr = LBOX.PIG(snap).FOFGroups.StarFormationRate()/h    # Mo/yr
    # halo_sfr = BOX.RSG(snap).RKSGroups.StarFormationRate()/h    # Mo/yr
    
    halo_luv = halo_sfr/kuv     # erg s-1 Hz-1
    
    halo_flux_uv = halo_luv/Area    # erg s-1 Hz-1 cm-2

    Q = halo_flux_uv/(jy)

    Q = Q[Q!=0]

    m_AB = -2.5*np.log10(Q)+8.90

    M_AB = m_AB -5*(np.log10(DL_in_pc)-1)



    # Binn function
    Vol = VOLUME
    m_AB = M_AB

    LogBinStep = 1
    LogBinStart = (int(min(m_AB)/LogBinStep)-1)*LogBinStep
    LogBinEnd   = (int(max(m_AB)/LogBinStep)+1)*LogBinStep
    MagBinCount = np.zeros(int((LogBinEnd-LogBinStart)/LogBinStep))

    for M in m_AB:
        i = int((M-LogBinStart)/LogBinStep)
        MagBinCount[i] +=1

    err = np.sqrt(MagBinCount)

    # Normalise
    MagBinCount /= (Vol*LogBinStep)
    err /= (Vol*LogBinStep)

    #  offset to center of bin
    M_UV = np.arange(LogBinStart,LogBinEnd,LogBinStep) + (LogBinStep/2)

    # Filter our zero bin count
    mask = (MagBinCount!=0)
    M_UV = M_UV[mask]
    MagBinCount = MagBinCount[mask]
    err = err[mask]



    ax.plot(M_UV,np.log10(MagBinCount),label="Ninja",color='r')
    # ax.fill_between(M_UV,MagBinCount+(0.8*err/2),MagBinCount-(0.8*err/2),alpha=0.1)
    ax.set_xlim(-24,-16)
    # ax.set_yscale('log')
    ax.invert_xaxis()

    ax.set_xlabel("$M_{UV}$")
    ax.set_ylabel("$\log_{10}(\phi_{UV}/Mpc^3 mag)$")


    if False:
        # Plot Digitised - Astrid fig 3
        # z=8
        x = [-22.875, -22.45, -22.125, -21.875, -21.275, -20.45, -19.55, -18.1, -16.5]
        y = [-6.916666666666667, -6.270833333333333, -5.770833333333334, -5.4375, -4.9375, -4.395833333333334, -3.8958333333333335, -3.166666666666667, -2.4375]
        ax.plot(x,y,label="Astrid",color='b')
        x = [-17.025, -17.6, -18, -18.5, -18.6, -19.025, -19.35, -19.5, -19.9, -20.1, -20.525, -20.85, -21, -21.375, -21.525, -21.675, -21.875, -22.025, -22.55, -23.05, -22.175, -22.925]
        y = [-2.208333333333334, -2.520833333333334, -2.708333333333334, -2.8125, -2.979166666666667, -3.2083333333333335, -3.166666666666667, -3.666666666666667, -3.8125, -3.916666666666667, -4.229166666666667, -4.395833333333334, -4.791666666666667, -4.916666666666667, -5.104166666666667, -5.541666666666667, -5.541666666666667, -5.4375, -5.458333333333334, -5.479166666666667, -6.229166666666667, -6.854166666666667]
        ax.plot(x,y,'.',color='k',ms=5)



    
Plot(ax,6)



# Digitised Plot - Astrid Figure 4


plt.grid(alpha=0.3)
plt.legend()
plt.show()