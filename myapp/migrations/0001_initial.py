# Generated by Django 5.1.7 on 2025-03-28 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_no', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=100)),
                ('loan_type', models.CharField(max_length=100)),
                ('borrower', models.CharField(max_length=100)),
                ('borrower_address', models.TextField(blank=True)),
                ('co_borrower_name', models.CharField(max_length=100)),
                ('co_borrower_address', models.TextField(blank=True)),
                ('current_dpd', models.IntegerField(default=0)),
                ('sanction_amount', models.BigIntegerField(default=0)),
                ('region', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
            ],
        ),
    ]
