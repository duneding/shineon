from django.http import HttpResponseRedirect
from .models import Tweet, Sentiment
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator
import engine
import converter

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

        docs = engine.search_all('gensory', 'tweets', self.paginate_by, pFrom)
        tweets = converter.tweets(docs)
        #paginator = Paginator(tweets, self.paginate_by)

        '''try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)'''

        context['latest_tweet_list'] = tweets#[{u'text':u'holaaaaaaaaa'}]#Tweet.objects.all()
        return context

class SentimentView(generic.DetailView):
    model = Tweet
    template_name = 'tagger/sentiment.html'

def submit(request, tweet_id):
    tweet = engine.get('gensory', 'tweets', tweet_id)
    text = tweet[u'_source'][u'text']
    '''
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
    '''
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('tagger:sentiment', args=(tweet,)))
