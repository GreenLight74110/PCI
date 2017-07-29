### 过滤垃圾信息

早期的策略为事先制定好一组规则。

现在我们想做的是，根据不同的用户所提供的消息——是否为垃圾信息，不断进行学习。



### 文档和单词

构造的分类器需要利用某些特征来对不同的内容项进行分类。

新建一个文件docclass.py，加入getwords函数，用以从文本中提取特征：

```python
import re
import math


def getwords(doc):
    splitter = re.compile('\\W*')
    # 根据非字母字符进行单词拆分
    words = [s.lower() for s in splitter.split(doc)
             if len(s) > 2 and len(s) < 20]
    # 返回一组不重复的单词
    return dict([(w, 1) for w in words])
	
```

### 分类器的训练

目的：从极为不确定的状态开始，随着分类器不断了解到哪些特征对于分类而言更为重要，其确定性也在逐步增加。

在docclass.py中新建一个名为classifier的类，针对不同用户、组群或查询，建立多个分类器实例，并对其加以训练，以相应特定组群的需求。

```python
class classifier:
    def __init__(self,getfeatures,filename=None):
        # 统计特征/分类组合的数量，记录位于各分类中的不同特征的数量
        # {'python': {'bad': 0, 'good': 6}, 'the': {'bad': 3, 'good': 3}}表示“the”被划归“bad”类的文档和“good”类的文档中各出现了三次，而“python”则只在"good"类文档中出现过
        self.fc={}
        # 统计每个分类中的文档数量，记录各分类被使用次数的字典
        self.cc={}
        # 提取特征，本例中对应getwords
        self.getfeatures=getfeatures
```

加入以下辅助函数，以实现计数值的增加和获取：

```python
# 增加特征/分类的计数值
def incf(self,f,cat):
  self.fc.setdefault(f,{})
  self.fc[f].setdefault(cat,0)
  self.fc[f][cat]+=1
# 增加对某一分类的计数值
def incc(self,cat):
  self.cc.setdefault(cat,0)
  self.cc[cat]+=1
# 某一特征出现于某一分类中的次数
def fcount(self,f,cat):
  if f in self.fc and cat in self.fc[f]:
  	return float(self.fc[f][cat])
  return 0.0
# 属于某一分类的内容项数量
def catcount(self,cat):
  if cat in self.cc:
  	return float(self.cc[cat])
  return 0
# 所有内容项的数量
def totalcount(self):
	return sum(self.cc.values( ))
# 所有分类的列表
def categories(self):
	return self.cc.keys( )
```

train方法接受一个文档和一个分类作为参数：

```python
def train(self,item,cat):
  features=self.getfeatures(item)
  # 针对该分类为每个特征增加计数值
  for f in features:
  	self.incf(f,cat)
  # 增加对该分类的计数值
  self.incc(cat)
```

输入以下语句：

```python
import docclass

cl = docclass.classifier(docclass.getwords)
cl.train('the quick brown fox jumps over the lazy dog', 'good')
cl.train('make quick money in the online casino', 'bad')
print cl.fcount('quick', 'good')
print cl.fcount('quick', 'bad')
```

返回：

```python
1.0
1.0
```

用一个函数将训练用的样本数据导入到分类器中。

```python
def sampletrain(cl):
  cl.train('Nobody owns the water.','good')
  cl.train('the quick rabbit jumps fences','good')
  cl.train('buy pharmaceuticals now','bad')
  cl.train('make quick money at the online casino','bad')
  cl.train('the quick brown fox jumps','good')
```

### 计算概率

在classifier中加入fprob()函数，对应于Pr(word | classification)，即对于一个给定的分类，某个单词出现的概率：

```python
def fprob(self,f,cat):
	if self.catcount(cat)==0: return 0
    # 特征在分类中出现的总次数除以分类中包含内容项的总数
	return self.fcount(f,cat)/self.catcount(cat)
```

执行以下语句：

