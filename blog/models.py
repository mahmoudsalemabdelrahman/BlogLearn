from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
# Create your models here.



def image_upload(instance, filename):
    imagename, extension = filename.split(".")
    return "jobs/%s/%s.%s"%(instance.id, instance.id,  extension)
class Post(models.Model):
    """Model definition for Post."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField( max_length=50)
    published_at = models.DateTimeField(default=timezone.now)
    # slug = models.SlugField( unique_for_date='title', max_length=140)
    description = models.TextField(max_length=1000)
    image = models.ImageField( upload_to=image_upload)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    tags = TaggableManager()

    slug = models.SlugField(null=True, blank=True, unique=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Post."""
        ordering = ('-published_at', )
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Unicode representation of Post."""
        return str(self.title)



    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args,**kwargs)


    def get_absolute_url(self):
        """Return absolute url for Post."""
        return ('')

    # TODO: Define custom methods here


class Category(models.Model):
    name = models.CharField( max_length=30)



    def __str__(self):
        return self.name







class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_active = models.BooleanField(default=False)
    reviewed = models.IntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author.email} on {self.post}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    class Meta:
        ordering = ('created_at',)