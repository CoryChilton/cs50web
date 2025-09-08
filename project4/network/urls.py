
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<str:page>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:user_id>", views.profile, name="profile"),
    path("profile/<str:user_id>/page/<str:page>", views.profile, name="profile"),
    path("follow/<str:user_id>", views.follow, name="follow"),
    path("unfollow/<str:user_id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("following/page/<str:page>", views.following, name="following"),
]
