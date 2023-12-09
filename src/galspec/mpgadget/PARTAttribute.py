from typing import Any
import numpy

class _Attr:
    def __init__(self, attrline: str) -> None:
        chunks      = attrline.split(" ")
        self.name   = chunks[0]
        self.dtype  = chunks[1]
        self.nmemb  = chunks[2]

        np_chunks   = numpy.array(chunks)
        sqbr_start  = int(numpy.where(np_chunks=='[')[0])
        sqbr_end    = int(numpy.where(np_chunks=="]")[0])
        self.value  = np_chunks[sqbr_start+1:sqbr_end].astype(self.dtype)
        
        if (self.value.size==1): self.value=self.value[0]

    def __repr__(self) -> str:
        return str(self.value)

    # @property
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.value


class PARTAttribute:
    def __init__(self, path: str) -> None:
        self.path = path

        with open(self.path) as f:
            self.contents=f.read()

        lines=self.contents.split("\n")[:-1]

        self.BoxSize            = _Attr(lines[0])
        self.CMBTemperatures    = _Attr(lines[1])
        self.DensityKernel      = _Attr(lines[4])
        self.HubbleParam        = _Attr(lines[5])
        self.MassTable          = _Attr(lines[6])
        self.Omega0             = _Attr(lines[7])
        self.OmegaBaryon        = _Attr(lines[8])
        self.OmegaLambda        = _Attr(lines[9])
        self.RSDFactor          = _Attr(lines[10])
        self.Time               = _Attr(lines[11])
        self.TimeIC             = _Attr(lines[12])
        self.TotNumPart         = _Attr(lines[13])
        self.TotNumPartInit     = _Attr(lines[14])
        self.UnitLength_in_cm           = _Attr(lines[15])
        self.UnitMass_in_g              = _Attr(lines[16])
        self.UnitVelocity_in_cm_per_s   = _Attr(lines[17])
        self.UsePeculiarVelocity        = _Attr(lines[18])


        # self.BoxSizeUnit    = "Kilo-parsec"          #<---get thse from paramgadegt file
        # self.CMBTemperatureUnit="Kelvin"


    def __repr__(self) -> str:
        return self.contents