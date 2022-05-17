import json
import re
import bcrypt
import jwt

from django.views       import View
from django.http        import JsonResponse
from django.conf        import settings

from users.models       import User

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
            data = json.loads(request.body)
    
            email    = data["email"]
            password = data["password"].encode('utf-8')

            user        = User.objects.get(email = email)
            db_password = user.password.encode('utf-8')

            if not bcrypt.checkpw(password, db_password):
                return JsonResponse({"messages" : "NOT_MATCH_PASSWORD"}, status=400)

            access_token      = jwt.encode({'id' : user_id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({
                "message"      : "success",
                "access_token" : access_token
            }, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_EMAIL"}, status=400)
