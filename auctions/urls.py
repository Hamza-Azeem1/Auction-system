from django.urls import path, include
from auctions import views
from auctions.views import user_history

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add_to_watchlist/<int:item_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:item_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path("categories", views.categories, name="categories"),
    path("success", views.success, name="success"),
    path("addListing", views.addListing, name="add_listing"),
    path("user_listings", views.user_listings, name="user_listings"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path('search/', views.search_results, name='search_results'),
    path('listing/<int:listing_id>/update/', views.update_listing, name='update_listing'),
    path('history/', user_history, name='user_history'),
]
