__author__ = 'root'

from elasticsearch import Elasticsearch
from django.conf import settings

es_config = getattr(settings, 'ELASTICSEARCH')['default']
host = es_config['HOST']
port = es_config['PORT']
es = Elasticsearch([{'host': host, 'port': port}])

def search_all(index, type, psize, pfrom):
    pfilter = {
        "not": {
            "filter": {
                "exists": {
                    "field": "sentiment"
                }
            }
        }
    }

    request_es = {"size":psize, "from":pfrom, "filter": pfilter, "query": {"match_all": {}}}
    docs = es.search('gensory', 'tweets', request_es)
    return docs[u'hits']

def count(index, type):
    return es.count(index, type)[u'count']

def get(index, type, id):
    return es.get(index=index, doc_type=type,id=id)

def update_sentiment(index, type, id, subjectivity, polarity):
    body = {
        "doc": {
            "sentiment": {
                "subjectivity": subjectivity,
                "polarity": polarity
            }
        }
    }

    return es.update(index=index, doc_type=type,id=id, body=body)