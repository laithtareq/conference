from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',LoginView.as_view(template_name='user/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='user/logout.html'),name='logout'),
    path('profile/',views.profile,name='profile'),
    path('AddNewManuscript/<str:user_id>/',views.AddNewManuscript,name='AddNewManuscript'),
    path('detail/<int:post_id>/',views.post_detail,name='detail'),
    path('MyManuscript/<str:user_id>/',views.MyManuscript,name='MyManuscript'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('update_manuscript/<int:post_id>/',views.update_manuscript,name='update_manuscript'),
]