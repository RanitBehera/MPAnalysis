

class Field:
    def __init__(self,parent_dir):
        self.fieldName  =   self.__class__.__name__     # str
        self.path   = parent_dir + "\\" + self.fieldName

# --------------------------------------------

class DelayTime(Field): pass
class Density(Field): pass
class EgyWtDensity(Field): pass
class ElectronAbundance(Field): pass
class Generation(Field): pass
class GroupID(Field): pass
class HeIIIIonized(Field): pass
class ID(Field): pass
class InternalEnergy(Field): pass
class Mass(Field): pass
class Metallicity(Field): pass
class Metals(Field): pass
class NeutralHydrogenFraction(Field): pass
class Position(Field): pass
class Potential(Field): pass
class SmoothingLength(Field): pass
class StarFormationRate(Field): pass
class Velocity(Field): pass
class BirthDensity(Field): pass
class LastEnrichmentMyr(Field): pass
class StarFormationTime(Field): pass
class TotalMassReturned(Field): pass
class BlackholeAccretionRate(Field): pass
class BlackholeDensity(Field): pass
class BlackholeJumpToMinPot(Field): pass
class BlackholeKineticFdbkEnergy(Field): pass
class BlackholeMass(Field): pass
class BlackholeMinPotPos(Field): pass
class BlackholeMseed(Field): pass
class BlackholeMtrack(Field): pass
class BlackholeProgenitors(Field): pass
class BlackholeSwallowID(Field): pass
class BlackholeSwallowTime(Field): pass
class Swallowed(Field): pass
class FirstPos(Field): pass
class GasMetalElemMass(Field): pass
class GasMetalMass(Field): pass
class Imom(Field): pass
class Jmom(Field): pass
class LengthByType(Field): pass
class MassByType(Field): pass
class MassCenterPosition(Field): pass
class MassCenterVelocity(Field): pass
class MassHeIonized(Field): pass
class MinID(Field): pass
class StellarMetalElemMass(Field): pass
class StellarMetalMass(Field): pass

# --------------------------------------------------------

class Gas:
    def __init__(self,parent_dir):
        self.path = parent_dir + "\\0"
        
        self.DelayTime                   = DelayTime(self.path)
        self.Density                     = Density(self.path)
        self.EgyWtDensity                = EgyWtDensity(self.path)
        self.ElectronAbundance           = ElectronAbundance(self.path)
        self.Generation                  = Generation(self.path)
        self.GroupID                     = GroupID(self.path)
        self.HeIIIIonized                = HeIIIIonized(self.path)
        self.ID                          = ID(self.path)
        self.InternalEnergy              = InternalEnergy(self.path)
        self.Mass                        = Mass(self.path)
        self.Metallicity                 = Metallicity(self.path)
        self.Metals                      = Metals(self.path)
        self.NeutralHydrogenFraction     = NeutralHydrogenFraction(self.path)
        self.Position                    = Position(self.path)
        self.Potential                   = Potential(self.path)
        self.SmoothingLength             = SmoothingLength(self.path)
        self.StarFormationRate           = StarFormationRate(self.path)
        self.Velocity                    = Velocity(self.path)

class DarkMatter:
    def __init__(self,parent_dir):
        self.path = parent_dir + "\\1"

        self.GroupID                     = GroupID(self.path)
        self.ID                          = ID(self.path)
        self.Mass                        = Mass(self.path)
        self.Position                    = Position(self.path)
        self.Potential                   = Potential(self.path)
        self.Velocity                    = Velocity(self.path)

class Neutrino:
    def __init__(self,parent_dir):
        self.path = parent_dir + "\\2"

        self.GroupID                     = GroupID(self.path)
        self.ID                          = ID(self.path)
        self.Mass                        = Mass(self.path)
        self.Position                    = Position(self.path)
        self.Potential                   = Potential(self.path)
        self.Velocity                    = Velocity(self.path)

class Star:
    def __init__(self,parent_dir):
        self.path = parent_dir + "\\4"

        self.BirthDensity                = BirthDensity(self.path)
        self.Generation                  = Generation(self.path)
        self.GroupID                     = GroupID(self.path)
        self.ID                          = ID(self.path)
        self.LastEnrichmentMyr           = LastEnrichmentMyr(self.path)
        self.Mass                        = Mass(self.path)
        self.Metallicity                 = Metallicity(self.path)
        self.Metals                      = Metals(self.path)
        self.Position                    = Position(self.path)
        self.Potential                   = Potential(self.path)
        self.SmoothingLength             = SmoothingLength(self.path)
        self.StarFormationTime           = StarFormationTime(self.path)
        self.TotalMassReturned           = TotalMassReturned(self.path)
        self.Velocity                    = Velocity(self.path)

