from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from root import settings

urlpatterns = [
                  path('', include('apps.urls')),
                  path("ckeditor5/", include('django_ckeditor_5.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    prefix_default_language=False
) + urlpatterns
