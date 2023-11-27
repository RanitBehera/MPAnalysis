import os,numpy,h5py,sys

class ascii:
    id,num_p,mvir,mbound_vir,rvir,vmax,rvmax,vrms,\
    x,y,z,vx,vy,vz,Jx,Jy,Jz,E,Spin,\
    PosUncertainty,VelUncertainty,\
    bulk_vx,bulk_vy,bulk_vz,BulkVelUnc,\
    n_core,m200b,m200c,m500c,m2500c,Xoff,\
    Voff,spin_bullock,\
    b_to_a,c_to_a,Ax,Ay,Az,b_to_a_500c,c_to_a_500c,Ax_500c,Ay_500c,Az_500c,\
    Rs,Rs_Klypin,T_U,M_pe_Behroozi,M_pe_Diemer,\
    Type,SM,Gas,BH,idx,i_so,i_ph,num_cp,mmetric=range(0,57)
    
class particles:
    x,y,z,vx,vy,vz,mass,\
    specific_energy,particle_id,type,\
    assigned_internal_haloid,internal_haloid,external_haloid=range(0,13)

class ConfigFile:
    def __init__(self,filedir,filename="rockstar.cfg"):
        self.path       = filedir + os.sep + filename
        self.parentpath = filedir
        
        file=open(self.path)
        lines=file.readlines()
        file.close()

        self.FillValues(lines)


    def FillValues(self,lines):
        val_dict={}
        for line in lines:
            field=line.split("=")[0].strip()
            value=line.split("=")[1].split("\n")[0]
            val_dict[field]=value


        self.FILE_FORMAT                            = val_dict["FILE_FORMAT"]
        self.PARTICLE_MASS                          = float(val_dict["PARTICLE_MASS"])
        self.MASS_DEFINITION                        = val_dict["MASS_DEFINITION"]
        self.MASS_DEFINITION2                       = val_dict["MASS_DEFINITION2"]
        self.MASS_DEFINITION3                       = val_dict["MASS_DEFINITION3"]
        self.MASS_DEFINITION4                       = val_dict["MASS_DEFINITION4"]
        self.MASS_DEFINITION5                       = val_dict["MASS_DEFINITION5"]
        self.STRICT_SO_MASSES                       = val_dict["STRICT_SO_MASSES"]
        self.MIN_HALO_OUTPUT_SIZE                   = val_dict["MIN_HALO_OUTPUT_SIZE"]
        # self.MIN_HALO_OUTPUT_MASS                   = val_dict["MIN_HALO_OUTPUT_MASS"]
        self.FORCE_RES                              = val_dict["FORCE_RES"]
        self.FORCE_RES_PHYS_MAX                     = val_dict["FORCE_RES_PHYS_MAX"]
        self.SCALE_NOW                              = float(val_dict["SCALE_NOW"])
        self.NON_COSMOLOGICAL                       = val_dict["NON_COSMOLOGICAL"]
        self.h0                                     = float(val_dict["h0"])
        self.Ol                                     = val_dict["Ol"]
        self.Om                                     = float(val_dict["Om"])
        self.W0                                     = val_dict["W0"]
        self.WA                                     = val_dict["WA"]
        self.GADGET_ID_BYTES                        = val_dict["GADGET_ID_BYTES"]
        self.GADGET_MASS_CONVERSION                 = val_dict["GADGET_MASS_CONVERSION"]
        self.GADGET_LENGTH_CONVERSION               = val_dict["GADGET_LENGTH_CONVERSION"]
        # self.GADGET_VELOCITY_CONVERSION             = val_dict["GADGET_VELOCITY_CONVERSION"]
        self.GADGET_HALO_PARTICLE_TYPE              = val_dict["GADGET_HALO_PARTICLE_TYPE"]
        self.RESCALE_PARTICLE_MASS                  = val_dict["RESCALE_PARTICLE_MASS"]
        # self.MPGADGET_MASS_CONVERSION               = val_dict["MPGADGET_MASS_CONVERSION"]
        # self.MPGADGET_LENGTH_CONVERSION             = val_dict["MPGADGET_LENGTH_CONVERSION"]
        # self.MPGADGET_VELOCITY_CONVERSION           = val_dict["MPGADGET_VELOCITY_CONVERSION"]
        # self.MPGADGET_HALO_PARTICLE_TYPE            = val_dict["MPGADGET_HALO_PARTICLE_TYPE"]
        self.TIPSY_LENGTH_CONVERSION                = val_dict["TIPSY_LENGTH_CONVERSION"]
        self.TIPSY_VELOCITY_CONVERSION              = val_dict["TIPSY_VELOCITY_CONVERSION"]
        # self.TIPSY_MASS_CONVERSION                  = val_dict["TIPSY_MASS_CONVERSION"]
        # self.NCHILADA_LENGTH_CONVERSION             = val_dict["NCHILADA_LENGTH_CONVERSION"]
        # self.NCHILADA_VELOCITY_CONVERSION           = val_dict["NCHILADA_VELOCITY_CONVERSION"]
        # self.NCHILADA_MASS_CONVERSION               = val_dict["NCHILADA_MASS_CONVERSION"]
        self.PARALLEL_IO                            = val_dict["PARALLEL_IO"]
        self.PARALLEL_IO_SERVER_ADDRESS             = val_dict["PARALLEL_IO_SERVER_ADDRESS"]
        self.PARALLEL_IO_SERVER_PORT                = val_dict["PARALLEL_IO_SERVER_PORT"]
        self.PARALLEL_IO_WRITER_PORT                = val_dict["PARALLEL_IO_WRITER_PORT"]
        self.PARALLEL_IO_SERVER_INTERFACE           = val_dict["PARALLEL_IO_SERVER_INTERFACE"]
        self.PARALLEL_IO_CATALOGS                   = val_dict["PARALLEL_IO_CATALOGS"]
        self.RUN_ON_SUCCESS                         = val_dict["RUN_ON_SUCCESS"]
        self.RUN_PARALLEL_ON_SUCCESS                = val_dict["RUN_PARALLEL_ON_SUCCESS"]
        self.LOAD_BALANCE_SCRIPT                    = val_dict["LOAD_BALANCE_SCRIPT"]
        self.INBASE                                 = val_dict["INBASE"]
        self.FILENAME                               = val_dict["FILENAME"]
        self.STARTING_SNAP                          = val_dict["STARTING_SNAP"]
        self.RESTART_SNAP                           = val_dict["RESTART_SNAP"]
        self.NUM_SNAPS                              = val_dict["NUM_SNAPS"]
        self.NUM_BLOCKS                             = val_dict["NUM_BLOCKS"]
        self.NUM_READERS                            = val_dict["NUM_READERS"]
        self.PRELOAD_PARTICLES                      = val_dict["PRELOAD_PARTICLES"]
        self.SNAPSHOT_NAMES                         = val_dict["SNAPSHOT_NAMES"]
        self.LIGHTCONE_ALT_SNAPS                    = val_dict["LIGHTCONE_ALT_SNAPS"]
        self.BLOCK_NAMES                            = val_dict["BLOCK_NAMES"]
        self.OUTBASE                                = val_dict["OUTBASE"]
        self.OVERLAP_LENGTH                         = val_dict["OVERLAP_LENGTH"]
        self.NUM_WRITERS                            = val_dict["NUM_WRITERS"]
        self.FORK_READERS_FROM_WRITERS              = val_dict["FORK_READERS_FROM_WRITERS"]
        self.FORK_PROCESSORS_PER_MACHINE            = val_dict["FORK_PROCESSORS_PER_MACHINE"]
        self.OUTPUT_FORMAT                          = val_dict["OUTPUT_FORMAT"]
        self.DELETE_BINARY_OUTPUT_AFTER_FINISHED    = val_dict["DELETE_BINARY_OUTPUT_AFTER_FINISHED"]
        self.FULL_PARTICLE_CHUNKS                   = val_dict["FULL_PARTICLE_CHUNKS"]
        self.BGC2_SNAPNAMES                         = val_dict["BGC2_SNAPNAMES"]
        self.SHAPE_ITERATIONS                       = val_dict["SHAPE_ITERATIONS"]
        self.WEIGHTED_SHAPES                        = val_dict["WEIGHTED_SHAPES"]
        self.BOUND_PROPS                            = val_dict["BOUND_PROPS"]
        self.BOUND_OUT_TO_HALO_EDGE                 = val_dict["BOUND_OUT_TO_HALO_EDGE"]
        self.DO_MERGER_TREE_ONLY                    = val_dict["DO_MERGER_TREE_ONLY"]
        self.IGNORE_PARTICLE_IDS                    = val_dict["IGNORE_PARTICLE_IDS"]
        self.EXACT_LL_CALC                          = val_dict["EXACT_LL_CALC"]
        self.TRIM_OVERLAP                           = val_dict["TRIM_OVERLAP"]
        self.ROUND_AFTER_TRIM                       = val_dict["ROUND_AFTER_TRIM"]
        self.LIGHTCONE                              = val_dict["LIGHTCONE"]
        self.PERIODIC                               = val_dict["PERIODIC"]
        self.LIGHTCONE_ORIGIN                       = val_dict["LIGHTCONE_ORIGIN"]
        self.LIGHTCONE_ALT_ORIGIN                   = val_dict["LIGHTCONE_ALT_ORIGIN"]
        self.LIMIT_CENTER                           = val_dict["LIMIT_CENTER"]
        self.LIMIT_RADIUS                           = val_dict["LIMIT_RADIUS"]
        self.SWAP_ENDIANNESS                        = val_dict["SWAP_ENDIANNESS"]
        self.GADGET_VARIANT                         = val_dict["GADGET_VARIANT"]
        self.ART_VARIANT                            = val_dict["ART_VARIANT"]
        self.FOF_FRACTION                           = val_dict["FOF_FRACTION"]
        self.FOF_LINKING_LENGTH                     = val_dict["FOF_LINKING_LENGTH"]
        self.INITIAL_METRIC_SCALING                 = val_dict["INITIAL_METRIC_SCALING"]
        self.INCLUDE_HOST_POTENTIAL_RATIO           = val_dict["INCLUDE_HOST_POTENTIAL_RATIO"]
        self.TEMPORAL_HALO_FINDING                  = val_dict["TEMPORAL_HALO_FINDING"]
        self.MIN_HALO_PARTICLES                     = val_dict["MIN_HALO_PARTICLES"]
        self.UNBOUND_THRESHOLD                      = val_dict["UNBOUND_THRESHOLD"]
        self.ALT_NFW_METRIC                         = val_dict["ALT_NFW_METRIC"]
        self.EXTRA_PROFILING                        = val_dict["EXTRA_PROFILING"]
        # self.SUPPRESS_GALAXIES                      = val_dict["SUPPRESS_GALAXIES"]
        # self.NON_DM_METRIC_SCALING                  = val_dict["NON_DM_METRIC_SCALING"]
        # self.GALAXY_POISSON_SIGMA                   = val_dict["GALAXY_POISSON_SIGMA"]
        # self.GALAXY_LINKING_LENGTH                  = val_dict["GALAXY_LINKING_LENGTH"]
        # self.DENSITY_MERGE_THRESH                   = val_dict["DENSITY_MERGE_THRESH"]
        self.TOTAL_PARTICLES                        = val_dict["TOTAL_PARTICLES"]
        self.BOX_SIZE                               = float(val_dict["BOX_SIZE"])
        self.OUTPUT_LEVELS                          = val_dict["OUTPUT_LEVELS"]
        self.DUMP_PARTICLES                         = val_dict["DUMP_PARTICLES"]
        self.ROCKSTAR_CONFIG_FILENAME               = val_dict["ROCKSTAR_CONFIG_FILENAME"]
        self.AVG_PARTICLE_SPACING                   = val_dict["AVG_PARTICLE_SPACING"]
        self.SINGLE_SNAP                            = val_dict["SINGLE_SNAP"]



