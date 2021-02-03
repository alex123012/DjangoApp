from django.urls import path

from . import views

app_name = 'ChromoGraph'
urlpatterns = [
    path('', views.ChromoGraph.as_view(), name='ChromoGraph'),
]
