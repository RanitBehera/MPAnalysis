import os
import galspec.snapshot.Field as fld

class _BlackHole:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "5"
        self.parentpath = parent_dir

        self.BlackholeAccretionRate      = fld._BlackholeAccretionRate(self.path)
        self.BlackholeDensity            = fld._BlackholeDensity(self.path)
        self.BlackholeJumpToMinPot       = fld._BlackholeJumpToMinPot(self.path)
        self.BlackholeKineticFdbkEnergy  = fld._BlackholeKineticFdbkEnergy(self.path)
        self.BlackholeMass               = fld._BlackholeMass(self.path)
        self.BlackholeMinPotPos          = fld._BlackholeMinPotPos(self.path)
        self.BlackholeMseed              = fld._BlackholeMseed(self.path)
        self.BlackholeMtrack             = fld._BlackholeMtrack(self.path)
        self.BlackholeProgenitors        = fld._BlackholeProgenitors(self.path)
        self.BlackholeSwallowID          = fld._BlackholeSwallowID(self.path)
        self.BlackholeSwallowTime        = fld._BlackholeSwallowTime(self.path)
        self.Generation                  = fld._Generation(self.path)
        self.GroupID                     = fld._GroupID(self.path)
        self.ID                          = fld._ID(self.path)
        self.Mass                        = fld._Mass(self.path)
        self.Position                    = fld._Position(self.path)
        self.Potential                   = fld._Potential(self.path)
        self.SmoothingLength             = fld._SmoothingLength(self.path)
        self.StarFormationTime           = fld._StarFormationTime(self.path)
        self.Swallowed                   = fld._Swallowed(self.path)
        self.Velocity                    = fld._Velocity(self.path)
