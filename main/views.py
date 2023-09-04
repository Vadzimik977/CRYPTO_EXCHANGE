from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
import uuid
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from .forms import CurrencyExchangeForm, OrderRatingForm, OrderCommentForm
from .models import Application, Order, Review
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator



from django.contrib.admin.views.decorators import staff_member_required
from users.models import UserProfile
from django.core import serializers
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.contrib import messages
def index(request):
    return render(request, 'main/index.html')
def help(request):
    return render(request, 'main/help.html')

def home(request, converted_amount=None):
    if request.method == 'POST':
        form = CurrencyExchangeForm(request.POST)
        if form.is_valid():
            from_currency = form.cleaned_data['from_currency']
            amount = form.cleaned_data['amount']


            api_url = f"https://api.coingecko.com/api/v3/simple/price?ids={form.cleaned_data['currency'].lower()}&vs_currencies=usd"
            response = requests.get(api_url)
            data = response.json()

            if form.cleaned_data['currency'].lower() in data:
                current_exchange_rate = data[form.cleaned_data['currency'].lower()]['usd']
                calculated_amount = converted_amount * current_exchange_rate
                return render(request, 'main/home.html', {'form': form, 'converted_amount': converted_amount,
                                                          'current_exchange_rate': current_exchange_rate,
                                                          'calculated_amount': calculated_amount})

    else:
        form = CurrencyExchangeForm()

    return render(request, 'main/home.html', {'form': form})

def get_exchange_rate(request):
    currency = request.GET.get('currency')
    api_key = 'YOUR_COINCAP_API_KEY'
    api_url = f"https://api.coincap.io/v2/rates/{currency}?apiKey={api_key}"
    response = requests.get(api_url)
    data = response.json()

    if response.status_code == 200:
        exchange_rate = data['data']['rateUsd']
        return JsonResponse({'rateUsd': exchange_rate})

    return JsonResponse({'rateUsd': 0})


def client_details(request,email):
    user_profile=get_object_or_404(UserProfile,user__email=email)
    print(user_profile)
    return render(request, 'main/client_details.html', {'user_profile': user_profile})
