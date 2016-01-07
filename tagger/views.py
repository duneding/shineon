from django.http import HttpResponseRedirect
from .models import Tweet
from django.core.urlresolvers import reverse
from django.views import generic
import engine
import converter
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
PAGE_SIZE = 25

class IndexView(generic.ListView):
    template_name = 'tagger/index.html'
    context_object_name = 'latest_tweet_list'
    paginate_by = PAGE_SIZE
    count = engine.count('gensory', 'tweets')

    def get_queryset(self):
        return [None]*self.count

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')

        if page:
            pFrom = self.paginate_by * int(page)
        else:
            pFrom = 0

        hits = engine.search_all('gensory', 'tweets', self.paginate_by, pFrom)

        docs = hits[u'hits']
        total = hits[u'total']

        tweets = converter.tweets(docs)

        context['latest_tweet_list'] = tweets
        context['tweets_pending'] = total
        return context

class SentimentView(generic.DetailView):
    model = Tweet
    template_name = 'tagger/sentiment.html'
    context_object_name = 'tweet_sentiment'

    def get_object(self):
        tweet_id = self.kwargs['tweet_id']
        doc = engine.get('gensory', 'tweets', tweet_id)
        text = doc[u'_source'][u'text']
        tweet = {
            'id': tweet_id,
            'text': text
        }
        return tweet

    def get_context_data(self, **kwargs):
        context = super(SentimentView, self).get_context_data(**kwargs)
        context['tweet_sentiment'] = kwargs['object']
        return context

@csrf_exempt
def save(request, tweet_id):
    polarity = float(request.POST[u'polarity'])
    subjectivity = float(request.POST[u'subjectivity'])
    engine.update_sentiment('gensory', 'tweets', tweet_id, subjectivity, polarity)
    return HttpResponseRedirect(reverse('tagger:index'))
