from django.urls import path

from apps.views import UserLoginView, MainBaseView, ProductListByCategoryListView, CoinsView, \
    FavoriteView, UserLogautView, PaymentView, DiagramView, CompetitionListView, StatisticView, MarketView, \
    OrderListView, InquiriesView, UserProfileView, UserSettingsView, StreamListView, \
    DistrictListView, StreamCreateView, UserChangePasswordView, UserChangeImage, AdminsView, \
    CreatedSuccessOrderedView, ProductStatisticView, HeaderSearchView, OperatorDetailView, OperatorOrderListView, \
    FavouriteListView, \
    ProductOrStreamDetailView

urlpatterns = [
    path('', MainBaseView.as_view(), name='main_base'),

    # auth
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('logout/', UserLogautView.as_view(), name='logaut_page'),

    path('stream/<int:pk>/', ProductOrStreamDetailView.as_view(), name='stream_detail'),
    path('product-detail/<slug:slug>/', ProductOrStreamDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', ProductListByCategoryListView.as_view(), name='category_by_slug'),
    path('category/', ProductListByCategoryListView.as_view(), name='category_list'),
    path('payment/', PaymentView.as_view(), name='payments'),
    path('search/', HeaderSearchView.as_view(), name='search'),

    # Profile
    path('profile/favourite/<int:pk>/', FavoriteView.as_view(), name='add_favourite_page'),
    path('profile/liked-products/', FavouriteListView.as_view(), name='favorite_page'),
    path('profile/ordered-products/', OrderListView.as_view(), name='order_page'),
    path('profile/', UserProfileView.as_view(), name='profile_page'),
    path('profile/settings/image/', UserChangeImage.as_view(), name='settings_change_image_page'),
    path('profile/settings/', UserSettingsView.as_view(), name='settings_page'),
    path('profile/settings/change-password/', UserChangePasswordView.as_view(), name='settings_change_page'),

    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/success/', CreatedSuccessOrderedView.as_view(), name='success_order_page'),
    path('get-districts/<int:region_id>', DistrictListView.as_view(), name='get_districts'),

    # Admin page
    path('admin-page/', AdminsView.as_view(), name='admin_page'),
    path('admin-page/coins/', CoinsView.as_view(), name='coins_user_list'),
    path('admin-page/diagrams/', DiagramView.as_view(), name='diagrams_page'),
    path('admin-page/competition/', CompetitionListView.as_view(), name='competition_page'),
    path('admin-page/statistika/', StatisticView.as_view(), name='statistika_page'),
    path('admin-page/statistika/<int:pk>', ProductStatisticView.as_view(), name='product_statistic'),
    path('admin-page/stream/', StreamListView.as_view(), name='steam_page'),
    path('admin-page/market/', MarketView.as_view(), name='market_page'),
    path('admin-page/market/<slug:slug>/', MarketView.as_view(), name='market_by_slug'),
    path('admin-page/requests/', InquiriesView.as_view(), name='inquiries_page'),
    path('admin-page/create-stream/', StreamCreateView.as_view(), name='create_stream_page'),

    # Operator page
    path('operator-page/', OperatorOrderListView.as_view(), name='operator_page'),
    path('operator-page/new/', OperatorOrderListView.as_view(), name='operator_new_page'),
    path('operator-page/ready/', OperatorOrderListView.as_view(), name='operator_ready_page'),
    path('operator-page/deliver/', OperatorOrderListView.as_view(), name='operator_deliver_page'),
    path('operator-page/delivered/', OperatorOrderListView.as_view(), name='operator_delivered_page'),
    path('operator-page/broken/', OperatorOrderListView.as_view(), name='operator_broken_page'),
    path('operator-page/cant_phone/', OperatorOrderListView.as_view(), name='operator_cantphone_page'),
    path('operator-page/cancelled/', OperatorOrderListView.as_view(), name='operator_cancelled_page'),
    path('operator-page/archived/', OperatorOrderListView.as_view(), name='operator_archived_page'),
    path('operator-page/all/', OperatorOrderListView.as_view(), name='operator_all_page'),
    path('operator/detail/<int:pk>/', OperatorDetailView.as_view(), name='operator_detail'),

]
