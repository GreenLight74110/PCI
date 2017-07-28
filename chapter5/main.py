import random
import optimization
s=[1,4,3,2,7,3,6,3,2,4,5,3]
domain=[(0,9)]*(len(optimization.people)*2)

#----------Representing Solutions-----------#
# optimization.printschedule(s)

#----------The Cost Function-----------#
# reload(optimization)
# print optimization.schedulecost(s)

#----------Random Searching-----------#
# reload(optimization)
# s=optimization.randomoptimize(domain,optimization.schedulecost)
# print optimization.schedulecost(s)
# print optimization.printschedule(s)

#----------Hill Climbing-----------#
# reload(optimization)
# s=optimization.hillclimb(domain,optimization.schedulecost)
# print optimization.schedulecost(s)
# print optimization.printschedule(s)

#----------Simulated Annealing-----------#
# reload(optimization)
# s=optimization.annealingoptimize(domain,optimization.schedulecost)
# print optimization.schedulecost(s)
# optimization.printschedule(s)


for i in range(10):
    print random.random()