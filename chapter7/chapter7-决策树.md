# 决策树建模

## 预测注册用户

预测一位用户成为付费顾客的可能性有多大。

| Referrer  | Location    | Read FAQ | Pages viewed | Service chosen |
| --------- | ----------- | -------- | ------------ | -------------- |
| Slashdot  | USA         | Yes      | 18           | None           |
| Google    | France      | Yes      | 23           | Premium        |
| Digg      | USA         | Yes      | 24           | Basic          |
| Kiwitobes | France      | Yes      | 23           | Basic          |
| Google    | UK          | No       | 21           | Premium        |
| (direct)  | New Zealand | No       | 12           | None           |
| (direct)  | UK          | No       | 21           | Basic          |
| Google    | USA         | No       | 24           | Premium        |
| Slashdot  | France      | Yes      | 19           | None           |
| Digg      | USA         | No       | 18           | None           |
| Google    | UK          | No       | 18           | None           |
| Kiwitobes | UK          | No       | 19           | None           |
| Digg      | New Zealand | Yes      | 12           | Basic          |
| Google    | UK          | Yes      | 18           | Basic          |
| Kiwitobes | France      | Yes      | 19           | Basic          |

新建treepredict.py文件，加入：

```python
my_data=[['slashdot','USA','yes',18,'None'],
         ['google','France','yes',23,'Premium'],
         ['digg','USA','yes',24,'Basic'],
         ['kiwitobes','France','yes',23,'Basic'],
         ['google','UK','no',21,'Premium'],
         ['(direct)','New Zealand','no',12,'None'],
         ['(direct)','UK','no',21,'Basic'],
         ['google','USA','no',24,'Premium'],
         ['slashdot','France','yes',19,'None'],
         ['digg','USA','no',18,'None'],
         ['google','UK','no',18,'None'],
         ['kiwitobes','UK','no',19,'None'],
         ['digg','New Zealand','yes',12,'Basic'],
         ['slashdot','UK','no',21,'None'],
         ['google','UK','yes',18,'Basic'],
         ['kiwitobes','France','yes',19,'Basic']]
```

## 引入决策树

沿着树往下走，可得答案；沿着叶节点向上回溯，可得推理过程。

首先，构造决策树的表达形式。新建一个类decisionnode，代表树上的每个节点：

```python
class decisionnode:
 def__init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col #待检验的判断条件所对应的列索引值
        self.value=value #为了使结果为true,当前列必须匹配的值
        self.results=results #针对于当前分支的结果,除了叶节点,其它节点都为None
        self.tb=tb #true or false的子树节点
        self.fb=fb
```

