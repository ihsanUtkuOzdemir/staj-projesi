from django.shortcuts import render, HttpResponse, get_object_or_404,HttpResponseRedirect,redirect,Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

def post_index(request):

    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        ).distinct()


    paginator = Paginator(post_list, 8)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "post/index.html", {'posts': posts})


def post_detail(request, slug):

    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

        paginator = Paginator(post_list, 8)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, "post/index.html", {'posts': posts})

    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post
    }

    return render(request, "post/detail.html", context)


def post_create(request):

    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

        paginator = Paginator(post_list, 8)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, "post/index.html", {'posts': posts})

    if not request.user.is_authenticated:
        raise Http404()

    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'BAŞARLI BİR ŞEKİLDE OLUŞTURULDU.')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'post/form.html', context)


def post_update(request, slug):

    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

        paginator = Paginator(post_list, 8)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, "post/index.html", {'posts': posts})

    if not request.user.is_authenticated:
        raise Http404()

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'BAŞARLI BİR ŞEKİLDE GÜNCELLENDİ.')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'post/form.html', context)



def post_delete(request,slug):

    if not request.user.is_authenticated:
        raise Http404()

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'BAŞARLI BİR ŞEKİLDE SİLİNDİ.')
    return redirect('post:index')