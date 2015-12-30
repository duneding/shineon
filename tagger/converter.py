__author__ = 'root'

def tweets(docs):
    tweets = []
    for doc in docs:
        tweet = {
            'id':doc[u'_id'],
            'text':doc[u'_source'][u'text'][:50]+'...'#.encode('utf-8')
                    }
        tweets.append(tweet)

    return tweets