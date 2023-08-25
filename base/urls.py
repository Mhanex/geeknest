from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="index"),

    path('login/', views.UserLogin, name="login"),
    path('logout/', views.logUserOut, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('account_activation/<uidb64>/<token>', views.accountActivation, name='activate'),
    path('profile/<str:username>/', views.userProfile, name='profile'),
    path('update-profile/<str:username>/', views.updateUserProfile, name='update-profile'),
    
  
    
    path('group/<str:pk>/', views.viewGroup, name="group"),

    path('create-group/', views.createGroup, name="create-group"),

    path('join-group/<int:pk>/', views.joinGroup, name="join-group"),
    path('update-group/<int:pk>/', views.updateGroup, name="update-group"),
    path('delete-group/<str:pk>/', views.deleteGroup, name="delete-group"),

    path('update-comment/<int:pk>/', views.updateComment, name="update-comment"),
    path('delete-comment/<int:pk>/', views.deleteComment, name="delete-comment"),


    path('topics/', views.browseTopics, name='browse-topics'),
    path('activity/', views.browseActivity, name='browse-activity'),


]