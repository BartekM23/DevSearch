from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('projects/<str:pk>', views.project, name='project'),
    path('createproject/', views.create_project, name='create_project'),
    path('updateproject/<str:pk>', views.update_project, name = 'update_project'),
    path('deleteproject/<str:pk>', views.delete_project, name = 'delete_project')
]
