import galspec
import numpy

# --- MP-GADGET FOF
galspec.CONFIG.MPGADGET_OUTPUT_DIR="/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10Mpc_N64c/output"
sim=galspec.InitConfig()

# In MP-GADGET, FOFGroup IDs are assigned such that most massive halo have ID 1
# l=sim.PIG(17).FOFGroups.LengthByType()[0,0]
# # ids=list(sim.PIG(17).Gas.ID()[0:l])
# hsfr=sum(sim.PIG(17).Gas.StarFormationRate()[0:l])
# print(hsfr)

sfr=sim.PART(17).Gas.StarFormationRate()
print(numpy.unique(sfr))




