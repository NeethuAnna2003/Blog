from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/create/', views.post_create, name='post_create'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('blog/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('blog/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('bloggers/', views.blogger_list, name='blogger_list'),
    path('blogger/<str:username>/', views.blogger_detail, name='blogger_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('search/', views.search_posts, name='search_posts'),
    path('blog/<slug:slug>/like/', views.like_post, name='like_post'),
    path('blog/<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
] 