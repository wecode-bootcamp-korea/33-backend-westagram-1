from django.db import models

class Post(models.Model):
    writer              = models.ForeignKey('users.User', on_delete=models.CASCADE, default=1, related_name="post")
    title               = models.CharField(max_length=100)
    posting_content     = models.TextField()
    registered_date     = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    top_fixed           = models.BooleanField(default=False)
    # like                = models.ForeignKey('Like', on_delete=models.CASCADE)

class Comment(models.Model):
    comment_writer      = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comment')
    posting_comment     = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_content     = models.CharField(max_length=200)
    comment_like        = models.ManyToManyField('users.User', through='CommentLike', related_name="commentcontent")
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

class File(models.Model):
    post_file           = models.ForeignKey('Post', on_delete=models.CASCADE)
    upload_files        = models.FileField(upload_to="images/", blank=True)

# class PostLike(models.Model):
#     user = models.ForeignKey('signup.User', on_delete=models.CASCADE)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
# comment_like = models.BooleanField(default=1)
    
class CommentLike(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="commentlike")
    comment      = models.ForeignKey('Comment', on_delete=models.CASCADE)
    comment_like = models.BooleanField(default=1)


    


