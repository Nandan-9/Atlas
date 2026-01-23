from django.urls import path
from .views import users_view,create_team

urlpatterns = [
    path("create/", users_view, name="users-create"),
    path("team/", create_team, name="create_team"),

]
