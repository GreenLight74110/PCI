# coding=utf-8

from random import random,randint
import math

from pylab import *

def wineprice(rating,age):
    peak_age=rating-50

    # 根据等级来计算价格
    price=rating/2
    if age>peak_age:
        # 经过“峰值年”，后面的5年里其品质将变差
        price=price*(5-(age-peak_age)/2)
    else:
        # 价格在接近“峰值年”时会增加到原值的5倍
        price=price*(5*((age+1)/peak_age))
    if price<0: price=0
    return price

def wineset1():
    rows=[]
    for i in range(300):
        # 随机生成年代和等级
        rating=random()*50+50
        age=random()*50

        # 得到一个参考价格
        price=wineprice(rating,age)

        # 增加“噪声”
        price*=(random()*0.2+0.9)

        # 加入数据集
        rows.append({'input':(rating,age),
                     'result':price})
    return rows

def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)


def getdistances(data,vec1):
    distancelist=[]

    # Loop over every item in the dataset
    for i in range(len(data)):
        vec2=data[i]['input']

        # Add the distance and the index
        distancelist.append((euclidean(vec1,vec2),i))

    # 根据距离大小排序
    distancelist.sort()
    return distancelist

def knnestimate(data,vec1,k=5):
    # 得到经过排序的距离值
    dlist=getdistances(data,vec1)
    avg=0.0

    # 对前k项结果求平均
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result']
    avg=avg/k
    return avg

def inverseweight(dist,num=1.0,const=0.1):
    return num/(dist+const)

def subtractweight(dist,const=1.0):
    if dist>const:
        return 0
    else:
        return const-dist

def gaussian(dist,sigma=5.0):
    return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=5,weightf=gaussian):
    # 得到距离值
    dlist=getdistances(data,vec1)
    avg=0.0
    totalweight=0.0

    # 得到加权平均
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    if totalweight==0: return 0
    avg=avg/totalweight
    return avg

def dividedata(data,test=0.05):
    trainset=[]
    testset=[]
    for row in data:
        if random()<test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset

def testalgorithm(algf,trainset,testset):
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
        #print row['result'],guess
    #print error/len(testset)
    return error/len(testset)

def crossvalidate(algf,data,trials=100,test=0.1):
    error=0.0
    for i in range(trials):
        trainset,testset=dividedata(data,test)
        error+=testalgorithm(algf,trainset,testset)
    return error/trials

def wineset2():
    rows=[]
    for i in range(300):
        rating=random()*50+50
        age=random()*50
        aisle=float(randint(1,20))
        bottlesize=[375.0,750.0,1500.0][randint(0,2)]
        price=wineprice(rating,age)
        price*=(bottlesize/750)
        price*=(random()*0.2+0.9)
        rows.append({'input':(rating,age,aisle,bottlesize),
                     'result':price})
    return rows

def rescale(data,scale):
    scaleddata=[]
    for row in data:
        scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
        scaleddata.append({'input':scaled,'result':row['result']})
    return scaleddata

def createcostfunction(algf,data):
    def costf(scale):
        sdata=rescale(data,scale)
        return crossvalidate(algf,sdata,trials=20)
    return costf

weightdomain=[(0,10)]*4

def wineset3():
    rows=wineset1()
    for row in rows:
        if random()<0.5:
            # 葡萄酒获得了折扣
            row['result']*=0.6
    return rows

def probguess(data,vec1,low,high,k=5,weightf=gaussian):
    dlist=getdistances(data,vec1)
    nweight=0.0
    tweight=0.0

    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        v=data[idx]['result']

        # 当前数据点是否位于指定范围内
        if v>=low and v<=high:
            nweight+=weight
        tweight+=weight
    if tweight==0: return 0

    # 概率位于指定范围内的权重值除以所有权重值
    return nweight/tweight

def cumulativegraph(data,vec1,high,k=5,weightf=gaussian):
    t1=arange(0.0,high,0.1)
    cprob=array([probguess(data,vec1,0,v,k,weightf) for v in t1])
    plot(t1,cprob)
    show()

def probabilitygraph(data,vec1,high,k=5,weightf=gaussian,ss=5.0):
    # 建立一个代表价格的值域范围
    t1=arange(0.0,high,0.1)

    # 得到整个值域范围内的所有概率
    probs=[probguess(data,vec1,v,v+0.1,k,weightf) for v in t1]

    # 通过加上近邻概率的高斯计算结果，对概率值做平滑处理
    smoothed=[]
    for i in range(len(probs)):
        sv=0.0
        for j in range(0,len(probs)):
            dist=abs(i-j)*0.1
            weight=gaussian(dist,sigma=ss)
            sv+=weight*probs[j]
        smoothed.append(sv)
    smoothed=array(smoothed)

    plot(t1,smoothed)
    show()