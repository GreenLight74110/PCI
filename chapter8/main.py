# coding=utf-8

import numpredict

def knn3(d,v): return numpredict.knnestimate(d,v,k=3)
def knn1(d,v): return numpredict.knnestimate(d,v,k=1)
def knninverse(d,v):return numpredict.weightedknn(d,v,weightf=numpredict.inverseweight)

# data=numpredict.wineset1( )
data=numpredict.wineset2( )

#=======Building Price Models========#
# print numpredict.wineprice(95.0,3.0)
# print numpredict.wineprice(95.0,8.0)
# print numpredict.wineprice(99.0,1.0)
# print numpredict.wineprice(66.0,3.0)
# print data[0]
# print data[1]

#=======k-Nearest Neighbors===========#
# reload(numpredict)
# print numpredict.knnestimate(data,(95.0,3.0))
# print numpredict.knnestimate(data,(99.0,3.0))
# print numpredict.knnestimate(data,(99.0,5.0))
# print numpredict.wineprice(99.0,5.0) # 得到实际价格
# print numpredict.knnestimate(data,(99.0,5.0),k=1) # 尝试较少的邻居

#========Weighted Neighbors===============#
# reload(numpredict)
# print numpredict.subtractweight(0.1)
# print numpredict.inverseweight(0.1)
# print numpredict.gaussian(0.1)
# print numpredict.gaussian(1.0)
# print numpredict.subtractweight(1)
# print numpredict.inverseweight(1)
# print numpredict.gaussian(3.0)

#========Weighted kNN==========#
# reload(numpredict)
# print numpredict.weightedknn(data,(99.0,5.0))
# print numpredict.knnestimate(data,(99.0,5.0))

#========Cross-Validation =============#
# reload(numpredict)
# print '=========== k=5 ============'
# print numpredict.crossvalidate(numpredict.knnestimate,data)
# print '=========== k=3 ============'
# print numpredict.crossvalidate(knn3,data)
# print '=========== k=1 ============'
# print numpredict.crossvalidate(knn1,data)
# print '===========不同的权重函数============'
# print numpredict.crossvalidate(numpredict.weightedknn,data)
# print numpredict.crossvalidate(knninverse,data)

#=======Heterogeneous Variables ======#
# print numpredict.crossvalidate(knn3,data)
# print numpredict.crossvalidate(numpredict.weightedknn,data)

#=========Scaling Dimensions=============#
# reload(numpredict)
# sdata=numpredict.rescale(data,[8, 4, 0, 10])
# print numpredict.crossvalidate(knn3,sdata)
# print numpredict.crossvalidate(numpredict.weightedknn,sdata)

#=======Optimizing the Scale==========#
# import optimization
# reload(numpredict)
# costf=numpredict.createcostfunction(numpredict.knnestimate,data)
# print optimization.annealingoptimize(numpredict.weightdomain,costf,step=2)
# print optimization.geneticoptimize(numpredict.weightdomain,costf,popsize=5,step=1,elite=0.2,maxiter=20)

#=======Uneven Distributions=========#
# reload(numpredict)
# data=numpredict.wineset3( )
# print numpredict.wineprice(99.0,20.0)
# print numpredict.weightedknn(data,[99.0,20.0])
# print numpredict.crossvalidate(numpredict.weightedknn,data)

#======Estimating the Probability Density=======#
# reload(numpredict)
# print numpredict.probguess(data,[99,20],40,80)
# print numpredict.probguess(data,[99,20],80,120)
# print numpredict.probguess(data,[99,20],120,1000)
# print numpredict.probguess(data,[99,20],30,120)

#=====Test Matplotlib=====#
# from pylab import *
# a=array([1,2,3,4])
# b=array([4,2,3,1])
# plot(a,b)
# show( )
# t1=arange(0.0,10.0,0.1)
# plot(t1,sin(t1))
# show( )

#===== cumulativegraph =====#
# reload(numpredict)
# numpredict.cumulativegraph(data,(1,1),120)

#====== probabilitygraph ===========#
reload(numpredict)
numpredict.probabilitygraph(data,(1,1),120)


