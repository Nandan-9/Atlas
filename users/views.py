import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Project,Team


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

        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            role=data.get("role", "intern"),
            password=data["password"],
        )

        return JsonResponse({
            "id": user.id,
            "message": "User created successfully"
        }, status=201)

    if request.method == "GET":
        users = User.objects.all().values(
            "id", "username", "email", "role"
        )
        return JsonResponse(list(users), safe=False)




@csrf_exempt
def create_project(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)

        user = User.objects.get(id=data["user_id"])
        team = Team.objects.get(id=data["team_id"])

        project = Project.objects.create(
            name=data["name"],
            created_by=user,
            team=team
        )

        return JsonResponse(
            {
                "id": project.id,
                "message": "Project created successfully"
            },
            status=201
        )

    except KeyError as e:
        return JsonResponse(
            {"error": f"Missing field: {str(e)}"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": "Something went wrong"},
            status=500
        )


@csrf_exempt
def get_all_projects(request):

    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=405)
    
    try:

        projects = Project.objects.all().values(
            "id",
            "name",
            "created_by_id",
            "team_id"
        )

        return JsonResponse(
            list(projects), safe=False
        )
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)

    except KeyError as e:
        return JsonResponse(
            {"error": f"Missing field: {str(e)}"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": "Something went wrong"},
            status=500
        )





@csrf_exempt
def create_team(request):

    print("dsdssds")
    if request.method == "POST":

        data = json.loads(request.body)
        team_lead =  User.objects.get(id=data["id"])
        team = Team.objects.create(
            name = data["name"],
            team_lead = team_lead
        )
        return JsonResponse({
            "id": team.id,
            "message": "Team created successfully"
        }, status=201) 

    if request.method == "GET":

        team = Team.objects.all().values(
            "id","name","team_lead"
        )
        return JsonResponse(list(team),safe=False)






import requests


def get_user_info(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }
    res = requests.get("https://api.github.com/user", headers=headers)
    res.raise_for_status()
    return res.json()
    



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