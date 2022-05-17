import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from .models import User

REGEX_EMAIL     = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
REGEX_PASSWORD  = "^(?=.{8,16}$)(?=.*[a-z])(?=.*[0-9]).*$"
REGEX_MOBILE    = "\d{3}-\d{3,4}-\d{4}"
REGEX_BIRTHDATE = "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"

class UserSignUpView(View):
    def post(self, request):
        try:
            input_data      = json.loads(request.body)
            input_name      = input_data["name"]
            input_email     = input_data["email"]
            input_password  = input_data["password"]
            input_mobile    = input_data["mobile_number"]
            input_birthdate = input_data["date_of_birth"]

            hashed_password  = bcrypt.hashpw(input_password.encode("utf-8"), \
                bcrypt.gensalt()).decode("utf-8")

            if not re.match(REGEX_EMAIL, input_email) or \
                User.objects.filter(email=input_email).exists():
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if not re.match(REGEX_PASSWORD, input_password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if not re.match(REGEX_MOBILE, input_mobile):
                return JsonResponse({"message": "INVALID_MOBILE_NUMNBER"}, status=400)

            if not re.match(REGEX_BIRTHDATE, input_birthdate):
                return JsonResponse({"message": "INVALID_DATE_OF_BIRTH"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        User.objects.create(
                name          = input_name,
                email         = input_email,
                password      = hashed_password,
                mobile_number = input_mobile,
                date_of_birth = input_birthdate,
        )

        return JsonResponse({"message": "SUCCESS"}, status=201)

class UserSignInView(View):
    def post(self, request):
        try:
            input_data     = json.loads(request.body)
            input_email    = input_data["email"]
            input_password = input_data["password"]
            user           = User.objects.get(email = input_email)
        
            if not User.objects.filter(email=input_email).exists() or \
            not bcrypt.checkpw(input_password.encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

        access_token = jwt.encode({"id": user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
        return JsonResponse({"message": "SUCCESS", "ACCESS_TOKEN": access_token}, status=200)