import numpy
from colossus.cosmology import cosmology
from colossus.lss import mass_function




# ===============================================
# --- BACK END
# ===============================================

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


#https://bdiemer.bitbucket.io/colossus/lss_mass_function.html
def _mass_function_litreture(sim_cosmology, model_name, redshift,mass_range,q_out):
    cosmology.setCosmology("my_cosmo",sim_cosmology)
    mass_func = mass_function.massFunction(mass_range, redshift, mdef = "fof", model = model_name, q_out = 'dndlnM')
    return mass_range,mass_func




# ===============================================
# --- FRONT END
# ===============================================
from typing import Literal

def MassFunction(self,
                 mass_list,
                 box_size,
                 LogBinStep=0.5):
    
    volume = (box_size/1000)**3
    log_M, dn_dlogM,error = _mass_function_from_mass_list(mass_list,volume,LogBinStep)
    M = numpy.exp(log_M)
    return M,dn_dlogM


# -----------------------------------------------
user_to_colossus_model_name_map =  { 
                "Press-Schechter" : "press74",
                "Seith-Tormen"    : "sheth99",
            }
user_to_colossus_qout_map =  { 
                "dn/dlnM" : "dndlnM",
                "(M2/rho0)*(dn/dm)"    : "M2dndM",
            }
def MassFunctionLitreture(self,
                        model_name : Literal["Press-Schechter","Seith-Tormen"],
                        cosmology,
                        redshift,
                        mass_range,
                        output : Literal["dn/dlnM","(M2/rho0)*(dn/dm)"]
                        ):
    model = user_to_colossus_model_name_map[model_name]
    q_out = user_to_colossus_qout_map[output]
    return _mass_function_litreture(cosmology, model,redshift,mass_range,q_out)