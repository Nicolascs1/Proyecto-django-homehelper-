
# app contacto
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('', include('core.urls')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('admin/', admin.site.urls),
    
    
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),


]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
