from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from .models import BlogPost, BlogPostImage
from .forms import BlogPostForm, BlogPostImageFormSet
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogPostSerializer, BlogPostImageSerializer
from rest_framework import generics
from django.views.decorators.http import require_POST


def home(request):
    posts = BlogPost.objects.all()
    return render(request, 'home.html', {'posts': posts})

def create_post(request):
    ImageFormSet = BlogPostImageFormSet(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid() and ImageFormSet.is_valid():
            post = form.save()
            ImageFormSet.instance = post
            ImageFormSet.save()
            return  HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form, 'formset': ImageFormSet})



@require_POST
def validate_title(request):
    title = request.POST.get('title')
    if title and len(title.strip()) > 0: 
        return JsonResponse({'valid': True})
    else:
        return JsonResponse({'valid': False})
    


class BlogPostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer




@api_view(['GET', 'POST'])
def blog_post_list(request):
    if request.method == 'GET':
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def blog_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'GET':
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlogPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST'])
def blog_post_image_list(request):
    if request.method == 'GET':
        images = BlogPostImage.objects.all()
        serializer = BlogPostImageSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.data.getlist('images'):
            return HttpResponseBadRequest('No image files submitted')
        
        post_id = request.data.get('post_id')
        post = get_object_or_404(BlogPost, pk=post_id)

        images = []
        for image in request.data.getlist('images'):
            images.append({'post': post.id, 'image': image})
        serializer = BlogPostImageSerializer(data=images, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def blog_post_image_detail(request, pk):
    image = get_object_or_404(BlogPostImage, pk=pk)

    if request.method == 'GET':
        serializer = BlogPostImageSerializer(image)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlogPostImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)