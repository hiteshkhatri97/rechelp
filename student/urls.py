from django.urls import path
from . import views

app_name = 'student'
urlpatterns = [
    path('', views.home,name='home'),
    path('profile/', views.profile,name='profile'),
    path('login/', views.studentLogin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.studentLogout, name='logout'),
]
