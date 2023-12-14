class _Field:
    def __init__(self,parent_dir):
        # Knowling field name is required to take different actions based on field under same name
        self.fieldName  =   self.__class__.__name__.split("_")[-1]     # str
        self.path       = parent_dir + os.sep + self.fieldName
        self.parentpath = parent_dir
        # self.value  = None

    # def ReadValues(self):
        # return mp.ReadField(self)



# --- PART Fields

# Common - All
class _GroupID(_Field):                     pass
class _ID(_Field):                          pass
class _Position(_Field):                    pass
class _Potential(_Field):                   pass
class _Velocity(_Field):                    pass
class _Mass(_Field):                        pass

# Common - Gas + Star + Blaclhole
class _Generation(_Field):                  pass
class _SmoothingLength(_Field):             pass


# Common - Gas + Star
class _Metallicity(_Field):                 pass
class _Metals(_Field):                      pass

# Common - Star + Blackhole
class _StarFormationTime(_Field):           pass

# Gas
class _DelayTime(_Field):                   pass
class _Density(_Field):                     pass
class _EgyWtDensity(_Field):                pass
class _ElectronAbundance(_Field):           pass
class _HeIIIIonized(_Field):                pass
class _InternalEnergy(_Field):              pass
class _NeutralHydrogenFraction(_Field):     pass
class _StarFormationRate(_Field):           pass

# Star
class _BirthDensity(_Field):                pass
class _LastEnrichmentMyr(_Field):           pass
class _TotalMassReturned(_Field):           pass

# Blackhole
class _BlackholeAccretionRate(_Field):      pass
class _BlackholeDensity(_Field):            pass
class _BlackholeJumpToMinPot(_Field):       pass
class _BlackholeKineticFdbkEnergy(_Field):  pass
class _BlackholeMass(_Field):               pass
class _BlackholeMinPotPos(_Field):          pass
class _BlackholeMseed(_Field):              pass
class _BlackholeMtrack(_Field):             pass
class _BlackholeProgenitors(_Field):        pass
class _BlackholeSwallowID(_Field):          pass
class _BlackholeSwallowTime(_Field):        pass
class _Swallowed(_Field):                   pass



# FOF
class _FirstPos(_Field):                    pass

class _GasMetalElemMass(_Field):            pass
class _GasMetalMass(_Field):                pass


class _Imom(_Field):                        pass
class _Jmom(_Field):                        pass
class _LengthByType(_Field):                pass


class _MassByType(_Field):                  pass
class _MassCenterPosition(_Field):          pass
class _MassCenterVelocity(_Field):          pass
class _MassHeIonized(_Field):               pass
class _MinID(_Field):                       pass



class _StellarMetalElemMass(_Field):        pass
class _StellarMetalMass(_Field):            pass