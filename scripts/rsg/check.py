import galspec
import numpy
import matplotlib.pyplot as plt



# galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Work/ResetRKSG/rsg_L50MpcN640c"
galspec.CONFIG.MPGADGET_OUTPUT_DIR = "sftp://cranit@pegasus.iucaa.in/mnt/home/student/cranit/Work/ResetRKSG/rsg_L50MpcN640c"
# galspec.CONFIG.MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Work/ResetRKSG/rsg_L10MpcN64c"
sim = galspec.InitConfig()


stars = sim.RSG(36).Star.ID()

print(len(stars))