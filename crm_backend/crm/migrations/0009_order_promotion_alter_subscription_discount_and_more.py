# Generated by Django 5.0.6 on 2024-05-30 12:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_alter_promotion_category_alter_subscription_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.promotion'),
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
