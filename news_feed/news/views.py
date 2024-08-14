from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Feed, LikeDislike

@login_required
def home(request):
    recent_feeds = Feed.objects.order_by('-published_at')[:10]  
    return render(request, 'news/home_page.html', {'feeds': recent_feeds})

@login_required  
@require_POST
def like_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, feed=feed)

    if created or like_dislike.like is False:
        if not created:
            feed.dislikes -= 1  
        like_dislike.like = True
        like_dislike.save()
        feed.likes += 1
        feed.save()
        return JsonResponse({'success': True, 'likes': feed.likes, 'dislikes': feed.dislikes})
    
    return JsonResponse({'success': False, 'message': 'Already liked'})

@login_required  
@require_POST
def dislike_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, feed=feed)

    if created or like_dislike.like is True:  
        if not created:
            feed.likes -= 1  
        like_dislike.like = False
        like_dislike.save()
        feed.dislikes += 1
        feed.save()
        return JsonResponse({'success': True, 'likes': feed.likes, 'dislikes': feed.dislikes})
    
    return JsonResponse({'success': False, 'message': 'Already disliked'})

def feed_detail(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    feed.view_count += 1
    feed.save()

    return render(request, 'news/feed_detail.html', {'feed': feed})

