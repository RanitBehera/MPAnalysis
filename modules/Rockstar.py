import numpy as np
import h5py



import sys
import os
sys.path.append(os.getcwd())
import modules as mp
from .Navigate import _PART

def OutputRockstarHDF5(snap:_PART,filepath:str,include_gas:bool,include_dm:bool,include_star:bool,include_bh:bool):
    attr=snap.ReadAttribute()

    with h5py.File(filepath,"w") as hdf5:
        head=hdf5.create_group("Header")
        head.attrs["OmegaLambda"]=attr.OmegaLambda
        head.attrs["Omega0"]=attr.Omega0
        head.attrs["HubbleParam"]=attr.HubbleParam
        head.attrs["Time"]=attr.Time
        head.attrs["BoxSize"]=attr.BoxSize # Rockstar accepts in Mpc/h, Might get handelled via Length conversion

        head.attrs["NumPart_ThisFile"]=attr.TotNumPart
        head.attrs["NumPart_Total"]=attr.TotNumPart
        head.attrs["NumPart_Total_HighWord"]=[0,0,0,0,0,0]
        head.attrs["MassTable"]=attr.MassTable

        if include_gas:
            gas=hdf5.create_group("PartType0")
            gas.create_dataset("ParticleIDs",data=snap.Gas.ID.ReadValues())
            gas.create_dataset("Coordinates",data=snap.Gas.Position.ReadValues())
            gas.create_dataset("Velocities",data=snap.Gas.Velocity.ReadValues())

        if include_dm:
            dm=hdf5.create_group("PartType1")
            dm.create_dataset("ParticleIDs",data=snap.DarkMatter.ID.ReadValues())
            dm.create_dataset("Coordinates",data=snap.DarkMatter.Position.ReadValues())
            dm.create_dataset("Velocities",data=snap.DarkMatter.Velocity.ReadValues())

        if include_star:
            star=hdf5.create_group("PartType4")
            star.create_dataset("ParticleIDs",data=snap.Star.ID.ReadValues())
            star.create_dataset("Coordinates",data=snap.Star.Position.ReadValues())
            star.create_dataset("Velocities",data=snap.Star.Velocity.ReadValues())

        if include_bh:
            bh=hdf5.create_group("PartType4")
            bh.create_dataset("ParticleIDs",data=snap.Star.ID.ReadValues())
            bh.create_dataset("Coordinates",data=snap.Star.Position.ReadValues())
            bh.create_dataset("Velocities",data=snap.Star.Velocity.ReadValues())

        

class RockstarConfig:
    def __init__(self):
        self.SetDefaultConfig()


    def SetDefaultConfig(self):
        FILE_FORMAT = "ASCII"
        PARTICLE_MASS = 1.36297e+08
        MASS_DEFINITION = "vir"
        MASS_DEFINITION2 = "200b"
        MASS_DEFINITION3 = "200c"
        MASS_DEFINITION4 = "500c"
        MASS_DEFINITION5 = "2500c"
        STRICT_SO_MASSES = 0
        MIN_HALO_OUTPUT_SIZE = 1
        FORCE_RES = 0.001
        FORCE_RES_PHYS_MAX = 0.001
        NON_COSMOLOGICAL = 0
        SCALE_NOW = 1
        h0 = 0.7
        Ol = 0.73
        Om = 0.27
        W0 = -1
        WA = 0
        GADGET_ID_BYTES = 4
        GADGET_MASS_CONVERSION = 1e+10
        GADGET_LENGTH_CONVERSION = 1
        GADGET_SKIP_NON_HALO_PARTICLES = 0
        GADGET_HALO_PARTICLE_TYPE = 1
        RESCALE_PARTICLE_MASS = 0
        TIPSY_LENGTH_CONVERSION = 1
        TIPSY_VELOCITY_CONVERSION = 1
        PARALLEL_IO = 0
        PARALLEL_IO_SERVER_ADDRESS = "auto"
        PARALLEL_IO_SERVER_PORT = "auto"
        PARALLEL_IO_WRITER_PORT = 32001
        PARALLEL_IO_SERVER_INTERFACE = ""
        PARALLEL_IO_CATALOGS = 0
        RUN_ON_SUCCESS = ""
        RUN_PARALLEL_ON_SUCCESS = ""
        LOAD_BALANCE_SCRIPT = ""
        INBASE = "/home/ranitbehera/DriveRanit/2 Work/MPAnalysis/"
        FILENAME = "test.ascii"
        STARTING_SNAP = 0
        RESTART_SNAP = 0
        NUM_SNAPS = 1
        NUM_BLOCKS = 1
        NUM_READERS = 1
        PRELOAD_PARTICLES = 0
        SNAPSHOT_NAMES = ""
        LIGHTCONE_ALT_SNAPS = ""
        BLOCK_NAMES = ""
        OUTBASE = "/home/ranitbehera/DriveRanit/1 Data/RKSTEST/PART017/"
        OVERLAP_LENGTH = 3
        NUM_WRITERS = 1
        FORK_READERS_FROM_WRITERS = 0
        FORK_PROCESSORS_PER_MACHINE = 1
        OUTPUT_FORMAT = "BOTH"
        DELETE_BINARY_OUTPUT_AFTER_FINISHED = 0
        FULL_PARTICLE_CHUNKS = 0
        OUTPUT_EVERY_N_PARTICLES = 1
        UNFILTERED_HALO_OUTPUT = 0
        BGC2_SNAPNAMES = ""
        WEAK_LENSING_FRACTION = 0
        SHAPE_ITERATIONS = 10
        WEIGHTED_SHAPES = 1
        BOUND_PROPS = 1
        BOUND_OUT_TO_HALO_EDGE = 0
        DO_MERGER_TREE_ONLY = 0
        IGNORE_PARTICLE_IDS = 0
        EXACT_LL_CALC = 0
        TRIM_OVERLAP = 0
        ROUND_AFTER_TRIM = 1
        LIGHTCONE = 0
        PERIODIC = 0
        LIGHTCONE_ORIGIN = (0, 0, 0)
        LIGHTCONE_ALT_ORIGIN = (0, 0, 0)
        LIMIT_CENTER = (0, 0, 0)
        LIMIT_RADIUS = 0
        SWAP_ENDIANNESS = 0
        GADGET_VARIANT = 0
        ART_VARIANT = 0
        FOF_FRACTION = 0.7
        FOF_LINKING_LENGTH = 0.28
        INITIAL_METRIC_SCALING = 1
        INCLUDE_HOST_POTENTIAL_RATIO = 0.3
        TEMPORAL_HALO_FINDING = 0
        MIN_HALO_PARTICLES = 10
        UNBOUND_THRESHOLD = 0.5
        ALT_NFW_METRIC = 0
        EXTRA_PROFILING = 1
        TOTAL_PARTICLES = 8589934592
        BOX_SIZE = 250
        OUTPUT_LEVELS = 0
        DUMP_PARTICLES = (0, 0, 0)
        ROCKSTAR_CONFIG_FILENAME = "mptest.cfg"
        AVG_PARTICLE_SPACING = 0.12207
        SINGLE_SNAP = 0













