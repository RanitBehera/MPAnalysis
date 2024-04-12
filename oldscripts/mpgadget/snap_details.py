import os,sys,numpy

sys.path.append(os.getcwd())
import galspecold as mp

op=mp.BaseDirectory("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10Mpc_N64c/txtfiles")
mp.ReadSnapshot(op.path).ShowSummeryTable()