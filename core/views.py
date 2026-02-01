from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
def hello(request):
    return JsonResponse({"hello": "world"})


def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        if not data.get("email"):
            return JsonResponse({"error": "Email required"}, status=400)

        
        user = User.objects.create_user(
            username=data['name'],
            email=data['email'],
            password=data['password']
        )
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "email": user.email,
            "id": user.id,
        }, status=201)


def get_user(request):
    user_id = request.GET.get('id')
    if not user_id:
        return JsonResponse({'error':'id required'}, status=400)
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({
            "username": user.username,
            "email": user.email,
            "id": user.id,
        })
    except User.DoesNotExist:
        return JsonResponse({'error':'not found'}, status=404)

