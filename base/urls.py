from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    
    path('logout/', views.logoutPage, name="logoutPage"),
    path('', views.home, name="home"),
    path('room/<int:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('edit-room/<int:pk>/', views.updateRoom, name="update-room"),
    path("delete-room/<int:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<int:pk>/", views.deleteMessage, name="delete-message"),
    path("user-profile/<int:pk>/", views.userProfile, name="user-profile"),
    path('edit-user/', views.updateUser, name="update-user"),

]