from tqdm import tqdm


sys.path.append(os.getcwd())
import modules as mp
from modules.Navigate import _PART


class PBar:
    def __init__(self,items:int):
        self.value=0
        self.tqdm_bar=tqdm(range(items))

    def Progress(self,value:int=1):
            self.value+=value
            self.tqdm_bar.update(self.value)
            self.tqdm_bar.refresh()

        


def OutputRockstarHDF5(snap:_PART,filepath:str,include_gas:bool,include_dm:bool,include_star:bool,include_bh:bool):
    bar_range=1 + include_gas*7 + include_dm*4 + include_star*4 + include_bh*4 + 1
    pb=PBar(bar_range)
    
    attr=snap.ReadAttribute()

    with h5py.File(filepath,"w") as hdf5:
        head=hdf5.create_group("Header")
        head.attrs["OmegaLambda"]=attr.OmegaLambda
        head.attrs["Omega0"]=attr.Omega0
        head.attrs["HubbleParam"]=attr.HubbleParam
        head.attrs["Time"]=attr.Time
        head.attrs["BoxSize"]=attr.BoxSize # Rockstar accepts in Mpc/h, Might get handelled via Length conversion

        head.attrs["NumPart_ThisFile"]=attr.TotNumPart
        head.attrs["NumPart_Total"]=attr.TotNumPartInit
        head.attrs["NumPart_Total_HighWord"]=[0,0,0,0,0,0]
        head.attrs["MassTable"]=attr.MassTable

        #Extra
        head.attrs["NumFilesPerSnapshot"]=1

        pb.Progress()

        if include_gas:
            gas=hdf5.create_group("PartType0")
            gas.create_dataset("ParticleIDs",data=snap.Gas.ID.ReadValues());pb.Progress()
            gas.create_dataset("Coordinates",data=snap.Gas.Position.ReadValues());pb.Progress()
            gas.create_dataset("Velocities",data=snap.Gas.Velocity.ReadValues());pb.Progress()
            gas.create_dataset("Masses",data=snap.Gas.Mass.ReadValues());pb.Progress()
            gas.create_dataset("SmoothingLength",data=snap.Gas.SmoothingLength.ReadValues());pb.Progress()
            gas.create_dataset("InternalEnergy",data=snap.Gas.InternalEnergy.ReadValues());pb.Progress()
            gas.create_dataset("Density",data=snap.Gas.Density.ReadValues());pb.Progress()

        if include_dm:
            dm=hdf5.create_group("PartType1")
            dm.create_dataset("ParticleIDs",data=snap.DarkMatter.ID.ReadValues());pb.Progress()
            dm.create_dataset("Coordinates",data=snap.DarkMatter.Position.ReadValues());pb.Progress()
            dm.create_dataset("Velocities",data=snap.DarkMatter.Velocity.ReadValues());pb.Progress()
            dm.create_dataset("Masses",data=snap.DarkMatter.Mass.ReadValues());pb.Progress()

        if include_star:
            star=hdf5.create_group("PartType4")
            star.create_dataset("ParticleIDs",data=snap.Star.ID.ReadValues());pb.Progress()
            star.create_dataset("Coordinates",data=snap.Star.Position.ReadValues());pb.Progress()
            star.create_dataset("Velocities",data=snap.Star.Velocity.ReadValues());pb.Progress()
            star.create_dataset("Masses",data=snap.Star.Mass.ReadValues());pb.Progress()

        if include_bh:
            bh=hdf5.create_group("PartType5")
            bh.create_dataset("ParticleIDs",data=snap.BlackHole.ID.ReadValues());pb.Progress()
            bh.create_dataset("Coordinates",data=snap.BlackHole.Position.ReadValues());pb.Progress()
            bh.create_dataset("Velocities",data=snap.BlackHole.Velocity.ReadValues());pb.Progress()
            bh.create_dataset("Masses",data=snap.BlackHole.Mass.ReadValues());pb.Progress()













