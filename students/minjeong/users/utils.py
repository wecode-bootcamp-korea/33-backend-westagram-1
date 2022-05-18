from django.http        import JsonResponse

import jwt

from my_settings        import SECRET_KEY, ALGORITHM
from .models            import User

def jwt_expression(func):
    def get_token(self, request):
        try:
            access_token = request.header.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            user         = User.objects.get(id=payload['id']).id
            
            if payload == user:
                func()
            return  JsonResponse({"message" : "SUCCESS"}, status=200)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_ID"}, status=400)
        

    return get_token