```python
reload(docclass)
cl = docclass.classifier(docclass.getwords)
docclass.sampletrain(cl)
print cl.fprob('quick', 'good')
```

返回：

```
0.6666666666666
```

### 从一个合理的推测开始

当掌握的有关当前特征的信息极为有限时，我们还需根据一个假设的概率来作出判断。

一个推荐的初始值为0.5。

在classifier类中加入weightprob()函数：

```python
def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
  # 计算当前概率
  basicprob=prf(f,cat)
  # 统计特征在所有分类中出现的次数
  totals=sum([self.fcount(f,c) for c in self.categories( )])
  # 计算加权平均
  bp=((weight*ap)+(totals*basicprob))/(weight+totals)
  return bp
```

执行如下语句：

```python
reload(docclass)
cl = docclass.classifier(docclass.getwords)
docclass.sampletrain(cl)
print cl.weightedprob('money', 'good', cl.fprob)
docclass.sampletrain(cl)
print cl.weightedprob('money', 'good', cl.fprob)
```

返回：

```python
0.25
0.166666666667
```

总之对于一个过滤器而言，他最好应该有能力处理极少会出现的单词。

### 朴素分类器

选择一种方法将各个单词的概率进行组合，从而得出整篇文档属于该分类的概率。

缺陷：假设被组合的各个单词的概率是相互独立的。事实上，在现实这个假设是不成立的。

### 整篇文档的概率

首先要假设概率的彼此独立性：可以通过将所有的概率相乘，计算出所有的概率值。

```mathematica
Python出现在Bad中的概率：Pr(Python | Bad) = 0.2

Casino出现在Bad中的概率：(Pr(Casino | Bad) = 0.8)

二者同时出现在一篇文章中的独立概率：Pr(Python & Casino | Bad)—to be 0.8 × 0.2 = 0.16
```

在docclass.py中，新建一个naivebayes的classifier的子类，并为其添加一个docprob()方法：

```python
class naivebayes(classifier):
  def docprob(self,item,cat):
    features=self.getfeatures(item)
    # 所有特征值的概率相乘
    p=1
    for f in features: p*=self.weightedprob(f,cat,self.fprob)
    return p
```

该方法计算了Pr(Document | Category)，但我们真正需要的是Pr(Category | Document)，即对任一篇文档，它属于某个分类的概率。

### 贝叶斯定理简介

公式：

```python
Pr(A | B) = Pr(B | A) x Pr(A)/Pr(B)
```



在本例中，即为：

```mathematica
Pr(Category | Document) = Pr(Document | Category) x Pr(Category) /Pr(Document)
```

Pr(Document | Category)由上一节给出

Pr(Category)是随机选择选择一篇文档属于该分类的概率，也就是该分类的文档除以文档的总数。

Pr(Document)其实都是一样的，因此没必要计算出来。

在naivebayes类中加入以下方法：

```python
def prob(self,item,cat):
  catprob=self.catcount(cat)/self.totalcount( )
  docprob=self.docprob(item,cat)
  return docprob*catprob
```

执行如下语句：

```python
reload(docclass)
cl = docclass.naivebayes(docclass.getwords)
docclass.sampletrain(cl)
print cl.prob('quick rabbit', 'good')
print cl.prob('quick rabbit', 'bad')
```

返回：

```python
0.15625
0.05
```

### 选择分类

为每个分类定义一个最小阀值，在classifier中加入一个新的实例变量：

```python
def __init_ _(self,getfeatures):
  classifier.__init_ _(self,getfeatures)
  self.thresholds={}
```

加入几个用于设值和取值的简单方法，令其默认返回为1.0：

```python
def setthreshold(self,cat,t):
	self.thresholds[cat]=t
def getthreshold(self,cat):
  if cat not in self.thresholds: return 1.0
  return self.thresholds[cat]
```

