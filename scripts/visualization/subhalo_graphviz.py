import galspec,os
import numpy
import matplotlib.pyplot as plt
from galspec.visualization.Matcube import PlotCube

from treelib import Tree, Node


# --- SIMS
BOX         = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640/")
PARTBOX     = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/L50N640/")

# --- FLAGS : Set flags
SAVE_PATH   = "/mnt/home/student/cranit/Work/RSGBank/Results_PMCAM/subhalo_tree_z0.svg" 
SNAP_NUM    = 171
HALO_OFFSET = 0


# --- AUTO-FLAGS
COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")
SNAP        = BOX.RSG(SNAP_NUM)
PSNAP       = PARTBOX.PART(SNAP_NUM)
REDSHIFT    = (1/SNAP.Attribute.Time())-1
BOX_SIZE    = SNAP.Attribute.BoxSize()/1000


# --- REORDER
ORDER       = numpy.argsort(SNAP.RKSGroups.VirialMass())[::-1]    # Reorders as decreasing mass

# TARGET HALO FEILDS
TIHID       = SNAP.RKSGroups.InternalHaloID()[ORDER][HALO_OFFSET]
TMVIR       = SNAP.RKSGroups.VirialMass()[ORDER][HALO_OFFSET]
TRVIR       = SNAP.RKSGroups.VirialRadius()[ORDER][HALO_OFFSET]
TPOS        = SNAP.RKSGroups.Position()[ORDER][HALO_OFFSET]

# GET PARTICLE
DM_IHIDS    = SNAP.DarkMatter.InternalHaloID()
DM_AIHIDS   = SNAP.DarkMatter.AssignedInternalHaloID()
# Filter for asciated particles
TDM_POS     = SNAP.DarkMatter.Position()[DM_IHIDS==TIHID]
# Get relative position
TDM_POS    -= TPOS




# ===================== SUBHALO TREE
def Get_Child_IHID(fihid): #facosued ihid (halo)
    fihid_mask = (DM_IHIDS==fihid)
    all_aihid  = DM_AIHIDS[fihid_mask]
    u,c = numpy.unique(all_aihid,return_counts=True)
    return u 

def GetTag(id):
    tag = "ID\n" + str(id)
    return tag


child_handled=[]
def RecursiveAddNode(tree:Tree,tihid):
    childs = Get_Child_IHID(tihid)
    childs = numpy.delete(childs,numpy.where(childs==tihid))
    num_childs   = len(childs)

    if num_childs<1: return # leaf
    # Branch
    for child in childs:
        if child in child_handled:continue
        tree.create_node(GetTag(child),child,parent=tihid)
        child_handled.append(child)
        RecursiveAddNode(tree,child)
        



t=Tree()
root_ihid=TIHID
t.create_node(GetTag(root_ihid),root_ihid)
RecursiveAddNode(t,root_ihid)


# t.show()

out_folder = os.path.dirname(SAVE_PATH)
gv_file_path    = os.path.join(out_folder,"subhalo_tree.gv")
t.to_graphviz(filename=gv_file_path, shape=u'circle', graph=u'digraph')
os.system(f"dot -Tsvg {gv_file_path} -o {SAVE_PATH}")   # (-Tpdf,-Tsvg,-Tpng,-Tgif,-Tjpg,-Tps)
print("Please clean temporary file at : " + gv_file_path)

