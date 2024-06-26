# Generated by Django 5.0.6 on 2024-05-30 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_remove_subscription_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='discount',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='types',
            field=models.JSONField(default=list),
        ),
    ]
