import galspec
import numpy


L50N640 = "/mnt/home/student/cranit/Work/RSGBank/OUT_L50N640"
BOX = galspec.NavigationRoot(L50N640)

rvir = BOX.RSG(36).RKSGroups.VirialRadius()
mvir = BOX.RSG(36).RKSGroups.VirialMass()
ihid = BOX.RSG(36).RKSGroups.InternalHaloID()

mvir_sort = numpy.argsort(mvir)[::-1]
mvir = mvir[mvir_sort]
rvir = rvir[mvir_sort]
ihid = ihid[mvir_sort]

tihid = ihid[0]
print(tihid)


