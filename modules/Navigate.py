# from typing import Any
import numpy as np
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.getcwd())
import modules as mp

# ----------------- INTERNAL -----------------

class _Field:
    def __init__(self,parent_dir):
        # Knowling field name is required to take different actions based on field under same name
        self.fieldName  =   self.__class__.__name__.split("_")[-1]     # str
        self.path       = parent_dir + os.sep + self.fieldName
        self.parentpath = parent_dir
        # self.value  = None

    def ReadValues(self):
        return mp.ReadField(self)
    
#---------------------------------------------
class _DelayTime(_Field): pass
class _Density(_Field): pass
class _EgyWtDensity(_Field): pass
class _ElectronAbundance(_Field): pass
class _Generation(_Field): pass
class _GroupID(_Field): pass
class _HeIIIIonized(_Field): pass
class _ID(_Field): pass
class _InternalEnergy(_Field): pass
class _Mass(_Field): pass
class _Metallicity(_Field): pass
class _Metals(_Field): pass
class _NeutralHydrogenFraction(_Field): pass
class _Position(_Field): pass
class _Potential(_Field): pass
class _SmoothingLength(_Field): pass
class _StarFormationRate(_Field): pass
class _Velocity(_Field): pass
class _BirthDensity(_Field): pass
class _LastEnrichmentMyr(_Field): pass
class _StarFormationTime(_Field): pass
class _TotalMassReturned(_Field): pass
class _BlackholeAccretionRate(_Field): pass
class _BlackholeDensity(_Field): pass
class _BlackholeJumpToMinPot(_Field): pass
class _BlackholeKineticFdbkEnergy(_Field): pass
class _BlackholeMass(_Field): pass
class _BlackholeMinPotPos(_Field): pass
class _BlackholeMseed(_Field): pass
class _BlackholeMtrack(_Field): pass
class _BlackholeProgenitors(_Field): pass
class _BlackholeSwallowID(_Field): pass
class _BlackholeSwallowTime(_Field): pass
class _Swallowed(_Field): pass
class _FirstPos(_Field): pass
class _GasMetalElemMass(_Field): pass
class _GasMetalMass(_Field): pass
class _Imom(_Field): pass
class _Jmom(_Field): pass
class _LengthByType(_Field): pass
class _MassByType(_Field): pass
class _MassCenterPosition(_Field):
    def showInCube(self):
        pos=self.ReadValues()
        x,y,z=np.transpose(pos)
        m=_Mass(self.parentpath).ReadValues()
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        mp.PlotBox(ax,10000,x,y,z,10*m**(1/3),fids=[[1,2,3],[4,5],[6,7]],fcolor=['r','g','b'])
        plt.show()

class _MassCenterVelocity(_Field): pass
class _MassHeIonized(_Field): pass
class _MinID(_Field): pass
class _StellarMetalElemMass(_Field): pass
class _StellarMetalMass(_Field): pass

# --------------------------------------------------------

class _Gas:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "0"
        self.parentpath = parent_dir

        self.DelayTime                   = _DelayTime(self.path)
        self.Density                     = _Density(self.path)
        self.EgyWtDensity                = _EgyWtDensity(self.path)
        self.ElectronAbundance           = _ElectronAbundance(self.path)
        self.Generation                  = _Generation(self.path)
        self.GroupID                     = _GroupID(self.path)
        self.HeIIIIonized                = _HeIIIIonized(self.path)
        self.ID                          = _ID(self.path)
        self.InternalEnergy              = _InternalEnergy(self.path)
        self.Mass                        = _Mass(self.path)
        self.Metallicity                 = _Metallicity(self.path)
        self.Metals                      = _Metals(self.path)
        self.NeutralHydrogenFraction     = _NeutralHydrogenFraction(self.path)
        self.Position                    = _Position(self.path)
        self.Potential                   = _Potential(self.path)
        self.SmoothingLength             = _SmoothingLength(self.path)
        self.StarFormationRate           = _StarFormationRate(self.path)
        self.Velocity                    = _Velocity(self.path)

class _DarkMatter:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "1"
        self.parentpath = parent_dir

        self.GroupID                     = _GroupID(self.path)
        self.ID                          = _ID(self.path)
        self.Mass                        = _Mass(self.path)
        self.Position                    = _Position(self.path)
        self.Potential                   = _Potential(self.path)
        self.Velocity                    = _Velocity(self.path)

class _Neutrino:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "2"
        self.parentpath = parent_dir

        self.GroupID                     = _GroupID(self.path)
        self.ID                          = _ID(self.path)
        self.Mass                        = _Mass(self.path)
        self.Position                    = _Position(self.path)
        self.Potential                   = _Potential(self.path)
        self.Velocity                    = _Velocity(self.path)

