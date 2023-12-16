import galspec as gs
import time

sim=gs.InitConfig()


n=(sim.PART(17).DarkMatter.Position.NValue())
b=(sim.PART(17).DarkMatter.Position.BValue())

center=64**3
ran=range(center-5,center+1)

print("Numpy")
# print(n[ran])
print("\n\nBigFile")
print(b[ran])








