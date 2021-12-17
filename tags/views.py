from django.shortcuts import render, redirect
from .models import Tag


def detail(request, id):
    tag = Tag.objects.get(id=id)
    return render(request, 'tags/detail.html', {'tag': tag})


def update_tag(request, id):
    tag = Tag.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        tag.title = title
        tag.save()
        return redirect('data')
    return render(request, 'tags/update.html')


def delete_tag(request, id):
    if request.method == 'POST':
        tag = Tag.objects.get(id=id)
        tag.delete()
        return redirect('data')
    return render(request, 'tags/delete.html')
