import docclass
import feedfilter

# Training the Classifier #
# cl = docclass.classifier(docclass.getwords)
# cl.train('the quick brown fox jumps over the lazy dog quick', 'good')
# cl.train('make quick money in the online casino', 'bad')
# print cl.fcount('quick', 'good')
# print cl.fcount('quick', 'bad')

# Calculating Probabilities #
# reload(docclass)
# cl = docclass.classifier(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.fprob('quick', 'good')

# Starting with a Reasonable Guess#
# reload(docclass)
# cl = docclass.classifier(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.weightedprob('money', 'good', cl.fprob)
# docclass.sampletrain(cl)
# print cl.weightedprob('money', 'good', cl.fprob)

# A Naive Classifier #
# reload(docclass)
# cl = docclass.naivebayes(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.prob('quick rabbit', 'good')
# print cl.prob('quick rabbit', 'bad')

# Choosing a Category #
# reload(docclass)
# cl=docclass.naivebayes(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.classify('quick rabbit',default='unknown')
# print cl.classify('quick money',default='unknown')
# cl.setthreshold('bad',3.0)
# print cl.classify('quick money',default='unknown')
# for i in range(10): docclass.sampletrain(cl)
# print cl.classify('quick money',default='unknown')

# Category Probabilities for Features#
# reload(docclass)
# cl=docclass.fisherclassifier(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.cprob('quick','good')
# print cl.cprob('money','bad')
# print cl.weightedprob('money', 'bad', cl.fprob)

# The Fisher Method #
# reload(docclass)
# cl = docclass.fisherclassifier(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.cprob('quick', 'good')
# print cl.fisherprob('quick rabbit', 'good')
# print cl.fisherprob('quick rabbit', 'bad')


# Classifying Items#
# reload(docclass)
# cl = docclass.fisherclassifier(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.classify('quick rabbit')
# print cl.classify('quick money')
# cl.setminimum('bad', 0.8)
# print cl.classify('quick money')
# cl.setminimum('good', 0.4)
# print cl.classify('quick money')


#Persisting the Trained Classifiers #
# reload(docclass)
# cl=docclass.fisherclassifier(docclass.getwords)
# cl.setdb('test1.db')
# docclass.sampletrain(cl)
# cl2=docclass.naivebayes(docclass.getwords)
# cl2.setdb('test1.db')
# print cl2.classify('quick money')

#Filtering Blog Feeds #
# cl=docclass.fisherclassifier(docclass.getwords)
# cl.setdb('python_feed.db') # Only if you implemented SQLite
# feedfilter.read('python_search.xml',cl)
#
# print cl.cprob('python','prog')
# print cl.cprob('python','snake')
# print cl.cprob('python','monty')
# print cl.cprob('eric','monty')
# print cl.fprob('eric','monty')

#Improving Feature Detection #
reload(feedfilter)
cl=docclass.fisherclassifier(feedfilter.entryfeatures)
cl.setdb('python_feed.db') # Only if using the DB version
feedfilter.read('python_search.xml',cl)
