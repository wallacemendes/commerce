from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories_view, name="categories"),
    path("listing/<str:listing_id>", views.listing_view, name="listing"),
    path("bid", views.bid, name="bid"),
    path("openclose", views.open_or_close_listing, name="openclose"),
    path("comment", views.add_comment, name="comment"),
    path("mybids", views.my_bids, name="mybids"),
]
