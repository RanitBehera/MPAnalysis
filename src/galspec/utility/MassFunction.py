import numpy
from colossus.cosmology import cosmology
from colossus.lss import mass_function
from typing import Literal

# Get ready-to-plot mass function data from list of mass
def _mass_function_from_mass_list(Mass,VOLUME,LogBinStep):
    # log10_Mass=numpy.log10(Mass)
    log_Mass=numpy.log(Mass)

    log_bin_start=numpy.floor(min(log_Mass))
    log_bin_end=numpy.ceil(max(log_Mass))

    BinCount=numpy.zeros(int((log_bin_end-log_bin_start)/LogBinStep))

    for lm in log_Mass:
        i=int((lm-log_bin_start)/LogBinStep)
        BinCount[i]+=1

    log_M=numpy.arange(log_bin_start,log_bin_end,LogBinStep)+(LogBinStep/2)
    dn_dlogM=BinCount/(VOLUME*LogBinStep)
    error=numpy.sqrt(BinCount)/(VOLUME*LogBinStep)

    return log_M,dn_dlogM,error



# Get ready-to-plot mass function of litrature mass functions
#https://bdiemer.bitbucket.io/colossus/lss_mass_function.html

def _mass_function_litreture(sim_cosmology, model_name, redshift,mass_range,q_out):
    cosmology.setCosmology("my_cosmo",sim_cosmology)
    mass_func = mass_function.massFunction(mass_range, redshift, mdef = "fof", model = model_name, q_out = 'dndlnM')
    return mass_range,mass_func




# --- Frontend
