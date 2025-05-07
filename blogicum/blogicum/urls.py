from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static

handler403 = 'blogicum.views.custom_403'
handler404 = 'blogicum.views.custom_404'
handler500 = 'blogicum.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', blog_views.register, name='registration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
