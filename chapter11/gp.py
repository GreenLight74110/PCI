# coding=utf-8

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


addw = fwrapper(lambda l: l[0] + l[1], 2, 'add')
subw = fwrapper(lambda l: l[0] - l[1], 2, 'subtract')
mulw = fwrapper(lambda l: l[0] * l[1], 2, 'multiply')


def iffunc(l):
    if l[0] > 0:
        return l[1]
    else:
        return l[2]


ifw = fwrapper(iffunc, 3, 'if')


def isgreater(l):
    if l[0] > l[1]:
        return 1
    else:
        return 0


gtw = fwrapper(isgreater, 2, 'isgreater')

# 创建了一个包含所有函数的列表，这样就可以稍后对它们进行随机选择了
flist = [addw, mulw, ifw, gtw, subw]


def exampletree():
    return node(ifw, [
        node(gtw, [paramnode(0), constnode(3)]),
        node(addw, [paramnode(1), constnode(5)]),
        node(subw, [paramnode(1), constnode(2)]),
    ]
                )


# pc给出了程序树所需输入参数的个数
# fpr给出了新建节点属于函数型节点的概率
# ppr给出了当新建节点不是函数型节点时，其属于paramnode节点的概率
def makerandomtree(pc, maxdepth=4, fpr=0.5, ppr=0.6):
    if random() < fpr and maxdepth > 0:
        f = choice(flist)
        children = [makerandomtree(pc, maxdepth - 1, fpr, ppr)
                    for i in range(f.childcount)]
        return node(f, children)
    elif random() < ppr:
        return paramnode(randint(0, pc - 1))
    else:
        return constnode(randint(0, 10))


def hiddenfunction(x, y):
    return x ** 2 + 2 * y + 3 * x + 5


def buildhiddenset():
    rows = []
    for i in range(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hiddenfunction(x, y)])
    return rows


def scorefunction(tree,s):
    dif=0
    for data in s:
        v=tree.evaluate([data[0],data[1]])
        dif+=abs(v-data[2])
    return dif


def mutate(t,pc,probchange=0.1):
    if random()<probchange:
        return makerandomtree(pc)
    else:
        result=deepcopy(t)
        if hasattr(t,"children"):
            result.children=[mutate(c,pc,probchange) for c in t.children]
        return result


def crossover(t1,t2,probswap=0.7,top=1):
    if random()<probswap and not top:
        return deepcopy(t2)
    else:
        result=deepcopy(t1)
        if hasattr(t1,'children') and hasattr(t2,'children'):
            result.children=[crossover(c,choice(t2.children),probswap,0)
                             for c in t1.children]
        return result


def getrankfunction(dataset):
    def rankfunction(population):
        scores=[(scorefunction(t,dataset),t) for t in population]
        scores.sort()
        return scores
    return rankfunction


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

