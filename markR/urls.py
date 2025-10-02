from django.contrib import admin
from django.urls import path, include
from core import urls as core_urls
from frontend import urls as frontend_urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(core_urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Corrected line below:
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #  Frontend Web Pages 
    # This makes pages like /login/ and /dashboard/ work
    path('', include(frontend_urls)),
]