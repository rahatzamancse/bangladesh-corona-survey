from django.urls import path

from heatmap import views

urlpatterns = [
    path('', views.index, name='heatmap'),
]