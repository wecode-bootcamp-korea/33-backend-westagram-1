from django.db import models

class Posting(models.Model):
    writer              = models.ForeignKey('signup.User', on_delete=models.CASCADE)
    title               = models.CharField(max_length=100)
    posting_content     = models.TextField()
    upload_images       = models.ForeignKey('Image', on_delete=models.CASCADE)
    upload_files        = models.ForeignKey('Files', on_delete=models.CASCADE)
    registered_date     = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    top_fixed           = models.BooleanField(default=False)
    hits                = models.OnetoOneField('signup.User', on_delete=models.CASCADE)

# 로그인을 했다고 가정하고 
class Comment(models.Model):
    posting_comment     = models.ForeignKey(Posting, on_delete=models.CASCADE)
    comment_content     = models.CharField(max_length=200, )

class Image(models.Model):
    posting_image
    image_url           = models.CharField(max_length=300)
