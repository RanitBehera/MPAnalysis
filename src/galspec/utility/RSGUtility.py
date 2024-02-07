
import galspec,numpy
from galspec.utility.MassFunction import _mass_function_from_mass_list
from galspec.navigation.MPGADGET.RSG.RSG import _RSG #Cicular import

class _RSGUtility(_RSG):
    def __init__(self,path) -> None:
        super.__init__(path)

    def MassFunction(self,LogBinStep=0.5):
        mass_list = self.RKSGroups.VirialMass()
        volume = (self.Attribute.BoxSize()/1000)**3
        log_M, dn_dlogM,error = _mass_function_from_mass_list(mass_list,volume,LogBinStep)

        M = numpy.exp(log_M)
        return M,dn_dlogM



