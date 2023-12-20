# from ete3 import Tree,TreeStyle, TextFace, NodeStyle
from ete3 import Tree, TreeStyle, TextFace, NodeStyle
import numpy as np


# file=open("tree_0_0_0.dat")
file=open("/mnt/home/student/cranit/Work/Merger_Tree_WNum/RKSG_L10N64c/trees/tree_0_0_0.dat")
lines=file.readlines()
file.close()

lines=[line for line in lines if not line.startswith("#")]
lines=lines[1:]

scale=np.loadtxt(lines,dtype='f',usecols=0)
halo_id=np.loadtxt(lines,dtype='i',usecols=1)
desc_scale=np.loadtxt(lines,dtype='f',usecols=2)
desc_id=np.loadtxt(lines,dtype='i',usecols=3)
prog=np.loadtxt(lines,dtype='i',usecols=4)

stops=np.where(desc_id==-1)[0]

# print(stops)

#tree_no
tn=0

# Validation : Handle last tree case

scale=scale[stops[tn]:stops[tn+1]]
halo_id=halo_id[stops[tn]:stops[tn+1]]
desc_scale=desc_scale[stops[tn]:stops[tn+1]]
desc_id=desc_id[stops[tn]:stops[tn+1]]
prog=prog[stops[tn]:stops[tn+1]]


# Build tree

def AddChildren(node:Tree,hid):
    hindex=np.where(halo_id==hid)
    prog_num=prog[hindex]
    hscale=scale[hindex]
    
    if prog_num==0: # Leaf
        n=node.add_child(name=str(hid))
    else:
        prog_id=halo_id[np.where(desc_id==hid)]
        n=node.add_child(name=str(hid))

        for pid in prog_id:
            AddChildren(n,pid)

    n.add_face(TextFace(" "+str(hid) + " ",fsize=40),column=0,position="branch-right")


t=Tree()
root_hid=halo_id[0]
AddChildren(t,root_hid)




# Tree Style
ts=TreeStyle()
ts.show_leaf_name = False
ts.show_branch_length = False
ts.show_branch_support = False
ts.scale=160
ts.branch_vertical_margin = 20
# ts.rotation = 90
# ts.mode = "c"
# ts.arc_start = -180 # 0 degrees = 3 o'clock
# ts.arc_span = 180

ts.title.add_face(TextFace("Merger Tree", fsize=40), column=0)


# Node Style
nstyle = NodeStyle()
nstyle["shape"] = "circle"
nstyle["size"] = 40
nstyle["fgcolor"] = "#000000"
nstyle["hz_line_type"] = 0
nstyle["vt_line_type"] = 0
nstyle["hz_line_width"] = 5
nstyle["vt_line_width"] = 5
nstyle["hz_line_color"] = "#000000"
nstyle["vt_line_color"] = "#000000"

for n in t.traverse():
   n.set_style(nstyle)

t.set_style(None)


# t.show(tree_style=ts)
t.render("/mnt/home/student/cranit/Work/Merger_Tree_WSFR_Mod/Results/my_tree.png", w=183, h=183, units="mm")







