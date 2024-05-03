import numpy
import galspec

BOX  = galspec.NavigationRoot("/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640")
SNAP = 36

# HALO
ihids       = BOX.RSG(SNAP).RKSGroups.InternalHaloID()
mvir        = BOX.RSG(SNAP).RKSGroups.VirialMass()
mvir_sort   = numpy.argsort(mvir)[::-1]
mvir        = mvir[mvir_sort]
ihids       = ihids[mvir_sort]
id_mass_map = dict(zip(ihids,mvir))




print("Massive Halo IDs:")
print(ihids[:10],end="\n\n")


# TARGET
tihid = 209
print("Target Halo IDs:",tihid,end="\n\n")
if tihid not in ihids: exit()

# SUBHALO
dm_ihid     =  BOX.RSG(SNAP).DarkMatter.InternalHaloID()
dm_aihid    =  BOX.RSG(SNAP).DarkMatter.AssignedInternalHaloID()


target_mask = (dm_ihid==tihid)
dm_ihid     = dm_ihid[target_mask]
dm_aihid    = dm_aihid[target_mask]

child,count = numpy.unique(dm_aihid,return_counts=True)

sub_sort = numpy.argsort(count)[::-1]
child = child[sub_sort]
count = count[sub_sort]

print("Sub Halos\n(ID-Count-In Group)")
for i in range(min(10,len(child))):
    print(child[i],"-",count[i],"-",child[i] in ihids)


exit()
child_mass = list([id_mass_map[c] for c in child])

print(child_mass[0])


