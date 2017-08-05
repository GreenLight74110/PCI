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
reload(numpredict)
sdata=numpredict.rescale(data,[10,10,0,0.5])
print numpredict.crossvalidate(knn3,sdata)
print numpredict.crossvalidate(numpredict.weightedknn,sdata)


# >>> reload(numpredict)
# <module 'numpredict' from 'numpredict.py'>
# >>> sdata=numpredict.rescale(data,[10,10,0,0.5])
# >>> numpredict.crossvalidate(knn3,sdata)
# 660.9964024835578
# >>> numpredict.crossvalidate(numpredict.weightedknn,sdata)



