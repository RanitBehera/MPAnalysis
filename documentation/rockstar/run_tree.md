# Run consystent tree
- When you run rockstar in parallel IO mode `out_#.list` files will be generated along with `*.ascii`, `*.bin` and/or `*.particles` files. These `out_#.list` files are already in correct input format.
- Note that there are three configuration `*.cfg` files when you run the `rockstar` or `rockstar-galaxies`.
  - Say, for example, `runconfig.cfg` config file you write and feed to master process to run it. Here you write the output path in `OUTBASE` flag.
  - Master process creates `auto-rockstar.cfg` config file, which you feed to worker (read/write) process, so that master process accepts connection.
  - The `rockstar.cfg` files generated in the output path when the codes run. usually this file will be alongside the `*.ascii`,`*.bin`,`*.particles`,`*.list` files.
- In `rockstar` or `rockstar-galaxies` find `/rockstar/scripts/gen_merger_cfg.pl` which is perl script file.
- Run this with
  ```bash
  perl /path/to/rockstar/scripts/gen_merger_cfg.pl <rockstar.cfg>
  ```
  Here `<rockstar.cfg>` is the file generated in the output of `rockstar` or `rockstar-galaxies` folder. This is the third config file in our example above.
- An run example (in rockstar folder as recommended)
  ```
  [cranit@ln4 rockstar-galaxies]$ perl scripts/gen_merger_cfg.pl /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/rockstar.cfg
  ```
  This will output
  ```
  Skipping /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/out_0.list (too few halos).
    Skipping /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/out_1.list (too few halos).
    Merger tree config file generated in /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/outputs/merger_tree.cfg

    To generate a merger tree, change to the consistent_trees directory and run
        make
        perl do_merger_tree_np.pl /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/outputs/merger_tree.cfg

    Trees will be generated in
    /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/trees

    Note that if /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c is not accessible from the machine you intend to run the merger tree code on, you will have to change the directories in /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/outputs/merger_tree.cfg appropriately.
  ```
- As mentioned, switch to `consistent-trees` folder, and run `make` to build it if you have not.
- Then copy the command as mentioned in above output and run
  ```
  perl do_merger_tree_np.pl /mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/outputs/merger_tree.cfg
  ```
- Switch back to rockstar output folder (the `OUTBASE` flag one) and you will find the `trees` folder (which is also mentioned in the above output).
- The files of intrest are within this folder as
  - `trees/forests.list` 
  - `trees/locations.dat` 
  - `trees/tree_0_0_0.dat`

