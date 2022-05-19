import json

from django.views       import View
from django.http        import JsonResponse

from postings.models    import Post, File, Comment, CommentLike
from users.utils        import jwt_expression

class PostingView(View):
    @jwt_expression
    def post(self, request):
        try:
            title           = request.POST["title"]
            posting_content = request.POST["posting_content"]
            upload_files    = request.FILES.getlist('upload_files')
            #여러장의 이미지를 하나의 키값으로 받을때 getlist
            #한장의 이미지가 하나의 키값에 존재할 때 __getitem__
            top_fixed       = request.POST["top_fixed"]
            writer_id       = request.user
            # writer_id       = request.POST["writer_id"]
            #원레는 request.user가 들어가야 하는데... 음...
            #request.user
            
            Post.objects.create(
                title           = title,
                posting_content = posting_content,
                top_fixed       = top_fixed,
                writer_id       = writer_id
            )

            for upload_file in upload_files:
                document = File.objects.create(
                    upload_files = upload_file,
                    post_file_id = Post.objects.get(title=title).id
                )

        

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    def get(self, request):
        try:
            
            results=[]
            
            posts = Post.objects.all()
            for post in posts:
                comments=[]
                # 
                results.append({
                    '아이디':post.id,
                    '제목': post.title,
                    '내용': post.posting_content,
                    '등록일': post.registered_date,
                    '상위고정': post.top_fixed,
                    # '관련 댓글': comments
                })

            return JsonResponse({"message" : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class PostingDetailView(View):
    def get(self, request, id):
        try:
            results=[]

            comments=[]
            [comments.append(comment.comment_content) for comment in Comment.objects.select_related('posting_comment').filter(posting_comment_id=id)]
            
            present_post=Post.objects.get(id=id)
            results.append({
                '제목'  : present_post.title,
                '내용'  : present_post.posting_content,
                '등록일' : present_post.registered_date,
                '상위고정': present_post.top_fixed,
                '댓글'   : comments
            })
            return JsonResponse({"message" : results}, status=200)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @jwt_expression
    def post(self, request, id): 
        try:
            data        = json.loads(request.body)

            comment_writer  = request.user
            comment_content = data["comment_content"]
            posting_comment = Post.objects.get(id=id).id

            Comment.objects.create(
                comment_writer_id = comment_writer,
                comment_content = comment_content,
                posting_comment_id = posting_comment
            )
            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)



