import sys
sys.path.append(r"C:\Users\ranit\OneDrive\My Drive\4 My Collections\Coadings\Python - MPAnalysis\MPAnalysis")

import modules.Navigate as mpn

op=mpn.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")
print(op.PIG(12).FOFGroups.GroupID.path)