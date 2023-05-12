from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import ads.urls
from djangoProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("ads.urls")),
    path('selection/', include("ads.urls")),
    path('user/', include("users.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)