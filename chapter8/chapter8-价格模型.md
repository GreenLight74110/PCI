## 构建价格模型

### 构造一个样本数据集

本节将根据一个人为假设的简单模型来构造一个有关葡萄酒价格的数据集。

酒的价格是根据酒的等级及其储藏年代共同决定的。高等级葡萄酒从高价位开始价格逐渐走高至其“峰值年”；而低等级葡萄酒则会从低价位开始价格一路走低。

针对这一现象建模，新建一个名为numpredict.py的文件，并加入wineprice函数：

```python
from random import random,randint
import math

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
```

还需要一个函数来构造表示葡萄酒价格的数据集。在numpredict.py中加入wineset1函数，该函数“生产”了200瓶葡萄酒，并根据模型求出其价格，然后在原有价格基础上随机加减了20%（用以表现价格的波动，同时也为了增加数值型预测的难度）。

```python
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
```

输入以下语句，测试一下葡萄酒的价格，并据此构造出一个新的数据集：

```python
import numpredict
print numpredict.wineprice(95.0,3.0)
print numpredict.wineprice(95.0,8.0)
print numpredict.wineprice(99.0,1.0)
data=numpredict.wineset1( )
print data[0]
print data[1]
```

返回：

```python
21.1111111111
47.5
10.1020408163
{'input': (84.74059946554698, 31.647294916905317), 'result': 208.38910634948277}
{'input': (62.32271844486547, 0.4218732689948823), 'result': 17.487677990696753}
```

可以看到，第二瓶酒年代太久，而且还过期了。

变量间的相互作用，使得这一数据集很适合对算法进行测试。

### k-最近邻算法

算法通过寻找与当前所关注的商品情况相似的一组商品，对这些商品价格求均值，进而作出价格预测。

#### 近邻数

kNN中的k表示为求最终结果而参与求平均运算的商品数量。

