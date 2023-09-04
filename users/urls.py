from django.urls import path
from . import views

urlpatterns = [
    # path(r'', views.index, name = 'catalog_page'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.profile, name='edit'),
    path('user/edit_user_info/', views.edit_user_info, name='edit_user_info'),
    path('get_user_info/', views.user_info, name='get_user_info'),
    path('get_my_orders/', views.my_orders, name='get_my_orders'),
    path("registration", views.register_request, name="register_request"),
    path("password_reset_done", views.password_reset_request, name="password_reset_done"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
]