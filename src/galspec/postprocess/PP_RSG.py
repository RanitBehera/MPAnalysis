import os,numpy
from galspec.navigation.MPGADGET.RSG.RSG import _RSG
from galspec.IO.BinaryFile import WriteField


NUM_TYPES = 6   # Number of particle types in MPGADGET


class PP_RSG:
    def __init__(self,path,show_progress=True) -> None:
        self.RSG = _RSG(path)
        self.show_progress = show_progress


    def StartAll(self):
        if(self.show_progress):print(" GENERATING FIELDS ".center(30,'='))
        self.LengthByTypeWC()
        self.LengthByTypeInRvirWC()



    def LengthByTypeWC(self,output_sum=True):
        if(self.show_progress):print("/RKSGroups/LengthByTypeWC : ",end="",flush=True)

        gihids = self.RSG.RKSGroups.InternalHaloID()
        LengthBTWC = numpy.zeros((len(gihids),NUM_TYPES))
        def AddCounts(pihids,column):
            # Filter out those pihids which are not in gihids
            gmask = numpy.isin(pihids,gihids)
            pihids=pihids[gmask]

            upihids, counts = numpy.unique(pihids,return_counts=True)
            uid_to_count_map=dict(zip(upihids,counts))
            for i,gihid in enumerate(gihids):
                if gihid in upihids:
                    LengthBTWC[i,column] += uid_to_count_map[gihid]
        AddCounts(self.RSG.Gas.InternalHaloID(),0)
        AddCounts(self.RSG.DarkMatter.InternalHaloID(),1)
        AddCounts(self.RSG.Star.InternalHaloID(),4)
        AddCounts(self.RSG.BlackHole.InternalHaloID(),5)

        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"LengthByTypeWC",LengthBTWC,"Overwrite")
        if(self.show_progress):print("Done")

        # if(output_sum):
        #     if(self.show_progress):print("/RKSGroups/LengthWC : ",end="")
        #     WriteField(os.path.join(self.RSG.path,"RKSGroups"),"LengthWC",LengthBTWC.sum(axis=1))
        #     if(self.show_progress):print("Done")
        
    def LengthByTypeInRvirWC(self,output_sum=True):
        if(self.show_progress):print("/RKSGroups/LengthByTypeInRvirWC : ",end="",flush=True)

        gihids = self.RSG.RKSGroups.InternalHaloID()
        LengthBTWCInRvir = numpy.zeros((len(gihids),NUM_TYPES))

        halo_pos = self.RSG.RKSGroups.Position()
        halo_rvir = self.RSG.RKSGroups.VirialRadius()/1000 # Kpc to Mpc
        ihid_pos_map = dict(zip(gihids,halo_pos))
        ihid_rvir_map = dict(zip(gihids,halo_rvir))

        def AddCounts(pihids,ppos,column):
            gmask = numpy.isin(pihids,gihids)
            pihids,ppos=pihids[gmask],ppos[gmask]


            rvir_mask = numpy.zeros((len(pihids)))
            # Algorithm-1 : Works but slow.
            # for i,ihid in enumerate(pihids):
            #     if ihid not in gihids:continue
            #     rvir_mask[i] = ( numpy.linalg.norm(ppos[i]-ihid_pos_map[ihid])<ihid_rvir_map[ihid] )

            # Algorithm-2 : Works and fast.
            linked_halo_center = [ihid_pos_map.get(ihid) for ihid in pihids]
            linked_halo_radius = [ihid_rvir_map.get(ihid) for ihid in pihids]
            rvir_mask = numpy.linalg.norm(ppos-linked_halo_center,axis=1)<linked_halo_radius
            
            # print(rvir_mask)
            
            pihids = pihids[rvir_mask]
            # --- Same as without Rvir
            upihids, counts = numpy.unique(pihids,return_counts=True)
            uid_to_count_map=dict(zip(upihids,counts))
            for i,ihid in enumerate(gihids):
                if ihid in upihids:
                    LengthBTWCInRvir[i,column] += uid_to_count_map[ihid]

        r = self.RSG
        AddCounts(r.Gas.InternalHaloID(),r.Gas.Position(),0)
        AddCounts(r.DarkMatter.InternalHaloID(),r.DarkMatter.Position(),1)
        AddCounts(r.Star.InternalHaloID(),r.Star.Position(),4)
        AddCounts(r.BlackHole.InternalHaloID(),r.BlackHole.Position(),5)

        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"LengthByTypeInRvirWC",LengthBTWCInRvir,"Overwrite")
        if(self.show_progress):print("Done")

