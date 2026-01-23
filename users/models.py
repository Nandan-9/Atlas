from django.db import models

# Create your models here.



class User(models.Model):

    ROLE_CHOICE = [
        ('team_lead','Team Lead'),
        ('mananger', 'Manager'),
        ('dev','Developer'),
        ('intern',"Intern")
    ]

    username = models.CharField(max_length=100,unique=True)
    email_id = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.email_id




class Teams(models.Model):
    name = models.CharField(max_length=100)
    team_lead = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="leading_teams")


    def __str__(self):
        return self.name

