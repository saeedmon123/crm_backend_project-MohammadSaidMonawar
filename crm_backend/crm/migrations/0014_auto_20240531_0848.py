# Generated by Django 3.2.4 on 2024-05-31 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_auto_20240531_0820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Promotion',
            new_name='promotion',
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
