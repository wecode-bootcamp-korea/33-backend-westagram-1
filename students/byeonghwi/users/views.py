import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View
from users.models import User
from django.conf import settings


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
      
      hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

      User.objects.create(
        name     = name,
        email    = email,
        password = hashed_password,
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
      
      user = User.objects.get(email = email)

      if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return JsonResponse({'message':'INCORRECT_PASSWORD'}, status = 401)

      token = jwt.encode({'id': user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

      return JsonResponse({
        'message':'SUCCESS',
        'access_token':token
        }, status = 200) 

    except User.DoesNotExist:
      return JsonResponse({'message':'INVALED_USER'}, status = 401)
    except KeyError:
      return JsonResponse({'message':'KEY_ERROR'}, status = 400)