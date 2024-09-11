from django.urls import path

from apps.views import CustomLoginView, ProductDetailView, MainBaseView, ProductListByCategoryListView, CoinsView, \
    FavoriteView, CustomLogautView, PaymentView, DiagramView, CompetitionView

urlpatterns = [
    path('', MainBaseView.as_view(), name='main_base'),
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('logaut/', CustomLogautView.as_view(), name='logaut_page'),
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', ProductListByCategoryListView.as_view(), name='category_list'),
    path('category/', ProductListByCategoryListView.as_view(), name='product_lists'),
    path('admin-page/coins/', CoinsView.as_view(), name='coins_user_list'),
    path('profile/liked-products/', FavoriteView.as_view(), name='favorite_page'),
    path('payment/', PaymentView.as_view(), name='payments'),
    path('admin-page/diagrams', DiagramView.as_view(), name='diagrams_page'),
    path('admin-page/competition/', CompetitionView.as_view(), name='competition_page'),
]
