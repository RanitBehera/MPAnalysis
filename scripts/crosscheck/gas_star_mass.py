import numpy
import galspec

BOX = galspec.NavigationRoot("/scratch/cranit/RSGBank/L10N64/output")

SNAP2=BOX.PART(2)
SNAP3=box.PART(3)

# check star mass just formed
stars_in_3 = snap3.Star.ID()
star_mass_in_3 = snap3.Star.Mass()
total_star_mass_in_3 = sum(snap3.Star.Mass())
print("Total Star Mass Formed :",total_star_mass_in_3)

gas_mass_in_2 = snap2.Gas.Mass()
total_gas_mass_in_2 = sum(gas_mass_in_2)



gas_mass_in_3 = snap3.Gas.Mass()
total_gas_mass_in_3 = sum(gas_mass_in_3)
u,c=numpy.unique(gas_mass_in_3,return_counts=True)

[print(l) for l in list(zip(u,c))]


# gas_mass_diff = abs(total_gas_mass_in_2-total_gas_mass_in_3)
# print(gas_mass_diff)
