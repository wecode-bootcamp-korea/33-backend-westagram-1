import json
import jwt

from django.http  import JsonResponse
from django.conf  import settings

from users.models import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError: 
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)

        except User.DoesNotExist: 
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
            
        return func(self, request, *args, **kwargs)
    
    return wrapper


# # 데코레이터 함수 작성
# def is_paid_user(func): # func는 이 함수 안에 넣을 함수 이름을 말함
#     user_paid = True    # 테스트를 위해 true로만 설정
	
#     # 실제 실행하려고 한 함수를 중첩 함수를 통해 실행시킨다.
#     def wrapper():      # 호출할 함수를 감싸는 함수 
#         if user_paid:
#             return func()
#         else:
#             return
            
#     return wrapper      # closure 함수로 만듦