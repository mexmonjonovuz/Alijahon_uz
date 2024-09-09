from django.urls import path

from apps.views import CustomLoginView, ProductDetailView, MainBaseView, ProductListByCategoryListView

urlpatterns = [
    path('', MainBaseView.as_view(), name='main_base'),
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', ProductListByCategoryListView.as_view(), name='category_list'),
]
