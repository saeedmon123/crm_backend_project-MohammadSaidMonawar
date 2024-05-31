# Generated by Django 5.0.6 on 2024-05-30 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Clothing', 'Clothing'), ('Books', 'Books'), ('Furniture', 'Furniture'), ('Food', 'Food'), ('Toys', 'Toys'), ('Tools', 'Tools'), ('Healthcare', 'Healthcare')], default='Electronics', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='coin_type',
            field=models.CharField(choices=[('US_Dollar', 'US_Dollar'), ('Euro', 'Euro'), ('British_Pound', 'British_Pound'), ('Japanese_Yen', 'Japanese_Yen')], default='US_Dollar', max_length=50),
        ),
    ]