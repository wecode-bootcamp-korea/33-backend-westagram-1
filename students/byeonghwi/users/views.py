import json
import re

from django.http import JsonResponse
from django.views import View
from users.models import User


class UsersView(View):
  def post(self, request):
    try:
      input_data   = json.loads(request.body)
      name         = input_data["name"]
      email        = input_data["email"]
      password     = input_data["password"]
      phone        = input_data["phone"]
      REX_EMAIL    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
      REX_PASSWORD = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

      if re.match(REX_EMAIL, email) == None:
        return JsonResponse({'message': 'Invalid_email'}, status = 400)
      
      if re.match(REX_PASSWORD, password) == None:
        return JsonResponse({'message': 'Invalid_password'}, status = 400)

      if User.objects.filter(email = email).exists():
        return JsonResponse({'message': 'duplicated_email'}, status = 400)

      if User.objects.filter(phone = phone).exists():
        return JsonResponse({'message': 'duplicated_phone'}, status = 400)

      User.objects.create(
        name     = name,
        email    = email,
        password = password,
        phone    = phone,
      )

      return JsonResponse({'message': 'SUCCESS'}, status = 201)

    except KeyError:
      return JsonResponse({'message': 'KEY_ERROR'}, status = 400)


class LoginView(View):

  def post(self, request):

    try:
      data     = json.loads(request.body)
      email    = data['email']
      password = data['password']
      
      if not User.objects.filter(email = email).exists():
        return JsonResponse({'message':'INVALED_USER'}, status = 401)

      if not User.objects.filter(password = password).exists():
        return JsonResponse({'message':'INCORRECT_PASSWORD'}, status = 401)

      return JsonResponse({'message':'SUCCESS'}, status = 200) 

    except KeyError:
      return JsonResponse({'message':'KEY_ERROR'}, status = 400)