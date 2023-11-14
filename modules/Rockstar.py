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