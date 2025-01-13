from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView, ExecuteCodeView, FileView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('execute/', ExecuteCodeView.as_view(), name='execute-code'),
    path('projects/<int:project_id>/files/', FileView.as_view()),
    path('projects/<int:project_id>/files/<int:file_id>/', FileView.as_view()),
]
