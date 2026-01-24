from django.urls import path
from .views import users_view,create_team,github_auth

urlpatterns = [
    path("create/", users_view, name="users-create"),
    path("team/", create_team, name="create_team"),
    path("github/", github_auth, name="github_auth"),


]
