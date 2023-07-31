from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path('payment/', views.payment, name='payment'),
    path('logout/', views.logout_view, name='logout'),
    path('listing/<int:listing_id>/', views.listing, name='listing'),
    path('update_listing/<int:listing_id>/', views.update_listing, name='update_listing'),
    path('bid/', views.bid, name='bid'),
    path('comment/', views.comment, name='comment'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add_to_watchlist/<int:item_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:item_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('categories/', views.categories, name='categories'),
    path('success/<int:listing_id>/', views.success, name='success'),
    path('addListing/', views.addListing, name='addListing'),
    path('user_listings/', views.user_listings, name='user_listings'),
    path('close_listing/<int:listing_id>/', views.close_listing, name='close_listing'),
    path('search_results/', views.search_results, name='search_results'),
    path('user_history/', views.user_history, name='user_history'),
]
