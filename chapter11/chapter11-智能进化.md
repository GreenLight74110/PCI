## 智能进化

本章将编写一个程序，尝试自动构造出解决某一问题的最佳程序来。从本质上来看，也就是构造一个能构造算法的算法。

### 什么是遗传编程

下图展示了遗传编程算法执行的一个大体过程。

![](http://img2.ph.126.net/8qwZ5HNDcQ6RHAThgh5OBg==/6632516922026554862.png)

### 程序以树形方式表示

大多数编程语言，在编译或解释时，首先会被转换成一颗解析树。

解析树的一个例子：

![](http://img2.ph.126.net/MKWNKLAeP9ibmzF0i1Y-Dw==/6632635669279760279.png)

树上有一个节点的操作为"if"，这表示：如果该节点左侧分支的计算结果为真，它将返回中间分支，如果不为真，返回右侧分支。

对整棵树进行遍历，其实就相当于下面这个python函数：

```python
def func(x,y):
    if x>3:
        return y + 5
    else:
        return y - 2
```

### 在python中表现树

新建gp.py文件，并且新建4个类：fwrapper、node、paramnode、constnode：

```python
from random import random, randint, choice
from copy import deepcopy
from math import log


# 一个封装类，对应于“函数型”节点上的函数。
class fwrapper:
    def __init__(self, function, childcount, name):
        self.function = function  # 函数本身
        self.childcount = childcount  # 函数接受的参数个数
        self.name = name  # 函数名称


# 对应于函数型节点。
class node:
    # 以fwrapper类对其进行初始化
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children

    # evaluate被调用时，会对各个子节点进行求值运算，然后将函数本身应用于求得的结果
    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    # 显示出整棵树的字符串表示形式
    def display(self, indent=0):
        print (' ' * indent) + self.name
        for c in self.children:
            c.display(indent + 1)


# 该类对应的节点只返回传递给程序的某个参数
class paramnode:
    def __init__(self, idx):
        self.idx = idx

    # evaluate返回的是由idx指定的参数
    def evaluate(self, inp):
        return inp[self.idx]

    # 打印出该节点返回参数的对应索引即可
    def display(self, indent=0):
        print '%sp%d' % (' ' * indent, self.idx)


# 返回常量值的节点
class constnode:
    def __init__(self, v):
        self.v = v

    # evaluate方法仅返回该类被初始化时所传入的值
    def evaluate(self, inp):
        return self.v

    # 打印常量值
    def display(self, indent=0):
        print '%s%d' % (' ' * indent, self.v)

```

此外，还会用到一些针对节点的操作函数，然后利用fwrapper类赋予它们名称和参数个数：

```python
addw=fwrapper(lambda l:l[0]+l[1],2,'add')
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract') 
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply')

def iffunc(l):
  if l[0]>0: return l[1]
  else: return l[2]
ifw=fwrapper(iffunc,3,'if')

def isgreater(l):
  if l[0]>l[1]: return 1
  else: return 0
gtw=fwrapper(isgreater,2,'isgreater')

# 创建了一个包含所有函数的列表，这样就可以稍后对它们进行随机选择了
flist=[addw,mulw,ifw,gtw,subw]
```

### 树的构造和评估

在gp.py中加入exampletree：

```python
def exampletree():
  return node(ifw,[
                  node(gtw,[paramnode(0),constnode(3)]),
                  node(addw,[paramnode(1),constnode(5)]),
                  node(subw,[paramnode(1),constnode(2)]),
                  ]
              )
```

利用刚刚创建的节点类来构造一颗程序树：

```python
import gp
exampletree = gp.exampletree()
print exampletree.evaluate([2, 3])
print exampletree.evaluate([5, 3])
```

输出：

```python
1
8
```

### 程序的展现

利用上述方法打印出整棵树：

```python
reload(gp)
exampletree=gp.exampletree( )
print exampletree.display( )
```

输出：

```python
if
 isgreater
  p0
  3
 add
  p1
  5
 subtract
  p1
  2
None
```

### 构造初始种群

创建一个随机程序的步骤包括：创建根节点并为其随机指定一个关联函数--->随机创建尽可能多的子节点--->子节点也可能会有它们自己的随机关联子节点。

在gp.py中添加makerandomtree函数：

```python
def makerandomtree(pc,maxdepth=4,fpr=0.5,ppr=0.6):
  if random()<fpr and maxdepth>0:
    f=choice(flist)
    children=[makerandomtree(pc,maxdepth-1,fpr,ppr) 
              for i in range(f.childcount)]
    return node(f,children)
  elif random()<ppr:
    return paramnode(randint(0,pc-1))
  else:
    return constnode(randint(0,10))
```

输入：

```python
random1=gp.makerandomtree(2)
print random1.evaluate([7,1])
print random1.evaluate([2,4])
random2=gp.makerandomtree(2)
print random2.evaluate([5,3])
print random2.evaluate([5,20])
random1.display( )
random2.display( )
```

输出：

```python
3
6
5
5
add
 multiply
  isgreater
   add
    p0
    p0
   p0
  2
 if
  7
  p1
  0
5

```

### 测试题解

#### 一个简单的数学测试

假设有一张包含输入和输出的表：

![](http://img1.ph.126.net/UhYHgarCro7CF2uQ13Qoww==/1277896394284420915.png)

在gp.py中加入hiddenfunction函数，其实就是上表的计算公式：

```python
def hiddenfunction(x,y):
    return x**2+2*y+3*x+5
```

加入buildhiddenset函数，用以构造数据集：

```python
def buildhiddenset():
  rows=[]
  for i in range(200):
    x=randint(0,40)
    y=randint(0,40)
    rows.append([x,y,hiddenfunction(x,y)])
  return rows
```

现在利用这些数据，让遗传编程重新构造出这一函数来。

#### 衡量程序的好坏

由于本例是在一个数值型结果的基础上对程序进行测试，因此用程序与代表正确答案的数据集之间的接近程度来测试。

在gp.py中加入scorefunction函数：

```python
def scorefunction(tree,s):
  dif=0
  for data in s:
    v=tree.evaluate([data[0],data[1]])
    dif+=abs(v-data[2])
  return dif
```

将计算函数的输出结果与实际结果进行比较，再将所有的差值累加起来。累加值越小，代表题解的表现越好。

```python
reload(gp)
print gp.scorefunction(random2,hiddenset)
print gp.scorefunction(random1,hiddenset)
```

输出：

```python
117070
117470
```

### 对程序进行变异

变异的做法是对该程序进行一些修改，在这里可以改变节点上的函数、也可以改变节点的分支。

下图展示了一个改变了子节点数目的函数，为此可以删除旧的分支，也可以增加新的分支。

![](http://img1.ph.126.net/vkcPehjt7b8dez-MOsjchA==/6632331104561469493.png)

另一种方式，是利用一颗全新的树来替换某一子树。

![](http://img2.ph.126.net/KMyrZv5UVtQiqYFjrkUxHA==/6632268432398689844.png)

变异的次数不宜过多。每次要修改时都定义一个相对较小的概率。

加入mutate函数，实现第二种变异方式：

```python
def mutate(t,pc,probchange=0.1):
  if random()<probchange:
    return makerandomtree(pc)
  else:
    result=deepcopy(t)
    if hasattr(t,"children"):
      result.children=[mutate(c,pc,probchange) for c in t.children]
    return result
```

尝试对此前随机生成的程序执行若干次mutate函数，看函数是如何对树进行修改的：

```python
print random2.display( )
muttree=gp.mutate(random2,2)
print muttree.display( )

print gp.scorefunction(random2,hiddenset)
print gp.scorefunction(muttree,hiddenset)
```

输出：

```python
isgreater
 add
  7
  p0
 p0
None

isgreater
 if
  if
   subtract
    9
    p0
   5
   p1
  if
   subtract
    subtract
     0
     2
    isgreater
     p1
     4
   2
   subtract
    add
     1
     p1
    p0
  add
   p1
   isgreater
    p0
    subtract
     p0
     7
 p0
None

118350
118495
```

### 交叉

做法：从众多程序中选出两个表现优异者，将其组合在一起构造出一个新的程序。

在gp.py中加入crossover函数：

```python
def crossover(t1,t2,probswap=0.7,top=1):
    if random()<probswap and not top:
        return deepcopy(t2)
    else:
        result=deepcopy(t1)
        if hasattr(t1,'children') and hasattr(t2,'children'):
            result.children=[crossover(c,choice(t2.children),probswap,0)
                             for c in t1.children]
        return result
```

针对部分随机生成的程序执行一下crosscover函数，看交叉后的结果如何。

```python
add
 subtract
  subtract
   add
    5
    3
   if
    6
    1
    p0
  p0
 1
    
subtract
 if
  p1
  subtract
   8
   p0
  p0
 add
  multiply
   if
    p1
    p1
    p0
   p1
  multiply
   isgreater
    2
    1
   p0

add
 if
  p1
  subtract
   8
   p0
  p0
 if
  p1
  subtract
   8
   p0
  p0
```

### 构筑环境

思路：生成一组随机程序并择优复制和修改，然后一直重复这一过程直到终止条件满足。

新建evolve函数：

```python
# rankfunction 将一组程序按从优到劣的顺序进行排列
# mutationrate 代表发生变异的概率
# breedingrate 代表发生交叉的概率
# popsize 初始种群大小
# probexp 表示构造新种群时，“选择评价较低的程序”这一概率的递减比率。值越大，相应的筛选过程就越严格
# probnew 表示在构造新种群时，“引入一个全新的随机程序”的概率
def evolve(pc,popsize,rankfunction,maxgen=500,
           mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
    # 返回一个随机数，通常是一个较小的数
    # pexp取值越小，得到的随机数越小
    def selectindex():
        return int(log(random())/log(pexp))

    # 创建一个随机的初始种群
    population=[makerandomtree(pc) for i in range(popsize)]
    for i in range(maxgen):
        scores=rankfunction(population)
        print scores[0][0]
        if scores[0][0]==0: break

        # 总能得到两个最优的程序
        newpop=[scores[0][1],scores[1][1]]

        # 构造下一代
        while len(newpop)<popsize:
            if random()>pnew:
                newpop.append(mutate(
                    crossover(scores[selectindex()][1],
                              scores[selectindex()][1],
                              probswap=breedingrate),
                    pc,probchange=mutationrate))
            else:
                # 加入一个随机节点，以增加种群的多样性
                newpop.append(makerandomtree(pc))

        population=newpop
    scores[0][1].display()
    return scores[0][1]
```

在gp.py中加入getrankfunction函数，返回一个针对给定数据集的排序函数：

```python
def getrankfunction(dataset):
  def rankfunction(population):
    scores=[(scorefunction(t,dataset),t) for t in population]
    scores.sort()
    return scores
  return rankfunction
```

执行如下语句，为前述数据集自动生成数学公式的程序：

```python
reload(gp)
rf=gp.getrankfunction(gp.buildhiddenset( ))
print gp.evolve(2,500,rf,mutationrate=0.2,breedingrate=0.1,pexp=0.7,pnew=0.1)
```

输出：

```
16622
8620
8620
...
16
16
16
10
3
3
0
subtract
 5
 subtract
  isgreater
   p0
   p0
  subtract
   multiply
    p0
    add
     p0
     subtract
      8
      5
   subtract
    isgreater
     3
     8
    add
     p1
     p1
```

此处的数字变化很慢，但它最终应该会逐步减到0。尽管复杂，但它给出的解是完全正确的，对应于根据前面生成的树得到的：
$$
5-[(p0>p0)-[(8-5)+p0]*p0]-[(3>8)-(p1+p1)]
$$

$$
= 5+(3+p0)*p0-2p1
$$

$$
= p0^2+3p0-2p1+5
$$

实际上我们可以发现，经常会有大段内容不做任何工作，但始终都返回同一结果的公式。例如上述的(p0>p0)和(3>8)实际上返回的都是0。

要让程序保持简单的一种更好的方法是：允许程序不断　进化以行程优解，然后在删除并简化树中不必要的部分。

### 多样性的重要价值

如果仅仅选择表现优异的少数几个题解会使得种群变得极端同质化，从而导致局部最大化的情况。事实证明，将表现极为优异的题解和大量成绩尚可的题解组合在一起，往往能得到更好的结果。

### 一个简单的游戏

本节中，将编写一个简单的游戏模拟程序。为游戏引入人工智能，通过彼此竞争以及真人对抗，为表现优异的程序提供更多的进入下一代的机会。

![](http://img1.ph.126.net/2Fz18ulXngOw0HhvABvgjQ==/1281555568981705996.png)

**游戏规则**：两位玩家，没人轮流在网格中选择4个方向移动，游戏区域受限，当一位玩家企图移到边界以外，他就丢掉了这一局。

**游戏目标**：将自己移到对方所在的区域。

**附加条件**：当试图在一行的同一方向上移动两次，就算自动认输。

首先，创建一个函数，该函数涉及两位玩家，并在双方之间模拟一场游戏。函数将玩家及对手所在位置，连同所走的上一步，依次传给每一个程序，并根据返回结果决定下一步该如何移动。用0到3来代表移动的方向。

在gp.py中加入gridgame函数：

```python
def gridgame(p):
    # 游戏区域大小
    max=(3,3)

    # 记住玩家的上一步
    lastmove=[-1,-1]

    # 记住玩家的位置
    location=[[randint(0,max[0]),randint(0,max[1])]]

    # 将第二位玩家放在离第一位玩家足够远的地方
    location.append([(location[0][0]+2)%4,(location[0][1]+2)%4])
    # 打成平局前的最大移动步数
    for o in range(50):

        # 针对每位玩家
        for i in range(2):
            locs=location[i][:]+location[1-i][:]
            locs.append(lastmove[i])
            move=p[i].evaluate(locs)%4

            # 如果在一行中朝同一方向移动了两次就判输
            if lastmove[i]==move: return 1-i
            lastmove[i]=move
            if move==0:
                location[i][0]-=1
                # 限制游戏区域
                if location[i][0]<0: location[i][0]=0
            if move==1:
                location[i][0]+=1
                if location[i][0]>max[0]: location[i][0]=max[0]
            if move==2:
                location[i][1]-=1
                if location[i][1]<0: location[i][1]=0
            if move==3:
                location[i][1]+=1
                if location[i][1]>max[1]: location[i][1]=max[1]

            # 如果抓住了对方玩家，就判赢
            if location[i]==location[1-i]: return i
    return -1
```

1赢返回0，2赢返回1，平局返回-1。

尝试构造两个随机程序，并让他们彼此展开竞争：

```python
reload(gp)
p1=gp.makerandomtree(5)
p1.display()
print 'p1================p2'
p2=gp.makerandomtree(5)
p2.display()
print gp.gridgame([p1,p2])
```

输出：

```python
multiply
 p2
 isgreater
  p4
  5
p1================p2
isgreater
 10
 if
  add
   p3
   p1
  multiply
   p0
   9
  add
   multiply
    7
    8
   subtract
    9
    p2
1
```

### 循环赛

先让这些程序在一场比赛中彼此展开竞争，借此得以进化。

在gp.py中加入tournament函数，接受一个玩家列表作为输入，并让每位玩家与其它玩家一一对抗，同时记录每个程序在游戏中失败的次数。

```python
def tournament(pl):
    # 统计失败的次数
    losses=[0 for p in pl]

    # 每位玩家都和其它玩家一一对抗
    for i in range(len(pl)):
        for j in range(len(pl)):
            if i==j: continue

            # 谁是胜利者
            winner=gridgame([pl[i],pl[j]])

            # 失败得2分，打平得1分
            if winner==0:
                losses[j]+=2
            elif winner==1:
                losses[i]+=2
            elif winner==-1:
                losses[i]+=1
                losses[i]+=1
                pass

    # 对结果排序并返回
    z=zip(losses,pl)
    z.sort()
    return z
```

在python会话中，尝试上述函数：

```python
reload(gp)
winner=gp.evolve(5,100,gp.tournament,maxgen=50)
print winner
```

输出：

```python
42
30
44
58
...
50
56
76
66
add
 add
  isgreater
   10
   add
    subtract
     .....
```

注意到，代表失败次数的数字并没有严格递减。这是因为下一代种群完全是有新进化来的程序构成，所以上一代中表现优异的程序，在下一代中也许会表现得极为糟糕。







































