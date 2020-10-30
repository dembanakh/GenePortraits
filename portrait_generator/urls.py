from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='generator'),
    path('result/', views.result, name='generator_result'),
    path('repository/', views.repository, name='repository'),
    path('track_user/', views.track_user, name='test')
]
