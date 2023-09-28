from django.shortcuts import render
from .models import Post

# Create your views here.

def post_list(request):
    post = Post.objects.all()


    return render(request, 'post_list.html', {'post':post})


def post_detail(request):
     post = Post.objects.all()


     return render(request,' post_detail.html',{'post':post})
