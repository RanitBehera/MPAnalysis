import numpy
from treelib import Tree, Node

TREE_PATH="/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L10N64c/trees/tree_0_0_0.dat"

with open(TREE_PATH) as file:
    lines = file.readlines()

lines=[line for line in lines if not line.startswith("#")]
NUM_TREES = int(lines[0])
lines=lines[1:]

# --- Extract fields
# scale (0,'f'), halo_id (1,'i'), desc_scale (2,'f'), desc_id (3,'i'), prog (4,'i'), orig_halo_id (30,'i') 
scale,halo_id,desc_id,orig_halo_id = numpy.loadtxt(lines,dtype='f',usecols=[0,1,3,30]).T
halo_id,desc_id,orig_halo_id = numpy.int32(halo_id),numpy.int32(desc_id),numpy.int32(orig_halo_id)

br=numpy.where(desc_id==-1)[0]  # break points which separate different trees

# --- Select sepcific tree
tn=6
start,end   = br[tn], br[tn+1]
span        = range(start,end)
scale, halo_id, desc_id, orig_halo_id = scale[span], halo_id[span], desc_id[span], orig_halo_id[span]


# --- Tag to print
def GetTag(i):
    tag=str(halo_id[i]) + " (" + str(orig_halo_id[i]) + " : z="+ str(round(1/scale[i]-1,2))+ ")"
    return tag


# --- Tree
t=Tree()
t.create_node(GetTag(0),halo_id[0])     # Root node with no parent
for i in range(1,len(halo_id)):
    t.create_node(GetTag(i),halo_id[i],parent=desc_id[i])
t.show()