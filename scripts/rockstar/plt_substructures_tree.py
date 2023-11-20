import sys,os, numpy
from ete3 import Tree,TreeStyle, TextFace, NodeStyle

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
FOCUS_EHID              = 2088  # most massive : 3972,2088,7444,6143,1250
SUBSTRUC_LIMIT          = 5

# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME

# --- DATA FILTERS
data=numpy.loadtxt(PFILEPATH)

def Get_IHID(EHID):
    ehid=numpy.int64(data[:,mp.particles.external_haloid])
    ihid=numpy.int64(data[:,mp.particles.internal_haloid])
    return ihid[ehid==EHID][0]

def Get_aIHIDs(IHID):
    ihid=numpy.int64(numpy.int64(data[:,mp.particles.internal_haloid]))
    aihid=numpy.int64(numpy.int64(data[:,mp.particles.assigned_internal_haloid]))
    u,c=numpy.unique(aihid[ihid==IHID],return_counts=True)
    # print(u);print(c)
    sort=numpy.argsort(c)[::-1][0:SUBSTRUC_LIMIT]
    u,c=u[sort],c[sort]
    # print(u);print(c)
    return u

def GetRow_Mask(AIHID,type):
    aihid=numpy.int64(numpy.int64(data[:,mp.particles.assigned_internal_haloid]))
    types=numpy.int64(numpy.int64(data[:,mp.particles.type]))
    aihid_mask=(aihid==AIHID)
    type_mask=(types==type)
    return aihid_mask & type_mask




# --- Tree
# face style

# col_scalar =np.log10(mass) 

# cs_min=min(col_scalar)
# cs_max=max(col_scalar)

# def GetRGB(scalar):
#     norm_scalar=(scalar-cs_min)/(cs_max-cs_min)
#     # print(norm_scalar)
#     a=norm_scalar/0.25

#     X=np.floor(a)
#     Y=np.floor(255*(a-X))
#     r=0;g=0;b=0
#     if(X==0): r=255;g=Y;b=0
#     elif(X==1):r=255-Y;g=255;b=0
#     elif(X==2):r=0;g=255;b=Y
#     elif(X==3):r=0;g=255-Y;b=255
#     elif(X==4):r=0;g=0;b=255
    
#     def clamp(x): 
#         return max(0, min(x, 255))
    
#     color='#%02x%02x%02x' % (int(clamp(r)),int(clamp(g)),int(clamp(b)))
#     return color

def NodeVis(t:Tree,col_scalar):
    nstyle = NodeStyle()
    nstyle["shape"] = "circle"
    nstyle["size"] = 8
    nstyle["fgcolor"] = "#000000"
    nstyle["hz_line_type"] = 0
    nstyle["vt_line_type"] = 0
    nstyle["hz_line_width"] = 2
    nstyle["vt_line_width"] = 2
    nstyle["hz_line_color"] = "#000000"
    nstyle["vt_line_color"] = "#000000"

    t.set_style(nstyle)




def AddChild(node,IHID):
    aIHIDs=Get_aIHIDs(IHID)
    for aIHID in aIHIDs:
        cn=node.add_child(name="("+str(aIHID)+")")

        NodeVis(cn,1)
        cn.add_face(TextFace(" ("+str(aIHID)+") ",fsize=40),column=0,position="branch-right")



t=Tree()
root_IHID=Get_IHID(FOCUS_EHID)
root=t.add_child(name=str(FOCUS_EHID)+"("+str(root_IHID)+")")

NodeVis(root,1)
t.add_face(TextFace(str(FOCUS_EHID)+"("+str(root_IHID)+")",fsize=40),column=0,position="branch-right")


AddChild(root,root_IHID)






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

ts.title.add_face(TextFace("Substructure Tree", fsize=80), column=3)
t.set_style(None)


t.show(tree_style=ts)