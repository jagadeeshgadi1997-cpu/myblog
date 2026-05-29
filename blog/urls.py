from django.urls import path
from . import views

urlpatterns = [
    path("posts/",                views.post_list,       name="post-list"),
    path("posts/<int:post_id>/",  views.post_detail,     name="post-detail"),
    path("authors/",              views.author_list,     name="author-list"),
    path("categories/",           views.category_list,   name="category-list"),
    path("posts/category/<str:category_slug>/", views.posts_by_category, name="posts-by-category"),
    
    path("auth/register/", views.register, name="register"),
    path("auth/me/", views.me, name="me"),
]