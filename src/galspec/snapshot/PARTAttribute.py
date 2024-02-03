from typing import Any
import numpy
from galspec.snapshot.DType import _DTYPE

class _Attr:
    def __init__(self, attrline: str) -> None:
        chunks      = attrline.split(" ")
        self.name   = chunks[0]
        self.DType  = _DTYPE(chunks[1])
        self.dtype  = self.DType()
        self.nmemb  = chunks[2]

        np_chunks   = numpy.array(chunks)
        sqbr_start  = int(numpy.where(np_chunks=='[')[0])
        sqbr_end    = int(numpy.where(np_chunks=="]")[0])
        self.value  = np_chunks[sqbr_start+1:sqbr_end].astype(self.dtype)
        
        if (self.value.size==1): self.value=self.value[0]

    def __str__(self) -> str:
        return str(self.value)
        
    def __repr__(self) -> str:
        return repr(self.value)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.value


class _PARTAttribute:
    def __init__(self, path: str) -> None:
        self.path = path

        with open(self.path) as f:
            self.contents=f.read()

        lines=self.contents.split("\n")[:-1]

        self.BoxSize                    = _Attr(lines[0])
        self.box_size                   = self.BoxSize()

        self.CMBTemperatures            = _Attr(lines[1])
        self.cmb_temperatures           = self.CMBTemperatures()

        self.DensityKernel              = _Attr(lines[4])
        self.density_kernel             = self.DensityKernel()

        self.HubbleParam                = _Attr(lines[5])
        self.hubble_param               = self.HubbleParam()

        self.MassTable                  = _Attr(lines[6])
        self.mass_table                 = self.MassTable()

        self.Omega0                     = _Attr(lines[7])
        self.omega0                     = self.Omega0()

        self.OmegaBaryon                = _Attr(lines[8])
        self.omega_baryon               = self.OmegaBaryon()

        self.OmegaLambda                = _Attr(lines[9])
        self.omega_lambda               = self.OmegaLambda()

        self.RSDFactor                  = _Attr(lines[10])
        self.rsd_factor                 = self.RSDFactor()

        self.Time                       = _Attr(lines[11])
        self.time                       = self.Time()  

        self.TimeIC                     = _Attr(lines[12])
        self.time_ic                    = self.TimeIC()

        self.TotNumPart                 = _Attr(lines[13])
        self.tot_num_part               = self.TotNumPart()

        self.TotNumPartInit             = _Attr(lines[14])
        self.tot_num_part_init          = self.TotNumPartInit()

        self.UnitLength_in_cm           = _Attr(lines[15])
        self.unit_length_un_cm          = self.UnitLength_in_cm()

        self.UnitMass_in_g              = _Attr(lines[16])
        self.unit_mass_in_g             = self.UnitMass_in_g()

        self.UnitVelocity_in_cm_per_s   = _Attr(lines[17])
        self.unit_velocity_in_cm_per_s  = self.UnitVelocity_in_cm_per_s()

        self.UsePeculiarVelocity        = _Attr(lines[18])
        self.use_peculiar_velocity      = self.UsePeculiarVelocity()

        # self.BoxSizeUnit    = "Kilo-parsec"          #<---get thse from paramgadegt file
        # self.CMBTemperatureUnit="Kelvin"

    def __str__(self) -> str:
        return self.contents

    def __repr__(self) -> str:
        return self.contents