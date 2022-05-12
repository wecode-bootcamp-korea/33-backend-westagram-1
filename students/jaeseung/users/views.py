import json

from django.http import JsonResponse
from django.views import View

from users.models import User

class UsersView(View):
    def post(self, request):
        data = json.loads(request.body)


        

        User.objects.create(
            name = data['name'],
            email = data['email'],
            password = data['password'],
            contact = data['contact']
        )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)