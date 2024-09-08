from django.urls import path

from apps.views import HomeTemplateView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='template')
]
