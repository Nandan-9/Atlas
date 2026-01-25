import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Teams,GitHubAccount


from django.shortcuts import redirect
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


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






import requests



@csrf_exempt

def github_auth(request):
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": "http://localhost:8000/users/github/callback/",
        "scope": "repo workflow read:org",
    }

    url = "https://github.com/login/oauth/authorize?" + urllib.parse.urlencode(params)
    return JsonResponse({"auth_url": url})

def github_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No code received"}, status=400)

    token_res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={  
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )




    data = token_res.json()
    access_token = data.get("access_token")

    if not access_token:
        return JsonResponse({"error": "Token exchange failed", "details": data}, status=400)

    # TEMP: store globally (MVP only)
    with open("github_token.txt", "w") as f:
        f.write(access_token)

    return JsonResponse({"status": "GitHub connected successfully"})