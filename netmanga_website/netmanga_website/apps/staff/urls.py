from django.urls import path

from .views import process_reports, process_withdraws, process_withdrawal

app_name='staff'
urlpatterns = [
    path('process_withdraws', process_withdraws, name='process_withdraws'),
    path('process_withdraws/order_id=<int:pk>', process_withdrawal, name='process_withdrawal'),
    path('process_reports', process_reports, name='process_reports')
]