现在开始构建classify方法。该方法将计算每个分类的概率，从中取出最大值，并将其与次最大概率比较，确定是否超过了指定的阀值。若没有一个分类满足上诉条件，方法就返回默认值。

```python
def classify(self,item,default=None):
  probs={}
  # 寻找概率的最大分类
  max=0.0
  for cat in self.categories( ):
    probs[cat]=self.prob(item,cat)
    if probs[cat]>max:
      max=probs[cat]
      best=cat
  # 确保概率值超出阈值×次大概率值
  for cat in probs:
    if cat==best: continue
    if probs[cat]*self.getthreshold(best)>probs[best]: return default
  return best
```

执行如下语句：

```python
reload(docclass)
cl=docclass.naivebayes(docclass.getwords)
docclass.sampletrain(cl)
print cl.classify('quick rabbit',default='unknown')
print cl.classify('quick money',default='unknown')
cl.setthreshold('bad',3.0)
print cl.classify('quick money',default='unknown')
for i in range(10): docclass.sampletrain(cl)
print cl.classify('quick money',default='unknown')
```

返回：

```python
good
bad
unknown
bad
```

### 费舍尔方法

朴素贝叶斯方法的一种替代方案。

### 针对特征的分类概率

本节将直接计算当一篇文档中出现某个特征时，该文档属于某个分类的可能性，即Pr(category | feature)。

计算Pr(category | feature)的常用方法：

```mathematica
（具有指定特征的属于某分类的文档数）/（具有指定特征的文档总数）
```

为了进行归一化计算，函数将分别求得3个量：

```mathematica
• 属于某分类的概率clf = Pr(feature | category)

• 属于所有分类的概率 freqsum = Sum of Pr(feature | category) 

• cprob = clf / (clf+nclf)

```

在docclass.py中为classifier新建一个子类，取名fisherclassifier，并加入以下方法：

```python
class fisherclassifier(classifier):
  def cprob(self,f,cat):
    # 特征在该分类中出现的概率
    clf=self.fprob(f,cat)
    if clf==0: return 0
    # 特征在所有分类中出现的概率
    freqsum=sum([self.fprob(f,c) for c in self.categories( )])
    # 概率等于特征在该分类中出现的概率除以总体概率
    p=clf/(freqsum)
    return p
```

尝试以下执行语句：

```python
reload(docclass)
cl=docclass.fisherclassifier(docclass.getwords)
docclass.sampletrain(cl)
print cl.cprob('quick','good')
print cl.cprob('money','bad')
print cl.weightedprob('money', 'bad', cl.fprob)
```

返回：

```python
0.571428571429
1.0
0.5
```

### 将各概率值组合起来

费舍尔方法的计算过程是将所有概率相乘起来，然后取自然对数，再将所得结果乘以-2。在fisherclassifier类中加入以下方法：

```python
def fisherprob(self,item,cat):
  # 所有概率相乘
  p=1
  features=self.getfeatures(item)
  for f in features:
  	p*=(self.weightedprob(f,cat,self.cprob))
  # 取自然对数再乘2
  fscore=-2*math.log(p)
  # 利用倒置对数卡方函数求得概率
  return self.invchi2(fscore,len(features)*2)
```

费舍尔方法有：如果概率彼此独立且随机分布，则这一计算结果将满足对数卡方分布。

将倒置对数卡方函数加入fisherclassifier类中：

```python
def invchi2(self,chi,df):
  m = chi / 2.0
  sum = term = math.exp(-m)
  for i in range(1, df//2):
    term *= m / i
    sum += term
  return min(sum, 1.0)
```

尝试以下执行语句：

```python
reload(docclass)
cl = docclass.fisherclassifier(docclass.getwords)
docclass.sampletrain(cl)
print cl.cprob('quick', 'good')
print cl.fisherprob('quick rabbit', 'good')
print cl.fisherprob('quick rabbit', 'bad')
```

返回：

```mathematica
0.571428571429
0.78013986589
0.356335962833
```

