from django.urls import path
from . import views

app_name = 'company'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.viewProfile, name='profile'),
    path('edit-profile/', views.editProfile, name='editprofile'),
    path('add-post/', views.addPost, name='addpost'),
    path('login/', views.companyLogin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.companyLogout, name='logout'),
]
