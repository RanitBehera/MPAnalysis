## Rockstar Default Parameters

1. Number of default output parameters in `halo.ascii` file.<br>
   57

2. Is it all the parameters in `rockstar-galaxies` or there are extra parameters which it is not outputing by default in halo file?<br>
   Checked that `output_ascii()` function does output 57 parameters.
   - 52/57 are from `struct halo`. The `struct halo` itself has 63 members. So 11 members are not printed. These are : (-----)
   - 3/57 are from `struct extra_halo_info`. The `struct extra_halo_info` itself has 31 members.
   - Rest two are `id+id_offset` and `i`.
## Dumping Criteria
3. What is `i`?<br>
   This is dumped under `idx` column with comment that it is internal debuging quantity. From synatx `i<num_halos`, we guess its for the halo index. In the beginig there is filtering whethere a halo indexed by `i` should be printed. 

4. How does it decide which halos, index by `i`/`idx`, are dumped?<br>
   - First if its not within bound, its not dumped.
   - Then if any last 4 bits of `halo->flag` is 1, its dumped.
   - Then if `SUPPRESS_GALAXIES` (set via rockstar from `config.cfg` file)  and (`halo->type` not dark matter) its not dumped.
   - Finally its not dumped if anyone of the following is true (ORed)
     - `halo->num_p` is less than `MIN_HALO_OUTPUT_SIZE` (set via rockstar `config.cfg` file) 
     - `halo->m` times `UNBOUND_THRESHOLD` is greather than equal to `halo->mgrav`.
     -  `((h->mgrav < 1.5*PARTICLE_MASS) && UNBOUND_THRESHOLD > 0)`
     -  `((MIN_HALO_OUTPUT_MASS>0) && (h->mgrav < MIN_HALO_OUTPUT_MASS)))`
  - Otherwise its dumped.

5. How `bound` is set?

6. How `halo->flag` is set?

7. How `SUPRESS_GALAXIES` is set?
   

8. How `halo->type` is set?

## halos
### id


### num_p
    - only number of dark matters particle in the halo
    - includes gas particles too
    - includes stars too
    - includes bh too

    Its




## Configuration
- MIN_HALO_PARTICLES:
  - It can be mimimum upto 3 particles. 2 particles gives segmentation fault.
- MIN_HALO_OUTPUT_SIZE:
  - It can be minimum upto 0:

