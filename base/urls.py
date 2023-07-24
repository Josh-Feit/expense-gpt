from django.urls import path
from . import views
from .views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', views.actionList, name='transactions'),
    path('add/', views.createAction, name='createAction'),
    path('update/<str:pk>', views.updateAction, name='updateAction'),
    path('delete/<str:pk>', views.deleteAction, name='deleteAction'),
]