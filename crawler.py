#-*- coding:utf-8 -*-

import urllib
import urllib2
import socket
import re
#import io
#from django.core.paginator import Page

init_url = r'http://hxen.com/interpretation/bilingualnews/'
numOfArticle_regex = b'<b>(\d+?)</b>'
numOfPage_regex = b'<b>(\d+?)</b>'

contenturls_regex = b'<td height="25"> <font face="Windings">v</font> <a href="(a-zA-Z0-9-\s\.\/)+)" target=_blank>'

title_regex = b'<b><h1>([\s\S]*?)</h1></b>'
content1_regex = b'<p>([\s\S]*?)</p>'
content2_regex = b'<p>([\s\w(),.`~!@#$%^&*/\\;:{}\[\]]*?)<script'

source_regex = b"Source: <a href='[\w:\/.\\_\s]*' target=_blank>([\s\S]*?)</a>"
date_regex = b'([\d-]+) '

#��������  
junk1_regex = b'&[\w]*?;' 
junk2_regex = b'<br[\s]*/>' 
junk3_regex = b'<a href=http://www.hxen.com/englishlistening/voaenglish/ target=_blank class=infotextkey>VOA</a>'


def crawler(url):
    getInfo(url)
    pageurls = getAllPageUrls(url)
    
    for pageurl in pageurls:
        contenturls = getContentUrls(pageurl)
        for contenturl in contenturls:
            if contenturl == 'http://hxen.com/interpretation/bilingualnews/20160607/429869.html':
                break
            else:
                content = getContentData(contenturl)
                print content
    
    print 'Crawl done!'
            


def getInfo(url):
    page = getPage(url)
    rawdata = page.read()
    
    numOfArticles = re.findall(numOfArticle_regex, rawdata)[0]
    numOfPages = re.findall(numOfPage_regex,rawdata)[0]
    
    print 'No. of all articles : %d' %int(numOfArticles)
    print 'No. of 1st page : %d' %int(numOfPages)
    
    return


def getPage(url):
    try:
        page = urllib.urlopen(url)
        code = page.getcode()
        if code < 200 or code > 300:
            print 'Define error!'
    except Exception as e:
        if isinstance(e, urllib2.HTTPError):
            print 'http error: {0}'.format(e.code)
        elif isinstance(e,urllib2.URLError) and isinstance(e.reason, socket.timeout):
            print 'url error: socket timeout {0}'.format(e.__str__())
        else:
            print 'misc error: '+ e.__str__()
    return page

def getAllPageUrls(url):
    page = getPage(url)
    rawdata = page.read()
    
    numOfPages = re.findall(numOfPage_regex, rawdata)[0]
    
    inumOfPages = int(numOfPages)
    pageurls = ['http://hxen.com/interpretation/bilingualnews/index.html']
    for x in range(2,inumOfPages+1):
        pageurls.append(r'http://hxen.com/interpretation/bilingualnews/index_%d.html' %x)
        
    print 'Index URL: '
    for x in pageurls:
        print x
        
    return pageurls
          
def getContentUrls(url):
    page = getPage(url)
    rawdata = page.read()
    
    rawcontenturls = re.findall(contenturls_regex, rawdata)
    contenturls = []
    
    for url in rawcontenturls:
        contenturls.append(r'http://hxen.com%s'%url.decode('gbk','ignore'))
    print 'Content URL: '
    for url in contenturls:
        print url
        
    return contenturls

def getContentData(url):
    print '\n Crawling web page: %s\n' %url
    
    page = getPage(url)
    rawdata = page.read()
    
    title = re.findall(title_regex, rawdata)
    print 'Title: %s' %title[0].decode('gbk','ignore')

    source = re.findall(source_regex, rawdata)
    print 'Source: %s' %source[0].decode('gbk','ignore')
    
    date_ = re.findall(date_regex,rawdata)
    print 'Report date: %s' %date_[0].decode('utf-8')
    
    encontent1 = re.findall(content1_regex, rawdata)
    encontent2 = re.findall(content2_regex, rawdata)
    
    if not encontent2 == []:
        encontent1.append(encontent2[0])
        
    print 'english'
    for sentence in encontent1:
        print '%s' %sentence.decode('utf-8')
        
    #in chinese
    url = url.replace('.html','_2.html')
    page = getPage(url)
    rawdata = page.read()
    
    chcontent1 = re.findall(content1_regex, rawdata)
    chcontent2 = re.findall(content2_regex, rawdata)
    
    if not chcontent2 == []:
        chcontent1.append(chcontent2[0])
        
    print 'chinese'
    for sentence in chcontent1:
        print '%s' %sentence.decode('gbk')
        
    return {'title':title,'source':source,'date':date_,'english':encontent1,'chinese':chcontent1}

#写入文件
def article2file(content):
    if content['title']!=[] and content['source']!=[] and content['date']!=[] and content['english']!=[] and content['chinese']!=[]:
        fp = open('./data/%s.txt'%content['date'][0].decode('gbk'),'wb+')
  
        fp.write(b'<title>'+content['title'][0]+b'</title>\r\n')
        fp.write(b'<source>'+content['source'][0]+b'</source>\r\n')
        fp.write(b'<date>'+content['date'][0]+b'</date>\r\n')
  
        fp.write(b'<english>\r\n')
    for e in content['english']:
        e = re.sub(junk1_regex,b'',e)
        e = re.sub(junk2_regex,b'',e)
        e = re.sub(junk3_regex,b'',e)
        fp.write(e+b'\r\n')
        fp.write(b'</english>\r\n')
  
        fp.write(b'<chinese>\r\n')
    for c in content['chinese']:
        c = re.sub(junk1_regex,b'',c)
        c = re.sub(junk2_regex,b'',c)
        c = re.sub(junk3_regex,b'',c)
        fp.write(c+b'\r\n')
        fp.write(b'</chinese>\r\n')
        fp.close()
 
    return

if __name__ == '__main__':
    #getInfo(init_url)
    #getContentUrls(init_url)
    print 'Spider start crawling ...\n'
    crawler(init_url)
    