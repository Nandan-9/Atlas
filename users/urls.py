from django.urls import path
from .views import users_view,create_team,github_auth,github_callback

urlpatterns = [
    path("create/", users_view, name="users-create"),
    path("team/", create_team, name="create_team"),
    path("github/", github_auth, name="github_auth"),
    path("github/callback/", github_callback, name="github_callback"),



]
