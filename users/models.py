from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICE = [
        ('team_lead','Team Lead'),
        ('mananger', 'Manager'),
        ('dev','Developer'),
        ('intern',"Intern")
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICE)

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=100)
    team_lead = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="leading_teams")


    def __str__(self):
        return self.name




class Project(models.Model):
    name = models.CharField(max_length=100)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_projects"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects"
    )








# class TeamMember(models.Model):
#     team = models.ForeignKey(
#         Teams,
#         on_delete=models.CASCADE,
#         related_name="members"
#     )
#     member = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="teams"
#     )
#     ROLE_CHOICE = [
#         ('team_lead','Team Lead'),
#         ('mananger', 'Manager'),
#         ('dev','Developer'),
#         ('intern',"Intern")
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICE)

#     class Meta:
#         unique_together = ("team", "member")

#     def __str__(self):
#         return f"{self.member.username} → {self.team.name}"
 

class GitHubAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    github_user_id = models.CharField(max_length=100)
