**定义：**  通过尝试许多不同题解并给这些题解打分以确定其质量的方式来找到一个问题的最优解。    

### 组团旅游    
新建一个文件，加入如下代码：
```python
import time
import random
import math

people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]
# Laguardia
destination='LGA'
```
家庭成员来自全国各地，并且希望在纽约会面。他们将在同一天到达，同一天离开，而且搭乘相同的交通工具往返机场。每天有很多航班，起飞时间、价格以及续航时间都不尽相同。    
将schedule.txt中的数据载入到一个字典中，以起止点为键，以可能的航班详情明细为值。    
```python
flights={}
# 
for line in file('schedule.txt'):
  origin,dest,depart,arrive,price=line.strip().split(',')
  flights.setdefault((origin,dest),[])

  # Add details to the list of possible flights
  flights[(origin,dest)].append((depart,arrive,int(price)))
```
定义工具函数getminutes()，用于计算某个给定时间在一天中的分钟数。    
```python
def getminutes(t):
  x=time.strptime(t,'%H:%M')
  return x[3]*60+x[4]
```

### 描述题解    

优化函数应该是通用的，能应用于许多不同类型的问题上。

一种通用的表达方式，就是数字序列。例如：s=[1,4,3,2,7,3,6,3,2,4,5,3]，表示Seymour搭乘当天第1趟航班出发，第4趟航班回家，Franny搭乘当天第3趟航班出发，第2趟航班回家...

函数printschedule用于将行程计划打印成表格，便于观察。   
```python
def printschedule(r):
  for d in range(len(r)/2):
    name=people[d][0]
    origin=people[d][1]
    out=flights[(origin,destination)][int(r[2*d])]  #纠错
    ret=flights[(destination,origin)][int(r[2*d+1])]
    print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                  out[0],out[1],out[2],
                                                  ret[0],ret[1],ret[2])
```
输入以下命令：  
```python
import optimization
s=[1,4,3,2,7,3,6,3,2,4,5,3]
optimization.printschedule(s)
```
得到：  
```python
Seymour       BOS  8:04-10:11 $95 12:08-14:05 $142
Franny       DAL 10:30-14:57 $290  9:49-13:51 $229
Zooey       CAK 17:08-19:08 $262 10:32-13:16 $139
Walt       MIA 15:34-18:11 $326 11:08-14:38 $262
Buddy       ORD  9:42-11:32 $169 12:08-14:47 $231
Les       OMA 13:37-15:08 $250 11:07-13:24 $171
```

### 成本函数    

任何优化算法的目标，就是要寻找一组能使得成本函数的返回结果达到最小化输出。

考查一些在组团旅游中能被度量的变量：

```python
价格    
    所有航班的总票价，也可以是考虑财务因素之后的加权平均。

旅行时间    
    每个人在飞机上花费的总时间。
    
等待时间
    在机场等待其它成员到达的时间。

出发时间
    不能出发得太早，因为这会白白浪费旅行者的时间。
        
汽车租用时间
    如果集体租用一辆汽车，他们必须按时归还以免多付一天的租金。
```

接下来，将找到一种方法将它们组合在一起形成一个值。

将函数schedulecost()加入到optimization类中。    

```python
def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol) / 2):
        # 得到往返航班
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d + 1])]

        # 计算所有往返航班的总价格
        totalprice += outbound[2]
        totalprice += returnf[2]

        # 记录最晚到达时间和最早离开时间
        if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])

    # 大家必须在机场等待最后一个到达者
    # 同样，他们也会在相同时间到达机场，等待他们的航班
    totalwait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d + 1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

        # 判断该题解是否需要多付一天的汽车租金
    if latestarrival < earliestdep: totalprice += 50

    return totalprice + totalwait
```

### 随机搜索    

它是一种很好的优化算法，也是用来评估其它算法优劣的基线。    

函数randomoptimize()接受两个参数。  

1.Domain，为一个由二元组构成的列表，它指定了每个变量的最大最小值。本例中，由于往返航班都是10，故而domain为(0,9)   

2.costf，成本函数，本例中为schedulecost。   

本例中将随机产生1000次猜测



```python
def randomoptimize(domain, costf):
    best = 999999999
    bestr = None
    for i in range(0, 1000):
        # 创建一个随机题解
        r = [float(random.randint(domain[i][0], domain[i][1]))
             for i in range(len(domain))]

        # 得到花费
        cost = costf(r)

        # 与目前最优解比较
        if cost < best:
            best = cost
            bestr = r
    return r
```

输入以下命令：  

```python
reload(optimization)
domain=[(0,8)]*(len(optimization.people)*2)
s=optimization.randomoptimize(domain,optimization.schedulecost)
print optimization.schedulecost(s)
print optimization.printschedule(s)
```

可以找到一个表现尚可的解（也许不是最优的）：

```python
6444
   Seymour       BOS 17:11-18:30 $108 17:03-18:03 $103
    Franny       DAL  6:12-10:22 $230  9:49-13:51 $229
     Zooey       CAK  8:27-10:45 $139 18:17-21:04 $259
      Walt       MIA  9:15-12:29 $225 16:50-19:26 $304
     Buddy       ORD  6:05- 8:32 $174  9:11-10:42 $172
       Les       OMA  9:15-12:03 $ 99 16:35-18:56 $144
```

