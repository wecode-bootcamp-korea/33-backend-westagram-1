import json
from json.decoder    import JSONDecodeError

from django.http     import JsonResponse
from django.views    import View

from postings.models import Post, Image
from users.models    import User
from users.utils     import signin_decorator

class PostView(View):
    @signin_decorator
    def post(self, request):
        try: 
            data = json.loads(request.body)
            user = request.user

            content    = data['content']
            image_list = data['image_url'].split(',')

            post = Post.objects.create(
                content = content,
                user    = user,
            )

            for image_url in image_list: 
                Image.objects.create(
                    image_url = image_url,
                    post      = post,
                )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError: 
            return JsonResponse({"message": 'KEY_ERROR'}, status=400)

    @signin_decorator
    def get(self, request):
        post_list = [{
            'username' : User.objects.get(id = post.user.id).name,
            'content' : post.content,
            'images' : [image.image_url for image in post.image_set.all()],
            'created_at' : post.created_at

        } for post in Post.objects.all()
        ]

        return JsonResponse({'RESULT' : post_list}, status=200)