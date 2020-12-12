from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.forms import SignUpForm, UserProfileForm, ChangeForm
from items.tools.clean_up import clean_up_files


def user_profile(request, pk=None):
    user = request.user if pk is None else User.objects.get(pk=pk)
    items = user.item_set.all()
    pic_count = len([x for x in items if x.type == 'pic'])
    mod_count = len([x for x in items if x.type == 'mod'])
    form = UserProfileForm()
    if request.method == 'GET':
        context = {'profile_user': user, 'items': items, 'form': form, 'pic_count': pic_count, 'mod_count': mod_count, }
        return render(request, 'accounts/user_profile.html', context)
    else:
        form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('current user profile')
        return redirect('current user profile')


def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('index')
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required
def edit_user(request, pk):
    user_edit = User.objects.get(pk=pk)
    if user_edit != request.user:
        return HttpResponse('FORBIDDEN !')
    user = request.user
    form = ChangeForm(instance=user)
    if request.method == 'POST':
        user = request.user
        form = ChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user profile', user.pk)
    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'accounts/edit_user.html', context)


@login_required
def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    if user != request.user:
        return HttpResponse('FORBIDDEN !')
    if request.method == 'POST':
        user_image = user.userprofile.profile_picture
        items_images = user.item_set.all()
        if items_images:
            [clean_up_files(x.image.path) for x in items_images]
        if user_image:
            clean_up_files(user_image.path)
        user.delete()
        return redirect('index')
    context = {
        'user': user,
    }
    return render(request, 'accounts/delete_user.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            pk = user.pk
            update_session_auth_hash(request, user)  # Important, otherwise login again !
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user profile', pk)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
