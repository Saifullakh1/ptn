from django.shortcuts import render, redirect
from .models import Post, Like
from tags.models import Tag
from comments.models import Comment, LikeComment
from django.db.models import Q


def get_data(request):
    if 'key_word' in request.GET:
        key = request.GET.get('words')
        posts = Post.objects.filter(Q(title__icontains=key) | Q(description__icontains=key) |
                                    Q(user__username__icontains=key))
    else:
        posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})


def post_data(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        tags = request.POST.get('tags')
        post_obj = Post.objects.create(user=request.user, title=title, description=description, image=file)
        if len(tags) != 0:
            try:
                tags_get = Tag.objects.get(title=tags)
                tags_get.posts.add(post_obj)
            except:
                tags_obj = Tag.objects.create(title=tags)
                tags_obj.posts.add(post_obj)
        return redirect("data")
    return render(request, 'posts/create.html')


def detail_data(request, id):
    posts = Post.objects.get(id=id)
    if request.method == 'POST':
        if 'comment' in request.POST:
            try:
                text = request.POST.get('text')
                comment_obj = Comment.objects.create(user=request.user, post=posts, text=text)
                return redirect('detail_data', posts.id)
            except:
                print("Error")
        if 'reply_comment' in request.POST:
            id = int(request.POST.get('reply_comment'))
            print(id)
            comment_object = Comment.objects.get(id=id)
            text = request.POST.get('text')
            comment_create = Comment.objects.create(user=request.user, post=posts, text=text, parent=comment_object)
            return redirect('detail_data', posts.id)
        if 'like' in request.POST:
            try:
                like = Like.objects.get(user=request.user, post=posts)
                like.delete()
            except:
                Like.objects.create(user=request.user, post=posts)
        if 'like_comment' in request.POST:
            id = int(request.POST.get('like_comment'))
            comment_object = Comment.objects.get(id=id)
            try:
                like = LikeComment.objects.get(user=request.user, comment=comment_object)
                like.delete()
            except:
                LikeComment.objects.create(user=request.user, comment=comment_object)
    return render(request, 'posts/detail.html', {"posts": posts})


def update_data(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        tags = request.POST.get('tag')
        post_update = Post.objects.get(id=id)
        post_update.title = title
        post_update.description = description
        post_update.image = file
        post_update.save()
        if len(tags) != 0:
            try:
                tags_get = Tag.objects.get(title=tags)
                tags_get.posts.add(post_update)
            except:
                tags_obj = Tag.objects.create(title=tags)
                tags_obj.posts.add(post_update)
        return redirect('detail_data', post_update.id)
    return render(request, 'posts/update.html')


def delete_data(request, id):
    if request.method == 'POST':
        post_object = Post.objects.get(id=id)
        post_object.delete()
        return redirect('data')
    return render(request, 'posts/delete.html')
