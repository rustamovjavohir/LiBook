from django.urls import path

from .views import RegisterViews, LoginViews, UserViews, LogoutViews

urlpatterns = [
    path('register/', RegisterViews.as_view(), name='register'),
    path('login/', LoginViews.as_view(), name='login'),
    path('user/', UserViews.as_view(), name='user'),
    path('logout/', LogoutViews.as_view(), name='logout'),
]
