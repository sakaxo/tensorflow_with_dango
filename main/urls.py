from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='index'),
    path('project info/', views.project_info, name='project info'),

]
