from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path(
        'create-post/',
        views.create_post,
        name='create_post'
    ),

    path(
        'comment/<int:post_id>/',
        views.add_comment,
        name='add_comment'
    ),

    path(
        'like/<int:post_id>/',
        views.like_post,
        name='like_post'
    ),

    path(
        'follow/<int:user_id>/',
        views.follow_user,
        name='follow_user'
    ),

    path(
        'profile/<int:user_id>/',
        views.profile,
        name='profile'
    ),

    path(
        'followers/<int:user_id>/',
        views.followers_list,
        name='followers_list'
    ),

    path(
        'following/<int:user_id>/',
        views.following_list,
        name='following_list'
    ),

    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),

    path(
        'delete-post/<int:post_id>/',
        views.delete_post,
        name='delete_post'
    ),
]