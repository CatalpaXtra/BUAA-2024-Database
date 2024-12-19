from django.urls import path
from . import views

app_name = 'zone'


urlpatterns = [
    path('all', views.zone_all, name='zone_all'),
    path('detail/<str:zone_id>', views.zone_detail, name='zone_detail'),
    path('create', views.create_zone, name='create_zone'),
    path('modify/<str:zone_id>', views.zone_modify, name='zone_modify'),
    path('follow/<str:zone_id>', views.follow_zone, name='follow_zone'),
    
    path('object/all', views.object_all, name='object_all'),
    path('object/detail/<str:object_id>', views.object_detail, name='object_detail'),
    path('object/star/<str:object_id>', views.star_object, name='star_object'),
    path('object/collect/<str:object_id>', views.collect_object, name='collect_object'),
    path('object/create/<str:zone_id>', views.create_object, name='create_object'),
    path('object/modify/<str:object_id>', views.object_modify, name='object_modify'),
    
    path('comment/pub', views.pub_comment, name='pub_comment'),
    path('cmtcomment/pub', views.pub_cmt_comment, name='pub_cmt_comment'),
    path('like_cmt/<int:cmt_id>', views.like_cmt, name='like_cmt'),
    path('dislike_cmt/<int:cmt_id>', views.dislike_cmt, name='dislike_cmt'),
    path('like_cmt_cmt/<int:cmt_id>', views.like_cmt_cmt, name='like_cmt_cmt'),
    path('dislike_cmt_cmt/<int:cmt_id>', views.dislike_cmt_cmt, name='dislike_cmt_cmt'),
    
    path('select_admin_set/<str:zone_id>', views.select_admin_set, name='select_admin_set'),
    path('select_admin_del/<str:zone_id>', views.select_admin_del, name='select_admin_del'),
    path('set_admin/<str:zone_id>/<str:admin_id>', views.set_admin, name='set_admin'),
    path('del_admin/<str:zone_id>/<str:admin_id>', views.del_admin, name='del_admin'),
    
    path('delete_zone/<int:zone_id>', views.delete_zone, name='delete_zone'),
    path('delete_obj/<int:object_id>', views.delete_object, name='delete_obj'),
    path('delete_cmt/<int:cmt_id>', views.delete_cmt, name='delete_cmt'),
    path('delete_cmt_cmt/<int:cmt_id>', views.delete_cmt_cmt, name='delete_cmt_cmt'),
]