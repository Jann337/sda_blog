from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostsListView.as_view(), name="home"),
    path("posts/create/", views.PostCreateView.as_view(), name="create_post"),
    path("posts/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
]
