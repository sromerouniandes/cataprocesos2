from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import authenticate
from .models import Image, Portfolio
import json

# Create your views here.
@csrf_exempt
def index(request):
    images_list = Image.objects.all()
    return HttpResponse(serializers.serialize("json", images_list))

@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        json_user = json.loads(request.body)
        username = json_user['username']
        first_name = json_user['first_name']
        last_name = json_user['last_name']
        password = json_user['password']
        email = json_user['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()
        return HttpResponse(serializers.serialize("json", [user_model]))

@csrf_exempt
def get_portfolio_view(request):
    if request.method == 'GET':
        portfolio_list = Portfolio.objects.all().filter(public=True)
        return HttpResponse(serializers.serialize("json", portfolio_list))

    if request.method == 'POST':
        json = json.loads(request.body)

        portfolio_model = Portfolio(user=User.objects.get(id=json['user']))
        portfolio_model.save()
        portfolio = Portfolio.objects.get(id=portfolio_model.id)
        return HttpResponse(json.dumps({'code':201}), status=201, content_type="application/json")

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        djson = json.loads(request.body)
        user = authenticate(username=djson['username'], password=djson['password'])
        if user is not None:
            return HttpResponse(json.dumps({'username':user.username,'first_name':user.first_name,'last_name':user.last_name,'email':user.email}), status=200, content_type="application/json")
        else:
            return HttpResponse(json.dumps({'code':401}), status=401, content_type="application/json")

@csrf_exempt
def user_view(request, pk):
    if request.method == 'PUT':
        user=User.objects.get(id=pk)
        json_user = json.loads(request.body)

        if 'first_name' in json_user:
            user.first_name =json_user['first_name']
        if 'last_name' in json_user:
            user.last_name =json_user['last_name']
        if 'email' in json_user:
            user.email =json_user['email']

        user.save()
        xjson = serializers.serialize("json", [user])
        return HttpResponse(xjson, status=202, content_type="application/json")



