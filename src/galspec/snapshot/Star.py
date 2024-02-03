import os
import galspec.snapshot.Field as fld

class _Star:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "4"
        self.parentpath = parent_dir

        self.BirthDensity                = fld._BirthDensity(self.path)
        self.Generation                  = fld._Generation(self.path)
        self.GroupID                     = fld._GroupID(self.path)
        self.ID                          = fld._ID(self.path)
        self.LastEnrichmentMyr           = fld._LastEnrichmentMyr(self.path)
        self.Mass                        = fld._Mass(self.path)
        self.Metallicity                 = fld._Metallicity(self.path)
        self.Metals                      = fld._Metals(self.path)
        self.Position                    = fld._Position(self.path)
        self.Potential                   = fld._Potential(self.path)
        self.SmoothingLength             = fld._SmoothingLength(self.path)
        self.StarFormationTime           = fld._StarFormationTime(self.path)
        self.TotalMassReturned           = fld._TotalMassReturned(self.path)
        self.Velocity                    = fld._Velocity(self.path)