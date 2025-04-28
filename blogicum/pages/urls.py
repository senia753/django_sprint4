from django.urls import path
from django.views.generic import TemplateView


app_name = 'pages'

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='about.html'),
         name='about'),
    path('rules/', TemplateView.as_view(template_name='rules.html'),
         name='rules'),
]
