from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import CustomUserPasswordHistory


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def change_password(request):
    if request.method == "POST":
        change_password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if change_password_form.is_valid():
            if (change_password_form.new_password1 != change_password_form.old_password):
                CustomUserPasswordHistory.remember_password(username =change_password_form.user.title, old_pass =change_password_form.old_password, pass_date=localtime())
            change_password_form.save()
            messages.success(request, f'Password successfully changed for user {change_password_form.user.title}!')
            return redirect('customers-home-page')

    else:
        change_password_form = PasswordChangeForm(User)
    return render(request, "users/change_password.html", {'form': change_password_form})


