from django.urls import path
from . import views

app_name = 'voucher'

urlpatterns = [
    path('', views.voucher_view, name='voucher-view'),
    path('create-ajax/', views.create_voucher_ajax, name='create-voucher-ajax'),
    path('update-ajax/<uuid:voucher_id>/', views.update_voucher_ajax, name='update-voucher-ajax'),
    path('delete-ajax/<uuid:voucher_id>/', views.delete_voucher_ajax, name='delete-voucher-ajax'),
    path('json/', views.get_vouchers_json, name='get-vouchers-json'),
]
