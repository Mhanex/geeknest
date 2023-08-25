
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('groups/', views.getGroups),
    path('groups/<int:pk>/', views.getGroup),
]