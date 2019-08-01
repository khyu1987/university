from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('', include('courses.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
