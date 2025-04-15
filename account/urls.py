from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.RegisterUserView, name="register"),
    path('profile/create', views.ProfileUserCreateView.as_view(), name="profile"),
    path('profile/detail/<int:id>', views.ProfileUserDetailView.as_view(), name="profile_detail"),

]
