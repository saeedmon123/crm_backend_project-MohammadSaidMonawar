# Generated by Django 5.0.6 on 2024-05-30 08:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_alter_product_category_alter_product_coin_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='status',
        ),
        migrations.AddField(
            model_name='subscription',
            name='discount',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='subscription',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='duration_unit',
            field=models.CharField(choices=[('Days', 'Days'), ('Months', 'Months'), ('Years', 'Years')], default='Months', max_length=20),
        ),
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='subscription',
            name='types',
            field=models.JSONField(default=list),
        ),
        migrations.CreateModel(
            name='SubscribedCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Cancelled', 'Cancelled'), ('Expired', 'Expired')], default='Active', max_length=20)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer')),
            ],
        ),
    ]
