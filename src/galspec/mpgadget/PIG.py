import os
from galspec.mpgadget.Gas import _Gas
from galspec.mpgadget.DarkMatter import _DarkMatter
from galspec.mpgadget.Neutrino import _Neutrino
from galspec.mpgadget.Star import _Star
from galspec.mpgadget.Blackhole import _BlackHole
from galspec.mpgadget.FOFGroups import _FOFGroups

class _PIG:
    def __init__(self,snap_num,base_dir):
        snap_num_fix='{:03}'.format(snap_num)
        self.path       = base_dir + os.sep + "PIG_" + snap_num_fix
        self.parentpath = base_dir
        self.snap_num   = snap_num

        self.Gas        = _Gas(self.path)
        self.DarkMatter = _DarkMatter(self.path)
        self.Neutrino   = _Neutrino(self.path)
        self.Star       = _Star(self.path)
        self.BlackHole  = _BlackHole(self.path)
        self.FOFGroups  = _FOFGroups(self.path)

    # def ReadAttribute(self):
    #     return mp.ReadAttribute(self)