from django.db    import models
from users.models import User

class Post(models.Model): 
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content     = models.TextField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'posts'

class Image(models.Model): 
    image_url = models.URLField(max_length=500)
    post      = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'images'