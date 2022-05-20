import json
from json.decoder    import JSONDecodeError

from django.http     import JsonResponse
from django.views    import View

from postings.models import Comment, Post, Image, Like
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
            'username'  : User.objects.get(id = post.user.id).name,
            'post_id'   : post.id,
            'content'   : post.content,
            'images'    : [image.image_url for image in post.image_set.all()],
            'created_at': post.created_at
            } for post in Post.objects.all()
            ]

        return JsonResponse({'RESULT' : post_list}, status=200)

# class CommentView(View):
#     @signin_decorator
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             user = request.user

#             post = Post.objects.get(id = data['post'])

#             Comment.objects.create(
#                 comment = data['comment'],
#                 user = user,
#                 post = post,
#             )
#             return JsonResponse({'message' : 'SUCCESS'}, status = 200)


#         except KeyError: 
#             return JsonResponse({"message": 'KEY_ERROR'}, status=400)

    # @signin_decorator
    # def get(self, request):
    #     # if not Post.objects.filter(id=10).exists()
    #     comment_list = [{
    #         'user_id' : User.objects.get(id= comment.user.id),
    #         'username' : User.objects.get(id= comment.user.id).name,
    #         'content' : comment.comment,
    #         'created_at' : comment.created_at,
    #     } for comment in Comment.objects.filter(post_id = 10)
    #     ]

    #     return JsonResponse({'RESULT' : comment_list}, status=200)

class CommentSearchView(View):
    @signin_decorator
    def post(self, request, post_id):
        try: 
            data = json.loads(request.body)
            user = request.user

            post = Post.objects.get(id = post_id)

            Comment.objects.create(
                comment = data['comment'],
                user    = user,
                post    = post,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)


        except KeyError: 
            return JsonResponse({"message": 'KEY_ERROR'}, status=400)

    @signin_decorator
    def get(self, request, post_id):

        comment_list = [{
            'id'        : User.objects.get(id= comment.user.id).id,
            'email'     : User.objects.get(id= comment.user.id).email,
            'username'  : User.objects.get(id= comment.user.id).name,
            'comment'   : comment.comment,
            'created_at': comment.created_at,
            } for comment in Comment.objects.filter(post_id = post_id)
        ]

        return JsonResponse({'RESULT' : comment_list}, status=200)

class LikeView(View):
    @signin_decorator
    def post(self, request):
        try: 
            data = json.loads(request.body)
            user = request.user
            post_id = data['post_id']

            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({'message':'POSTING_DOES_NOT_EXIST'}, status=404)
            
            if Post.objects.filter(post_id )

            Like.objects.create(
                user = user,
                post = post_id
            )

        except KeyError: 
            return JsonResponse({"message": 'KEY_ERROR'}, status=400)