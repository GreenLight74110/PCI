## 高阶分类：核方法与SVM

### 婚介数据集

站点收集的信息：年龄、是否吸烟、是否要孩子、兴趣列表、家庭住址；同时还包括：两个人是否成功配对、是否开始交往以及是否决定见面。

编写一个加载数据集的函数。

新建advancedclassify.py文件，将matchrow和loadrow加入其中：

```python
class matchrow:
  def __init__(self,row,allnum=False):
    if allnum:
      self.data=[float(row[i]) for i in range(len(row)-1)]
    else:
      self.data=row[0:len(row)-1]
    self.match=int(row[len(row)-1])

def loadmatch(f,allnum=False):
  rows=[]
  for line in file(f):
    rows.append(matchrow(line.split(','),allnum))
  return rows
```

利用该函数加载只包含年龄信息和包含完整信息的数据集：

```python
import advancedclassify
agesonly=advancedclassify.loadmatch('agesonly.csv',allnum=True)
matchmaker=advancedclassify.loadmatch('matchmaker.csv')
```

### 数据中的难点

数据集中值得注意的是，变量的相互作用和非线性特点。

尝试对某些变量进行可视化，并从中生成一个涉及男女年龄对比情况的散布图：

````python
from pylab import *
def plotagematches(rows):
  xdm,ydm=[r.data[0] for r in rows if r.match==1],\
          [r.data[1] for r in rows if r.match==1]
  xdn,ydn=[r.data[0] for r in rows if r.match==0],\
          [r.data[1] for r in rows if r.match==0] 
  
  plot(xdm,ydm,'bo')
  plot(xdn,ydn,'b+')
  
  show()
````

执行以下代码：

```python
reload(advancedclassify)
advancedclassify.plotagematches(agesonly)
```

