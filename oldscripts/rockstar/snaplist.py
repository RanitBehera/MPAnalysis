import os

dir     = str(input("Directory : "))
start   = int(input("Starting Snap : "))
end     = int(input("Ending Snap : "))

with open(dir + os.sep + "snaplist.txt","w") as f:
    for s in range(start,end+1):
        f.write("PART_" + '{:03}'.format(s) + ".hdf5" + "\n")

print("Output : " + dir + os.sep + "snaplist.txt")