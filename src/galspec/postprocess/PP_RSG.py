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
        self.LengthByTypeInRvirWC() # Also outputs MassByTypeInRvirWC
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
        MassBTInRvirWC = numpy.zeros((len(gihids),NUM_TYPES))

        halo_pos = self.RSG.RKSGroups.Position()
        halo_rvir = self.RSG.RKSGroups.VirialRadius()/1000 # Kpc to Mpc
        ihid_pos_map = dict(zip(gihids,halo_pos))
        ihid_rvir_map = dict(zip(gihids,halo_rvir))

        def AddCounts(pihids,ppos,pmass,column):
            # Filter for all particle type ihid rows which are there in group ihid
            gmask = numpy.isin(pihids,gihids)
            pihids,ppos,pmass=pihids[gmask],ppos[gmask],pmass[gmask]
            # initialise opaque rvir mask
            rvir_mask = numpy.zeros((len(pihids)))
            # form corresponding halo center and rvir column - particle wise row
            linked_halo_center = [ihid_pos_map.get(ihid) for ihid in pihids]
            linked_halo_radius = [ihid_rvir_map.get(ihid) for ihid in pihids]
            # update rvir mask by comparing distance
            rvir_mask = numpy.linalg.norm(ppos-linked_halo_center,axis=1)<linked_halo_radius
            # Filter particle type ihids again with rvir mask
            pihids = pihids[rvir_mask]
            # mass lookup table
            pmass = pmass[rvir_mask]

 
            # Then do the same as ordinary count without rvir mask
            upihids, counts = numpy.unique(pihids,return_counts=True)
            upihid_to_count_map=dict(zip(upihids,counts))
            for i,ihid in enumerate(gihids):
                if ihid in upihids:
                    LengthBTInRvirWC[i,column] += upihid_to_count_map[ihid]

            # Now distribute masses
            gihid_to_mass_map=dict(zip(gihids,numpy.zeros(len(gihids))))
            for i,pihid in enumerate(pihids):
                gihid_to_mass_map[pihid] += pmass[i]
            MassBTInRvirWC[:,column] = numpy.array(list(gihid_to_mass_map.values()))
                    
        s = self.RSG
        AddCounts(s.Gas.InternalHaloID(),s.Gas.Position(),s.Gas.Mass(),0)
        AddCounts(s.DarkMatter.InternalHaloID(),s.DarkMatter.Position(),s.DarkMatter.Mass(),1)
        AddCounts(s.Star.InternalHaloID(),s.Star.Position(),s.Star.Mass(),4)
        AddCounts(s.BlackHole.InternalHaloID(),s.BlackHole.Position(),s.BlackHole.Mass(),5)

        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"LengthByTypeInRvirWC",LengthBTInRvirWC,"Overwrite")
        if(self.show_progress):print("Done")

        # MassByTypeInRvirWC
        if(self.show_progress):print("/RKSGroups/MassByTypeInRvirWC : ",end="",flush=True)
        # mass_table = self.RSG.Attribute.MassTable()
        # M_gas   = LengthBTInRvirWC[:,0] * mass_table[0]
        # M_dm    = LengthBTInRvirWC[:,1] * mass_table[1]
        # M_u1    = LengthBTInRvirWC[:,2] * mass_table[2]
        # M_u2    = LengthBTInRvirWC[:,3] * mass_table[3]
        # M_star  = LengthBTInRvirWC[:,4] * mass_table[4]
        # M_bh    = LengthBTInRvirWC[:,5] * mass_table[5]
        # MassBTInRvirWC = numpy.column_stack([M_gas,M_dm,M_u1,M_u2,M_star,M_bh])
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
            # gpsfr=box_gid_sfr_map[gpid]
            ihid_sfr_map[gpihid] += box_gid_sfr_map[gpid]
        
        IHID_SFR= list(ihid_sfr_map.values())
        WriteField(os.path.join(self.RSG.path,"RKSGroups"),"StarFormationRate",IHID_SFR,"Overwrite")
        if(self.show_progress):print("Done")

    def StellarMetallicity(self):
        if(self.show_progress):print("/RKSGroups/StellarMetallicity : ",flush=True)
        try:
            IHID_STAR_COUNT = self.RSG.RKSGroups.LengthByTypeInRvirWC()[:,4]
        except: 
            print("ERROR : No LengthByTypeInRVirWC field found,")
            return
        
        # Get (id,ihid) of all Group star particles
        spids = self.RSG.Star.ID()
        spihids = self.RSG.Star.InternalHaloID()
        # Note that these IDs are not unique.
        # The same particle is again output as child ...
        # when any of its hierarchical-parent is target for output.
        # All of those hierarchical-parent have different ihid however.
        # So get all output ihid, which are unique from group data.
        ihids = self.RSG.RKSGroups.InternalHaloID()
        # now we filter gpihids for elements such that its in ihids.
        # it will remove sub halos which got supressed
        mask = numpy.isin(spihids,ihids)
        spids,spihids = spids[mask],spihids[mask]
        
        # Our end goal is to assign sfr to these ihids.
        # So lets form dict to easily update linked sfr, initilised to zero.
        ihid_met_map = dict(zip(ihids,numpy.zeros(len(ihids))))
        
        # Now get all (id,sfr) pair from corresponding part snap.
        box_spids   = self.PART.Star.ID()
        box_spmet   = self.PART.Star.Metallicity()

        # these ids are unique. 
        # So we could zip them now. But we will filter first.
        # So we fiter for those box ids which are present in grouping data.  
        mask = numpy.isin(numpy.int64(box_spids),numpy.int64(spids))
        box_spids   = box_spids[mask]  
        box_spmet   = box_spmet[mask]
        # Now we can zip them.
        box_gid_met_map = dict(zip(box_spids,box_spmet))
        # Now we can cross check for its length.
        # Its length should be always less than length of group gpids
        # as there are no duplicate ids
        print("   CROSS CHECK 1 : ","Success." if len(box_spids)<=len(spids) else "Failed.",flush=True)
        if len(box_spids)>len(spids):return
        # Now we itterate throw for every element of gpids and gpihid 
        # look where it is in box_gpids, get corresponding box_gpsfr
        # and add it to ihid_sfr_map for that gpihid
        # the last two operations are easily done by the dict we formed
        for spid,spihid in numpy.column_stack((spids,spihids)):
            # gpsfr=box_gid_sfr_map[gpid]
            ihid_met_map[spihid] += box_gid_met_map[spid]
        
        IHID_SMET = list(ihid_met_map.values())

        # Check if lengths match before dividing for average
        print("   CROSS CHECK 2 : ","Success." if len(IHID_SMET)==len(IHID_STAR_COUNT) else "Failed.",flush=True)
        if len(IHID_SMET)!=len(IHID_STAR_COUNT):return
        
        # Validate for no stars
        nostar_mask = (IHID_STAR_COUNT==0.0)
        val1=sum(IHID_STAR_COUNT[nostar_mask])
        val2=max(numpy.array(IHID_SMET)[nostar_mask])
        # val=val1+val2

        for i,val in enumerate(numpy.array(IHID_SMET)[nostar_mask]):
            if val!=0:
                print(i,val)

        # print("   CROSS CHECK 3 : ","Success." if val==0 else "Failed.",flush=True)
        # if val!=0:return
        
        # IHID_SMET[~nostar_mask] /= IHID_STAR_COUNT[~nostar_mask]
        
        import matplotlib.pyplot as plt
        plt.hist(numpy.array(IHID_SMET)[nostar_mask],bins=numpy.arange(0,0.25,0.01))
        plt.show()

        # WriteField(os.path.join(self.RSG.path,"RKSGroups"),"StellarMetallicity",IHID_SMET,"Overwrite")
        if(self.show_progress):print("Done")




    # def MassByTypeInRvirWC(self):
    #     if(self.show_progress):print("/RKSGroups/MassByTypeInRvirWC2 : ",end="",flush=True)
        
    #     # get dumped ihids for filtering suppresed halos
    #     gihids = self.RSG.RKSGroups.InternalHaloID()

    #     halo_pos = self.RSG.RKSGroups.Position()
    #     halo_rvir = self.RSG.RKSGroups.VirialRadius() /1000 # Kpc to Mpc
    #     ihid_pos_map = dict(zip(gihids,halo_pos))
    #     ihid_rvir_map = dict(zip(gihids,halo_rvir))


    #     # Read relavant fields
    #     gas_ihids   = self.RSG.Gas.InternalHaloID()
    #     dm_ihids    = self.RSG.DarkMatter.InternalHaloID()
    #     star_ihids  = self.RSG.Star.InternalHaloID()
    #     bh_ihids    = self.RSG.BlackHole.InternalHaloID()

    #     gas_mass    = self.RSG.Gas.Mass()
    #     dm_mass     = self.RSG.DarkMatter.Mass()
    #     star_mass   = self.RSG.Star.Mass()
    #     bh_mass     = self.RSG.BlackHole.Mass()

    #     gas_pos     = self.RSG.Gas.Position()
    #     dm_pos      = self.RSG.DarkMatter.Position()
    #     star_pos    = self.RSG.Star.Position()
    #     bh_pos      = self.RSG.BlackHole.Position()


    #     # create masks for filtering supressed halos
    #     gas_mask    = numpy.isin(numpy.int64(gas_ihids),numpy.int64(gihids))
    #     dm_mask     = numpy.isin(numpy.int64(dm_ihids),numpy.int64(gihids))
    #     star_mask   = numpy.isin(numpy.int64(star_ihids),numpy.int64(gihids))
    #     bh_mask     = numpy.isin(numpy.int64(bh_ihids),numpy.int64(gihids))

    #     # filter with the created mask
    #     gas_ihids,dm_ihids,star_ihids,bh_ihids = gas_ihids[gas_mask],dm_ihids[dm_mask],star_ihids[star_mask],bh_ihids[bh_mask]
    #     gas_mass,dm_mass,star_mass,bh_mass = gas_mass[gas_mask],dm_mass[dm_mask],star_mass[star_mask],bh_mass[bh_mask]

    #     # distribute mass to corresponding ihid bins
    #     rows = len(gihids)
    #     def Distribute(type_ihids,type_masses):
    #         ihid_tmass_map = dict(zip(gihids,numpy.zeros(rows)))
    #         for i,tihid in enumerate(type_ihids):
    #             ihid_tmass_map[tihid] += type_masses[i] 
    #         return numpy.array(list(ihid_tmass_map.values()))

        
    #     M_gas   = Distribute(gas_ihids,gas_mass)
    #     M_dm    = Distribute(dm_ihids,dm_mass)
    #     M_star  = Distribute(star_ihids,star_mass)
    #     M_bh    = Distribute(bh_ihids,bh_mass)
    #     M_u1    = numpy.zeros((rows,1))
    #     M_u2    = numpy.zeros((rows,1))

    #     MassUnit = 1e10         # <--- Auto detect this 

    #     MassBTInRvirWC = numpy.column_stack([M_gas,M_dm,M_u1,M_u2,M_star,M_bh])/MassUnit
    #     WriteField(os.path.join(self.RSG.path,"RKSGroups"),"MassByTypeInRvirWC2",MassBTInRvirWC,"Overwrite")
    #     if(self.show_progress):print("Done") 






