# coding=utf-8

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

flights={}
#
for line in file('schedule.txt'):
  origin,dest,depart,arrive,price=line.strip().split(',')
  flights.setdefault((origin,dest),[])

  # Add details to the list of possible flights
  flights[(origin,dest)].append((depart,arrive,int(price)))

def getminutes(t):
  x=time.strptime(t,'%H:%M')
  return x[3]*60+x[4]

def printschedule(r):
  for d in range(len(r)/2):
    name=people[d][0]
    origin=people[d][1]
    out=flights[(origin,destination)][int(r[2*d])]
    ret=flights[(destination,origin)][int(r[2*d+1])]
    print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                  out[0],out[1],out[2],
                                                  ret[0],ret[1],ret[2])

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
