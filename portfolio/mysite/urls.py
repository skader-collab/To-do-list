from django.urls import path
from . import views
from .views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView  
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('mysite/logout/', views.logout_view, name='logout'), 
    path('register/', views.register, name='register'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='api-tasks'),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='api_task_detail'),
    path('api/token/', obtain_auth_token, name='api_token'),
]