import treepredict

#======Training the Tree=======#
# print treepredict.divideset(treepredict.my_data,2,'yes')

#======Choosing the Best Split=======#
# reload(treepredict)
# print treepredict.giniimpurity(treepredict.my_data)
# print treepredict.entropy(treepredict.my_data)
# set1,set2=treepredict.divideset(treepredict.my_data,2,'yes')
# print treepredict.entropy(set1)
# print treepredict.giniimpurity(set1)

#======Recursive Tree Building=======#
reload(treepredict)
tree=treepredict.buildtree(treepredict.my_data)

#======Displaying the Tree =======#
# reload(treepredict)
# treepredict.printtree(tree)

#======Graphical Display =======#
# reload(treepredict)
# treepredict.drawtree(tree,jpeg='treeview.jpg')

#======Classifying New Observations=======#
# reload(treepredict)
# print treepredict.classify(['(direct)','USA','yes',5],tree)

#==========Pruning the Tree===========#
# reload(treepredict)
# treepredict.prune(tree,0.1)
# treepredict.printtree(tree)
# treepredict.prune(tree,1.0)
# treepredict.printtree(tree)

#========Dealing with Missing Data=========#
# reload(treepredict)
# print treepredict.mdclassify(['google',None,'yes',None],tree)
# print treepredict.mdclassify(['google','France',None,None],tree)

