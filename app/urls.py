from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Rutas de tu aplicación
    path('accounts/', include('django.contrib.auth.urls')),  # Rutas de autenticación
]
