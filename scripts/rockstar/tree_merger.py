import numpy,os
import galspec.mpgadget as mpg
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
tn=1
start,end   = br[tn], br[tn+1]
span        = range(start,end)
scale, halo_id, desc_id, orig_halo_id = scale[span], halo_id[span], desc_id[span], orig_halo_id[span]


# --- Tag to print
def GetTag(i):
    # Tree HID
    # tag=str(halo_id[i])

    # Snap HID
    # tag=str(orig_halo_id[i])
    
    # Redshift
    # tag = str(round((1/scale[i]-1),2))
    
    # Snap Num
    # tag = str(mpg.get_snapshot_number_from_time(scale[i]))
    
    # Snap Num (Redshift) + Snap HID
    # tag = "S" + str(mpg.get_snapshot_number_from_time(scale[i]))
    # tag += "(z=" + str(round((1/scale[i]-1),2)) + ")"
    # tag += " : "
    # tag += "HID-" + str(orig_halo_id[i])

    # Snap Num (Redshift) + Snap HID + SFR
    sn=mpg.get_snapshot_number_from_time(scale[i])
    tag = ""
    # tag += "S" + str(mpg.get_snapshot_number_from_time(scale[i]))
    # tag += "z=" + str(round((1/scale[i]-1),2)) + ""
    # tag += ":"
    # tag += "HID-" + str(orig_halo_id[i])
    # tag += " " + chr(9472)*5 + chr(9675) +" "

    part_fixed=mpg.get_fixed_format_snapshot_number(sn)
    part_file_name = "halos_PART_" + part_fixed + ".0.particles"
    rksg_part_path = "/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/RKSG_L10N64c"
    part_file_path = rksg_part_path + os.sep + part_file_name
    mvir,ndm,ngas,nstar,nbh,sfr,aihid,ihid,ehid = numpy.loadtxt(part_file_path).T
    index=numpy.where(ehid==orig_halo_id[i])
    # tag += " (" + str(int(ndm[index][0])) + "," + str(int(ngas[index][0])) + "," + str(int(nstar[index][0])) + "," +str(int(nbh[index][0])) + ") "
    tag += "SFR = "
    try:
        tag += str((sfr[index])[0])
    except:
        tag += ""


    return tag


# --- Tree
t=Tree()
t.create_node(GetTag(0),halo_id[0])     # Root node with no parent
for i in range(1,len(halo_id)):
    t.create_node(GetTag(i),halo_id[i],parent=desc_id[i])
t.show()