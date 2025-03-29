from django.urls import path
from .views import  items_list, loan_operations


urlpatterns = [
  path('items/', items_list, name='items-list'),
  path('items/<int:loan_no>/', loan_operations, name='loan-operations'),
]