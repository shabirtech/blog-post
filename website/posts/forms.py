from django import forms
from django.forms.models import inlineformset_factory
from .models import BlogPost, BlogPostImage

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author']

class BlogPostImageForm(forms.ModelForm):
    class Meta:
        model = BlogPostImage
        fields = ['image']

BlogPostImageFormSet = inlineformset_factory(BlogPost, BlogPostImage, form=BlogPostImageForm, extra=5, can_delete=False)
