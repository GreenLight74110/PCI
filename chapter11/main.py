# def func(x,y):
#     if x>3:
#         return y + 5
#     else:
#         return y - 2
# coding=utf-8

import gp

#=====Building and Evaluating Trees=====#
# exampletree = gp.exampletree()
# print exampletree.evaluate([2, 3])
# print exampletree.evaluate([5, 3])

#=====Displaying the Program====#
# reload(gp)
# exampletree=gp.exampletree( )
# print exampletree.display( )

#=======Creating the Initial Population==========#
# random1=gp.makerandomtree(2)
# print random1.evaluate([7,1])
# print random1.evaluate([2,4])
# random2=gp.makerandomtree(2)
# print random2.evaluate([5,3])
# print random2.evaluate([5,20])
# random1.display( )
# random2.display( )

#======A Simple Mathematical Test====#
# reload(gp)
# hiddenset=gp.buildhiddenset( )


#======Measuring Success========#
# reload(gp)
# print gp.scorefunction(random2,hiddenset)
# print gp.scorefunction(random1,hiddenset)

#=====Mutating Programs=====#
# print random2.display( )
# muttree=gp.mutate(random2,2)
# print muttree.display( )
#
# print gp.scorefunction(random2,hiddenset)
# print gp.scorefunction(muttree,hiddenset)


#=====Crossover=====#
# random1=gp.makerandomtree(2)
# random1.display( )
#
#
# random2=gp.makerandomtree(2)
# random2.display( )
#
# cross=gp.crossover(random1,random2)
# cross.display( )

#=====Building the Environment======#
# reload(gp)
# rf=gp.getrankfunction(gp.buildhiddenset( ))
# print gp.evolve(2,500,rf,mutationrate=0.2,breedingrate=0.1,pexp=0.7,pnew=0.1)


#======A Simple Game=====#
# reload(gp)
# p1=gp.makerandomtree(5)
# p1.display()
# print 'p1================p2'
# p2=gp.makerandomtree(5)
# p2.display()
# print gp.gridgame([p1,p2])


#======A Round-Robin Tournament========#
reload(gp)
winner=gp.evolve(5,100,gp.tournament,maxgen=50)
print winner