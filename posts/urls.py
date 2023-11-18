from django.urls import path
from . import views


urlpatterns = [
    path("", views.all_posts, name="home"),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/<int:pk>", views.post_detail, name="post_detail"),
    path("posts/<int:pk>/edit/", views.post_update, name="post_update"),
    path('user-posts/', views.user_posts, name='user_posts'),
    path('longer-reads/', views.longer_reads, name='longer_reads'),
]
