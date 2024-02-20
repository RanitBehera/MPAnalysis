import os,numpy
from galspec.navigation.MPGADGET.RSG.RSG import _RSG
from galspec.navigation.MPGADGET.PART.PART import _PART
from galspec.IO.BinaryFile import WriteField


NUM_TYPES = 6   # Number of particle types in MPGADGET


class PP_RSG:
    def __init__(self,path,linked_part_path:None,show_progress=True) -> None:
        self.RSG = _RSG(path)
        self.PART =  _PART(linked_part_path)
        self.show_progress = show_progress


    def StartAll(self):
        if(self.show_progress):print(" GENERATING FIELDS ".center(30,'='))
        self.LengthByTypeWC()
        self.LengthByTypeInRvirWC()     # Also adds MassByTypeInRvirWC()
        self.StarFormationRate()


    def LengthByTypeWC(self):
        if(self.show_progress):print("/RKSGroups/LengthByTypeWC : ",end="",flush=True)
        # Get all exported halo ids
        gihids = self.RSG.RKSGroups.InternalHaloID()
        # Form and emptry array to fill in counts
        LengthBTWC = numpy.zeros((len(gihids),NUM_TYPES))
        # general counting function for any particle type
        # input is list of particle type ihid
        def AddCounts(pihids,column):
            # get unique ihids and corresponding counts for that particle type
            upihids, counts = numpy.unique(pihids,return_counts=True)
            # Here the unique ihids may contain element other than those in group ihid
            # This is due to suppressed halos in group ihid
            # So we form a dictionary for one to one correspondence
            upihid_to_count_map=dict(zip(upihids,counts))
            # Then for each group ihid we look for corresponding count in the dictionary and add it
            for i,gihid in enumerate(gihids):
                # one particular gihid may not be in upihid 
                # if that halo is of different particle type, hence validation
                if gihid in upihids: LengthBTWC[i,column] += upihid_to_count_map[gihid]
        AddCounts(self.RSG.Gas.InternalHaloID(),0)
        AddCounts(self.RSG.DarkMatter.InternalHaloID(),1)
        AddCounts(self.RSG.Star.InternalHaloID(),4)
        AddCounts(self.RSG.BlackHole.InternalHaloID(),5)

        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"LengthByTypeWC",LengthBTWC,"Overwrite")
        if(self.show_progress):print("Done")

        

    def LengthByTypeInRvirWC(self):
        if(self.show_progress):print("/RKSGroups/LengthByTypeInRvirWC : ",end="",flush=True)

        gihids = self.RSG.RKSGroups.InternalHaloID()
        LengthBTInRvirWC = numpy.zeros((len(gihids),NUM_TYPES))

        halo_pos = self.RSG.RKSGroups.Position()
        halo_rvir = self.RSG.RKSGroups.VirialRadius()/1000 # Kpc to Mpc
        ihid_pos_map = dict(zip(gihids,halo_pos))
        ihid_rvir_map = dict(zip(gihids,halo_rvir))

        def AddCounts(pihids,ppos,column):
            # Filter for all particle type ihid rows which are there in group ihid
            gmask = numpy.isin(pihids,gihids)
            pihids,ppos=pihids[gmask],ppos[gmask]
            # initialise opaque rvir mask
            rvir_mask = numpy.zeros((len(pihids)))
            # form corresponding halo center and rvir column
            linked_halo_center = [ihid_pos_map.get(ihid) for ihid in pihids]
            linked_halo_radius = [ihid_rvir_map.get(ihid) for ihid in pihids]
            # update rvir mask by comparing distance
            rvir_mask = numpy.linalg.norm(ppos-linked_halo_center,axis=1)<linked_halo_radius
            # Filter particle type ihids again with rvir mask
            pihids = pihids[rvir_mask]
            # Then do the same as count without rvir mask
            upihids, counts = numpy.unique(pihids,return_counts=True)
            upihid_to_count_map=dict(zip(upihids,counts))
            for i,ihid in enumerate(gihids):
                if ihid in upihids:
                    LengthBTInRvirWC[i,column] += upihid_to_count_map[ihid]
                    
        s = self.RSG
        AddCounts(s.Gas.InternalHaloID(),s.Gas.Position(),0)
        AddCounts(s.DarkMatter.InternalHaloID(),s.DarkMatter.Position(),1)
        AddCounts(s.Star.InternalHaloID(),s.Star.Position(),4)
        AddCounts(s.BlackHole.InternalHaloID(),s.BlackHole.Position(),5)

        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"LengthByTypeInRvirWC",LengthBTInRvirWC,"Overwrite")
        if(self.show_progress):print("Done")

        # MassByTypeInRvirWC
        if(self.show_progress):print("/RKSGroups/MassByTypeInRvirWC : ",end="",flush=True)
        mass_table = self.RSG.Attribute.MassTable()
        M_gas   = LengthBTInRvirWC[:,0] * mass_table[0]
        M_dm    = LengthBTInRvirWC[:,1] * mass_table[1]
        M_u1    = LengthBTInRvirWC[:,2] * mass_table[2]
        M_u2    = LengthBTInRvirWC[:,3] * mass_table[3]
        M_star  = LengthBTInRvirWC[:,4] * mass_table[4]
        M_bh    = LengthBTInRvirWC[:,5] * mass_table[5]
        MassBTInRvirWC = numpy.column_stack([M_gas,M_dm,M_u1,M_u2,M_star,M_bh])
        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"MassByTypeInRvirWC",MassBTInRvirWC,"Overwrite")
        if(self.show_progress):print("Done")


    def StarFormationRate(self):
        if(self.show_progress):print("/RKSGroups/StarFormationRate : ",flush=True)
        
        # Get (id,ihid) of all Group gas particles
        gpids = self.RSG.Gas.ID()
        gpihids = self.RSG.Gas.InternalHaloID()
        # Note that these IDs are not unique.
        # The same particle is again output as child ...
        # when any of its hierarchical-parent is target for output.
        # All of those hierarchical-parent have different ihid however.
        # So get all output ihid, which are unique from group data.
        ihids = self.RSG.RKSGroups.InternalHaloID()
        # now we filter gpihids for elements such that its in ihids.
        # it will remove sub halos which got supressed
        mask = numpy.isin(gpihids,ihids)
        gpids,gpihids = gpids[mask],gpihids[mask]
        
        # Our end goal is to assign sfr to these ihids.
        # So lets form dict to easily update linked sfr, initilised to zero.
        ihid_sfr_map = dict(zip(ihids,numpy.zeros(len(ihids))))
        
        # Now get all (id,sfr) pair from corresponding part snap.
        box_gpids = self.PART.Gas.ID()
        box_gpsfr  = self.PART.Gas.StarFormationRate()
        # these ids are unique. 
        # So we could zip them now. But we will filter first.
        # So we fiter for those box ids which are present in grouping data.  
        mask = numpy.isin(numpy.int64(box_gpids),numpy.int64(gpids))
        box_gpids = box_gpids[mask]  
        box_gpsfr  = box_gpsfr[mask]  
        # Now we can zip them.
        box_gid_sfr_map = dict(zip(box_gpids,box_gpsfr))
        # Now we can cross check for its length.
        # Its length should be always less than length of group gpids
        # as there are no duplicate ids
        print("   CROSS CHECK 1 : ","Success." if len(box_gpids)<=len(gpids) else "Failed.",flush=True)
        if len(box_gpids)>len(gpids):return
        # Now we itterate throw for every element of gpids and gpihid 
        # look where it is in box_gpids, get corresponding box_gpsfr
        # and add it to ihid_sfr_map for that gpihid
        # the last two operations are easily done by the dict we formed
        for gpid,gpihid in numpy.column_stack((gpids,gpihids)):
            gpsfr=box_gid_sfr_map[gpid]
            ihid_sfr_map[gpihid] += gpsfr
        
        IHID_SFR= list(ihid_sfr_map.values())
        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"StarFormationRate",IHID_SFR,"Overwrite")
        if(self.show_progress):print("Done")
            








