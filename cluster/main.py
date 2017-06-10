import trafficCluster

data = trafficCluster.readfile('C:\\Users\\Administrator\\Desktop\\2.txt')

clust = trafficCluster.hcluster(data)

trafficCluster.printclust(clust)