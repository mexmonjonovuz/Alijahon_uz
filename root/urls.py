import debug_toolbar
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, path, re_path

from apps.admin import admin_site
from root import settings

if settings.DEBUG:
    pass

handler40 = 'apps.views.utils_views.handler404'
handler50 = 'apps.views.utils_views.handler500'

urlpatterns = [
                  path('', include('apps.urls')),
                  path("ckeditor5/", include('django_ckeditor_5.urls')),
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('logout/', LogoutView.as_view(), name="logout"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT) + i18n_patterns(
    path('admin/', admin_site.urls),
    prefix_default_language=False
)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

#
# urlpatterns += [
#     path('i18n/', include('django.conf.urls.i18n')),
# ]
