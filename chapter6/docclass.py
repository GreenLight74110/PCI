# coding=utf-8

import re
import math


def getwords(doc):
    splitter = re.compile('\\W*')
    # 根据非字母字符进行单词拆分
    words = [s.lower() for s in splitter.split(doc)
             if len(s) > 2 and len(s) < 20]
    # 返回一组不重复的单词
    return dict([(w, 1) for w in words])


class classifier:
    def __init__(self, getfeatures, filename=None):
        # 统计特征/分类组合的数量，记录位于各分类中的不同特征的数量
        # {'python': {'bad': 0, 'good': 6}, 'the': {'bad': 3, 'good': 3}}表示“the”被划归“bad”类的文档和“good”类的文档中各出现了三次，而“python”则只在"good"类文档中出现过
        self.fc = {}
        # 统计每个分类中的文档数量，记录各分类被使用次数的字典
        self.cc = {}
        self.getfeatures = getfeatures

    # 增加特征/分类的计数值
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    # 增加对某一分类的计数值
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    # 某一特征出现于某一分类中的次数
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # 属于某一分类的内容项数量
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # 所有内容项的数量
    def totalcount(self):
        return sum(self.cc.values())

    # 所有分类的列表
    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        # 针对该分类为每个特征增加计数值
        for f in features:
            self.incf(f, cat)
        # 增加对该分类的计数值
        self.incc(cat)

    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0
        # 特征在分类中出现的总次数除以分类中包含内容项的总数
        return self.fcount(f,cat)/self.catcount(cat)

def sampletrain(cl):
    cl.train('Nobody owns the water.', 'good')
    cl.train('the quick rabbit jumps fences', 'good')
    cl.train('buy pharmaceuticals now', 'bad')
    cl.train('make quick money at the online casino', 'bad')
    cl.train('the quick brown fox jumps', 'good')
