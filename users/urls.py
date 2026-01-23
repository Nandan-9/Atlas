from django.urls import path
from .views import users_view

urlpatterns = [
    path("create/", users_view, name="users-create"),
]
