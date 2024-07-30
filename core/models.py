from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = ((0, 'Draft'), (1, 'Published'))

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author =models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_category', null=True, blank=True)
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/images')
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return self.title
    
    def snipet(self):
        return self.content[: 150] + '...'
    
    def get_category_name(self):
        return self.category.__str__()
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)