class _Star:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "4"
        self.parentpath = parent_dir

        self.BirthDensity                = _BirthDensity(self.path)
        self.Generation                  = _Generation(self.path)
        self.GroupID                     = _GroupID(self.path)
        self.ID                          = _ID(self.path)
        self.LastEnrichmentMyr           = _LastEnrichmentMyr(self.path)
        self.Mass                        = _Mass(self.path)
        self.Metallicity                 = _Metallicity(self.path)
        self.Metals                      = _Metals(self.path)
        self.Position                    = _Position(self.path)
        self.Potential                   = _Potential(self.path)
        self.SmoothingLength             = _SmoothingLength(self.path)
        self.StarFormationTime           = _StarFormationTime(self.path)
        self.TotalMassReturned           = _TotalMassReturned(self.path)
        self.Velocity                    = _Velocity(self.path)

class _BlackHole:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "5"
        self.parentpath = parent_dir

        self.BlackholeAccretionRate      = _BlackholeAccretionRate(self.path)
        self.BlackholeDensity            = _BlackholeDensity(self.path)
        self.BlackholeJumpToMinPot       = _BlackholeJumpToMinPot(self.path)
        self.BlackholeKineticFdbkEnergy  = _BlackholeKineticFdbkEnergy(self.path)
        self.BlackholeMass               = _BlackholeMass(self.path)
        self.BlackholeMinPotPos          = _BlackholeMinPotPos(self.path)
        self.BlackholeMseed              = _BlackholeMseed(self.path)
        self.BlackholeMtrack             = _BlackholeMtrack(self.path)
        self.BlackholeProgenitors        = _BlackholeProgenitors(self.path)
        self.BlackholeSwallowID          = _BlackholeSwallowID(self.path)
        self.BlackholeSwallowTime        = _BlackholeSwallowTime(self.path)
        self.Generation                  = _Generation(self.path)
        self.GroupID                     = _GroupID(self.path)
        self.ID                          = _ID(self.path)
        self.Mass                        = _Mass(self.path)
        self.Position                    = _Position(self.path)
        self.Potential                   = _Potential(self.path)
        self.SmoothingLength             = _SmoothingLength(self.path)
        self.StarFormationTime           = _StarFormationTime(self.path)
        self.Swallowed                   = _Swallowed(self.path)
        self.Velocity                    = _Velocity(self.path)


# -------------------------------------------------------

class _FOF:
    def __init__(self,parent_dir):
        self.path = parent_dir + os.sep + "FOFGroups"
        self.parentpath = parent_dir

        self.BlackholeAccretionRate      = _BlackholeAccretionRate(self.path)
        self.BlackholeMass               = _BlackholeMass(self.path)
        self.FirstPos                    = _FirstPos(self.path)
        self.GasMetalElemMass            = _GasMetalElemMass(self.path)
        self.GasMetalMass                = _GasMetalMass(self.path)
        self.GroupID                     = _GroupID(self.path)
        self.Imom                        = _Imom(self.path)
        self.Jmom                        = _Jmom(self.path)
        self.LengthByType                = _LengthByType(self.path)
        self.Mass                        = _Mass(self.path)
        self.MassByType                  = _MassByType(self.path)
        self.MassCenterPosition          = _MassCenterPosition(self.path)
        self.MassCenterVelocity          = _MassCenterVelocity(self.path)
        self.MassHeIonized               = _MassHeIonized(self.path)
        self.MinID                       = _MinID(self.path)
        self.StarFormationRate           = _StarFormationRate(self.path)
        self.StellarMetalElemMass        = _StellarMetalElemMass(self.path)
        self.StellarMetalMass            = _StellarMetalMass(self.path)

# --------------------------------------------------------

class _PART:
    def __init__(self,snap_num,base_dir):
        snap_num_fix='{:03}'.format(snap_num)
        self.path       = base_dir + os.sep + "PART_" + snap_num_fix
        self.parentpath = base_dir

        self.Gas        = _Gas(self.path)
        self.DarkMatter = _DarkMatter(self.path)
        self.Neutrino   = _Neutrino(self.path)
        self.Star       = _Star(self.path)
        self.BlackHole  = _BlackHole(self.path)

class _PIG:
    def __init__(self,snap_num,base_dir):
        snap_num_fix='{:03}'.format(snap_num)
        self.path       = base_dir + os.sep + "PIG_" + snap_num_fix
        self.parentpath = base_dir

        self.Gas        = _Gas(self.path)
        self.DarkMatter = _DarkMatter(self.path)
        self.Neutrino   = _Neutrino(self.path)
        self.Star       = _Star(self.path)
        self.BlackHole  = _BlackHole(self.path)
        self.FOFGroups  = _FOF(self.path)

# -------------------- USER LEVEL-----------------------------

class BaseDirectory:
    def __init__(self,output_dir:str):
        if not isinstance(output_dir,str):raise TypeError
        self.path = output_dir

    def PART(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PART(snap_num,self.path)

    def PIG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PIG(snap_num,self.path)
























