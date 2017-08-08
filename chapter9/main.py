
#======Matchmaker Dataset========#
import advancedclassify
agesonly=advancedclassify.loadmatch('agesonly.csv',allnum=True)
matchmaker=advancedclassify.loadmatch('matchmaker.csv')

#=======Difficulties with the Data========#
# reload(advancedclassify)
# advancedclassify.plotagematches(agesonly)

#======Basic Linear Classification======= #
# reload(advancedclassify)
# avgs=advancedclassify.lineartrain(agesonly)
# reload(advancedclassify)
# print advancedclassify.dpclassify([30,30],avgs)
# print advancedclassify.dpclassify([30,25],avgs)
# print advancedclassify.dpclassify([25,40],avgs)
# print advancedclassify.dpclassify([48,20],avgs)

#=====Creating the New Dataset====#
# reload(advancedclassify)
numericalset=advancedclassify.loadnumerical( )
# print numericalset[0].data

#====Scaling the Data=====#
# reload(advancedclassify)
scaledset,scalef=advancedclassify.scaledata(numericalset)
# avgs=advancedclassify.lineartrain(scaledset)
# print numericalset[0].data
# print numericalset[0].match
# print advancedclassify.dpclassify(scalef(numericalset[0].data),avgs)
# print numericalset[11].match
# print advancedclassify.dpclassify(scalef(numericalset[11].data),avgs)

#=====The Kernel Trick=====#
# offset = advancedclassify.getoffset(agesonly)
# print advancedclassify.nlclassify([30,30],agesonly,offset)
# print advancedclassify.nlclassify([30,25],agesonly,offset)
# print advancedclassify.nlclassify([25,40],agesonly,offset)
# print advancedclassify.nlclassify([48,20],agesonly,offset)

# ssoffset=advancedclassify.getoffset(scaledset)
# print numericalset[0].match
# print advancedclassify.nlclassify(scalef(numericalset[0].data),scaledset,ssoffset)
# print numericalset[1].match
# print advancedclassify.nlclassify(scalef(numericalset[1].data),scaledset,ssoffset)
# print numericalset[2].match
# print advancedclassify.nlclassify(scalef(numericalset[2].data),scaledset,ssoffset)
# newrow=[28.0,-1,-1,26.0,-1,1,2,0.8] # Man doesn't want children, woman does
# print advancedclassify.nlclassify(scalef(newrow),scaledset,ssoffset)
# newrow=[28.0,-1,1,26.0,-1,1,2,0.8] # Both want children
# print advancedclassify.nlclassify(scalef(newrow),scaledset,ssoffset)

