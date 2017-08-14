from svm import *
from svmutil import *

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
# numericalset=advancedclassify.loadnumerical( )
# print numericalset[0].data

#====Scaling the Data=====#
# reload(advancedclassify)
# scaledset,scalef=advancedclassify.scaledata(numericalset)
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

#=====A Sample Session======#

# svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]
# prob = svm_problem([1,-1],[[1,0,1],[-1,0,-1]])
# param = svm_parameter()
# param.kernel_type = LINEAR
# param.C = 10
# m=svm_train(prob, param)
# m.predict([1,1,1])
# svm_save_model('test.model',m)
# m = svm_load_model('test.model')

#======Applying SVM to the Matchmaker Dataset========#
# answers,inputs=[r.match for r in scaledset],[r.data for r in scaledset]
#
# param = svm_parameter()
# param.kernel_type = RBF
# prob = svm_problem(answers,inputs)
# m=svm_train(prob, param)
#
# newrow=[28.0,-1,-1,26.0,-1,1,2,0.8] # Man doesn't want children, woman does
# m.predict(scalef(newrow))
# newrow=[28.0,-1,1,26.0,-1,1,2,0.8] # Both want children
# m.predict(scalef(newrow))


import facebook
s=facebook.fbsession( )
friends=s.getfriends( )
print friends[1]
u'iY5TTbS-0fvs.'
print s.getinfo(friends[0:2])