from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 
                  'loan_no', 
                  'category', 
                  'loan_type',
                  'borrower',
                  'borrower_address',
                  'co_borrower_name',
                  'co_borrower_address',
                  'current_dpd',
                  'sanction_amount',
                  'region',
                  'state',
                  ]