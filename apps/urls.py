from django.urls import path

from apps.views import CategoryListView

urlpatterns = [
    path('', CategoryListView.as_view(),name='main_base')
]
