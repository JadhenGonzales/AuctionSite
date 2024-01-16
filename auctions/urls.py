from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add_view, name="add_listing"),
    path("bid/<str:post_id>", views.add_bid, name="bid"),
    path("comment/<str:post_id>", views.add_comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post/<str:post_id>", views.post, name="post"),
    path("register", views.register, name="register"),
    path("show/<str:category>", views.view_all, name="show"),
    path("watchlist", views.watchlist, name="watchlist"),
]
