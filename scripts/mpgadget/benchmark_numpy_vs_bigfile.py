import galspec
import time

sim=galspec.InitConfig()

ITTER = 1

# --- Numpy
npstart=time.time()
for i in range(ITTER):
    n=(sim.PART(36).DarkMatter.Position.NValue())
npend=time.time()
nptook=npend-npstart

# --- BigFile
bfstart=time.time()
for i in range(ITTER):
    b=(sim.PART(36).DarkMatter.Position.BValue())
bfend=time.time()
bftook=bfend-bfstart

# --- Report
print("Box : ",galspec.CONFIG.MPGADGET_OUTPUT_DIR)
print("Reading","PART_036 >","Darkmatter >","Position")

print("For "+str(ITTER)+" itterations; 'numpy' took".ljust(32)  ," : ",nptook," seconds")
print("For "+str(ITTER)+" itterations; 'bigfile' took".ljust(32)," : ",bftook," seconds")