class BlackHole:
    def __init__(self,parent_dir):
        self.path = parent_dir + "\\5"

        self.BlackholeAccretionRate      = BlackholeAccretionRate(self.path)
        self.BlackholeDensity            = BlackholeDensity(self.path)
        self.BlackholeJumpToMinPot       = BlackholeJumpToMinPot(self.path)
        self.BlackholeKineticFdbkEnergy  = BlackholeKineticFdbkEnergy(self.path)
        self.BlackholeMass               = BlackholeMass(self.path)
        self.BlackholeMinPotPos          = BlackholeMinPotPos(self.path)
        self.BlackholeMseed              = BlackholeMseed(self.path)
        self.BlackholeMtrack             = BlackholeMtrack(self.path)
        self.BlackholeProgenitors        = BlackholeProgenitors(self.path)
        self.BlackholeSwallowID          = BlackholeSwallowID(self.path)
        self.BlackholeSwallowTime        = BlackholeSwallowTime(self.path)
        self.Generation                  = Generation(self.path)
        self.GroupID                     = GroupID(self.path)
        self.ID                          = ID(self.path)
        self.Mass                        = Mass(self.path)
        self.Position                    = Position(self.path)
        self.Potential                   = Potential(self.path)
        self.SmoothingLength             = SmoothingLength(self.path)
        self.StarFormationTime           = StarFormationTime(self.path)
        self.Swallowed                   = Swallowed(self.path)
        self.Velocity                    = Velocity(self.path)


# -------------------------------------------------------

class FOF:
    def __init__(self,parent_dir):
        self.path = parent_dir + "\\FOFGroups"

        self.BlackholeAccretionRate      = BlackholeAccretionRate(self.path)
        self.BlackholeMass               = BlackholeMass(self.path)
        self.FirstPos                    = FirstPos(self.path)
        self.GasMetalElemMass            = GasMetalElemMass(self.path)
        self.GasMetalMass                = GasMetalMass(self.path)
        self.GroupID                     = GroupID(self.path)
        self.Imom                        = Imom(self.path)
        self.Jmom                        = Jmom(self.path)
        self.LengthByType                = LengthByType(self.path)
        self.Mass                        = Mass(self.path)
        self.MassByType                  = MassByType(self.path)
        self.MassCenterPosition          = MassCenterPosition(self.path)
        self.MassCenterVelocity          = MassCenterVelocity(self.path)
        self.MassHeIonized               = MassHeIonized(self.path)
        self.MinID                       = MinID(self.path)
        self.StarFormationRate           = StarFormationRate(self.path)
        self.StellarMetalElemMass        = StellarMetalElemMass(self.path)
        self.StellarMetalMass            = StellarMetalMass(self.path)

# --------------------------------------------------------

class PART:
    def __init__(self,snap_num,base_dir):
        snap_num_fix='{:03}'.format(snap_num)
        self.path       = base_dir + "\\" + "PART_" + snap_num_fix

        self.Gas        = Gas(self.path)
        self.DarkMatter = DarkMatter(self.path)
        self.Neutrino   = Neutrino(self.path)
        self.Star       = Star(self.path)
        self.BlackHole  = BlackHole(self.path)

class PIG:
    def __init__(self,snap_num,base_dir):
        snap_num_fix='{:03}'.format(snap_num)
        self.path       = base_dir + "\\" + "PIG_" + snap_num_fix

        self.Gas        = Gas(self.path)
        self.DarkMatter = DarkMatter(self.path)
        self.Neutrino   = Neutrino(self.path)
        self.Star       = Star(self.path)
        self.BlackHole  = BlackHole(self.path)
        self.FOFGroups  = FOF(self.path)

# ------------------------------------------------------------

class BaseDirectory:
    def __init__(self,output_dir):
        self.path = output_dir

    def PART(self,snap_num):
        return PART(snap_num,self.path)

    def PIG(self,snap_num):
        return PIG(snap_num,self.path)
























