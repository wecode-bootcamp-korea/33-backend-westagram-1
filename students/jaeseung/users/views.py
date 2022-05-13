import json
import re

from django.http import JsonResponse
from django.views import View

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
                password = password,
                contact  = contact
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError: 
            return JsonResponse({"message": "KEY_ERROR"}, status=400)