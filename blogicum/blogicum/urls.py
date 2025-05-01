from django.conf.urls import handler403, handler404, handler500
from django.contrib import admin
from django.urls import path, include
from blogicum.views import UserRegistrationView


handler403 = 'blogicum.views.custom_403'
handler404 = 'blogicum.views.custom_404'
handler500 = 'blogicum.views.custom_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('category/', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', UserRegistrationView.as_view(),
         name='registration'),
]
