from django.urls import path
from .views import users_view,create_team,create_project,get_all_projects

urlpatterns = [
    path("register/", users_view, name="users-create"),
    path("team/", create_team, name="create_team"),
    path("project/",create_project, name="create_project"),
    path("all-project/",get_all_projects, name="get_all_projects")

    # path("github/", github_auth, name="github_auth"),
    # path("github/callback/", github_callback, name="github_callback"),



]
