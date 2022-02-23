from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.get_routes),
    path('projects/', views.get_projects),
    path('project/<str:pk>', views.get_project),
    path('projects/<str:pk>/vote/', views.project_vote),
    path('remove-tag/', views.remove_tag),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
