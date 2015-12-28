from django.http import HttpResponseRedirect
from .models import Tweet, Sentiment
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from elasticsearch import Elasticsearch
from django.conf import settings

# Create your views here.
es_config = getattr(settings, 'ELASTICSEARCH')['default']
host = es_config['HOST']
port = es_config['PORT']
es = Elasticsearch([{'host': host, 'port': port}])

class IndexView(generic.ListView):
    template_name = 'tagger/index.html'
    context_object_name = 'latest_tweet_list'

    def get_queryset(self):
        request={"size":50, "from":0, "query": {"match_all": {}}}
        docs = es.search('gensory', 'tweets', request)
        return docs[u'hits'][u'hits'] #Tweet.objects.all().order_by('-id')[:5]

class DetailView(generic.DetailView):
    model = Tweet
    template_name = 'tagger/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Tweet.objects.all()

def SubmitView(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    try:
        selected_sentiment = tweet.choice_set.get(pk=request.POST['sentiment'])
    except (KeyError, Sentiment.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'tagger/detail.html', {
            'question': tweet,
            'error_message': "You didn't select a choice.",
        })
    else:
        #selected_choice.votes += 1
        #selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tagger:results', args=(tweet.id,)))
