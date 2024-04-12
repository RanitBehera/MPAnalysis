from ete3 import Tree,TreeStyle, TextFace, NodeStyle
import numpy as np


file=open("tree_0_0_0.dat")
lines=file.readlines()
file.close()

lines=[line for line in lines if not line.startswith("#")]
lines=lines[1:]

scale=np.loadtxt(lines,dtype='f',usecols=0)
halo_id=np.loadtxt(lines,dtype='i',usecols=1)
desc_scale=np.loadtxt(lines,dtype='f',usecols=2)
desc_id=np.loadtxt(lines,dtype='i',usecols=3)
prog=np.loadtxt(lines,dtype='i',usecols=4)
mass=np.loadtxt(lines,dtype='f',usecols=10)

stops=np.where(desc_id==-1)[0]

# print(stops)

#tree_no
tn=2

# Validation : Handle last tree case

scale=scale[stops[tn]:stops[tn+1]]
halo_id=halo_id[stops[tn]:stops[tn+1]]
desc_scale=desc_scale[stops[tn]:stops[tn+1]]
desc_id=desc_id[stops[tn]:stops[tn+1]]
prog=prog[stops[tn]:stops[tn+1]]
mass=mass[stops[tn]:stops[tn+1]]


col_scalar =np.log10(mass) 
# col_scalar =scale

cs_min=min(col_scalar)
cs_max=max(col_scalar)

def GetRGB(scalar):
    norm_scalar=(scalar-cs_min)/(cs_max-cs_min)
    # print(norm_scalar)
    a=norm_scalar/0.25

    X=np.floor(a)
    Y=np.floor(255*(a-X))
    r=0;g=0;b=0
    if(X==0): r=255;g=Y;b=0
    elif(X==1):r=255-Y;g=255;b=0
    elif(X==2):r=0;g=255;b=Y
    elif(X==3):r=0;g=255-Y;b=255
    elif(X==4):r=0;g=0;b=255
    
    def clamp(x): 
        return max(0, min(x, 255))
    
    color='#%02x%02x%02x' % (int(clamp(r)),int(clamp(g)),int(clamp(b)))
    return color



# face style
def NodeVis(t:Tree,col_scalar):
    nstyle = NodeStyle()
    nstyle["shape"] = "circle"
    nstyle["size"] = 40
    nstyle["fgcolor"] = GetRGB(col_scalar) #"#000000"
    nstyle["hz_line_type"] = 0
    nstyle["vt_line_type"] = 0
    nstyle["hz_line_width"] = 5
    nstyle["vt_line_width"] = 5
    nstyle["hz_line_color"] = "#000000"
    nstyle["vt_line_color"] = "#000000"

    t.set_style(nstyle)



# Build tree

def AddChildren(node:Tree,hid):
    hindex=np.where(halo_id==hid)
    prog_num=prog[hindex]
   
    hcol_scalar=col_scalar[hindex]


    if prog_num==0: # Leaf
        n=node.add_child(name=str(hid))
    else:
        prog_id=halo_id[np.where(desc_id==hid)]
        n=node.add_child(name=str(hid))
        for pid in prog_id:
            AddChildren(n,pid)

    NodeVis(n,hcol_scalar)
    n.add_face(TextFace(" "+str(hid) + " ",fsize=40),column=0,position="branch-right")


t=Tree()
root_hid=halo_id[0]
AddChildren(t,root_hid)




# Tree Style
ts=TreeStyle()
ts.show_leaf_name = False
ts.show_branch_length = False
ts.show_branch_support = False
ts.show_scale = False
ts.scale=160
ts.branch_vertical_margin = 20
# ts.rotation = 90
# ts.mode = "c"
# ts.arc_start = -180 # 0 degrees = 3 o'clock
# ts.arc_span = 180

ts.title.add_face(TextFace("Merger Tree", fsize=80), column=3)



















# Node Style
# nstyle = NodeStyle()
# nstyle["shape"] = "circle"
# nstyle["size"] = 40
# nstyle["fgcolor"] = GetRGB(0.5) #"#000000"
# nstyle["hz_line_type"] = 0
# nstyle["vt_line_type"] = 0
# nstyle["hz_line_width"] = 5
# nstyle["vt_line_width"] = 5
# nstyle["hz_line_color"] = "#000000"
# nstyle["vt_line_color"] = "#000000"

# for n in t.traverse():
#    n.set_style(nstyle)

t.set_style(None)


t.show(tree_style=ts)
# t.render("mytree.png", w=300, units="mm",dpi=200)
# t.render("mytree.svg", w=300)







