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
reload(treepredict)
treepredict.printtree(tree)

#======Graphical Display =======#
reload(treepredict)
treepredict.drawtree(tree,jpeg='treeview.jpg')