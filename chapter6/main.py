import docclass

# Training the Classifier #
# cl = docclass.classifier(docclass.getwords)
# cl.train('the quick brown fox jumps over the lazy dog', 'good')
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

#Choosing a Category #
reload(docclass)
cl=docclass.naivebayes(docclass.getwords)
docclass.sampletrain(cl)
print cl.classify('quick rabbit',default='unknown')
print cl.classify('quick money',default='unknown')
cl.setthreshold('bad',3.0)
print cl.classify('quick money',default='unknown')
for i in range(10): docclass.sampletrain(cl)
print cl.classify('quick money',default='unknown')