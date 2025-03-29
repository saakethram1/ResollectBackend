from django.db import models

class Loan(models.Model):
  loan_no = models.IntegerField(default=0,unique=True)
  category = models.CharField(max_length=100)
  loan_type = models.CharField(max_length=100)
  borrower = models.CharField(max_length=100)
  borrower_address = models.TextField(blank=True)
  co_borrower_name = models.CharField(max_length=100)
  co_borrower_address = models.TextField(blank=True)
  current_dpd = models.IntegerField(default=0)
  sanction_amount = models.BigIntegerField(default=0)
  region = models.CharField(max_length=20)
  state = models.CharField(max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.loan_no}-{self.borrower}"
  
  class meta:
    db_table = 'loans'
    ordering = ['-created_at']