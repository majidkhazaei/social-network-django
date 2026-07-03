from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='user_unfollow'),
    path('edit_user', views.EditUserView.as_view(), name='edit_user'),
    #API URLS
    path('api/register/', views.UserRegisterAPI.as_view()),
    path('api/follow/<int:user_id>/', views.FollowToggleAPI.as_view()),
    path('api/profile/', views.ProfileRetrieveUpdateAPIView.as_view()),
    path('api/users/', views.UserListAPIView.as_view()),
]