def exchange_form(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')

        application = Application.objects.create(
            first_name=first_name,
            last_name=last_name,
            amount=amount,
            currency=currency
        )

        return redirect('main/exchange_confirmation')

    return render(request, 'main/exchange_form.html')

def exchange_confirmation(request):
    return render(request, 'main/exchange_confirmation.html')


def success(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(order_id=order_id)
    if request.method == 'POST':
        rating_form = OrderRatingForm(request.POST)
        comment_form = OrderCommentForm(request.POST)
        if rating_form.is_valid():
            rating_value = rating_form.cleaned_data['rating']
            if comment_form.is_valid():
                comment_text = comment_form.cleaned_data['text']
            else:
                comment_text = " "
            review = Review(order=order, user=request.user, text=comment_text)
            review.rating = rating_value
            review.save()
            reviews_list = Review.objects.all()
            return render(request, 'main/reviews.html', {'reviews_list': reviews_list})
    else:
        rating_form = OrderRatingForm()
        comment_form = OrderCommentForm()
    return render(request, 'main/success.html',
                  {'rating_form': rating_form, 'comment_form': comment_form, 'order': order})


def fail(request):
    return render(request, 'main/fail.html')

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        crypto_currency = request.POST.get('crypto_currency')
        order = Order(email=email, amount=amount, crypto_currency=crypto_currency)
        order.save()
        response_data = {
            'data': f'Order created: Email - {email}, Amount - {amount}, Crypto - {crypto_currency}'
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'})
@csrf_exempt
def create_buy_order(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        crypto_currency = request.POST.get('crypto_currency')
        created_at = request.POST.get('timestamp')
        operation_type = request.POST.get('operation_type')
        order = Order(email=email, amount=amount, crypto_currency=crypto_currency, operation_type=operation_type, created_at=created_at)
        order.save()
        response_data = {
            'data': f'Order created: Email - {email}, Amount - {amount}, Crypto - {crypto_currency}, Type - {operation_type}, Time - {created_at}',
            'order_id': order.order_id
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def create_sell_order(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        crypto_currency = request.POST.get('crypto_currency')
        created_at = request.POST.get('timestamp')
        operation_type = 'Sell'
        processed=0
        order = Order(email=email, amount=amount, crypto_currency=crypto_currency, operation_type=operation_type, created_at=created_at, processed=processed)
        order.save()
        response_data = {
            'data': f'Order created: Email - {email}, Amount - {amount}, Crypto - {crypto_currency}, Type - {operation_type}, Time - {created_at}, Processed - {processed}',
            'order_id': order.order_id
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'})



def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.delete()
        messages.add_message(request, messages.ERROR, "Запись удалена!")
        return render(request, 'main/admin_template.html')
    else:
        messages.add_message(request, messages.ERROR, "Не получилось!")

@staff_member_required
def admin_panel(request):
    orders_list = Order.objects.all().order_by('-created_at')
    paginator = Paginator(orders_list, 10)  # Показывать по 10 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}  # Создаем контекст
    return render(request, 'main/admin_template.html', context)  # Передаем контекст


def new_page_with_timer(request):
    amount = request.POST.get('amount')
    order_id = request.POST.get('order_id')
    currency = request.POST.get('currency')
    context = {
        'order_id': order_id,
        'amount': amount,
        'currency': currency,
    }
    return render(request, 'main/new_page_with_timer.html', context)

def new_page_with_timer1(request):
    amount = request.POST.get('amount')
    order_id = request.POST.get('order_id')
    crypto_currency=request.POST.get('crypto_currency')
    context = {
        'order_id': order_id,
        'amount': amount,
        'crypto_currency':crypto_currency,
    }
    return render(request, 'main/new_page_with_timer1.html', context)
def waiting(request):
    order_id = request.GET.get('order_id')
    context = {
        'order_id': order_id,
    }
    return render(request, 'main/waiting.html', context)
@csrf_exempt
def process_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(order_id=order_id)
            order.processed=1
            processed=1
            order.save()
            response_data = {
                'data': f'Order processed: order_id - {order_id}, processed - {processed}'
            }
            return JsonResponse(response_data)
        except Order.DoesNotExist:
            response_data = {
                'error': 'Order not found'
            }
            return JsonResponse(response_data, status=404)

@csrf_exempt
def process_order1(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(order_id=order_id)
            order.processed=2
            processed=2
            order.save()
            response_data = {
                'data': f'Order processed: order_id - {order_id}, processed - {processed}'
            }
            return JsonResponse(response_data)
        except Order.DoesNotExist:
            response_data = {
                'error': 'Order not found'
            }
            return JsonResponse(response_data, status=404)

@csrf_exempt
def mark_order_as_paid(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.is_paid = True
        is_paid=True
        order.save()
        response_data = {
            'data': f'Order processed: order_id - {order_id}, is_paid - {is_paid}'
        }
        return JsonResponse(response_data)
def check_order_status(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        try:
            if order.processed == 1:
                return JsonResponse({'order_processed': 1})
            elif order.processed == 2:
                return JsonResponse({'order_processed': 2})
            # Замените на свою логику статус
        except Order.DoesNotExist:
            return JsonResponse({'order_processed': False})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def reviews(request):
    reviews_list = Review.objects.all()
    paginator = Paginator(reviews_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/reviews.html', {'page_obj': page_obj, 'reviews_list': reviews_list})



def rate_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        rating_form = OrderRatingForm(request.POST)
        comment_form = OrderCommentForm(request.POST)
        if rating_form.is_valid() and comment_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.order = order
            rating.user = request.user
            rating.save()
            comment = comment_form.save(commit=False)
            comment.order = order
            comment.user = request.user
            comment.save()
            return redirect('reviews', order_id=order_id)
    else:
        rating_form = OrderRatingForm()
        comment_form = OrderCommentForm()
    return render(request, 'rate_order.html', {'rating_form': rating_form, 'comment_form': comment_form, 'order': order})
@csrf_exempt
def send_email_to_admin(request):
    if request.method == 'POST':
        subject = 'Новый запрос от пользователя'
        message = 'Вам поступил ордер от: {}'.format(request.POST.get('request_text', ''))
        from_email = 'vadi977@mail.ru'
        recipient_list = ['vadi977@mail.ru']

        send_mail(subject, message, from_email, recipient_list)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



