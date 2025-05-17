from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # For our auth views
    path('accounts/', include('django.contrib.auth.urls')),  # For built-in auth views
    path('', include('converter.urls')),  # Include app's URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