### 爬山法  

随即尝试没有充分利用已发现的优解，相当低效。

一种替代方法便是爬山法。爬山法以一个随机解开始，然后在其临近的解集中寻找更好的解。  

![pic](http://img1.ph.126.net/wZo8QUqK7d9YRRjDAQWMYw==/6631871508702533206.png) 

先从一个随机的时间安排开始，然后再找与之相邻的安排。在本例中，即对每个相邻的时间安排都进行成本计算，具有最低成本的安排将成为新的题解。重复直到不再变化为止。  

将hillclimb函数加入optimization类中：   

```python
def hillclimb(domain, costf):
    # 创建一个随机题解
    sol = [random.randint(domain[i][0], domain[i][1])
           for i in range(len(domain))]
    # 死循环
    while 1:
        # 创建邻居解
        neighbors = []

        for j in range(len(domain)):
            # 在每个方向相对于原值偏离
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j] + [(sol[j] + 1) if ((sol[j] + 1)<domain[j][1]) else domain[j][0]] + sol[j + 1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j] + [(sol[j] - 1) if ((sol[j] - 1)>domain[j][0]) else domain[j][1]] + sol[j + 1:])

        # 在相邻点中寻找最优解
        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]

        # 直到不再变化为止
        if best == current:
            break
    return sol
```

执行该函数：    

```python
reload(optimization)
s=optimization.hillclimb(domain,optimization.schedulecost)
print optimization.schedulecost(s)
print optimization.printschedule(s)
```

得到结果：  

```python
3554
   Seymour       BOS 18:34-19:36 $136  8:23-10:28 $149
    Franny       DAL 18:26-21:29 $464  9:49-13:51 $229
     Zooey       CAK 18:35-20:28 $204  8:19-11:16 $122
      Walt       MIA 18:23-21:35 $134  6:33- 9:14 $172
     Buddy       ORD 19:50-22:24 $269  6:03- 8:43 $219
       Les       OMA 20:05-22:06 $261  8:04-10:59 $136
```

![pic](http://img1.ph.126.net/KRzJBQi-04tO-UKoV2mGSw==/6632119998330410374.png) 

从上图中可以看出，有可能只是得到一个局部最优解。解决这一问题的方法被称为随机重复爬山法，即让爬山法以多个随机生成的初始解为起点运行若干次，希望其中的一个解能逼近全局最小值。    

### 模拟退火算法    

算法的最关键部分在于：如果新的成本值更低，则新的题解就会成为当前题解。这与爬山法很相似。不过，如果成本值更高，则新的题解仍将可能成为当前题解。这就从一定程度上避免了局部最小值的问题。

它之所以管用，不仅因为它总是会接受一个更优的解，而且因为他在退火过程的开始阶段会接受表现较差的解。随着算法的不断进行，其越来越不可能接受较差的解，直到最后它只会接受更优的解。其数学公式如下：

​	p=e (-(highcost–lowcost)/temperature)

由公式可见，温度开始非常高，指数总将接近于0，所以概率几乎为１,随着温度的递减，高低成本值之间的差异越来越重要——差异越大，概率越低，因此该算法只倾向于稍差的解而不是非常差的解。

```python
def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
  # 随机初始化值
  vec=[float(random.randint(domain[i][0],domain[i][1])) 
       for i in range(len(domain))]
  
  while T>0.1:
    # 选择一个索引值
    i=random.randint(0,len(domain)-1)

    # 选择一个改变索引值的方向
    dir=random.randint(-step,step)

    # 创建一个代表题解的新列表，改变其中的一个值
    vecb=vec[:]
    vecb[i]+=dir
    if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
    elif vecb[i]>domain[i][1]: vecb[i]=domain[i][1]

    # 计算当前成本和新的成本
    ea=costf(vec)
    eb=costf(vecb)
    p=pow(math.e,(-eb-ea)/T)

    # 判断是否为更好的解，或者趋向最优解可能的临界解？
    if (eb<ea or random.random()<p):
      vec=vecb      

    # 降低温度
    T=T*cool
  return vec
```

运行如下代码：

```python
reload(optimization)
s=optimization.annealingoptimize(domain,optimization.schedulecost)
print optimization.schedulecost(s)
optimization.printschedule(s)
```

输出结果：

```python
3376
   Seymour       BOS 12:34-15:02 $109 10:33-12:03 $ 74
    Franny       DAL 10:30-14:57 $290 10:51-14:16 $256
     Zooey       CAK  8:27-10:45 $139 13:37-15:33 $142
      Walt       MIA 11:28-14:40 $248 15:23-18:49 $150
     Buddy       ORD  9:42-11:32 $169 10:33-13:11 $132
       Les       OMA  9:15-12:03 $ 99 15:07-17:21 $129
```

### 遗传算法

运行过程：先随机生成一组解，称之为种群。优化过程的每一步，算法会计算整个种群的成本函数，从而得到一个有关题解的有序列表。

| Solution                             | Cost |
| ------------------------------------ | ---- |
| [7, 5, 2, 3, 1, 6, 1, 6, 7, 1, 0, 3] | 4394 |
| [7, 2, 2, 2, 3, 3, 2, 3, 5, 2, 0, 8] | 4661 |
| ...                                  | ...  |
| [0, 4, 0, 3, 8, 8, 4, 4, 8, 5, 6, 1] | 7845 |
| [5, 8, 0, 2, 8, 8, 8, 2, 1, 6, 6, 8] | 8088 |

在对题解进行排序之后，我们将创建出一个新的种群，称之为下一代。

首先，将当前种群中位于最顶端的题解加入其所在的新种群中，称为精英选拔。

新种群中的余下部分是由修改最优解后形成的全新解组成。

两种修改题解的方法：

- 变异

  较为简单。通常是对一个现有解进行微小的、简单的、随机的改变。

  [7, 5, 2, 3, 1, 6, 1, **6**, 7, 1, 0, 3]----->[7, 5, 2, 3, 1, 6, 1, **5**, 7, 1, 0, 3]

  [7, 2, 2, 2, 3, 3, 2, 3, 5, 2, **0**, 8]----->[7, 2, 2, 2, 3, 3, 2, 3, 5, 2, **1**, 8]

- 交叉（配对）

  选取最优解中的两个解，然后将它们按某种方式进行结合。

  [**7, 5, 2, 3, 1, 6, 1, 6,**｜ 7, 1, 0, 3]------------>

  ​								[**7, 5, 2, 3, 1, 6, 1, 6,** |**5, 2, 0, 8**]

  [7, 2, 2, 2, 3, 3, 2, 3,｜ **5, 2, 0, 8**]-------------------------------------->

一个新的种群是通过对最优解进行随机变异和配对处理构造出来的，其大小通常与旧种群相同。尔后，重复这一过程——新的种群经过排序，构造一个新的种群。达到指定的迭代次数后，或者经过数代后题解都没有得到改善，整个过程就结束了。

将geneticoptimize加入optimization.py中：

```python
# popsize 种群大小 mutprob种群新成员是由变异而非交叉得来的概率 
# elite 种群被认为是优解且允许被传入下一代的部分 maxiter 需运行多少代
def geneticoptimize(domain,costf,popsize=50,step=1,
                    mutprob=0.2,elite=0.2,maxiter=100):
    # 变异操作(原作中没有添加else语句从而会导致“Python: TypeError: object of type 'NoneType' has no len()”的错误)
    def mutate(vec):
        if random.random()<0.7:
            i=random.randint(0,len(domain)-1)
            if vec[i]>domain[i][0]:
                return vec[0:i]+[vec[i]-step]+vec[i+1:]
            elif vec[i]<domain[i][1]:
                return vec[0:i]+[vec[i]+step]+vec[i+1:]
            elif vec[i]==domain[i][1]:
                return vec[0:i]+domain[i][0]+vec[i+1:]
            elif vec[i]==domain[i][0]:
                return vec[0:i]+domain[i][1]+vec[i+1:]
        return vec

    # 交叉操作
    def crossover(r1,r2):
        i=random.randint(1,len(domain)-2)
        return r1[0:i]+r2[i:]

    # 构造初始种群
    pop=[]
    for i in range(popsize):
        vec=[random.randint(domain[i][0],domain[i][1])
             for i in range(len(domain))]
        pop.append(vec)

    # 每一代中有多少胜出者？
    topelite=int(elite*popsize)

    # 主循环
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        ranked=[v for (s,v) in scores]

        # 从纯粹的胜出者开始
        pop=ranked[0:topelite]

        # 添加变异和配对后的胜出者
        while len(pop)<popsize:
            if random.random()<mutprob:

                # 变异
                c=random.randint(0,topelite)
                pop.append(mutate(ranked[c]))
            else:

                # 交叉
                c1=random.randint(0,topelite)
                c2=random.randint(0,topelite)
                pop.append(crossover(ranked[c1],ranked[c2]))

        # 打印当前最优值
        print scores[0][0]

    return scores[0][1]
```

运行以下语句：

```python
s=optimization.geneticoptimize(domain,optimization.schedulecost)
print s
optimization.printschedule(s)
```

输出：

```python
4971
4692
4219
...
2675
2675
2675
[3, 1, 2, 2, 3, 1, 2, 1, 2, 1, 2, 1]
   Seymour       BOS 11:16-13:29 $ 83  8:23-10:28 $149
    Franny       DAL  9:08-12:12 $364  9:49-13:51 $229
     Zooey       CAK 10:53-13:36 $189  8:19-11:16 $122
      Walt       MIA  9:15-12:29 $225  8:23-11:07 $143
     Buddy       ORD  9:42-11:32 $169  7:50-10:08 $164
       Les       OMA  9:15-12:03 $ 99  8:04-10:59 $136
```

下图展示了一种十分难达到最佳优化的示例。

![很难达到最佳优化的情况](http://img2.ph.126.net/swC9jSN0nVsygC3DPyVxbg==/6632485036189151948.png)



