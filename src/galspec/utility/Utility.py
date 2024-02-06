from typing import Literal
from .MassFunction import _mass_function_litreture



user_to_colossus_model_name_map =  { 
                "Press-Schechter" : "press74",
                "Seith-Tormen"    : "sheth99",
            }

user_to_colossus_qout_map =  { 
                "dn/dlnM" : "dndlnM",
                "(M2/rho0)*(dn/dm)"    : "M2dndM",
            }

# Separate Utility for RSG. etc rewire accordingly.
class _Utility:
    def __init__(self) -> None:
        pass

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