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

#### 对缩放结果进行优化

当不知道各个变量的重要程度时，就需要一种方法来选择一个合适的缩放参数。

crossvalidate函数对于较差的题解，会返回一个较高的数值结果，可以被看成是一个天然的成本函数，在这里可以将它封装起来，令其接受一组数值作为参数，然后对数据按比例缩放，并计算交叉验证的误差。

在numpredict.py中加入createcostfunction函数：

```python
def createcostfunction(algf,data):
  def costf(scale):
    sdata=rescale(data,scale)
    return crossvalidate(algf,sdata,trials=20)
  return costf
```

定义域为每个维度上的权重范围。

从实际出发，将权重限制在20即可。在numpredict.py中加入：

```python
weightdomain=[(0,10)]*4
```

尝试一下退火优化算法：

```python
import optimization
reload(numpredict)
costf=numpredict.createcostfunction(numpredict.knnestimate,data)
print optimization.annealingoptimize(numpredict.weightdomain,costf,step=2)
```

输出：

```python
[5, 10.0, 1, 1]
```

尝试一下速度更慢但是更加精确的geneticoptimize函数：

```python
print optimization.geneticoptimize(numpredict.weightdomain,costf,popsize=5,step=1,elite=0.2,maxiter=20)
```

输出：

```python
[8, 4, 0, 10]
```

### 不对称分布

设想，葡萄酒购买者分别来自两个彼此独立的群组：一部分人从小酒馆买的，另一部分人则从折扣店买的（50% cutoff）。然而，这些信息都没有被记录下来。

葡萄酒随机获得了6折折扣：

```python
def wineset3():
    rows=wineset1()
    for row in rows:
        if random()<0.5:
            # 葡萄酒获得了折扣
            row['result']*=0.5
    return rows
```

验证一下这种情况：

```python
reload(numpredict)
data=numpredict.wineset3( )
print numpredict.wineprice(99.0,20.0)
print numpredict.weightedknn(data,[99.0,20.0])
print numpredict.crossvalidate(numpredict.weightedknn,data)
```

输出：

```python
106.071428571
74.9127009541
751.681417598
```

### 估计概率密度

这里将研究葡萄酒落入指定价格区间的概率。

在numpredict.py中新建probguess函数：

```python
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
  
  # The probability is the weights in the range
  # divided by all the weights
  return nweight/tweight
```

输入：

```python
reload(numpredict)
print numpredict.probguess(data,[99,20],40,80)
print numpredict.probguess(data,[99,20],80,120)
print numpredict.probguess(data,[99,20],120,1000)
print numpredict.probguess(data,[99,20],30,120)
```

输出：

```python
0.0
0.834513263514
0.165486736486
0.834513263514
```

### 绘制概率分布

为了避免胡乱猜测范围区间，可以建立概率密度的图形化表达。

先安装matplotlib函数库，测试是否安装成功：

```python
from pylab import *
a=array([1,2,3,4])
b=array([4,2,3,1])
plot(a,b)
show( )
t1=arange(0.0,10.0,0.1)
plot(t1,sin(t1))
show( )
```

两种不同的查看概率分布的方法：

累积概率。在numpredict.py中加入cumulativegraph函数：

```python
def cumulativegraph(data,vec1,high,k=5,weightf=gaussian):
    t1=arange(0.0,high,0.1)
    cprob=array([probguess(data,vec1,0,v,k,weightf) for v in t1])
    plot(t1,cprob)
    show()
```

![](http://img1.ph.126.net/cBPuY945Df6hzT7iP0HpLg==/2594636335336826986.png)

概率密度。在numpredict.py中加入probabilitygraph函数：

```python
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
```

![](http://img0.ph.126.net/xP56yomgBwPvI6x5bi-vWA==/6632524618607917251.png)