### 对内容项进行分类

利用fisherprob的返回值来决定如何分类。此处我们将为每个分类指定下限。例如在垃圾信息过滤器中，将bad类的下限值设的很高(0.6)，good的分类下限值设置为很低(0.2)，其它的则划分到未知分类中。这样做可以将正常邮件被错归到bad分类的可能性减到最小，同时允许少量垃圾邮件进入到收件箱中。

在fisherclassifier类中新建一个init方法，再增加一个保存临界值的变量：

```python
def __init__(self,getfeatures):
  classifier.__init_ _(self,getfeatures)
  self.minimums={}
```

接着在该类中加入两个用于设值和取值的方法，默认取值为0：

```python
def setminimum(self,cat,min):
	self.minimums[cat]=min
def getminimum(self,cat):
  if cat not in self.minimums: return 0
  return self.minimums[cat]
```

最后再添加一个方法，用以计算每个分类的概率，并找到超过指定下限值的最佳结果：

```python
def classify(self,item,default=None):
  # 循环遍历寻找最佳结果
  best=default
  max=0.0
  for c in self.categories( ):
    p=self.fisherprob(item,c)
    # 确保超过下限值
    if p>self.getminimum(c) and p>max:
      best=c
      max=p
  return best
```

尝试以下执行语句：

```python
reload(docclass)
cl = docclass.fisherclassifier(docclass.getwords)
docclass.sampletrain(cl)
print cl.classify('quick rabbit')
print cl.classify('quick money')
cl.setminimum('bad',0.8)
print cl.classify('quick money')
cl.setminimum('good',0.4)
print cl.classify('quick money')
```

输出：

```mathematica
good
bad
good
good
```

### 将经过训练的分类器持久化

#### 使用SQLLite

在docclass.py中加入以下语句，引入pysqlite：

```python
from pysqlite2 import dbapi2 as sqlite
```

本节中将当前classifier类中所用的字典结构都替换为了一个持久化的数据存储结构。

在classifier中添加一个方法，为该分类器打开数据库，并在必要时执行建表操作。这些表与它们所替换的字典在结构上时相匹配的：

```python
def setdb(self,dbfile):
  self.con=sqlite.connect(dbfile)
  self.con.execute('create table if not exists fc(feature,category,count)')
  self.con.execute('create table if not exists cc(category,count)')
```

替换所有用于获取和累加计数值的辅助函数：

```python
def incf(self,f,cat):
  count=self.fcount(f,cat)
  if count==0:
  	self.con.execute("insert into fc values ('%s','%s',1)"
  % (f,cat))
  else:
    self.con.execute("update fc set count=%d where feature='%s' and category='%s'" % (count+1,f,cat))
    
def fcount(self,f,cat):
  res=self.con.execute('select count from fc where feature="%s" and category="%s"'%(f,cat)).fetchone( )
  if res==None: return 0
  else: return float(res[0])

def incc(self,cat):
  count=self.catcount(cat)
  if count==0:
    self.con.execute("insert into cc values ('%s',1)" % (cat))
  else:
    self.con.execute("update cc set count=%d where category='%s'"% (count+1,cat))

def catcount(self,cat):
  res=self.con.execute('select count from cc where category="%s"' %(cat)).fetchone( )
  if res==None: return 0
  else: return float(res[0])
```

获取所有分类的列表与文档总数的方法也应该被替换掉：

```python
def categories(self):
  cur=self.con.execute('select category from cc');
  return [d[0] for d in cur]

def totalcount(self):
  res=self.con.execute('select sum(count) from cc').fetchone( );
  if res==None: return 0
  return res[0]
```

最后，为了使所有计数值被更新之后程序能将数据存入数据库，在classifier中加入以下语句到train方法的末尾处：

```python
self.con.commit( )
```

### 过滤博客订阅源

新建feedfilter.py，加入以下代码：

