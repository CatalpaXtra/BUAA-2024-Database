from django.urls import path
from . import views


app_name = 'user'


urlpatterns = [
    path('login', views.mylogin, name='login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha'),
    path('forget', views.forget, name='forget'),
    path('recover_captcha', views.send_recover_email_captcha, name='recover_email_captcha'),
    
    path('center', views.center, name='center'),
    path('center/<str:user_id>', views.center_id, name='center_id'),
    path('modify_information', views.modify_information, name='modify_information'),
    path('modify_password', views.modify_password, name='modify_password'),
    path('upload_avatar', views.upload_avatar, name='upload_avatar'),
    
    path('zone_followed', views.zone_followed, name='zone_followed'),
    path('blog_collected', views.blog_collected, name='blog_collected'),
    path('object_stared', views.object_stared, name='object_stared'),
    path('blog_pubed', views.blog_pubed, name='blog_pubed'),
    path('object_pubed', views.object_pubed, name='object_pubed'),
]