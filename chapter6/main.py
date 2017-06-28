import docclass

# Training the Classifier #
# cl = docclass.classifier(docclass.getwords)
# cl.train('the quick brown fox jumps over the lazy dog', 'good')
# cl.train('make quick money in the online casino', 'bad')
# print cl.fcount('quick', 'good')
# print cl.fcount('quick', 'bad')

# Calculating Probabilities #
reload(docclass)
cl = docclass.classifier(docclass.getwords)
docclass.sampletrain(cl)
print cl.fprob('quick', 'good')