```python
import feedparser
import re
# 接受一个博客订阅源的url文件名并对内容项进行分类
def read(feed,classifier):
  # 得到订阅源的内容项并遍历循环
  f=feedparser.parse(feed)
  for entry in f['entries']:
    print
    print '-----'
    # 将内容项打印输出
    print 'Title:
    '+entry['title'].encode('utf-8')
    print 'Publisher: '+entry['publisher'].encode('utf-8')
    print
    print entry['summary'].encode('utf-8')
    # 将所有文件组合在一起，为分类器构建一个内容项
    fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])
    # 将当前分类的最佳推测结果打印输出
    print 'Guess: '+str(classifier.classify(fulltext))
    # 请求用户给出正确分类，并据此进行训练
    cl=raw_input('Enter category: ')
    classifier.train(fulltext,cl)
```

运行如下语句：

```python

import feedfilter
cl=docclass.fisherclassifier(docclass.getwords)
cl.setdb('python_feed.db') # Only if you implemented SQLite
feedfilter.read('python_search.xml',cl)
```

输出：

```python
-----
Title:
My new baby boy!
Publisher: Shetan Noir, the zombie belly dancer! - MySpace Blog
This is my new baby, Anthem. He is a 3 and half month old ball <b>python</b>,
orange shaded normal pattern. I have held him about 5 times since I brought him
home tonight at 8:00pm...
Guess: None
Enter category: snake
-----
Title:
If you need a laugh...
Publisher: Kate&#39;s space
Even does 'funny walks' from Monty <b>Python</b>. He talks about all the ol'
Guess: snake
Enter category: monty
-----
Title:
And another one checked off the list..New pix comment ppl
Publisher: And Python Guru - MySpace Blog
Now the one of a kind NERD bred Carplot male is in our possesion. His name is Broken
(not because he is sterile) lol But check out the pic and leave one
Guess: snake
Enter category: snake

.......
```

可以发现，推测的结果随着时间的推移在逐渐的改善。

### 对特征检测的改进

改进方法主要有以下几种：

- 将含有许多大写单词作为一种特征；
- 不仅使用单词，也可以使用词组；
- 捕获更多元信息，即用户对内容项的归类；
- 对url和数字不进行拆分。

将这个新的特征提取函数加入feedfilter.py中：

```python
def entryfeatures(entry):
  splitter=re.compile('\\W*')
  f={}
  # 提取标题中的单词并进行标识
  titlewords=[s.lower( ) for s in splitter.split(entry['title']) if len(s)>2 and len(s)<20]
  for w in titlewords: f['Title:'+w]=1
  # 提取摘要中的单词
  summarywords=[s.lower( ) for s in splitter.split(entry['summary'])　if len(s)>2 and len(s)<20]
  # 统计大写单词
  uc=0
  for i in range(len(summarywords)):
    w=summarywords[i]
    f[w]=1
    if w.isupper( ): uc+=1
    # 将从摘要中获取的词组作为特征
    if i<len(summarywords)-1:
      twowords=' '.join(summarywords[i:i+1])
      f[twowords]=1
  # 保持文章创建者和发布者名字的完整性
  f['Publisher:'+entry['publisher']]=1
  # UPPERCASE 用以指示存在过多的大写内容
  if float(uc)/len(summarywords)>0.3: f['UPPERCASE']=1
  return f
```

在read的函数末尾作如下修改：

```python
# 将当前分类的最佳推测结果打印输出
print 'Guess: ' + str(classifier.classify(entry))
# 请求用户给出正确分类，并据此进行训练
cl = raw_input('Enter category: ')
classifier.train(entry, cl)
```



现在，可以初始化分类器，并将entryfeatures用作特征提取函数了：

```python
reload(feedfilter)
cl=docclass.fisherclassifier(feedfilter.entryfeatures)
cl.setdb('python_feed.db') # Only if using the DB version
feedfilter.read('python_search.xml',cl)
```





















