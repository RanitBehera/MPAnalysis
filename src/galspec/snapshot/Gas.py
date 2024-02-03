import os
import galspec.snapshot.Field as fld

class _Gas:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "0"
        self.parentpath = parent_dir

        self.DelayTime                   = fld._DelayTime(self.path)
        self.Density                     = fld._Density(self.path)
        self.EgyWtDensity                = fld._EgyWtDensity(self.path)
        self.ElectronAbundance           = fld._ElectronAbundance(self.path)
        self.Generation                  = fld._Generation(self.path)
        self.GroupID                     = fld._GroupID(self.path)
        self.HeIIIIonized                = fld._HeIIIIonized(self.path)
        self.ID                          = fld._ID(self.path)
        self.InternalEnergy              = fld._InternalEnergy(self.path)
        self.Mass                        = fld._Mass(self.path)
        self.Metallicity                 = fld._Metallicity(self.path)
        self.Metals                      = fld._Metals(self.path)
        self.NeutralHydrogenFraction     = fld._NeutralHydrogenFraction(self.path)
        self.Position                    = fld._Position(self.path)
        self.Potential                   = fld._Potential(self.path)
        self.SmoothingLength             = fld._SmoothingLength(self.path)
        self.StarFormationRate           = fld._StarFormationRate(self.path)
        self.Velocity                    = fld._Velocity(self.path)