![](http://img0.ph.126.net/ewdjYxtW1cKfsjpVb60fwg==/6632737923861080442.png)

![](http://img1.ph.126.net/U_dFYsVGOOArbZHI7FP7GQ==/1037798239150155316.png)

#### 定义相似度

在这里，我们选用欧式距离作为度量。将euclidian函数加入numpredict.py：

```python
def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)
```

#### k-最近邻算法的代码

k-NN计算量大，但每次有新数据加入时，都无须重新训练。

在numpredict.py中加入getdistances函数，用以计算给定商品与原数据集中任一其它商品间的距离：

```python
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
```

在numpredict.py中加入knnestimate函数，对前k项结果求出平均值：

```python
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
```

现在可以对一件新商品进行评估了，尝试不同的参数和k，观察对结果的影响：

```python
reload(numpredict)
print numpredict.knnestimate(data,(95.0,3.0))
print numpredict.knnestimate(data,(99.0,3.0))
print numpredict.knnestimate(data,(99.0,5.0))
print numpredict.wineprice(99.0,5.0) # 得到实际价格
print numpredict.knnestimate(data,(99.0,5.0),k=1) # 尝试较少的邻居
```

输出：

```python
15.675129313
26.1430052752
29.2564177677
30.306122449
48.8609628516
```

### 为近邻分配权重

目前的算法可能会选择距离太远的近邻。一种补偿办法便是，根据距离的远近为其赋以相应的权重。

#### 反函数

最简单的形式是返回距离的倒数，但有必要在求倒数前先加一个常量。

将inverseweight函数加入numpredict.py中：

```python
def inverseweight(dist,num=1.0,const=0.1):
    return num/(dist+const)
```

![](http://img1.ph.126.net/ongND9TKaqZguCv43oRVKg==/92886742332490945.png)

优点：执行速度快，容易实现。

缺点：为近邻赋很大的权重，而稍远的项，其权重则会“衰减”很快，从而会使算法对噪声变得更加敏感。

#### 减法函数

用一个常量值减去距离，如果结果大于0，则权重为相减的结果；否则为0。

在numpredict.py中加入substractweight函数：

```python
def subtractweight(dist,const=1.0):
    if dist>const:
        return 0
    else:
        return const-dist
```

![](http://img0.ph.126.net/0Gui32N2_ARSLqPju8rjCQ==/3079336245232552329.png)

优点：克服了对近邻项权重分配过大的潜在问题。

缺点：由于权重值最终会跌至0，因此可能找不到距离足够近的项，将其视作近邻，即对于某些项，算法根本就无法作出预测。

#### 高斯函数

也称为“钟型曲线”。

![](http://img2.ph.126.net/XpGlsZshI5em8azobZX74Q==/6632482837166034119.png)

优点：解决了上述两个函数的缺陷。

缺点：代码复杂，执行速度不够快。

在numpredict.py中加入gaussian函数：

```python
def gaussian(dist,sigma=5.0):
    return math.e**(-dist**2/(2*sigma**2))
```

尝试不同的参数，观察不同方法间的差异如何：

```python
reload(numpredict)
print numpredict.subtractweight(0.1)
print numpredict.inverseweight(0.1)
print numpredict.gaussian(0.1)
print numpredict.gaussian(1.0)
print numpredict.subtractweight(1)
print numpredict.inverseweight(1)
print numpredict.gaussian(3.0)
```

输出：

```python
0.9
5.0
0.999800019999
0.980198673307
0.0
0.909090909091
0.835270211411
```

#### 加权kNN

与普通kNN相比，区别在于它求的是加权平均。

在numpredict.py中加入weightedknn函数：

```python
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
```

尝试与普通knn函数做下性能上的对比：

```python
reload(numpredict)
print numpredict.weightedknn(data,(99.0,5.0))
```

输出：

```python
32.1046766961
```

### 交叉验证

指将数据拆分为训练集和测试集的一系列技术的统称。（典型情况下，测试集占5%，训练集占95%。）

在numpredict.py中加入dividedata函数，拆分原数据集：

```python
def dividedata(data,test=0.05):
    trainset=[]
    testset=[]
    for row in data:
        if random()<test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset
```

将testalgorithm加入numpredict.py：

```python
def testalgorithm(algf,trainset,testset):
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2 #对数字求平方可以突显较大的差值
        #print row['result'],guess
    #print error/len(testset)
    return error/len(testset)
```

最后再编写一个函数，对数据采取不同划分，并在每个划分上执行testalgorithm函数，然后累加结果，得到最终评分值。

在numpredict.py中加入crossvalidate函数：

```python
def crossvalidate(algf,data,trials=100,test=0.1):
    error=0.0
    for i in range(trials):
        trainset,testset=dividedata(data,test)
        error+=testalgorithm(algf,trainset,testset)
    return error/trials
```

利用不同的k值或者不同的权重函数来试验knnestimate函数：

```python
reload(numpredict)
print '=========== k=5 ============'
print numpredict.crossvalidate(numpredict.knnestimate,data)
print '=========== k=3 ============'
def knn3(d,v): return numpredict.knnestimate(d,v,k=3)
print numpredict.crossvalidate(knn3,data)
print '=========== k=1 ============'
def knn1(d,v): return numpredict.knnestimate(d,v,k=1)
print numpredict.crossvalidate(knn1,data)
print '===========不同的权重函数============'
print numpredict.crossvalidate(numpredict.weightedknn,data)
def knninverse(d,v):return numpredict.weightedknn(d,v,weightf=numpredict.inverseweight)
print numpredict.crossvalidate(knninverse,data)
```

输出：

```python
=========== k=5 ============
306.400845867
=========== k=3 ============
240.48778635
=========== k=1 ============
333.683037941
===========不同的权重函数============
274.380679739
221.13639126
```

可以看到，k=3比1和5都要好。加权kNN似乎能给出更好的结果。

### 不同类型的变量

引入的新变量可能比原变量对结果产生更显著的影响，也可能是一个完全不相关的变量。

#### 加入数据集

新建wineset2函数，向数据集加入新的变量：

```python
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
```

![](http://img0.ph.126.net/oyuaY1d-l_WNfSipm2SBkw==/6632534514212546808.png)

构造一个带有通道信息（无关变量）和酒瓶尺寸（强相关变量）的新数据集，并使用之前得到的最佳参数值，试验新数据集对kNN预测算法的影响情况：

```python
data=numpredict.wineset2( )
print numpredict.crossvalidate(knn3,data)
print numpredict.crossvalidate(numpredict.weightedknn,data)
```

输出：

```python
1543.53881399
1606.32845174
```

可以看到，crossvalidate返回结果很糟糕，原因在于，算法现在还不知道如何对不同变量加以区别对待。

#### 按比例缩放

对数值进行归一化处理，从而使所有变量都位于相同的值域范围内，同时也有助于找到减少多余变量的方法。

最简单的形式是将每个维度上的数值乘以一个在该维度上的常量。可以看到代表酒瓶尺寸的维度被值为10的比例因子缩小了，该做法解决了一部分变量天生比其它变量更“强势”的问题。

![](http://img1.ph.126.net/cR8yYwmNbVsADdVW8KQ0ag==/6632443254747440641.png)

对于重要程度不高的变量，可以将该维度上每一项数值都乘以0。

![](http://img2.ph.126.net/nQfrxihhNwMyEhFq7S9faw==/6632239845094985600.png)

在numpredict.py中加入resacle函数：

```python
def rescale(data,scale):
    scaleddata=[]
    for row in data:
        scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
        scaleddata.append({'input':scaled,'result':row['result']})
    return scaleddata
```

挑选一些参数，试着对数据集按比例重新进行缩放：

```python
reload(numpredict)
sdata=numpredict.rescale(data,[10,10,0,0.5])
print numpredict.crossvalidate(knn3,sdata)
print numpredict.crossvalidate(numpredict.weightedknn,sdata)
```

输出：

```python
1340.96158489
985.031294278
```



