![](http://img1.ph.126.net/q5RCMm5ecs2gidU_Z_HVbg==/6632742321907629676.png)

如果两两配对，则标记为o，否则标记x。

可以看到，人们的年龄越见长越能忍受更大的年龄差距。

### 决策树分类器

如果直接对数据进行决策训练，将会得到以下结果：

![](http://img1.ph.126.net/_wT1mCL328-OSpJFGJ8ViA==/2593510435430011252.png)

可见，上述结果对于解释决策的过程显然没有任何用处。

为了明白决策树到底做了什么，进一步观察散布图以及根据决策树生成的决策边界：

![](http://img2.ph.126.net/lsATj6vPmsikMMna0OD5Gg==/6632225551445177327.png)

位于决策边界一侧的每个点被赋予某个分类，而另一侧则会被赋予另一分类。可以看到，决策树的约束条件使边界线呈现出垂直或水平向的分布。

总结：

1. 在没弄清楚数据本身的含义及如何将其转换成更易于理解的形式前，轻率地使用提供数据是错误的。建立散布图有助于找到数据真正的划分方式。
2. 如果存在多个数值型输入，且输入间呈现的关系并不见但，决策树常常不是最有效的方法。

### 基本的线性分类

工作原理：寻找每个分类中所有数据的平均值，并构造一个代表该分类中心位置的点。然后通过判断距离哪个中心点位置最近来对新的坐标点进行分类。

在advancedclassify.py中加入lineartrain函数，用以计算分类的均值点：

```python
def lineartrain(rows):
    averages={}
    counts={}

    for row in rows:
        # 得到该坐标点所属分类
        cl=row.match

        averages.setdefault(cl,[0.0]*(len(row.data)))
        counts.setdefault(cl,0)

        # 将该坐标点加入averages中
        for i in range(len(row.data)):
            averages[cl][i]+=float(row.data[i])

        # 记录每个分类中有多少坐标点
        counts[cl]+=1

    # 将总和除以计数值以求得平均值
    for cl,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[cl]

    return averages
```

运行以上函数，以求得平均值：

```python
reload(advancedclassify)
avgs=advancedclassify.lineartrain(agesonly)
```

![](http://img2.ph.126.net/4HSjf-GBeQX1l4VKYm6c7g==/6632278328003314043.png)

图中的x表示上述函数求得的均值点，划分数据的直线位于两个x的中间位置。

要推测是否匹配，只须判断其更接近于哪个均值点即可。

在advancedclassify.py中加入dotproduct函数，用以计算向量点积：

```python
def dotproduct(v1,v2):
  return sum([v1[i]*v2[i] for i in range(len(v1))])
```

![](http://img0.ph.126.net/vzcBeVb4UPGQZxjtaUGATA==/6632532315189330144.png)

夹角大者点积为负，夹角小者点积为正，故而通过观察点积结果的正负号，就可以判断出新的坐标点属于哪个分类。

C是M0和M1的均值点，寻找分类的公式如下：
$$
class=sign((X – (M 0 +M 1 )/2) . (M 0 -M 1 ))
$$
相乘后的结果：
$$
class=sign(X.M 0 – X.M 1 + (M 0 .M 0 – M 1 .M 1 )/2)
$$
在advancedclassify.py中加入dpclassify函数，用以确定分类：

```python
def dpclassify(point,avgs):
  b=(dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
  y=dotproduct(point,avgs[0])-dotproduct(point,avgs[1])+b
  if y>0: return 0
  else: return 1
```

尝试利用线性分类器得出一些结论：

```python
reload(advancedclassify)
print advancedclassify.dpclassify([30,30],avgs)
print advancedclassify.dpclassify([30,25],avgs)
print advancedclassify.dpclassify([25,40],avgs)
print advancedclassify.dpclassify([48,20],avgs)
```

这只是一个线性分类器，所以它只找出了一条分界线来。接下来，会对其进行改进，使其能够处理非线性分类。

### 分类特征

将原数据转换成数值类型数据。

#### 是否问题

三种情况：yes--->1;no--->-1;unknown--->0。

在advancedclassify.py中加入yesno函数：

```python
def yesno(v):
  if v=='yes': return 1
  elif v=='no': return -1
  else: return 0
```

#### 兴趣列表

由于本例中处理的是一对一对的人，因此要将具备共同兴趣爱好的数量视为变量。

在advancedclassify.py中加入matchcount函数，以浮点数的形式返回列表中匹配项的数量：

```python
def matchcount(interest1,interest2):
  l1=interest1.split(':')
  l2=interest2.split(':')
  x=0
  for v in l1:
    if v in l2: x+=1
  return x
```

如果每项兴趣都新建一个变量则会使分类器变得更复杂，一种办法是将兴趣爱好按层级排列。

例如，滑雪和滑板都属于雪地运动，而雪地运动又属于体育运动的子分类，如果两人都对雪地运动感兴趣，但并不是同一个项目，那么其matchcount值可能会加上0.8而不是1。层级越靠近上级，相应的分值也就越小。

#### 利用Yahoo!Maps来确定距离

由于无法使用Yahoo!API，所以在advancedclassify.py中加入milesdistance空函数：

```python
def milesdistance(a1,a2):
    return 0
```

### 构造新的数据集

在advancedclassify.py中加入loadnumerical空函数：

```python
def loadnumerical():
    oldrows=loadmatch('matchmaker.csv')
    newrows=[]
    for row in oldrows:
        d=row.data
        data=[float(d[0]),yesno(d[1]),yesno(d[2]),
              float(d[5]),yesno(d[6]),yesno(d[7]),
              matchcount(d[3],d[8]),
              milesdistance(d[4],d[9]),
              row.match]
        newrows.append(matchrow(data))
    return newrows
```

输入以下语句，以构造新的数据集：

```python
reload(advancedclassify)
numericalset=advancedclassify.loadnumerical( )
print numericalset[0].data
```

输出：

````python
[24.0, -1, -1, 41.0, -1, 1, 0, 0]
````

### 对数据进行缩放处理

将所有数据缩放为同一尺度，从而使每个变量上的差值都具有可比性。

在advancedclassify.py中加入scaledata函数：

```python
def scaledata(rows):
    low=[999999999.0]*len(rows[0].data)
    high=[-999999999.0]*len(rows[0].data)
    # 寻找最大值和最小值
    for row in rows:
        d=row.data
        for i in range(len(d)):
            if d[i]<low[i]: low[i]=d[i]
            if d[i]>high[i]: high[i]=d[i]

    # 对数据进行缩放处理的函数
    def scaleinput(d):
        return [(d[i]-low[i])/(high[i]-low[i])
                for i in range(len(low))]

    # 对所有数据进行缩放处理
    newrows=[matchrow(scaleinput(row.data)+[row.match])
             for row in rows]

    # 返回新的数据和缩放处理函数
    return newrows,scaleinput
```

上述函数实际上将所有数据都转换成了介于0和1之间的值。

### 理解核方法

![](http://img2.ph.126.net/Hyo8NWaN1Xjs0u7i2WEWEw==/6632235447048493298.png)

对于以上的情况，两个分类的均值都位于相似的位置，但是线性分类器却无法识别这两个分类。

但是，对每个x和y求平方，所有的x将移到左下角，而o将移到角落以外的区域。这时，就比较容易通过一条直线来划分x和o了。

![](http://img0.ph.126.net/kS3mrYHasl6hed6D_Me29g==/2597451085103951964.png)

#### 核技法

对于任何用到了点积运算的算法，可以采用一种叫做核技法的技术。

思路：用一个新的函数来取代原来的点积函数，但借助某个映射函数将数据第一次变换到更高维度的坐标空间时，新函数将会返回高维度坐标空间内的点积结果。

一种经典的方法被称为**径向基函数**。与点积类似，接受两个向量作为输入，返回一个标量值；不同的是，径向基函数是非线性的，能将数据映射到更为复杂的空间中。

在advancedclassify.py中加入rbf函数：

```python
# gamma是一个调节参数，以达到针对给定数据集的最佳线性分离
def rbf(v1,v2,gamma=10):
    dv=[v1[i]-v2[i] for i in range(len(v1))]
    l=veclength(dv)
    return math.e**(-gamma*l)
```

在advancedclassify.py中加入nlclassify函数，先计算出某个坐标点与分类中其余每个坐标点之间的点积或径向基函数的结果，然后再对它们求均值：

```python
def nlclassify(point,rows,offset,gamma=10):
    sum0=0.0
    sum1=0.0
    count0=0
    count1=0

    for row in rows:
        if row.match==0:
            sum0+=rbf(point,row.data,gamma)
            count0+=1
        else:
            sum1+=rbf(point,row.data,gamma)
            count1+=1
    y=(1.0/count0)*sum0-(1.0/count1)*sum1+offset

    if y>0: return 0
    else: return 1
    
def getoffset(rows,gamma=10):
  l0=[]
  l1=[]
  for row in rows:
    if row.match==0: l0.append(row.data)
    else: l1.append(row.data)
  sum0=sum(sum([rbf(v1,v2,gamma) for v1 in l0]) for v2 in l0)
  sum1=sum(sum([rbf(v1,v2,gamma) for v1 in l1]) for v2 in l1)
  
  return (1.0/(len(l1)**2))*sum1-(1.0/(len(l0)**2))*sum0
```

尝试一下新的分类器，只考虑年龄因素：

```python
offset = advancedclassify.getoffset(agesonly)
print advancedclassify.nlclassify([30,30],agesonly,offset)
print advancedclassify.nlclassify([30,25],agesonly,offset)
print advancedclassify.nlclassify([25,40],agesonly,offset)
print advancedclassify.nlclassify([48,20],agesonly,offset)
```

输出：

```python
1
1
0
0
```



