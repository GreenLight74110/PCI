###    搜集偏好
####    构造数据集
```
# A dictionary of movie critics and their ratings of a small set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

```
查询、修改的测试语句
```
python  # 打开python解释器
from recommendations import critics #   将critics加载到内存中，但一般更通常的做法是将其存入一个数据库中
critics['Lisa Rose']['Lady in the Water']   #   查询Lisa Rose对Lady in the Water的评分
critics['Toby']['Snakes on a Plane']=4.6    # 修改'Snakes on a Plane'由4.5到4.6
critics['Toby']     #查询Toby的所有电影评分
```

###    需找相似的用户
####    欧几里德距离评价    
思想：以经过人们一致评价的物品作为坐标轴，将参与评价的人绘制到图上，考查他们彼此间的距离远近。距离越近，则二者的相似度越高。  
![image](http://img2.ph.126.net/GBR10qQbhDMYyvi4cCu3sQ==/6631908892094782217.png)   
在recommendnations.py中加入以下语句
```
from math import sqrt


# 返回person1和person2基于距离的相似度评价
def sim_distance(prefs, person1, person2):
    # 得到二者一致评价的物品的列表
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1

    # 如果二者没有一致评价的物品，则返回0
    if len(si) == 0: return 0

    # 计算所有差值的平方和
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)
```
给出Lisa Rose和Gene Seymour的相似度评价
```
import recommendations
import importlib
importlib.reload(recommendations)   #   python3中的reload用法
recommendations.sim_distance(recommendations.critics,'Lisa Rose','Gene Seymour')    #   retrun 0.148148.... （此处中文版的书中有误）
```
####    皮尔逊相关度评价    （实际上就是概率论里学的相关系数，等于X、Y的协方差除以X、Y标准差的乘积）    
思想：以参与评价的人作为坐标轴，将一致评价的物品绘制到图上，拟合出一条直线，尽可能的经过（靠近）多的点。通过比较两组数据与拟合直线的拟合度，来决定二者的相似度。  
![image](http://img1.ph.126.net/pcPm4o7Ql7fSRB7sPjlDFQ==/6632007848141282272.png)
```
# 返回p1和p2的皮尔逊相关系数
def sim_pearson(prefs, p1, p2):
    # 得到二者一致评价的物品（偏好）的列表
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # 如果二者没有一致评价的物品（偏好），则返回0
    if len(si) == 0: return 0

    # 一致评价的物品总数
    n = len(si)

    # 所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # 所有偏好求平方和
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # 求乘积和
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # 计算皮尔逊相关系数r
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r

```


```
import recommendations
import importlib
importlib.reload(recommendations)
recommendations.sim_pearson(recommendations.critics,'Lisa Rose','Gene Seymour') 
#   return 0.39605901719066977
```
####    为评论者打分    
```
# 从偏好字典中返回最佳匹配者 
# 返回结果个数和相似度函数均为可选参数
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
# 对评论进行排序，由高到低
  scores.sort()
  scores.reverse()
  return scores[0:n]
```

```
import recommendations
import importlib
importlib.reload(recommendations)
recommendations.topMatches(recommendations.critics,'Toby',n=3) 
#   return [(0.9912407071619299, 'Lisa Rose'), (0.9244734516419049, 'Mick LaSalle'), (0.8934051474415647, 'Claudia Puig')]
```
####    推荐物品    
![image](http://img2.ph.126.net/9TkxyrO3LsxF6AZyMs-w4g==/6631950673536638996.png)   
```
# 利用其他所有人的加权平均，为某人提供建议
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # 不要和自己作比较
        if other == person: continue
        sim = similarity(prefs, person, other)

        # 忽略不大于0的相似度评分
        if sim <= 0: continue
        for item in prefs[other]:

            # 仅为我没有看过的电影评分
            if item not in prefs[person] or prefs[person][item] == 0:
                # 相似度*评分
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # 参与评分的人的相似度求和
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # 建立归一化列表
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # 排序，返回
    rankings.sort()
    rankings.reverse()
    return rankings

```

```
import recommendations
import importlib
importlib.reload(recommendations)
recommendations.getRecommendations(recommendations.critics,'Toby')  
#  return [(3.3477895267131013, 'The Night Listener'), (2.8325499182641614, 'Lady in the Water'), (2.530980703765565, 'Just My Luck')]    
```
也可以指定使用欧几里德距离评价方式  
```
recommendations.getRecommendations(recommendations.critics,'Toby',similarity=recommendations.sim_distance)  
#   return [(3.5002478401415877, 'The Night Listener'), (2.7561242939959363, 'Lady in the Water'), (2.461988486074374, 'Just My Luck')]
```
####    匹配商品    
将人与物品对调，就可以复用之前写的方法了。  
```
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # 将物品与人交换
      result[item][person]=prefs[person][item]
  return result
```
```
import recommendations
import importlib
importlib.reload(recommendations)
movies=recommendations.transformPrefs(recommendations.critics)
recommendations.topMatches(movies,'Superman Returns')
#   [(0.6579516949597695, 'You, Me and Dupree'), (0.4879500364742689, 'Lady in the Water'), (0.11180339887498941, 'Snakes on a Plane'), (-0.1798471947990544, 'The Night Listener'), (-0.42289003161103106, 'Just My Luck')]
#   相关度为负代表有不喜欢、讨厌的倾向
```

####    基于物品的过滤  
- 基于用户的协作型过滤  
即上述算法
- 基于物品的协作型过滤  
思路：为每件物品预先计算好最为接近的其它物品    
优点：不会像用户间的比较那么频繁变化    

####    构造物品比较数据集  

```
def calculateSimilarItems(prefs,n=10):
  # 为与这些物品最为相近的其它物品建立字典
  result={}
  # 转变为以物品为中心
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # 为大数据集更新状态变量
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # 找出最为接近的物品
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result
```

```
reload(recommendations)
itemsim=recommendations.calculateSimilarItems(recommendations.critics)  
itemsim 
#   return {
'Lady in the Water': [(0.4, 'You, Me and Dupree'), (0.2857142857142857, 'The Night Listener'), (0.2222222222222222, 'Snakes on a Plane'), (0.2222222222222222, 'Just My Luck'), (0.09090909090909091, 'Superman Returns')], 
'Snakes on a Plane': [(0.2222222222222222, 'Lady in the Water'), (0.18181818181818182, 'The Night Listener'), (0.16666666666666666, 'Superman Returns'), (0.10526315789473684, 'Just My Luck'), (0.05128205128205128, 'You, Me and Dupree')], 
'Just My Luck': [(0.2222222222222222, 'Lady in the Water'), (0.18181818181818182, 'You, Me and Dupree'), (0.15384615384615385, 'The Night Listener'), (0.10526315789473684, 'Snakes on a Plane'), (0.06451612903225806, 'Superman Returns')], 
'Superman Returns': [(0.16666666666666666, 'Snakes on a Plane'), (0.10256410256410256, 'The Night Listener'), (0.09090909090909091, 'Lady in the Water'), (0.06451612903225806, 'Just My Luck'), (0.05333333333333334, 'You, Me and Dupree')], 
'You, Me and Dupree': [(0.4, 'Lady in the Water'), (0.18181818181818182, 'Just My Luck'), (0.14814814814814814, 'The Night Listener'), (0.05333333333333334, 'Superman Returns'), (0.05128205128205128, 'Snakes on a Plane')], 
'The Night Listener': [(0.2857142857142857, 'Lady in the Water'),(0.18181818181818182, 'Snakes on a Plane'), (0.15384615384615385, 'Just My Luck'), (0.14814814814814814, 'You, Me and Dupree'), (0.10256410256410256, 'Superman Returns')]
}
```
####    获得推荐    
![image](http://img1.ph.126.net/-3SHL2Mki9XZQN_JM8Vt0g==/6632165078304080311.png)   
类似于上面的“推荐物品”中的算法
```
def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # 循环遍历用户评分过的物品
  for (item,rating) in userRatings.items( ):

    # 循环遍历与当前物品相似的物品
    for (similarity,item2) in itemMatch[item]:

      # 忽略用户已经评价过的物品
      if item2 in userRatings: continue
      # 当前物品的评分与相似物品相似度的加权和
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # 相似物品的相似度求和
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # 加权和除以相似度和，求出归一化评分
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings
```
```
reload(recommendations)
recommendations.getRecommendedItems(recommendations.critics,itemsim,'Toby') 
#   return [(3.182634730538922, 'The Night Listener'), (2.5983318700614575, 'Just My Luck'), (2.4730878186968837, 'Lady in the Water')]
```

####    使用movielens数据集 
```
def loadMovieLens(path='D:/Documents/PycharmProjects/jtzhbc/chapter2'):
    # 获取影片标题
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    # 加载数据
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs
```
生成数据集
```
reload(recommendations)
prefs=recommendations.loadMovieLens( )
```
查看任意一位用户的评分情况  
```
prefs['87']
#   return {'Birdcage, The (1996)': 4.0, 'E.T. the Extra-Terrestrial (1982)': 3.0,
'Bananas (1971)': 5.0, 'Sting, The (1973)': 5.0, 'Bad Boys (1995)': 4.0,
'In the Line of Fire (1993)': 5.0, 'Star Trek: The Wrath of Khan (1982)': 5.0,
'Speechless (1994)': 4.0, etc...
```
基于用户的推荐
```
recommendations.getRecommendations(prefs,'87')[0:30]
#   return [(5.0, 'They Made Me a Criminal (1939)'), (5.0, 'Star Kid (1997)'),
(5.0, 'Santa with Muscles (1996)'), (5.0, 'Saint of Fort Washington (1993)'),
etc...]
```
基于物品的推荐
```
itemsim=recommendations.calculateSimilarItems(prefs,n=50)   # 生成物品相似度字典的过程可能比较耗时，但当生成以后的推荐耗时则不会再随着用户的增加而增加
recommendations.getRecommendedItems(prefs,itemsim,'87')[0:30]
# return [(5.0, "What's Eating Gilbert Grape (1993)"), (5.0, 'Vertigo (1958)'),
(5.0, 'Usual Suspects, The (1995)'), (5.0, 'Toy Story (1995)'),etc...]
```
