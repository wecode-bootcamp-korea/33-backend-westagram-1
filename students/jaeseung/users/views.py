import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            name     = data['name']
            email    = data['email']
            password = data['password']
            contact  = data['contact']

            email_regex    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            password_regex = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$'
            
            if not re.match(email_regex, email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if not re.match(password_regex, password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({"message": "EMAIL_IS_ALREADY_REGISTERED"}, status=400)

            User.objects.create(
                name     = name,
                email    = email,
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                contact  = contact
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError: 
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email)
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            token = jwt.encode({'id': user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return JsonResponse({"ACCESS": "SUCCESS", "ACCESS_TOKEN" : token}, status=200)
            
        except KeyError: 
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)