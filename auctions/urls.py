from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create, name="create"),
    path("<str:id>", views.listing, name="item"),
    path("<str:id>/comment", views.add_comment, name="comment"),
    path("<str:id>/edit", views.edit_listing, name="edit"),
    path("categories/<str:category>", views.listings_category, name="listings_category"),
    path("<str:id>/added", views.add_to_watchlist, name="add_to_watchlist"),
    path("<str:id>/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<str:id>/bid", views.place_bid, name="bid"),
    path("<str:id>/close", views.close_listing, name="close"),


]
