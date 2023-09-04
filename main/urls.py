from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),

    path('', views.exchange_form, name='exchange_form'),
    path('confirmation/', views.exchange_confirmation, name='confirmation'),

    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('create_buy_order/', views.create_buy_order, name='create_buy_order'),
    path('create_sell_order/', views.create_sell_order, name='create_sell_order'),
    path('process_order/', views.process_order, name='process_order'),
    path('process_order1/', views.process_order1, name='process_order1'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('mark_order_as_paid/', views.mark_order_as_paid, name='mark_order_as_paid'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
    path('check_order_status/', views.check_order_status, name='check_order_status'),

    path('new_page_with_timer/', views.new_page_with_timer, name='new_page_with_timer'),
    path('new_page_with_timer1/', views.new_page_with_timer1, name='new_page_with_timer1'),
    path('waiting/', views.waiting, name='waiting'),

    path('client_details/<str:email>', views.client_details, name='client_details'),
    path('help/', views.help, name='help'),
    path('send_email_to_admin/', views.send_email_to_admin, name='send_email_to_admin'),

    path('reviews/', views.reviews, name='reviews'),
    path('rate_order/<int:order_id>/', views.rate_order, name='rate_order'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)