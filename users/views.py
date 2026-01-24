import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Teams

@csrf_exempt
def users_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user = User.objects.create(
            username=data["username"],
            email_id=data["email_id"],
            role=data["role"],
            password=data["password"],
        )

        return JsonResponse({
            "id": user.id,
            "message": "User created successfully"
        }, status=201)

    if request.method == "GET":
        users = User.objects.all().values(
            "id", "username", "email_id", "role"
        )
        return JsonResponse(list(users), safe=False)


@csrf_exempt
def create_team(request):

    print("dsdssds")
    if request.method == "POST":

        data = json.loads(request.body)
        team_lead =  User.objects.get(id=data["id"])
        team = Teams.objects.create(
            name = data["name"],
            team_lead = team_lead
        )
        return JsonResponse({
            "id": team.id,
            "message": "Team created successfully"
        }, status=201) 
    
    if request.method == "GET":

        team = Teams.objects.all().values(
            "id","name","team_lead"
        )
        return JsonResponse(list(team),safe=False)


@csrf_exempt
def github_auth(request):

    if request.method == "POST":

        content = "hait there "
        return JsonResponse({
            "message" : content
        })