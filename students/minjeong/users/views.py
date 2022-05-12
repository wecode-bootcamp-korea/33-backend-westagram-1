from django.shortcuts import render
from .models import User
import json
from django.views import View
from django.http import JsonResponse
import re

class SignupView(View):
    def post(self,request):
        input_data=json.loads(request.body)
        a = re.search('(\w|\W)+@{1}\w+\.(\w|\W)+', input_data["email"])
        b = re.search('^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-z|A-Z|가-핳])(?=.*\W).*$',input_data["password"])
       
        if a==None and b==None:
            return JsonResponse({"message": "@과.이 포함된 이메일 형식이 필요합니다,8자리 이상, 문자, 숫자, 특수문자의 복합이어야 합니다"}, status=400)
        elif a==None:
            return JsonResponse({"message": "@과.이 포함된 이메일 형식이 필요합니다"}, status=400)
        elif b==None:
            return JsonResponse({"message":"8자리 이상, 문자, 숫자, 특수문자의 복합이어야 합니다"}, status=400)
        else:
            User.objects.create(
                    email       = input_data["email"],
                    password    = input_data["password"],
                    name        = input_data["name"],
                    phonenumber = input_data["phonenumber"],
                    personal    = input_data["personal"]
                )
        return JsonResponse({"message" : "SUCCESS"}, status=201)
