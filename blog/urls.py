from django.urls import path
from blog.views import *

app_name = 'blog'
urlpatterns = [
    path('',Blog.as_view(), name = 'blog_index'),
    path('category/<str:category>',BlogArticleCategory.as_view(), name = 'blog_category'),
    path('article/<slug:slug>',BlogArticle.as_view(), name = 'blog_article'),
    path('comment/',Comment.as_view(), name = 'blog_comment'),
    path('search/',search_view, name = 'blog_search'),
    
]
