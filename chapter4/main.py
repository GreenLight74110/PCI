import socket
socket.setdefaulttimeout(60)
import searchengine

#-----------Crawler Code----------------#

# pagelist=['http://english.sina.com']
# # pagelist=['http://sohu.com']
# crawler=searchengine.crawler('')
# crawler.crawl(pagelist,2)

#-----------Setting Up the Schema----------------#
# reload(searchengine)
# crawler=searchengine.crawler('searchindex-my.db')
# crawler.createindextables( )

#-----------Adding to the Index----------------#
# reload(searchengine)
# crawler=searchengine.crawler('searchindex-my.db')
# pages= ['http://english.sina.com']
# crawler.crawl(pages)

# ----------test for searchindex.db-------------#
# crawler=searchengine.crawler('searchindex.db')
# print [row for row in crawler.con.execute('select rowid from wordlocation where wordid=1')]

#-----------Querying----------------#
# reload(searchengine)
# e=searchengine.searcher('searchindex.db')
# print e.getmatchrows('astana africa china trump')

#-----------Content-Based Ranking----------------#
# reload(searchengine)
# e=searchengine.searcher('searchindex.db')
# print e.query('functional programming')

#-----------The PageRank Algorithm---------------#
# reload(searchengine)
# crawler=searchengine.crawler('searchindex.db')
# crawler.calculatepagerank( )