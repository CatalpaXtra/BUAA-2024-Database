from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('all', views.blog_all, name='blog_all'),
    path('interest', views.blog_interest, name='blog_interest'),
    path('ctg_all', views.category_all, name='category_all'),
    path('search_kwd', views.search_by_keyword, name='search_by_keyword'),
    path('category/<int:category_id>', views.search_by_category, name='search_by_category'),
    
    path('detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('modify/<int:blog_id>', views.blog_modify, name='blog_modify'),
    path('pub', views.pub_blog, name='pub_blog'),
    path('comment/pub', views.pub_comment, name='pub_comment'),
    path('cmtcomment/pub', views.pub_cmt_comment, name='pub_cmt_comment'),
    
    path('collect/<int:blog_id>', views.collect_blog, name='collect_blog'),
    path('like/<int:blog_id>', views.like_blog, name='like_blog'),
    path('dislike/<int:blog_id>', views.dislike_blog, name='dislike_blog'),
    path('like_cmt/<int:cmt_id>', views.like_cmt, name='like_cmt'),
    path('dislike_cmt/<int:cmt_id>', views.dislike_cmt, name='dislike_cmt'),
    path('like_cmt_cmt/<int:cmt_id>', views.like_cmt_cmt, name='like_cmt_cmt'),
    path('dislike_cmt_cmt/<int:cmt_id>', views.dislike_cmt_cmt, name='dislike_cmt_cmt'),
    
    path('delete/<int:blog_id>', views.delete_blog, name='delete'),
    path('delete_cmt/<int:cmt_id>', views.delete_cmt, name='delete_cmt'),
    path('delete_cmt_cmt/<int:cmt_id>', views.delete_cmt_cmt, name='delete_cmt_cmt'),
]