from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_pk>/', views.user_detail, name='user_detail'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
]