import os
import galspec.mpgadget.Field as fld

class _FOFGroups:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "FOFGroups"
        self.parentpath = parent_dir

        self.BlackholeAccretionRate      = fld._BlackholeAccretionRate(self.path)
        self.BlackholeMass               = fld._BlackholeMass(self.path)
        self.FirstPos                    = fld._FirstPos(self.path)
        self.GasMetalElemMass            = fld._GasMetalElemMass(self.path)
        self.GasMetalMass                = fld._GasMetalMass(self.path)
        self.GroupID                     = fld._GroupID(self.path)
        self.Imom                        = fld._Imom(self.path)
        self.Jmom                        = fld._Jmom(self.path)
        self.LengthByType                = fld._LengthByType(self.path)
        self.Mass                        = fld._Mass(self.path)
        self.MassByType                  = fld._MassByType(self.path)
        self.MassCenterPosition          = fld._MassCenterPosition(self.path)
        self.MassCenterVelocity          = fld._MassCenterVelocity(self.path)
        self.MassHeIonized               = fld._MassHeIonized(self.path)
        self.MinID                       = fld._MinID(self.path)
        self.StarFormationRate           = fld._StarFormationRate(self.path)
        self.StellarMetalElemMass        = fld._StellarMetalElemMass(self.path)
        self.StellarMetalMass            = fld._StellarMetalMass(self.path)