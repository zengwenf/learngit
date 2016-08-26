import requests
from pyquery import PyQuery as Pq


class MyClass(object):

    def __init__(self, segmentfault_id):
        self.url ='http://segmentfault.com/q/{0}'.format(segmentfault_id)
        self.dom = None
    
    def dom(self):
        if not self.dom:
            document = requests.get(self.url)
            document.encoding = 'utf-8'
            self.dom = Pq(document.text)
        return self.dom
    
    def title(self):
        return self.dom('h1#questionTitle')