from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/<int:pk>/', views.feed_detail, name='feed_detail'),
    path('feed/<int:pk>/like/', views.like_feed, name='like_feed'),
    path('feed/<int:pk>/dislike/', views.dislike_feed, name='dislike_feed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
