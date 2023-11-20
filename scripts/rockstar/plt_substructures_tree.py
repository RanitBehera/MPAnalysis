import sys,os, numpy
from ete3 import Tree,TreeStyle, TextFace, NodeStyle

sys.path.append(os.getcwd())
import modules as mp

# --- CONFIG PARAMETERS
OUTPUTDIR               = "/home/ranitbehera/MyDrive/Data/RKS_NEW/rks/output2"
HALO_FILENAME           = "halos_0.0.ascii"
PARTICLES_FILENAME      = "halos_0.0.particles"
FOCUS_EHID              = 2088  # most massive : 3972,2088,7444,6143,1250
SUBSTRUC_LIMIT          = 10

# --- DERIVED PARAMETERS
HFILEPATH=OUTPUTDIR + os.sep + HALO_FILENAME
PFILEPATH=OUTPUTDIR + os.sep + PARTICLES_FILENAME

# --- DATA FILTERS
data=numpy.loadtxt(PFILEPATH)
type_mask=(data[:,mp.particles.type]==0)
data=data[type_mask]

def Get_intHID(extHID):
    ehid=numpy.int64(data[:,mp.particles.external_haloid])
    ihid=numpy.int64(data[:,mp.particles.internal_haloid])
    return ihid[ehid==extHID][0]

def Get_AintHIDs(intHID):
    ihid=numpy.int64(numpy.int64(data[:,mp.particles.internal_haloid]))
    aihid=numpy.int64(numpy.int64(data[:,mp.particles.assigned_internal_haloid]))
    u,c=numpy.unique(aihid[ihid==intHID],return_counts=True)
    sort=numpy.argsort(c)[::-1][0:SUBSTRUC_LIMIT]
    u=u[sort] # c=c[sort]
    return u

# def GetRow_Mask(AintHID,type):
#     aihid=numpy.int64(numpy.int64(data[:,mp.particles.assigned_internal_haloid]))
#     types=numpy.int64(numpy.int64(data[:,mp.particles.type]))
#     aihid_mask=(aihid==AintHID)
#     type_mask=(types==type)
#     return aihid_mask & type_mask




# --- Tree
def NodeVis(t:Tree):
    nstyle = NodeStyle()
    nstyle["shape"] = "circle"
    nstyle["size"] = 20
    nstyle["fgcolor"] = "#000000"
    nstyle["hz_line_type"] = 0
    nstyle["vt_line_type"] = 0
    nstyle["hz_line_width"] = 2
    nstyle["vt_line_width"] = 2
    nstyle["hz_line_color"] = "#000000"
    nstyle["vt_line_color"] = "#000000"
    t.set_style(nstyle)


def AddChild(node,intHID):
    node.add_face(TextFace(str(intHID),fsize=40),column=0,position="branch-right")
    AintHIDs=Get_AintHIDs(intHID)
    print(AintHIDs)
    # length=len(AintHIDs)
    
    # for AintHID in AintHIDs:
    #     cn=node.add_child(name="("+str(AintHID)+")")
    #     NodeVis(cn)
    #     # cn.add_face(TextFace(str(AintHID),fsize=40),column=0,position="branch-right")
    #     AddChild(cn,AintHID)
            





t=Tree()
root_IHID=Get_intHID(FOCUS_EHID)
AddChild(t,root_IHID)

# print(Get_AintHIDs(7770))




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
ts.title.add_face(TextFace("Substructure Tree\n(ext-HID)int-HID:("+str(FOCUS_EHID)+")"+str(root_IHID), fsize=80), column=3)
t.set_style(None)


# t.show(tree_style=ts)