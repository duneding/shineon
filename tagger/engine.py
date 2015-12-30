__author__ = 'root'

from elasticsearch import Elasticsearch
from django.conf import settings

es_config = getattr(settings, 'ELASTICSEARCH')['default']
host = es_config['HOST']
port = es_config['PORT']
es = Elasticsearch([{'host': host, 'port': port}])

def search_all(index, type, psize, pfrom):
    request_es = {"size":psize, "from":pfrom, "query": {"match_all": {}}}
    docs = es.search('gensory', 'tweets', request_es)
    return docs[u'hits'][u'hits']

def count(index, type):
    return es.count(index, type)[u'count']

def get(index, type, id):
    return es.get(index=index, doc_type=type,id=id)