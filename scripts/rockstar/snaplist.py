start=input("Starting Snap : ")
end=input("Ending Snap : ")

with open("snaplist.txt","w") as f:
    for s in range(start,end+1):
        f.write("PART_"+'{:03}'.format(s)+"\n")

print("Output : snaplist.txt")