![决策树示例](http://img2.ph.126.net/l47Xt8kWKWqk_d5NYOKpcg==/6632594987351942735.png)

## 对树进行训练

分类回归树算法(CART)：首先创建一个根节点。然后通过评估表中的所有观测变量，从中选出最合适的变量对数据进行拆分。为此，算法考查了所有不同的变量，然后从中选出一个条件（eg. Read FAQ）对结果数据进行分解，以使我们能更容易地推测出用户的意图来（which service the user signed up for）。

在中加入divideset函数：

```python
# 在某一列上对数据集进行拆分，能够处理数值型数据或名词性数据
def divideset(rows,column,value):
    # 定义一个函数，令其告诉我们数据行属于第一组或是第二组（true or false）
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value

    # 将数据集拆分成两个集合，并返回
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)
```

运行以下语句：

```python
import treepredict
print treepredict.divideset(treepredict.my_data,2,'yes')
```

返回的结果并不理想，true or false两边都混杂了各种情况：

```python
([['slashdot', 'USA', 'yes', 18, 'None'],
  ['google', 'France', 'yes', 23, 'Premium'],
  ['digg', 'USA', 'yes', 24, 'Basic'],
  ['kiwitobes', 'France', 'yes', 23, 'Basic'],
  ['slashdot', 'France', 'yes', 19, 'None'], 
  ['digg', 'New Zealand', 'yes', 12, 'Basic'],
  ['google', 'UK', 'yes', 18, 'Basic'],
  ['kiwitobes', 'France', 'yes', 19, 'Basic']],
 [['google', 'UK', 'no', 21, 'Premium'],
  ['(direct)', 'New Zealand', 'no', 12, 'None'],
  ['(direct)', 'UK', 'no', 21, 'Basic'],
  ['google', 'USA', 'no', 24, 'Premium'],
  ['digg', 'USA', 'no', 18, 'None'], 
  ['google', 'UK', 'no', 18, 'None'],
  ['kiwitobes', 'UK', 'no', 19, 'None'],
  ['slashdot', 'UK', 'no', 21, 'None']])
```

## 选择最合适的拆分方案

为了选择合适的变量，需要一种方法来衡量数据集合中各种因素的混合情况。所以，在treepredict.py中加入以下函数，来对数据集中每一项结果进行计数：

```python
# 对各种可能的结果进行计数
def uniquecounts(rows):
    results={}
    for row in rows:
        # 计数结果在最后一列
        r=row[len(row)-1]
        if r not in results: results[r]=0
        results[r]+=1
    return results
```

对于混杂程度的测量，有几种不同的度量方式可供选择：基尼不纯度和熵。

### 基尼不纯度

指将来自集合中的某种结果随机应用于集合中某一数据项的预期误差率。

基尼不纯度的计算函数如下：

```python
# 随机放置的数据项出现于错误分类中的概率
def giniimpurity(rows):
    total=len(rows)
    counts=uniquecounts(rows)
    imp=0
    for k1 in counts:
        p1=float(counts[k1])/total
        for k2 in counts:
            if k1==k2: continue
            p2=float(counts[k2])/total
            imp+=p1*p2
    return imp
```

该函数利用集合中每一项结果出现的次数除以集合的总行数来计算相应的概率，然后将所有这些概率值的乘积累加起来。这样就会得到某一行数据被随机分配到错误结果的总概率。概率越高，说明结果越不理想。

### 熵

代表集合的无序程度。如果所有结果都相同，则熵为0，之所以将数据拆分成两个新组，其目的就是要降低熵。

数学公式如下：
$$
p(i) = frequency(outcome) = count(outcome) / count(total rows)
$$

$$
Entropy = sum 　of 　p(i) x log(p(i))　 for　 all 　outcomes
$$

在treepredict.py中以下函数：

```python
# 熵是遍历所有可能结果之后所得到的p(x)logp(x)之和
def entropy(rows):
    from math import log
    log2=lambda x:log(x)/log(2)
    results=uniquecounts(rows)
    # 此处开始计算熵的值
    ent=0.0
    for r in results.keys():
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent
```

分别尝试一下基尼不纯度和熵这两种度量方法：

```python
reload(treepredict)
print treepredict.giniimpurity(treepredict.my_data)
print treepredict.entropy(treepredict.my_data)
set1,set2=treepredict.divideset(treepredict.my_data,2,'yes')
print treepredict.entropy(set1)
print treepredict.giniimpurity(set1)
```

输出：

```python
0.6328125
1.50524081494
1.2987949407
0.53125	
```

二者的主要区别在于，熵达到峰值的过程相对慢一些，即熵对于混乱集合的判罚往往更重。

### 以递归方式构造树

**信息增益**：指当前熵与两个新群组经加权平均后的熵之间的差值。

算法会针对每个属性计算相应的信息增益，然后从中选出信息增益最大的属性。

![](http://img2.ph.126.net/7TNfKHCva7o98vwb3Ah_qQ==/6632310213840346388.png)

![](http://img0.ph.126.net/DjBakCruCpfwdl2rZcYdHQ==/6632291522142674874.png)

通过计算每个新生节点的最佳拆分属性，对分支的拆分过程和树的构造过程会持续下去。当拆分某个节点所得的信息增益不大于0的时候，对分支的拆分才会停止。

在treepredict.py中新建一个函数buildtree：

```python
# 通过为当前数据集选择最合适的拆分条件来实现决策树的构造过程
def buildtree(rows,scoref=entropy):
    if len(rows)==0: return decisionnode()
    current_score=scoref(rows)

    # 定义一些变量以记录最佳拆分条件
    best_gain=0.0
    best_criteria=None
    best_sets=None

    column_count=len(rows[0])-1
    for col in range(0,column_count):
        # 在当前列中生成一个由不同值构成的序列
        column_values={}
        for row in rows:
            column_values[row[col]]=1
        # 接下来尝试根据这一列中的每个值，尝试对数据集进行拆分
        for value in column_values.keys():
            (set1,set2)=divideset(rows,col,value)

            # 信息增益
            p=float(len(set1))/len(rows)
            gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)
    # 创建子分支
    if best_gain>0:
        trueBranch=buildtree(best_sets[0])
        falseBranch=buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0],value=best_criteria[1],
                            tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))
```

运行以下语句生成决策树：

```python
reload(treepredict)
tree=treepredict.buildtree(treepredict.my_data)
```

### 决策树的显示

以纯文本的方式显示：

```python
def printtree(tree,indent=''):
    # 这是一个叶节点吗？
    if tree.results!=None:
        print str(tree.results)
    else:
        # 打印判断条件
        print str(tree.col)+':'+str(tree.value)+'? '

        # 打印分支
        print indent+'T->',
        printtree(tree.tb,indent+'  ')
        print indent+'F->',
        printtree(tree.fb,indent+'  ')
```

输入以下语句：

```python
reload(treepredict)
treepredict.printtree(tree)
```

输出：

```python
0:google? 
T-> 3:21? 
  T-> {'Premium': 3}
  F-> 2:yes? 
    T-> {'Basic': 1}
    F-> {'None': 1}
F-> 0:slashdot? 
  T-> {'None': 3}
  F-> 2:yes? 
    T-> {'Basic': 4}
    F-> 3:21? 
      T-> {'Basic': 1}
      F-> {'None': 3}
```

图形方式显示：

```python
def getwidth(tree):
    if tree.tb==None and tree.fb==None: return 1
    return getwidth(tree.tb)+getwidth(tree.fb)

def getdepth(tree):
    if tree.tb==None and tree.fb==None: return 0
    return max(getdepth(tree.tb),getdepth(tree.fb))+1

from PIL import Image,ImageDraw

def drawtree(tree,jpeg='tree.jpg'):
    w=getwidth(tree)*100
    h=getdepth(tree)*100+120

    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    drawnode(draw,tree,w/2,20)
    img.save(jpeg,'JPEG')

def drawnode(draw,tree,x,y):
    if tree.results==None:
        # 得到每个分支的宽度
        w1=getwidth(tree.fb)*100
        w2=getwidth(tree.tb)*100

        # 确定此节点所要占据的总空间
        left=x-(w1+w2)/2
        right=x+(w1+w2)/2

        # 绘制判断条件字符串
        draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

        # 绘制到分支的连线
        draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))

        # 绘制分支的节点
        drawnode(draw,tree.fb,left+w1/2,y+100)
        drawnode(draw,tree.tb,right-w2/2,y+100)
    else:
        txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
        draw.text((x-20,y),txt,(0,0,0))
```

输出：

![](http://img2.ph.126.net/uUvuIpsCx-kEyoKSZcknLg==/6632560902491505824.jpg)

### 对新的观测数据进行分类

在treepredict.py中加入以下函数，接受新的观测数据作为参数，然后根据决策树对其进行分类。

```python
def classify(observation,tree):
  if tree.results!=None:
    return tree.results
  else:
    v=observation[tree.col]
    branch=None
    if isinstance(v,int) or isinstance(v,float):
      if v>=tree.value: branch=tree.tb
      else: branch=tree.fb
    else:
      if v==tree.value: branch=tree.tb
      else: branch=tree.fb
    return classify(observation,branch)
```

采用与printtree完全相同的方式对树进行遍历：

```python
reload(treepredict)
print treepredict.classify(['(direct)','USA','yes',5],tree)
```

输出：

```
{'Basic': 4}
```

### 决策树的剪枝

前述的训练方法可能存在过拟合问题，即过于针对训练数据。

一种可能的解决方法是，当信息增益小于某个最小值时，就停止分支的创建。但是也存在一些缺陷，比如某一次分支的创建并不会另熵降低多少，但是随后创建的分支却会使熵大幅降低。对此一种替代策略便是，先构造好如前所述的整棵树，然后再尝试消除多余的节点。

在treepredict.py中加入用于枝剪的新函数：

```python
def prune(tree,mingain):
    # 如果分支不是叶节点，则对其进行剪枝操作
    if tree.tb.results==None:
        prune(tree.tb,mingain)
    if tree.fb.results==None:
        prune(tree.fb,mingain)

    # 如果两个子分支都是叶节点，则判断它们是否需要合并
    if tree.tb.results!=None and tree.fb.results!=None:
        # 构造合并后的数据集
        tb,fb=[],[]
        for v,c in tree.tb.results.items():
            tb+=[[v]]*c
        for v,c in tree.fb.results.items():
            fb+=[[v]]*c

        # 检查熵的减少情况
        delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)

        if delta<mingain:
            # 合并分枝
            tree.tb,tree.fb=None,None
            tree.results=uniquecounts(tb+fb)
```

输入不同的最小增益值，看是否会有节点被合并：

```python
reload(treepredict)
treepredict.prune(tree,0.1)
treepredict.printtree(tree)
treepredict.prune(tree,1.0)
treepredict.printtree(tree)
```

输出：

```python
0:google? 
T-> 3:21? 
  T-> {'Premium': 3}
  F-> 2:yes? 
    T-> {'Basic': 1}
    F-> {'None': 1}
F-> 0:slashdot? 
  T-> {'None': 3}
  F-> 2:yes? 
    T-> {'Basic': 4}
    F-> 3:21? 
      T-> {'Basic': 1}
      F-> {'None': 3}
0:google? 
T-> 3:21? 
  T-> {'Premium': 3}
  F-> 2:yes? 
    T-> {'Basic': 1}
    F-> {'None': 1}
F-> {'None': 6, 'Basic': 5}
```

可以看到，当最小增益值调的很高的时候，某个叶节点才会被合并。

### 处理缺失数据

决策树的另一个优点，就是它处理缺失数据的能力。

```python
def mdclassify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        if v==None:
            tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
            tcount=sum(tr.values())
            fcount=sum(fr.values())
            tw=float(tcount)/(tcount+fcount)
            fw=float(fcount)/(tcount+fcount)
            result={}
            for k,v in tr.items(): result[k]=v*tw
            for k,v in fr.items(): result[k]=v*fw
            return result
        else:
            if isinstance(v,int) or isinstance(v,float):
                if v>=tree.value: branch=tree.tb
                else: branch=tree.fb
            else:
                if v==tree.value: branch=tree.tb
                else: branch=tree.fb
            return mdclassify(observation,branch)
```

针对关键信息缺失的数据行，输入：

```python
reload(treepredict)
print treepredict.mdclassify(['google',None,'yes',None],tree)
print treepredict.mdclassify(['google','France',None,None],tree)
```

输出：

```python
{'Premium': 2.25, 'Basic': 0.25}
{'None': 0.125, 'Premium': 2.25, 'Basic': 0.125}
```

注：由于种种原因，我们不一定总是能掌握足够的信息来做出正确的分类——某些节点可能具有多种结果值，但是又无法进一步拆分，于是返回一个字典对象，其中包含不同结果的统计量，借助于此可以判断出结果的可信度。

### 处理数值型结果

在以数字作为输出结果的数据集上执行buildtree函数时，效果不一定理想。例如，有的数字离得很近，而其它数字则相差很远，但我们将这些数字都完全看作了绝对的离散。

此时应使用方差作为评价函数来构造决策树，节点的判断条件就变成了：拆分之后令数字较大者位于树的一侧，数字较小者位于树的另一侧。

将variance加入到treepredict.py中，用以计算一个数据集的统计方差：

```python
def variance(rows):
  if len(rows)==0: return 0
  data=[float(row[len(row)-1]) for row in rows]
  mean=sum(data)/len(data)
  variance=sum([(d-mean)**2 for d in data])/len(data)
  return variance
```

### 

