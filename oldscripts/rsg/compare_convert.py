import numpy

file1 = open("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64/converted.txt")
file2 = open("/mnt/home/student/cranit/Work/ResetRKSG/RSG_L10N64/halos_PART_017.0.particles")


data1 = numpy.loadtxt(file1)
data2 = numpy.loadtxt(file2)

id1 = data1[:,0]

type2 = data2[:,9]
mask2 = (type2==3)
id2 = data2[:,8][mask2]

print((id1))
print((id2))



file1.close()
file2.close()