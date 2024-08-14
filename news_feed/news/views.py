from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Feed, LikeDislike

@login_required
def home(request):
    recent_feeds = Feed.objects.order_by('-published_at')[:10]  # Fetch the latest 10 feeds
    return render(request, 'news/home_page.html', {'feeds': recent_feeds})

@login_required  # Ensure the user is logged in to like/dislike
@require_POST
def like_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, feed=feed)

    if created or like_dislike.like is False:  # If newly created or changing from dislike to like
        if not created:
            feed.dislikes -= 1  # Reduce the dislike count
        like_dislike.like = True
        like_dislike.save()
        feed.likes += 1
        feed.save()
        return JsonResponse({'success': True, 'likes': feed.likes, 'dislikes': feed.dislikes})
    
    return JsonResponse({'success': False, 'message': 'Already liked'})

@login_required  # Ensure the user is logged in to like/dislike
@require_POST
def dislike_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, feed=feed)

    if created or like_dislike.like is True:  # If newly created or changing from like to dislike
        if not created:
            feed.likes -= 1  # Reduce the like count
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

@login_required
def liked_feeds(request):
    liked_feeds = Feed.objects.filter(likedislike__user=request.user, likedislike__like=True)
    return render(request, 'news/liked_feeds.html', {'feeds': liked_feeds})
