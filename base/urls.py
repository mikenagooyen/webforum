from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('thread/<str:pk>/', views.thread, name="thread"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    
    path('create-thread/', views.createThread, name="create-thread"),
    path('update-thread/<str:pk>', views.updateThread, name="update-thread"),
    path('delete-thread/<str:pk>', views.deleteThread, name="delete-thread"),
    path('update-comment/<str:pk>', views.updateComment, name="update-comment"),
    path('delete-comment/<str:pk>', views.deleteComment, name="delete-comment"),
]
