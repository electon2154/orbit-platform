# Generated by Django 5.2 on 2025-04-26 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0003_alter_customer_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='company_category',
            field=models.CharField(blank=True, max_length=100, verbose_name='Company Category'),
        ),
    ]
