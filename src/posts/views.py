from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from comments.forms import CommentForm
from .forms import PostForm
from .models import Post, Likes


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect(instance.get_absolute_url())
    context = {"form": form,
               "foreword": "Create new Post!",
               "inset": "Create",
               }
    return render(request, "post_form.html", context)


@login_required
def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    count_likes = instance.likes_set.all().count()
    data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    comment_form = CommentForm(request.POST or None, initial=data)
    if comment_form.is_valid():
        cont_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=cont_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data
            )

    content_type = ContentType.objects.get_for_model(Post)
    object_id = instance.id
    comments = Comment.objects.filter(content_type=content_type, object_id=object_id)

    paginator = Paginator(comments, 2)

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": instance.title,
        "instance": instance,
        "queryset": queryset,
        "comment_form": comment_form,
        "count_likes": count_likes,
    }
    return render(request, "post_detail.html", context)


@login_required
def post_list(request):
    queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__country__icontains=query)|
            Q(user__city__icontains=query)
            ).distinct()
    paginator = Paginator(queryset_list, 2)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {"object_list": queryset,
               "page_request_var": page_request_var,
               "foreword": "Welcome to DjangoApp!"
               }
    return render(request, "post_list.html", context)


@login_required
def post_like(request, id=None):
    instance = get_object_or_404(Post, id=id)
    new_like, created = Likes.objects.get_or_create(user=request.user, post=instance)
    if not created:
        new_like.delete()
    return redirect(instance.get_absolute_url())