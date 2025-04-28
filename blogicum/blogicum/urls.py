from django.conf.urls import handler403, handler404, handler500
from django.contrib import admin
from django.urls import path, include
from blogicum.views import UserRegistrationView, UserProfileView


handler403 = 'blogicum.views.csrf_error'
handler404 = 'blogicum.views.page_not_found'
handler500 = 'blogicum.views.server_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', UserRegistrationView.as_view(),
         name='registration'),
    path('profile/<username>/', UserProfileView.as_view(),
         name='profile'),
]
