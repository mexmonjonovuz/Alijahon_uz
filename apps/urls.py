from django.urls import path

from apps.views import CustomLoginView, ProductDetailView, MainBaseView, ProductListByCategoryListView, CoinsView, \
    FavoriteView, CustomLogautView, PaymentView, DiagramView, CompetitionView, StatisticView, SteamView, MarketView, \
    OrderListView, InquiriesView, CustomProfileView, CustomSettingView

urlpatterns = [
    path('', MainBaseView.as_view(), name='main_base'),
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('logaut/', CustomLogautView.as_view(), name='logaut_page'),
    path('products-detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', ProductListByCategoryListView.as_view(), name='category_list'),
    path('category/', ProductListByCategoryListView.as_view(), name='product_lists'),
    path('admin-page/coins/', CoinsView.as_view(), name='coins_user_list'),
    path('profile/liked-products/', FavoriteView.as_view(), name='favorite_page'),
    path('payment/', PaymentView.as_view(), name='payments'),
    path('admin-page/diagrams', DiagramView.as_view(), name='diagrams_page'),
    path('admin-page/competition/', CompetitionView.as_view(), name='competition_page'),
    path('admin-page/statistika/', StatisticView.as_view(), name='statistika_page'),
    path('admin-page/steam/', SteamView.as_view(), name='steam_page'),
    path('admin-page/market/', MarketView.as_view(), name='market_page'),
    path('admin-page/requests/', InquiriesView.as_view(), name='inquiries_page'),
    path('profile/ordered-products/', OrderListView.as_view(), name='order_page'),
    path('profile/', CustomProfileView.as_view(), name='profile_page'),
    path('profile/settings/', CustomSettingView.as_view(), name='settings_page'),
]
