import sys
sys.path.append(r"C:\Users\ranit\OneDrive\My Drive\4 My Collections\Coadings\Python - MPAnalysis\MPAnalysis")

from .. import modules as mp

op=mp.BaseDirectory(r"D:\Ubuntu Back\Desktop\Sim\hydro\std_hydro\seed_181170\fg11\output")

print(mp.ReadHeader(op.PART(17).DarkMatter.Position).memberLength)

