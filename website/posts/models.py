from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    author = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BlogPostImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.image.url