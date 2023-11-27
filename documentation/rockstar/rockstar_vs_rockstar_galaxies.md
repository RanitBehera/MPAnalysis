# Rockstar Benchmark

In this study we analyse the output of following two halo finder softwares
- rockstar (RKS)
- rockstar-galaxies (RKSG)

The **rockstar** supports only single-mass particles while **rockstar-galaxies** supports multi-mass particles. So the former only accepts one type of particles (typically dark-matter), while the later accepts all types of particles.

### Orig:
These two softwares accept GADGET format natively but MP-GADGET format. To feed MP-GADGET format, we convert the directory structure to HDF5 format whose details will be shared in corresponding section.

### Mod:
However, for convenience we added suuport for direct feeding of MP-GADGET data by modifing respective files, again whose details will be shared in corresponding section.

## Step 1 : Create Directory Structure
- RKS_Benchmark
  - data
    - MP-GADGET
      - L10N64c_PART_017
      - L10N64c_PIG_017
      - L50N640c_PART_036
      - L50N640c_PIG_036
    - RKS_Orig
    - RKS_Mod
    - RKSG_Orig
    - RKSG_Mod
  - software
    - RKS_Orig
    - RKS_Mod
    - RKSG_Orig
    - RKSG_Mod 
  - libs
    - tirpc
  - results 



## Step 2 : Get Snapshot
For testing both software builds we have the small L10N64c box. However, primary benchmark will be done on L50N640c box. Note that due to resource avialability we will be running the softwares for L50N640c box on pegasus and download the data to local system for analysis.

## Step 3 : Build softwares 

Do `git clone https://bitbucket.org/gfcstanford/rockstar.git` in following two folders.
- RKS_Orig
- RKS_Mod

Do `git clone https://bitbucket.org/pbehroozi/rockstar-galaxies.git` in following two folders.
- RKSG_Orig
- RKSG_Mod

For the two "RKS_Orig" and "RKSG_Orig" build it. Please look for "rockstar_build.md" for details. Make sure to build `with_hdf5`.

For the two "RKS_Mod" and "RKSG_Mod" modify it to accept MP-GADGET directly and then build. Please look for "MPGADGET_input_support" for details.

## Step 4 : Modify the softwares.
Look for "rockstar_io_mpgadget" for details.

## Step 5: Run

