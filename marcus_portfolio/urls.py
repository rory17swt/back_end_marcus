from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static
from utils.views import keep_alive

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include('events.urls')),
    path('api/', include('bio.urls')),
    path('api/', include('media.urls')),
    path('api/', include('contact.urls')),
    path('api/', include('users.urls')),
    path('api/keep-alive/', keep_alive),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
