from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='generator'),
    path('result/', views.result, name='generator_result')
]
