import galspec
import time


ITTER   = 10000
SNAP    = 17


sim=galspec.InitConfig()

# --- Numpy
npstart=time.time()
for i in range(ITTER):
    n=(sim.PART(SNAP).DarkMatter.Position.NValue())
npend=time.time()
nptook=npend-npstart

# --- BigFile
bfstart=time.time()
for i in range(ITTER):
    b=(sim.PART(SNAP).DarkMatter.Position.BValue())
bfend=time.time()
bftook=bfend-bfstart

# --- Report
print("\n")
print("Box : ",galspec.CONFIG.MPGADGET_OUTPUT_DIR)
print("Reading","PART_017 >","Darkmatter >","Position")
print("\n")
print("For "+str(ITTER)+" itterations:")
print("\t - 'numpy' took".ljust(32)  ," : ",round(nptook,3)," seconds")
print("\t - 'bigfile' took".ljust(32)," : ",round(bftook,3)," seconds")
print("\n")









