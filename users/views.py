from django.shortcuts import render, redirect
from .forms import PasswordResetForm, NewUserForm,UserProfileForm
from django.db.models.query_utils import Q
from .models import UserProfile
from main.models import Order
from django.http import JsonResponse
from django.core import serializers

from django.contrib import messages

from .models import User

#password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_info = {
        'name': user_profile.name,
        'surname': user_profile.surname,
        'father': user_profile.father,
        'bitcoin_address': user_profile.bitcoin_address,
        'card_number': user_profile.card_number,
        'passport_number': user_profile.passport_number,
        'email': user_profile.email,
    }
    return render(request, 'users/profile.html', {'user_profile': user_profile, 'user_info': user_info})

def edit(request):
    return render(request, 'users/edit.html')
def edit_user_info(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        consent_given = request.POST.get('consentCheckbox')  # Проверяем, установлена ли галочка
        if form.is_valid() and consent_given:
            form.save()
            return redirect('profile')  # Перенаправляем обратно на страницу редактирования
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'users/edit_user_info.html', {'form': form})

@login_required
def user_info(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_info = {
        'email':user_profile.email,
        'name': user_profile.name,
        'surname': user_profile.surname,
        'father': user_profile.father,
        'bitcoin_address': user_profile.bitcoin_address,
        'ethereum_address': user_profile.ethereum_address,
        'card_number': user_profile.card_number,
        'passport_number': user_profile.passport_number,
    }
    return JsonResponse(user_info)

@login_required
def my_orders(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_email = user_profile.email
        user_orders = Order.objects.filter(email=user_email)
        serialized_orders = serializers.serialize('json', user_orders)
        return JsonResponse({'orders': serialized_orders})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'UserProfile not found'})

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            user_email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=user_email)).first()
            if associated_users:
                subject = "Восстановление пароля"
                email_template_name = "password_reset_email.html"
                c = {
                    "email":associated_users.email,
                    'domain':get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(associated_users.pk)),
                    "user": associated_users,
                    'token': default_token_generator.make_token(associated_users),
                    'protocol': 'https' if request.is_secure() else 'http',
                }
                email = render_to_string(email_template_name, c)
                print(email)
                try:
                    print('Запускаю функцию сенд_емаил')
                    send_mail(subject, email, 'django_academy_shop@mail.ru', [associated_users.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Ошибка.')
                return redirect ("registration/password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"form":password_reset_form})

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def passwordResetConfirm(request, uidb64, token):
    return redirect("main")

def register_request(request):
    if not Group.objects.filter(name='Customer').exists():
        Group.objects.create(name='Customer')

    customer_group = Group.objects.get(name='Customer')
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(customer_group)
            user.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно")
            return redirect('edit_user_info')
        else:
            messages.error(request, "Ошибка. Неверно введенная информация")

    form = NewUserForm()
    return render(request, 'users/register.html', context={'registration_form': form})

