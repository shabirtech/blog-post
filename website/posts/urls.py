from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("create_post/", create_post, name="create_post"),
    path('validate_title/', validate_title, name='validate_title'),
    path('blog-posts/', blog_post_list),
    path('blog-posts/<int:pk>/', blog_post_detail),
    path('blog-post-images/', blog_post_image_list),
    path('blog-post-images/<int:pk>/', blog_post_image_detail),

    
    path('api/blog-posts/', BlogPostList.as_view()),
    path('api/blog-posts/<int:pk>/', BlogPostDetail.as_view()),
    
]