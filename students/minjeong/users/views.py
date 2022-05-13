from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse

import json
import re

from .models            import User


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
           
            User.objects.create(
                email       = email,
                password    = password,
                name        = name,
                phonenumber = phonenumber,
                personal    = personal
            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError :
                return JsonResponse({"message" : "KEY_ERROR"}, status=400)