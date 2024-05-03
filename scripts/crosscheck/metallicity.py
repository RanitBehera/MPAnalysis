import galspec,numpy


root=galspec.NavigationRoot("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640")

metallicity = root.PART(36).Star.Metallicity()
# metals      = root.PART(36).Gas.Metals()
# print(len(metals[0,:]))
# mask        = (metals[:,2]!=0)

# metallicity = metallicity[mask]
# metals      = metals[mask]

# metals = metals[:,2:]
# metallicity_2 = numpy.sum(metals,axis=1)


# print(metallicity)
# print(metallicity_2)
# ratio=metallicity_2/metallicity
# print(max(ratio))

# ind=100
# print(metallicity[ind])
# print(len(metals[ind,:]))
# print(sum(metals[ind,:]))


print(max(metallicity/0.0127))