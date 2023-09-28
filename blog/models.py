from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
# Create your models here.



def image_upload(instance, filename):
    imagename, extension = filename.split(".")
    return "jobs/%s/%s.%s"%(instance.id, instance.id,  extension)
class Post(models.Model):
    """Model definition for Post."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField( max_length=50)
    published_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField( unique_for_date='title', max_length=140)
    description = models.TextField(max_length=1000)
    image = models.ImageField( upload_to=image_upload)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    tags = TaggableManager()
    # TODO: Define fields here

    class Meta:
        """Meta definition for Post."""
        ordering = ('-published_at', )
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Unicode representation of Post."""
        return self.title

    # def save(self, *args, **kwargs):
    #     """Save method for Post."""
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)


    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        """Return absolute url for Post."""
        return ('')

    # TODO: Define custom methods here


class Category(models.Model):
    name = models.CharField( max_length=30)



    def __str__(self):
        return self.name
