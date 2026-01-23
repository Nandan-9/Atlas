import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

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
