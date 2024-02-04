import galspec

galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10Mpc_N64c/output/"
sim = galspec.InitConfig()


pos=sim.PART(17).DarkMatter.Position()

with open("/mnt/home/student/cranit/Work/TestDebug/p17.asc",'w') as f:
    for p in pos:
        f.write(str(p[0]/100) + " " + str(p[1]/100) + " " + str(p[2]/100) + " 1 0 0\n" )
        f.write(str(p[0]/100) + " " + str(p[1]/100) + " " + str(p[2]/100) + " 1 0 0\n" )
        f.write(str(p[0]/100) + " " + str(p[1]/100) + " " + str(p[2]/100) + " 1 0 0\n" )
        f.write(str(p[0]/100) + " " + str(p[1]/100) + " " + str(p[2]/100) + " 1 0 0\n" )
        f.write(str(p[0]/100) + " " + str(p[1]/100) + " " + str(p[2]/100) + " 1 0 0\n" )
    