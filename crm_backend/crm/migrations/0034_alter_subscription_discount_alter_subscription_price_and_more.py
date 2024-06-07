# Generated by Django 5.0.6 on 2024-06-04 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0033_rename_loyaltpointsused_order_loyalty_point_used_and_more'),
    ]

    operations = [
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
        migrations.CreateModel(
            name='loyalRedemption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('points_used', models.IntegerField(blank=True, default=0, null=True)),
                ('redemption_date', models.DateTimeField(auto_now_add=True)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer')),
                ('LoyaltyModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.loyaltymodel')),
            ],
        ),
    ]