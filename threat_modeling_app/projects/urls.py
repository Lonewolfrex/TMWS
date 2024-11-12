from django.urls import path
from .views import signup, project_list, create_project, edit_project, delete_project, login_view, home, logout_view

urlpatterns = [
    path('', home, name='home'),  # Home view for the root URL
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('projects/', project_list, name='project_list'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/edit/<int:pk>/', edit_project, name='edit_project'),
    path('projects/delete/<int:pk>/', delete_project, name='delete_project'),
    path('logout/', logout_view, name='logout'),  
]