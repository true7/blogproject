from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (authenticate,
                                 login,
                                 logout,
                                 )
from .forms import UserLoginForm, UserRegisterForm
from .models import User


def login_view(request):
    form = UserLoginForm(request.POST or None)
    context = {
        'form': form,
        'inset': 'Login'
    }
    next = request.GET.get('next')
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    return render(request, 'form.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    context = {
        'form': form,
        'inset': 'Register'
    }
    if form.is_valid():
        user = form.save(commit=False)
        password2 = form.cleaned_data.get('password2')
        user.set_password(password2)
        # user.first_name = form.cleaned_data.get('first_name')
        # user.last_name = form.cleaned_data.get('last_name')
        # user.birthday = form.cleaned_data.get('birthday')
        # user.country = form.cleaned_data.get('country')
        # user.city = form.cleaned_data.get('city')
        user.save()
        send_mail(
            'Confirmation email',
            'Thank you. Your activation link:  https://blogproject-13.herokuapp.com/activate/{}'.format(user.id),
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return redirect('confirm')
    return render(request, 'form.html', context)


def activate(request, id=None):
    user = get_object_or_404(User, id=id)
    user.is_active = True
    user.save()
    return redirect('login')