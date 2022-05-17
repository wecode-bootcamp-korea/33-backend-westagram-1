from django.db import models

class Post(models.Model):
    writer              = models.ForeignKey('signup.User', on_delete=models.CASCADE)
    title               = models.CharField(max_length=100)
    posting_content     = models.TextField()
    upload_images       = models.ForeignKey('Image', on_delete=models.CASCADE, null=True)
    upload_files        = models.ForeignKey('Files', on_delete=models.CASCADE, null=True)
    registered_date     = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    top_fixed           = models.BooleanField(default=False, null=True)
    # like                = models.ForeignKey('Like', on_delete=models.CASCADE)

# class Comment(models.Model):
#     posting_comment     = models.ForeignKey('Post', on_delete=models.CASCADE)
#     comment_content     = models.CharField(max_length=200, )

class Image(models.Model):
    post_image          = models.ForeignKey('Post', on_delete=models.CASCADE)
    image_url           = models.CharField(max_length=300)
# 한 포스팅당 다양한 이미지가 있을 수 있고 
# 한 이미지는 다양한 포스팅에 있을 수 없는데 
class File(models.Model):
    post_file           = models.FileField()
    file_url            = models.CharField(max_length=300)

# class Like(models.Model):
#     user = models.ForeignKey('signup.User', on_delete=models.CASCADE)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
    


