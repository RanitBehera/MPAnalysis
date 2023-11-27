import numpy as np
import h5py
from tqdm import tqdm


import sys
import os
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













