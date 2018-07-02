from django.urls import path

from . import views

app_name = 'switchinweb'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('breakdown/', views.BreakdownView.as_view(), name='breakdown'),
    path('detail/', views.detail, name='detail'),
    path('upload/', views.upload, name='upload'),
    path('manual/', views.manual, name='manual'),
]
