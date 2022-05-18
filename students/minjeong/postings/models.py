from django.db import models

class Post(models.Model):
    writer              = models.ForeignKey('users.User', on_delete=models.CASCADE, default=1)
    title               = models.CharField(max_length=100)
    posting_content     = models.TextField()
    registered_date     = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    top_fixed           = models.BooleanField(default=False)
    # like                = models.ForeignKey('Like', on_delete=models.CASCADE)

# class Comment(models.Model):
#     posting_comment     = models.ForeignKey('Post', on_delete=models.CASCADE)
#     comment_content     = models.CharField(max_length=200, )

# 한 포스팅당 다양한 이미지가 있을 수 있고 
# 한 이미지는 다양한 포스팅에 있을 수 없는데

class File(models.Model):
    post_file           = models.ForeignKey('Post', on_delete=models.CASCADE)
    upload_files        = models.FileField(upload_to="images/", blank=True)

# class Like(models.Model):
#     user = models.ForeignKey('signup.User', on_delete=models.CASCADE)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
    


