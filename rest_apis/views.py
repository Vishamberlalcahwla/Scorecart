from django.shortcuts import render
from pandas.io.formats.format import format_array
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_apis.models import *
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
import pymysql.cursors
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from . TodoSerializer import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

@csrf_exempt     
@api_view(["POST"])
@permission_classes((AllowAny,))
def register_api(request):        # Create your views here. 
    try:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        output = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,confirm_password=confirm_password,password=password)
        token,_ = Token.objects.get_or_create(user=output)
        response = {'error': False,'auth_token':token.key ,'data': output.asjson(),"message": "Your Profile Created Successfully."}
        return JsonResponse(response, safe=False)
    except Exception as e:
        response = {'error': True, 'data': 0, "message": str(e)}
        return JsonResponse(response, safe=False)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Login(request): 
    try:
        email = request.POST.get("email")
        password = request.POST.get("password")
        response=CustomUser.Login(email=email,password=password)
        return JsonResponse(response, safe=False)
    except Exception as e:
        response = {'error': True, 'data': 0, "message": str(e)}
        return JsonResponse(response, safe=False)


@csrf_exempt
@api_view(["POST"])
def Home(request): 
    try:
        response = {'error': False, 'data': 0, "message": "Data"}
        return JsonResponse(response, safe=False)
    except Exception as e:
        response = {'error': True, 'data': 0, "message": str(e)}
        return JsonResponse(response, safe=False)                        



class ListTodoAPIView(APIView):
    def get(self,request):
        try:
            user_id = Token.objects.get(key=request.auth.key).user_id
            todos = Todo.objects.filter(user_id=user_id)
            serializer = TodoSerializer(todos, many=True)
            response = {'error': False, 'data': serializer.data, "message": "Get"}
            return JsonResponse(response, safe=False)
        except Exception as e:
            response = {'error': True, 'data': 0, "message": str(e)}
            return JsonResponse(response, safe=False)  

class TodoDetailAPIView(APIView):
    def get(self,request,pk):
        try:
            todos = Todo.objects.get(id=pk)
            serializer = TodoSerializer(todos, many=False)
            response = {'error': False, 'data': serializer.data, "message": "Get"}
            return JsonResponse(response, safe=False) 
        except Exception as e:
            response = {'error': True, 'data': 0, "message": str(e)}
            return JsonResponse(response, safe=False)   
        except Todo.DoesNotExist:
            response = {'error': True, 'data': "", "message": "Task can't find"}
            return JsonResponse(response, safe=False)


class CreateTodoAPIView(APIView):
    def post(self,request):
        try:
            serializer = TodoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'error': False, 'data': serializer.data, "message": "Saved."}
                return JsonResponse(response, safe=False)
            response = {'error': True, 'data': serializer.errors, "message": "There is an error."}
            return JsonResponse(response, safe=False) 
        except Exception as e:
            response = {'error': True, 'data': 0, "message": str(e)}
            return JsonResponse(response, safe=False)

class UpdateTodoAPIView(APIView):
    def post(self,request,pk):
        try:
            todo = Todo.objects.get(id=pk)
            serializer = TodoSerializer(instance=todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'error': False, 'data': serializer.data, "message": "Task status has been changed"}
                return JsonResponse(response, safe=False)   
            response = {'error': True, 'data': serializer.errors, "message": "There is an error."}
            return JsonResponse(response, safe=False)
        except Todo.DoesNotExist:
            response = {'error': True, 'data': "", "message": "Task can't find"}
            return JsonResponse(response, safe=False)     



class CompleteTodoTask(APIView):
    def post(self,request):
        try:
            if request.POST.get("id") == '':
                response = {'error': True, 'data': 0, "message": "Please provide task id."}
                return JsonResponse(response, safe=False) 
            r_id = int(request.POST.get("id"))
            todo = Todo.objects.get(id=r_id)
            todo.is_completed = True  # change field
            todo.save() 
            serializer = TodoSerializer(todo, many=False)
            #todo = Todo.objects.filter(id=r_id).update(is_completed = True)
            response = {'error': False, 'data': serializer.data, "message": "Task status has been changed"}
            return JsonResponse(response, safe=False)
        except Todo.DoesNotExist:
            response = {'error': True, 'data': "", "message": "Task can't find"}
            return JsonResponse(response, safe=False)

class DeleteTodoAPIView(APIView):
    def get(self,request,pk):
        try:
            todo = Todo.objects.get(id=pk)
            todo_instance = Todo.objects.get(id=pk)
            todo_instance.delete()
            response = {'error': False, 'data': pk, "message": "Task deleted"}
            return JsonResponse(response, safe=False)
        except Todo.DoesNotExist:
            response = {'error': True, 'data': "", "message": "Task can't find"}
            return JsonResponse(response, safe=False)          

