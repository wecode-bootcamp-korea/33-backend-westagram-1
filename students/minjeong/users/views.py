from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse

import json
import re

from .models            import User


class SignupView(View):
    def post(self, request):
        
        try:
            data    = json.loads(request.body)

            if not re.match('(\w|\W)+@{1}\w+\.(\w|\W)+', data["email"]) and not re.match('^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-z|A-Z|가-핳])(?=.*\W).*$', data["password"]):
                return JsonResponse({"message" : "INVALID_EMAIL_PASSWORD"}, status=400)

            if not re.match('(\w|\W)+@{1}\w+\.(\w|\W)+', data["email"]):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status=400)

            if not re.match('^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-z|A-Z|가-핳])(?=.*\W).*$', data["password"]):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)
            
            if User.objects.filter(email=data["email"]):
                return JsonResponse({"messages" : "EMAIL_EXIST"}, status=400)
           
            User.objects.create(
                email       = data["email"],
                password    = data["password"],
                name        = data["name"],
                phonenumber = data["phonenumber"],
                personal    = data["personal"]
                            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError :
                return JsonResponse({"message" : "WRONG_FIELD_NAME"}, status=400)

        except Exception as e :
            return JsonResponse({"message" : e}, status=400)

class LoginView(View):
    def post(self, request):

        data     = json.loads(request.body)
        email    = data["email"]
        password = data["password"]
#         signups=Signup.objects.all()

#         # if input_data["email"] not in request.body or input_data["password"] not in request.body:
#         #     return JsonResponse( {"message": "KEY_ERROR"}, status=400)
        
#         # Signup.objects.get(email=input_data["email"]) == None:
#         #     return JsonResponse({"message" : "SUCCESS"}, status=201)
#         # 계정이나 패스워드 키가 전달되지 않았을 경우, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.
#         try:
#             for signup in signups:
#                 if input_data["email"] not in signup.email:
#                     return JsonResponse({"message":"등록된 아이디가 없습니다. 올바른 아이디를 입력해주세요. "},status=400)
#                 else:
#                     if Signup.objects.get(email=input_data["email"]).password != input_data["password"]:
#                         return JsonResponse( {"message": "해당하는 비밀번호가 존재하지 않습니다."}, status=400)
#                     else:
#                         return JsonResponse( {"message": "SUCCESS"}, status=201)
#         except :
#             return JsonResponse({"message":"계정이나 패스워드가 전달되지 않았습니다. "},status=400)


