from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/new", views.new_listing, name="new_listing"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name='watchlist'),
    path("watchlist/<str:listing_id>/delete", views.delete_from_watchlist, name='delete_from_watchlist'),
    path("listing/bid/<str:listing_id>", views.bid, name="bid"),
    path("listing/close/<str:listing_id>", views.close_listing, name='close_listing'),
    path("listing/comment/<str:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path('categories/<str:category>/', views.category, name="category")
]
