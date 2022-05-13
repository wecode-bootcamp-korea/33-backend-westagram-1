from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse

import json
import re

from .models            import User


class SignupView(View):
    def post(self,request):
        input_data=json.loads(request.body)
        a = re.match('(\w|\W)+@{1}\w+\.(\w|\W)+', input_data["email"])
        b = re.match('^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-z|A-Z|가-핳])(?=.*\W).*$',input_data["password"])

        data=input_data

        if a==None and b==None:
            return JsonResponse({"message": "@과.이 포함된 이메일 형식이 필요합니다,8자리 이상, 문자, 숫자, 특수문자의 복합이어야 합니다"}, status=400)
        elif a==None:
            return JsonResponse({"message": "@과.이 포함된 이메일 형식이 필요합니다"}, status=400)
        elif b==None:
            return JsonResponse({"message":"비밀번호는 8자리 이상, 문자, 숫자, 특수문자의 복합이어야 합니다"}, status=400)
        else:
            User.objects.create(
                    email       = data["email"],
                    password    = data["password"],
                    name        = data["name"],
                    phonenumber = data["phonenumber"],
                    personal    = data["personal"]
                )
        return JsonResponse({"message" : "SUCCESS"}, status=201)
       