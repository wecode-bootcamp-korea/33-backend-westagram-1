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
      rex_email    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
      rex_password = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

      if re.match(rex_email, email) == None:
        return JsonResponse({'message': 'Invalid_email'}, status = 400)
      
      if re.match(rex_password, password) == None:
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

      return JsonResponse({'message': 'success'}, status = 201)

    except KeyError:
      return JsonResponse({'message': 'key_error'}, status = 400)