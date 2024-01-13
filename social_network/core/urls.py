from django.urls import path

from social_network.core.views import posts, post_dislike, post_like,post_like_analytics


urlpatterns = [
    path('', posts, name='posts'),
    path('<uuid:post_id>/likes', post_like, name='post_likes'),
    path('<uuid:post_id>/dislikes', post_dislike, name='post_dislikes'),
    path('likes/analytics', post_like_analytics, name='post_likes_analytics'),
]
