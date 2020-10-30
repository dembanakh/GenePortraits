from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='generator'),
    path('result/', views.result, name='generator_result'),
    path('repository/', views.repository, name='repository'),
    path('track_user_1/', views.track_user_1, name='test_1'),
    path('track_user_2/', views.track_user_2, name='test_2')
]
