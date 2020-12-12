from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from items.forms import CommentForm, ItemForm, FilterForm
from items.tools.clean_up import clean_up_files

from items.models import Item, Like, Comment


def index(request):
    items = Item.objects.all()
    if items:
        total_item_list = [item for item in items]
        items_dict = dict(
            sorted({item: item.like_set.count() for item in total_item_list}.items(), key=lambda x: x[1], reverse=True))
        items_list = [x for x in items_dict.keys() if x.like_set.count() > 0]
        n = len(items_list)
        if n >= 10:
            n = 10
        top_10 = [items_list[x] for x in range(n)]
        context = {'top_ten': top_10, 'n': range(len(top_10))}
        return render(request, 'index.html', context)
    return render(request, 'index.html')


def list_view(pics, request, template):
    paginator = Paginator(pics, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = FilterForm()
    if request.method == 'POST':
        category = request.POST.dict()['category']
        filter_form = FilterForm(initial={'category': category})
        filtered_pics = [x for x in pics.filter(category=category)]
        paginator = Paginator(filtered_pics, 6)
        page_obj_filtered = paginator.get_page(page_number)
        context = {
            'pics': filtered_pics,
            'page_object': page_obj_filtered,
            'form': filter_form,
        }

        return render(request, template, context)

    context = {
        'pics': pics,
        'page_object': page_obj,
        'form': form,
    }

    return render(request, template, context)


def list_pics(request):
    pics = Item.objects.filter(type='pic')
    return list_view(pics, request, 'pic_list.html')


def list_mods(request):
    pics = Item.objects.filter(type='mod')
    return list_view(pics, request, 'mod_list.html')


def comment_item(request, pk, item):
    if not request.user.is_authenticated:
        return redirect('login')
    if item.user == request.user:
        return HttpResponse('FORBIDDEN !')
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(text=form.cleaned_data['text'])
        comment.user = request.user
        comment.item = item
        comment.save()
        return redirect('details', pk)
    context = {
        'item': item,
        'form': form,

    }

    return render(request, 'detail.html', context)


def details(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'item': item,
            'form': CommentForm(),
            'can_delete': request.user == item.user,
            'can_edit': request.user == item.user,
            'can_like': request.user != item.user,
            'can_comment': request.user != item.user,
            'has_liked': item.like_set.filter(user_id=request.user.id).exists(),
        }

        return render(request, 'detail.html', context)
    else:
        return comment_item(request, pk, item)


def influence_item(request, item, template_name):
    if request.method == 'GET':
        user = request.user
        form = ItemForm(instance=item, initial={'user': user})
        form.fields['user'].widget = forms.HiddenInput()

        context = {
            'form': form,
            'item': item,
        }

        return render(request, f'{template_name}.html', context)
    else:
        old_image = item.image
        user = request.user
        form = ItemForm(request.POST, request.FILES, instance=item, initial={'user': user})
        if form.is_valid():
            form.save()
            likes = Like.objects.filter(item_id=item.pk)
            likes.delete()
            if old_image:
                clean_up_files(old_image.path)
            return redirect('details', item.pk)

        context = {
            'form': form,
            'item': item,
        }

        return render(request, f'{template_name}.html', context)


@login_required
def edit(request, pk):
    item = Item.objects.get(pk=pk)
    if item.user != request.user:
        return HttpResponse('FORBIDDEN !')
    return influence_item(request, item, 'edit')


@login_required
def create(request):
    item = Item()
    return influence_item(request, item, 'create')


@login_required
def delete(request, pk):
    item = Item.objects.get(pk=pk)
    if item.user != request.user:
        return HttpResponse('FORBIDDEN !')
    if request.method == 'GET':
        context = {
            'item': item,
        }

        return render(request, 'delete.html', context)
    else:
        image = item.image
        if image:
            clean_up_files(image.path)
        item.delete()
        return redirect('current user profile')


@login_required
def like_item(request, pk):
    item = Item.objects.get(pk=pk)
    likes = item.like_set.filter(user_id=request.user.id)
    like = Like(value=str(pk))
    if likes.exists():
        likes.delete()
    else:
        like.item = item
        like.user = request.user
        like.save()
    return redirect('details', pk)
