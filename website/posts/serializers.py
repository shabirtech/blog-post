from rest_framework import serializers
from .models import BlogPost, BlogPostImage

class BlogPostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostImage
        fields = ('id', 'image')

class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogPostImageSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author', 'pub_date', 'images')

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        blog_post = BlogPost.objects.create(**validated_data)
        for image_data in images_data.values():
            BlogPostImage.objects.create(post=blog_post, image=image_data)
        return blog_post