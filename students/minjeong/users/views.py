from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse

import json
import re
import bcrypt
import jwt

from .models            import User
from my_settings        import SECRET_KEY
from my_settings        import ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)

            email       = data["email"]
            password    = data["password"]
            name        = data["name"]
            phonenumber = data["phonenumber"]
            personal    = data["personal"]

            if not re.match('(\w|\W)+@{1}\w+\.(\w|\W)+', email) and not re.match('^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-z|A-Z|가-핳])(?=.*\W).*$', password):
                return JsonResponse({"message" : "INVALID_EMAIL_PASSWORD"}, status=400)

            if not re.match('(\w|\W)+@{1}\w+\.(\w|\W)+', email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status=400)

            if not re.match('^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-z|A-Z|가-핳])(?=.*\W).*$', password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({"messages" : "EMAIL_EXIST"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
           
            User.objects.create(
                email       = email,
                password    = hashed_password,
                name        = name,
                phonenumber = phonenumber,
                personal    = personal
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
                return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
    
            email    = data["email"]
            password = data["password"]

            user = User.objects.get(email = email)

            if user.password != password:
                return JsonResponse({"messages" : "INVALID_PASSWORD"}, status=400)

            id           = User.objects.get(email=email).id
            access_token = jwt.encode({'id' : id}, SECRET_KEY, algorithm = ALGORITHM)


            return JsonResponse({"ACCESS_TOKEN" : access_token}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_EMAIL"}, status=400)
